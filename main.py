from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
from settings import TELEGRAM_BOT_TOKEN


def hello(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(f'Hello {update.effective_user.first_name}')


updater = Updater(TELEGRAM_BOT_TOKEN)

updater.dispatcher.add_handler(CommandHandler('hello', hello))

updater.start_polling()
updater.idle()
