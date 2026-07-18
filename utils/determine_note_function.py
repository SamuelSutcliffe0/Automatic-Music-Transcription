def build_guitar_fretboard(max_fret=20):

    open_strings = {
        "1": 82.41,
        "2": 110.00,
        "3": 146.83,
        "4": 196.00,
        "5": 246.94,
        "6": 329.63,
    }

    fretboard = []

    for string in open_strings:
        fundamental_frequency = open_strings[string]
        for fret in range(max_fret + 1):
            freq = round(
                fundamental_frequency * (2 ** (fret / 12)), 2
            )
            fretboard.append({"string": string, "fret": fret, "frequency": freq})

    return fretboard

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

fretboard = build_guitar_fretboard()
quicksort(fretboard, 0, len(fretboard) - 1)

def determine_note(frequency: int) -> dict[int, int, float]:

    fretboard = build_guitar_fretboard()
    quicksort(fretboard, 0, len(fretboard) - 1)
    low, high = 0, len(fretboard) - 1

    while low <= high:
        mid = (low + high) // 2
        mid_freq = fretboard[mid]["frequency"]


        if mid_freq == frequency:
            return fretboard[mid]


        if frequency < mid_freq:
            high = mid - 1
        else:
            low = mid + 1

    candidates = []
    if 0 <= high < len(fretboard):
        candidates.append(fretboard[high])
    if 0 <= low < len(fretboard):
        candidates.append(fretboard[low])

    def frequency_difference(note):
        return abs(note["frequency"] - frequency)
    return min(candidates, key=frequency_difference)