import json


system_prompt = """
    Given user thoughts in JSON , try to guess the PHQ9 Answer ( Yes / No ) , Provide an answer for each question: 
    Questions:
        "Over the last 2 weeks, how often have you been bothered by any of the following problems?",
        "1. Little interest or pleasure in doing things.",
        "2. Feeling down, depressed, or hopeless.",
        "3. Trouble falling or staying asleep, or sleeping too much.",
        "4. Feeling tired or having little energy.",
        "5. Poor appetite or overeating.",
        "6. Feeling bad about yourself — or that you are a failure or have let yourself or your family down.",
        "7. Trouble concentrating on things, such as reading the newspaper or watching television.",
        "8. Moving or speaking so slowly that other people could have noticed? Or the opposite — being so fidgety or restless that you have been moving around a lot more than usual.",
        "9. Thoughts that you would be better off dead, or of hurting yourself in some way."
    
    Only answer with yes if you find Explicit Evidence Or Implicit ones Otherwise it's No
    Response Format : 
        Output Only the list { "answer",: ["Yes/No","Yes/No",...] } 9 Times in a list with the answer in order for each question 
    Example:
        { "answer" : ["Yes","No","No","No","Yes","Yes","Yes","No","Yes"] }
"""

class PHQ9():
    def __init__(self,bot):
        """
        
        """
        self.bot = bot

    def get_answers(self,query):
        result = self.bot.chat([{
            "role":"system",
            "content": system_prompt
        },{
            "role":"user","content": query
        }],{
            "response_format": {
          "type": "json_object",
      }
        })
        print("PHQ9:",result)
        answers= json.loads(result.strip())['answer']
        return list(map(lambda d: d=="Yes",answers))