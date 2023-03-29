from fastapi import FastAPI, Request, HTTPException
import os
import openai
from telegram import Update, Bot
from telegram.ext import Dispatcher, MessageHandler, Filters, CallbackContext

app = FastAPI()

openai.api_key = os.getenv("OPENAI_API_KEY")
conversation = []

class ChatGPT:
    def __init__(self):
        self.messages = conversation
        self.model = os.getenv("OPENAI_MODEL", default="gpt-3.5-turbo")

    def get_response(self, user_input):
        conversation.append({"role": "user", "content": user_input})
        response = openai.Completion.create(
            engine=self.model,
            prompt=self._format_messages(self.messages) + user_input,
            max_tokens=60,
        )
        conversation.append({"role": "assistant", "content": response["choices"][0]["text"]})
        return response["choices"][0]["text"].strip()

    @staticmethod
    def _format_messages(messages):
        messages_str = ""
        for message in messages:
            role = message["role"]
            content = message["content"]
            messages_str += f"{role}: {content}\n"
        return messages_str


bot_token = str(os.getenv("TELEGRAM_BOT_TOKEN"))
bot = Bot(token=bot_token)

chatgpt = ChatGPT()

def reply_handler(update: Update, context: CallbackContext):
    text = update.message.text
    ai_reply_response = chatgpt.get_response(text)
    update.message.reply_text(ai_reply_response)

dp = Dispatcher(bot, None)
dp.add_handler(MessageHandler(Filters.text, reply_handler))

async def webhook_handler(request: Request):
    if request.method == 'POST':
        update = Update.de_json(await request.json(), bot)
        dp.process_update(update)
        return 'ok'

#if __name__ == '__main__':
    #app.run(debug=True)
