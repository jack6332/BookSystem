from UI import UI,BookInterface
from core import Room,Event
class UIloader:
    def __init__(self):
        return
    def load(self,ui,rooms):
        for room_index in range(len(rooms)): #room manager載入UI
            ui.roomListInsert(rooms[room_index].name)
            print("123" + rooms[room_index].name)
