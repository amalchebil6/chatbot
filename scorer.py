import json
from analyzer.phq9 import PHQ9
from config import MISTRAL_KEY, MONGO_URI
from dbs.mongo import MongoConversationStore
from llms.MistralAPI import MistralApi
from utils import logger
import pandas as pd

logger.Logger.get_root_logger("emotibot_scorer")

bot = MistralApi(api_key=MISTRAL_KEY, model="mistral-large-latest")
db = MongoConversationStore(MONGO_URI, "EMOTI", "CONVERSATIONS")
all_chats = db.get_all()
phq9 = PHQ9(bot)

# Find the longest conversation
longest_conversation = max(all_chats, key=lambda conver: len(conver["general_history"]))
history = longest_conversation["general_history"]
res=[]
# Process conversation in batches of 10
batch_size = 10
for start_idx in range(0, len(history), batch_size):
    batch = history[start_idx:start_idx + batch_size]
    batch = list(map(lambda d: json.dumps(d), batch))
    
    result = []
    for i in range(len(batch) // 2):
        user = batch[2 * i]
        docteur = batch[2 * i + 1]
        final_query = f"User Thoughts : {user}"
        result.append(phq9.get_answers(final_query))
    
    # Create a DataFrame to handle the results
    df = pd.DataFrame(result)
    final_result = df.sum()  # Aggregate the results
    res.append(final_result.sum())
print(res)