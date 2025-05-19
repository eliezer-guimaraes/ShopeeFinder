import os
import requests
from bs4 import BeautifulSoup
from telegram import Bot
from telegram.ext import Updater, CommandHandler, CallbackContext

TELEGRAM_TOKEN = os.getenv("8035768767:AAGM65uwc9pdvZ9hOp2wMHOYqr9bd5VzuAo")
CHAT_ID = os.getenv("filmeseriesgratuitas2025")

bot = Bot(token=TELEGRAM_TOKEN)

def buscar_produtos_baratos():
    url = "https://shopee.com.br/search?keyword=produtos%20baratos"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    produtos = []

    for item in soup.find_all("div", class_="shopee-search-item-result__item"):
        titulo = item.find("div", class_="yQmmFK _1POlWt _36CEnF").text
        preco = item.find("div", class_="_1w9jLI _37ge-4 _2ZYSiu").text
        link = "https://shopee.com.br" + item.find("a")["href"]
        produtos.append(f"{titulo}\nPreço: {preco}\nLink: {link}\n")

        if len(produtos) >= 5:  # Limitar a 5 produtos
            break

    return produtos

def postar_produtos(context: CallbackContext):
    produtos = buscar_produtos_baratos()
    for produto in produtos:
        bot.send_message(chat_id=CHAT_ID, text=produto)

def iniciar(update, context):
    update.message.reply_text("Bot de produtos baratos da Shopee ativado!")
    context.job_queue.run_repeating(postar_produtos, interval=3600, first=5)

if __name__ == "__main__":
    updater = Updater(token=TELEGRAM_TOKEN)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", iniciar))
    updater.start_polling()
    updater.idle()
