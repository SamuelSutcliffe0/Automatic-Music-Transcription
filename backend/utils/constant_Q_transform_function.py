from .imports import *

def constant_q_transform(input_signal, sample_frequency: int, minimum_bandwidth: int = 82.41, quality_factor: int = 8, frequency_bins: int = 84, bins_per_octave: int = 12):

    # define variables
    x = np.array(input_signal)
    sample_f = sample_frequency
    k = frequency_bins
    n = bins_per_octave
    min_f = minimum_bandwidth
    Q = quality_factor
    X = []  # output (frames × bins)

    # define bandwidths using geometric progression
    delta_f = []
    for i in range(0, k-1):
        delta_f.append((2**(1/n))**i * min_f)

    # define centre frequencies from bandwidths 
    centre_f = []
    for i in range(0, k-1):
        centre_f.append(min_f * (2**(i/n)))

    # compute the transform for each bin, scrolling window across signal
    for i in range(0, k-1):

        # this bin's window length
        window_len = int(Q * sample_f / centre_f[i])

        # create window (Hamming window)
        alpha = 25/46
        window = alpha - (1 - alpha) * np.cos(
            (2*np.pi*np.arange(window_len)) / (window_len - 1)
        )

        # kernel frequency
        kernal_f = 2 * math.pi * centre_f[i] / sample_f

        # hop length = quarter window length (for speed)
        hop_length = window_len // 4

        # compute transform for each frame
        for t in range(0, len(x) - window_len, hop_length):

            segment = x[t : t + window_len]

            # sum up the transform for this bin and this frame
            sum = 0
            for j in range(0, window_len):
                sum += (window[j] * segment[j] * np.exp(-1j * kernal_f * j))

            # normalise and store
            X.append(sum / window_len)

    return np.array(X)

def extract_dominant_frequency(input_frequency_domain, frequency_bins: int = 84, minimum_bandwidth: int = 82.41, bins_per_octave: int = 12):

    # define variables
    num_bins = frequency_bins
    X = input_frequency


    # turn into frames and which bins each frame is 
    num_frames = len(X) // num_bins
    X = X[:num_frames * num_bins].reshape(num_frames, num_bins)

    # magnitudenitude
    magnitude = np.abs(X)

    # average over time
    avg_magnitude = magnitude.mean(axis=0)

    # index of dominant bin
    dominant_bin = np.argmax(avg_magnitude)

    # convert bin to frequency
    min_f = minimum_bandwidth
    n = bins_per_octave
    dominant_freq = min_f * (2 ** (dominant_bin / n))




    













