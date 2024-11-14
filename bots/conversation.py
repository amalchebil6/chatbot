import uuid


class Conversation():
    def __init__(self,bot,db,id=None) -> None:
        self.bot = bot
        self.db = db
        self.id = id
        if( id == None ):
            self.id = uuid.uuid4().__str__()
            return
        old_history = self.db.get_conversation(self.id)
        self.bot.set_history(old_history)        
        
    def get_result(self,user_query):
        res = self.bot.get_result(user_query)
        conver = self.bot.export()
        self.db.save_conversation(self.id,conver)
        return res