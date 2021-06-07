from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext, PicklePersistence, \
    CallbackQueryHandler

from settings import TELEGRAM_BOT_TOKEN

print("bot is running 🏃")


def help(update: Update, context: CallbackContext):
    # send help text
    update.message.reply_text(
        text="Available Commands:\n"
             "/new Finish Assignment \n"
             "/list - to show the list of TODOs"
    )


def create_todo(update: Update, context: CallbackContext):
    # a function to create todos for user
    message_id = update.effective_message.message_id
    message_text = update.effective_message.text
    todo_title = message_text.replace("/new ", "")
    context.user_data[message_id] = {"title": todo_title, "completed": False}
    update.message.reply_text("new todo has been created.")

    # check for empty string


def show_todo_list(update: Update, context: CallbackContext):
    # send help text
    text = "Here are the list of todos:\n"
    keyboard = []
    for key, value in context.user_data.items():
        status_emoji = "✅ " if value["completed"] else "☑️"
        title = status_emoji + " " + value["title"]
        keyboard.append(
            [InlineKeyboardButton(title, callback_data=key)]
        )
        text += title + "\n"
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(text, reply_markup=reply_markup)


def button_click(update: Update, context: CallbackContext):
    text = "Here are the list of todos:\n"
    query = update.callback_query
    todo_id = int(query.data)
    current_status = context.user_data[todo_id]["completed"]
    context.user_data[todo_id]["completed"] = not current_status
    keyboard = []
    for key, value in context.user_data.items():
        status_emoji = "✅ " if value["completed"] else "☑️"
        title = status_emoji + " " + value["title"]
        keyboard.append(
            [InlineKeyboardButton(title, callback_data=key)]
        )
        text += title + "\n"
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(text=text, reply_markup=reply_markup)


my_persistence = PicklePersistence(filename='my_file')
updater = Updater(TELEGRAM_BOT_TOKEN, persistence=my_persistence, use_context=True)

updater.dispatcher.add_handler(CommandHandler("new", create_todo))
updater.dispatcher.add_handler(CommandHandler("help", help))
updater.dispatcher.add_handler(CommandHandler("list", show_todo_list))
updater.dispatcher.add_handler(CallbackQueryHandler(button_click))
updater.start_polling()
updater.idle()
