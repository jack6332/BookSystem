import time
from core import BookSystem
from database import DataBase
class Event:
    BookSystem = None
    id = "" # event id from google calendar
    name = ""
    description = ""
    start_time = None
    end_time = None
    participants = ["","",""]
    def __init__(self,_BookSystem,_id,_name,_description,_start_time,_end_time): #TODO: time
        self.BookSystem = _BookSystem
        self.id = _id
        self.name = _name
        self.description = _description
        self.start_time = _start_time
        self.end_time = _end_time
        return
    def addParticipant():
        return
    def deleteParticipant():
        return
