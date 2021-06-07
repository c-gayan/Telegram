from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters
from settings import TELEGRAM_BOT_TOKEN, CUSTOM_REPLIES


print("bot is running 🏃")


def hello(update: Update, context: CallbackContext) -> None:
    print(update)
    update.message.reply_text(f'Hello {update.effective_user.first_name}')


def custom_reply(update: Update, context: CallbackContext):
    # listen messages coming from user and send reply
    message_text = update.effective_message.text
    reply_text = CUSTOM_REPLIES.get(message_text)
    if reply_text:
        update.message.reply_text(text=reply_text)


updater = Updater(TELEGRAM_BOT_TOKEN, use_context=True)

updater.dispatcher.add_handler(CommandHandler('hello', hello))
updater.dispatcher.add_handler(
    MessageHandler(Filters.chat_type.private, custom_reply)
)

updater.start_polling()
updater.idle()
