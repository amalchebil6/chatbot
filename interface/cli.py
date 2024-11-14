class CLI():
    def __init__(self,bot) -> None:
        self.bot = bot
    
    def render(self):
        
        while True:
            query = input("UserInput: ")
            if query == "exit":
                break
        
            result = self.bot.get_result(query)
            print("EmotiBot",result)
            