from .imports import *

class TabNode:
    def __init__(self, string_number: int = None, fret_number: int = None):
        self.string_number = string_number
        self.fret_number = fret_number
        self.next = None

def convert_to_tablature_form(head: TabNode):

    tab = []
    tab.append(["e","B","G","D","A","E"])

    current = head 
    while current:
        
        note = []

        for i in range(1,7):
            if i == current.string_number:
                note.append(current.fret_number)
            else:
                note.append("-")
        tab.append(note)

        current = current.next

    tab.append(["|" for _ in range(6)])
    tab = np.array(tab)

    return tab.T


        

