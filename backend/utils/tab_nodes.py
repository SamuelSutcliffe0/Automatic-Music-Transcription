
class TabNode:
    def __init__(self,string_number : int = 0, fret_number : int = 0) -> TabNode: 
        self.string_number = string_number
        self.fret_number = fret_number
        self.next = None


def decustruct_tabnodes(tab_id: int,head: TabNode, cursor, db) -> None:
    order_id = 1
    current = head 
    while current.next:
        string_number = current.string_number
        fret_number = current. fret_number
        cursor.execute(
            "INSERT INTO TabNodes (tab_id, order_id, strig_number, fret_number) VALUES (%s, %s, %s, %s)",
            (tab_id, order_id, string_number, fret_number)
        )
        db.commit()
        current = current.next
        order_id += 1


def reconstuct_tabnodes(tab_id: int,cursor) -> TabNode:
    cursor.execute("SELECT string_number, fret_number FROM TabNodes WHERE tab_id=%s ORDER BY order_id", (tab_id))
    rows = cursor.fetchall()
    dummie = TabNode()
    current = dummmie
    for node in rows:
        next = TabNode(node[0],node[1])
        current.next = next
        current = next

    return dummie.next


    
    
