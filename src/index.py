
from fastapi import FastAPI, Request, HTTPException


import telegram, os
from telegram.ext import Dispatcher, MessageHandler, Filters


app = FastAPI()
################################################################
import openai
	
openai.api_key = os.getenv("OPENAI_API_KEY")



	
conversation = []

class ChatGPT:  
    

    def __init__(self):
        
        self.messages = conversation
        self.model = os.getenv("OPENAI_MODEL", default = "gpt-3.5-turbo")



    def get_response(self, user_input):
        conversation.append({"role": "user", "content": user_input})
        

        response = openai.ChatCompletion.create(
	            model=self.model,
                messages = self.messages

                )

        conversation.append({"role": "assistant", "content": response['choices'][0]['message']['content']})
        
        print("AI回答內容：")        
        print(response['choices'][0]['message']['content'].strip())


        
        return response['choices'][0]['message']['content'].strip()
	


telegram_bot_token = str(os.getenv("TELEGRAM_BOT_TOKEN"))
# Initial bot by Telegram access token
bot = telegram.Bot(token=telegram_bot_token)

chatgpt = ChatGPT()





@app.post("/callback")
async def webhook_handler(request: Request):
    """Set route /hook with POST method will trigger this method."""
    if request.method == "POST":
        update = telegram.Update.de_json(request.get_json(force=True), bot)

        # Update dispatcher process that handler to process this message
        dispatcher.process_update(update)
    return 'ok'

async def reply_handler(bot, update):
    """Reply message."""
    #text = update.message.text
    #update.message.reply_text(text)
    chatgpt = ChatGPT()        
    
    chatgpt.prompt.add_msg(update.message.text) #人類的問題 the question humans asked
    ai_reply_response = chatgpt.get_response() #ChatGPT產生的回答 the answers that ChatGPT gave
    
    update.message.reply_text(ai_reply_response) #用AI的文字回傳 reply the text that AI made
    
# New a dispatcher for bot
dispatcher = Dispatcher(bot, None)

# Add handler for handling message, there are many kinds of message. For this handler, it particular handle text
# message.
dispatcher.add_handler(MessageHandler(Filters.text, reply_handler))

if __name__ == "__main__":
    # Running server
    app.run(debug=True)

