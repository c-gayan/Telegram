from telegram import Update, Bot
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters, PicklePersistence
from settings import TELEGRAM_BOT_TOKEN, MAX_AGE_IN_SECONDS
from datetime import datetime, timezone
from threading import Thread
from time import sleep

print("bot is running 🏃")

bot = Bot(TELEGRAM_BOT_TOKEN)


# read messages
def handle_new_channel_posts(update: Update, context: CallbackContext):
    message_id = update.channel_post.message_id
    timestamp = update.channel_post.date
    context.chat_data[message_id] = {"timestamp": timestamp, "message_id": message_id, "deleted": False}


# delete the old messages
def check_and_delete():
    while True:
        keys_to_be_removed = []
        for key, value in dp.chat_data.items():
            for message_id, message_data in value.items():
                if message_data.get("deleted"):
                    # delete that row
                    keys_to_be_removed.append(message_id)
                    continue

                else:
                    age = (datetime.now(tz=timezone.utc) - message_data["timestamp"]).total_seconds()
                    if age > MAX_AGE_IN_SECONDS:
                        # print("deleting " + str(message_id))
                        try:
                            bot.delete_message(chat_id=key, message_id=message_id)
                        except Exception:
                            pass
                        message_data["deleted"] = True
                        sleep(0.1)
            for k in keys_to_be_removed:
                del value[k]
        sleep(1)


my_persistence = PicklePersistence(filename='my_file')
updater = Updater(TELEGRAM_BOT_TOKEN, persistence=my_persistence, use_context=True)

dp = updater.dispatcher

Thread(target=check_and_delete).start()

updater.dispatcher.add_handler(MessageHandler(Filters.update.channel_post, handle_new_channel_posts))

updater.start_polling()
updater.idle()
