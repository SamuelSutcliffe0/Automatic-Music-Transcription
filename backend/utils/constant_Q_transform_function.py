from .imports import *

def constant_q_transform(input_signal, sample_frequency: int,minimum_bandwidth: int = 82.41, quality_factor: int = 8, frequency_bins: int = 84, bins_per_octave: int = 12):

    # define variables
    x = np.array(input_signal)
    sample_f = sample_frequency
    k = frequency_bins
    n = bins_per_octave
    min_f = minimum_bandwidth
    Q = quality_factor
    X = [] # output

    # define bandwidths using geometric progression
    delta_f = [] 
    for i in range(0, k-1):
        delta_f.append((2**(1/n))**i * min_f)

    # define centre frequencies from bandwidths 
    centre_f = []
    for i in range(0, k-1):
        centre_f.append(min_f * (2**(i/n)))   

    # compute the tranform for each bin 
    for i in range(0, k-1):

        # this bin's window length
        window_len = int(Q * sample_f / centre_f[i])  

        # create_window (using hamming window, so not strict constant Q tranform as it is like steps rather than a perfectly smooth curve)
        alpha = 25/46
        window = alpha - (1 - alpha) * np.cos((2*np.pi*np.arange(window_len-1))/(window_len-1))

        # kernal frequency
        kernal_f = 2 * math.pi * centre_f[i] / sample_f

        # sum up the tranform
        sum = 0
        segment = x[:window_len]
        for j in range(0, window_len-1):
            sum += ( window[j] * segment[j] * np.exp(-1j * kernal_f * j) )

        # normalise
        X.append(sum / window_len)

    return np.array(X)



    













