from .imports import *


def constant_q_transform(
    input_signal,
    sample_frequency: int,
    minimum_bandwidth: int = 82.41,
    quality_factor: int = 8,
    frequency_bins: int = 84,
    bins_per_octave: int = 12,
):

    # define variable   s
    x = np.array(input_signal)
    sample_f = sample_frequency
    k = frequency_bins
    n = bins_per_octave
    min_f = minimum_bandwidth
    Q = quality_factor

    # instead of one long list, make list-of-lists (one per bin)
    X = [[] for _ in range(k)]  # output (frames × bins)

    # define bandwidths using geometric progression
    delta_f = []
    for i in range(0, k):
        delta_f.append((2 ** (1 / n)) ** i * min_f)

    # define centre frequencies from bandwidths
    centre_f = []
    for i in range(0, k):
        centre_f.append(min_f * (2 ** (i / n)))

    # compute the transform for each bin, scrolling window across signal
    for i in range(0, k):
        # this bin's window length
        window_len = int(Q * sample_f / centre_f[i])

        # create window (Hamming window)
        alpha = 25 / 46
        window = alpha - (1 - alpha) * np.cos(
            (2 * np.pi * np.arange(window_len)) / (window_len - 1)
        )

        # kernel frequency
        kernel_f = 2 * math.pi * centre_f[i] / sample_f

        # hop length = quarter window length (for speed)
        hop_length = window_len // 4

        # compute transform for each frame
        for t in range(0, len(x) - window_len, hop_length):
            segment = x[t : t + window_len]

            # sum up the transform for this bin and this frame
            sum = 0
            for j in range(0, window_len):
                sum += window[j] * segment[j] * np.exp(-1j * kernel_f * j)

            # normalise and store
            X[i].append(sum / window_len)

    # convert list-of-lists into equal-length frames × bins matrix
    min_frames = min(len(bin_frames) for bin_frames in X)
    X = np.array(
        [bin_frames[:min_frames] for bin_frames in X]
    ).T  # here .T flips the rows and columns in the numpy array, short for transpose,
    # swapping from frames with all the bins in them to bins with all the frames in them, such that the bin with the biggest amplitude frame can be extracted

    return X


def extract_dominant_frequency(
    input_frequency_domain,
    minimum_bandwidth: int = 82.41,
    bins_per_octave: int = 12,
    max_harmonics: int = 6,
    frequency_bins: int = 84,
):
    X = input_frequency_domain
    magnitude = np.abs(X)  # turn all magnitudes positive and real for easy comparison
    mean_mag = magnitude.mean(axis=0)  # average over time for each bin

    k = frequency_bins
    scores = np.zeros(
        k
    )  # blank array of scores all with value zero the size of the number bins

    # score each bin as a candidate for the fundamental
    for i in range(k):
        score = 0
        valid_harmonics = 0
        for m in range(1, max_harmonics + 1):
            harm_bin = int(
                round(i + bins_per_octave * math.log2(m))
            )  # compute the bin index corresponding to the m‑th harmonic of candidate bin i using logarithmic spacing,
            # so if the current bin is the fundamental, what score does the whole selection of harmonics get
            if harm_bin >= k:
                score -= mean_mag[i]  # remove score if harmonics are missing
                continue
            valid_harmonics += 1
            if (
                2 * i < k and mean_mag[i] > mean_mag[2 * i]
            ):  # eliminate harmonics pretending to be fundamentals as they don't follow the rule of 2nd harmonic being 2x the fundamental as the next harmonic up won't be the 2nd
                score *= 0.1
            score += (
                mean_mag[harm_bin] / m
            )  # add the magnitude of the m‑th harmonic, weighted by 1/m
        scores[i] = (
            score / valid_harmonics
        )  # normalise scores based on how many harmonics were recorded, relative to the number that fitted in the CQT window

    best_bin = np.argmax(scores)  # takes maximum score from list

    min_f = minimum_bandwidth
    n = bins_per_octave
    dominant_f = min_f * (2 ** (best_bin / n))
    return dominant_f
