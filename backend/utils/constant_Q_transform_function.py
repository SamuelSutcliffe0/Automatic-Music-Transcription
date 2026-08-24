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
    sample_frequency: int,
    minimum_bandwidth: int = 82.41,
    bins_per_octave: int = 12,
    max_harmonics: int = 6,
    frequency_bins: int = 84,
    quality_factor: int = 8,
):

    # define variables
    X = input_frequency_domain
    sample_f = sample_frequency
    min_f = minimum_bandwidth
    n = bins_per_octave
    k = frequency_bins
    Q = quality_factor

    # magnitude spectrum
    magnitude = np.abs(X) ** 2
    mean_magnitude = magnitude.mean(axis=0)

    # Bias 1: window-length variance correction
    centre_f = min_f * (2 ** (np.arange(k) / n))
    window_len = Q * sample_f / centre_f
    mean_magnitude_corrected = mean_magnitude * np.sqrt(window_len)

    # Bias 2: harmonic-density correction
    harmonic_count = (centre_f[-1] / centre_f).clip(min=1)
    mean_magnitude_corrected /= harmonic_count

    # Bias 3: spectral-slope whitening

    # creates a 15 point moving average. A moving average slides along the array, making each bin just the sum of its 14 neighbours, averaging out the curve
    kernel = np.ones(15) / 15

    # Here convolve is a slider for the array kernel, kernel being an array of just 15 1/15s like [1/15, 1/15, 1/15, ..., 1/15].
    # So the current bin the function is looking at becomes the result of the kernel applied to the 7 neighbours and itself each side. mode = "same" makes input length = output length,
    # needed for the division between the two arrays
    trend = np.convolve(mean_magnitude_corrected, kernel, mode="same")

    # adjust by the smooth trend and add tiny number to prevent divide by zero errors
    mean_magnitude_corrected /= trend + (1 * (10**-12))

    # scoring
    scores = np.zeros(k)

    for i in range(k):
        score = 0
        valid_harmonics = 0

        for m in range(1, max_harmonics + 1):
            harm_bin = int(round(i + bins_per_octave * math.log2(m)))

            if harm_bin >= k:
                score -= mean_magnitude_corrected[i]
                continue

            valid_harmonics += 1

            # harmonic suppression to prevent false fundementals
            if 2 * i < k:
                if mean_magnitude_corrected[2 * i] > 2 * mean_magnitude_corrected[i]:
                    score *= 0.1

            score += mean_magnitude_corrected[harm_bin] / m

        scores[i] = score * (valid_harmonics / max_harmonics)

    best_bin = np.argmax(scores)
    dominant_f = min_f * (2 ** (best_bin / n))
    return dominant_f
