from UI import UI,UIloader
from core.Participant import Participant
from database import DataBase,DBloader
from google_calendar import CalendarAPI
from core import Room,Authorization,Event,Participant
import datetime
class BookSystem:
    users = []
    rooms = []
    participants = []
    last_update_time : datetime
    def __init__(self):
        self.ui = UI.BookSystemUI(self)
        self.gc = CalendarAPI.calendar_API()
        self.db = DataBase.DataBaseManager()
        self.dbl = DBloader.DBloader()
        self.uil = UIloader.UIloader()
        self.auth = Authorization.Authorization()
        return
    def start(self):
        self.ui.initialUI()
        self.update()
        #self.garbage_event_collection()
        self.ui.runUI()
    def update(self):
        self.rooms.clear()
        self.participants.clear()
        self.dbl.load(self,self.db)
        print("participant amount:")
        print(len(self.participants))
        for i in range(len(self.participants)):
            print(self.participants[i].email)
        self.uil.load(self.ui,self.rooms)
        self.last_update_time = datetime.datetime.now()
        print("-----------<update>------------")
    def check_db_update(self):
        if self.last_update_time < self.db.get_lastupdate():
            self.update()
            #TODO 節省更新UI次數
            self.ui.bookInterface.UpdateRoomList()
            if self.ui.bookInterface.TargetDay != -1:
                self.ui.bookInterface.UpdateTimeLineEvent()
    def getRoom(self,name):
        for i in range(len(self.rooms)):
            if self.rooms[i].name == name:
                return self.rooms[i]
        return None
    def getRoomById(self,id):
        for i in range(len(self.rooms)):
            if self.rooms[i].id == id:
                return self.rooms[i]
        return None
    def getRoomEvents(self,room_name):
        for i in range(len(self.rooms)):
            if self.rooms[i].name == room_name:
                return self.rooms[i].events
        return None

    def addRoom(self,room):        
        if room.name == "":
            print('Room_name is Empty!')
            return        
        self.check_db_update()
        for i in range(len(self.rooms)):
            if self.rooms[i].name == room.name:
                #TODO 彈出警告視窗
                self.ui.MessageBoxWarn('BookSystem Warning','Room name is Duplicated!')
                print('Room_name is Duplicated!')
                return
        print('Add Room!')
        room.id = self.gc.Create_Calendar(room.name)
        self.rooms.append(room)
        self.db.create_room(room.id,room.name)
        self.ui.roomListInsert(room.name)
        print('Add Room successful!')
        return
    def deleteRoom(self,room):
        self.check_db_update()
        found=False
        for i in range(len(self.rooms)):
            if self.rooms[i].name == room.name:
                room.id = self.rooms[i].id
                found = True
                del self.rooms[i]
                break
        if not found:
            return
        print('Delete Room!')
        self.db.delete_room(room.name)     
        self.ui.roomListDelete(room.name)
        self.gc.Delete_Calendar(room.id)
        print('Delete Room successful!')
        self.db.update_lastupdate()
        return
    def updateRoom(self,old_name,new_name):
        self.check_db_update()        
        found=False
        for i in range(len(self.rooms)):
            if self.rooms[i].name == old_name:
                print('found room')
                found = True
                self.rooms[i].name = new_name
                roomID = self.rooms[i].id
                break
        if not found:
            #TODO 彈出警告視窗
            print("========================================Room is not found!")
            self.ui.MessageBoxError('BookSystem Error','Room is not found!')
            return
        print('Update Room!')
        self.db.update_room(old_name,new_name)
        self.gc.Update_Calendar(roomID,new_name)
        self.db.update_lastupdate()
        print('Update Room successful!')
    def addParticipant(self,email):
        get = self.getParticipant(email)
        if get == None:
            self.participants.append(Participant.Participant(email))
            return self.participants[-1]
        return get
    def getParticipant(self,email):
        for i in range(len(self.participants)):
            if self.participants[i].email == email:
                return self.participants[i]
        return None
    def getUserEvents(self,CurrentUser):
        events = list()
        for EventID in self.db.get_myEventID(CurrentUser):
            x = self.db.get_myEvent(EventID[0])
            event = Event.Event(self,x[0][5],x[0][1],x[0][2],x[0][3],x[0][4])
            event.id = x[0][0]
            events.append(event)
        return events
    def garbage_event_collection(self):
        for room_index in range(len(self.rooms)):
            self.rooms[room_index].garbage_event_collection()
    def login(self,account,password):
        self.auth.login(account,password)
        if account == "Admin" and self.auth.valid:
            self.ui.AdminLogin()
        return self.auth.valid
    
