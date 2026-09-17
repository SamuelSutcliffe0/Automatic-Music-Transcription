from .imports import *

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


        

