from llms import LLM


class BotWithHistory():
    def __init__(self,llm: LLM,system_prompt=""):
        self.history = [{
            "role":"system",
            "content": system_prompt
        }]
        self.llm = llm
        
    def export(self):
        return self.history 
    
    def set_history(self,history):
        self.history = history

        
    def chat(self,query):
        self.history.append({
            "role": "user",
            "content": query
        })
        
        result =  self.llm.chat(self.history)
        
        self.history.append({
            "role": "assistant",
            "content": result
        })
        
        return result