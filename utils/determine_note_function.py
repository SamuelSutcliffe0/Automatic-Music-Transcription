def build_guitar_frequencies(max_fret=20):

    open_strings = {
        "1": 82.41,
        "2": 110.00,
        "3": 146.83,
        "4": 196.00,
        "5": 246.94,
        "6": 329.63,
    }

    guitar_map = []

    for string_name in open_strings:
        fundamental_frequency = open_strings[string_name]
        for fret in range(max_fret + 1):
            freq = round(
                fundamental_frequency * (2 ** (fret / 12)), 2
            )  # Because the 12th fret is exactly half the length of the open string, which means the frequency is exactly double the open note. This doubling is how an octave is physically defined in music.
            guitar_map.append({"string": string_name, "fret": fret, "frequency": freq})

    return guitar_map

def quicksort(array: list, low: int, high: int):
   if low < high:
       pivot = partition(array, low, high)
       quicksort(array, low, pivot)
       quicksort(array, pivot + 1, high)
   return
  
def partition(array: list, low: int, high: int):
   pivot = array[(high + low) // 2]
   i = low-1
   j = high+1
   
   while True:
       while True:
           i = i + 1
           if array[i] >= pivot:
               break
       while True:
           j = j - 1
           if array[j] <= pivot:
               break
       if i >= j:
           return j
       array[i], array[j] = array[j], array[i]

guitar_map = build_guitar_frequencies()
quicksort(guitar_map, 0, len(guitar_map) - 1)

def determine_note(frequency: int):
    low, high = 0, len(guitar_map) - 1

    while low <= high:
        mid = (low + high) // 2
        mid_freq = guitar_map[mid]["frequency"]


        if mid_freq == frequency:
            return guitar_map[mid]


        if frequency < mid_freq:
            high = mid - 1
        else:
            low = mid + 1

    candidates = []
    if 0 <= high < len(guitar_map):
        candidates.append(guitar_map[high])
    if 0 <= low < len(guitar_map):
        candidates.append(guitar_map[low])

    def frequency_difference(note):
        return abs(note["frequency"] - frequency)
    return min(candidates, key=frequency_difference)