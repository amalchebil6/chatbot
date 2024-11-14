import json
from analyzer.phq9 import PHQ9
from config import MISTRAL_KEY, MONGO_URI
from dbs.mongo import MongoConversationStore
from llms.MistralAPI import MistralApi
from utils import logger
import pandas as pd

logger.Logger.get_root_logger("emotibot_scorer")

bot = MistralApi(api_key=MISTRAL_KEY, model="mistral-large-latest")
db = MongoConversationStore(MONGO_URI,"EMOTI","CONVERSATIONS")
all_chats= db.get_all()
phq9 = PHQ9(bot)
for conver in all_chats[::-1]:
    current = conver["general_history"][-10:]
    current = list(map(lambda d: json.dumps(d),current))
    result = []
    for i in range(len(current) // 2):
        user = current[2*i]
        docteur = current[2*i+1]
        final_query = f"User Thoughts : {user}"
        result.append(phq9.get_answers(final_query))
    
    df = pd.DataFrame(result)
    final_result =  df.sum()
    print(final_result)
    break