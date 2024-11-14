from bots.emotibot import EmotiBot
from config import MONGO_URI
from dbs.mongo import MongoConversationStore
from interface.cli import CLI
from bots.conversation import Conversation

emotibot = EmotiBot()
db = MongoConversationStore(MONGO_URI,"EMOTI","CONVERSATIONS")

conver = Conversation(emotibot,db)

cli = CLI(conver)
cli.render()