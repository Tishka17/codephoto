import logging
import os
from queue import Queue

import telegram
from telegram import Update
from telegram.ext import Updater, Filters, MessageHandler, CallbackContext, CommandHandler, Dispatcher

from highlighter import make_image
from logic import get_random_bg
from uploader import gen_name_uniq, UPLOAD_DIR


def process_code(update: Update, context: CallbackContext):
    print("process_code: ", update.message.text)
    name = gen_name_uniq(5)
    path = os.path.join(UPLOAD_DIR, name + ".jpg")
    make_image(update.message.text, path, lang=None, background=get_random_bg())
    print("created: ", path)
    with open(path, "rb") as f:
        context.bot.send_photo(
            chat_id=update.effective_chat.id,
            photo=f,
            reply_to_message_id=update.effective_message.message_id,
            caption="http://codephoto.ru/i/"+name
        )


def start(update: Update, context: CallbackContext):
    print("start")


def create_dispatcher(token):
    bot = telegram.Bot(token=token)
    update_queue = Queue()
    dp = Dispatcher(bot, update_queue, use_context=True)
    return bot, update_queue, dp


def register_handlers(dispatcher):
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text, process_code))


def main():
    logging.basicConfig(level=logging.INFO)
    TG_TOKEN = os.environ.get("TG_TOKEN")
    bot = telegram.Bot(token=TG_TOKEN)
    print(bot.get_me())
    updater = Updater(bot=bot, use_context=True)
    register_handlers(updater.dispatcher)
    updater.start_polling()


if __name__ == "__main__":
    main()
