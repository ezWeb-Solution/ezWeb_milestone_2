
# Importing python-telegram-bot's library functions
from telegram.ext import *
from telegram import *
import requests
import gspread
import os

# Setting up our logger
import logging


bot_token = os.environ.get('ezWeb_bot_token')

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

# polls
updater = Updater(token=bot_token, use_context=True)
dispatcher = updater.dispatcher

url = ''
desc = ''
current_state = ''
#for updating
target_row = ''
# sa = gspread.service_account()
# sh = sa.open('ezWeb database')
# wks = sh.worksheet("Sheet1")
# print("Rows: ", wks.row_count)
# print("Cols: ", wks.col_count)
# if wks.acell('C1').value is None:
#     print("True!")
# else:
#     print(wks.acell('C1'))
#     print("False")
#access cell: wks.acell('A9').value or wks.cell(3, 4).value
#if access multiple cells: wks.get('A7:E9'), wks.get_all_records())
#wks.update('F2', ='UPPER(E2)', raw=False)
#wks.delete_rows(25)

# Functions to handle each command
def start(update, context):
    buttons = [[InlineKeyboardButton("Create new website.", callback_data = "create_website")],
               [InlineKeyboardButton("Manage my websites.", callback_data = "manage_website")],
               [InlineKeyboardButton("Random cat fact.", callback_data = "cat_fact")]]
    welcome_text = "Welcome! I'm Tim, the bot designed by ezWeb that will service all your needs. How can I help you today?"

    context.bot.send_message(chat_id=update.effective_chat.id, text=welcome_text,
                             reply_markup=InlineKeyboardMarkup(buttons))

def echo(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)


def caps(update, context):
    text_caps = ' '.join(context.args).upper()
    context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)


def get_cat_fact(update, context):
    endpoint = "https://catfact.ninja/fact"
    response = requests.get(endpoint)
    fact = response.json()["fact"]
    context.bot.send_message(chat_id=update.effective_chat.id, text=fact, reply_markup=None)


def create_url(update, context):
    global current_state
    if current_state == 'create_website':
        response = "Certainly! Please input your desired domain name: (Must end with .com/.sg)"
        context.bot.send_message(chat_id=update.effective_chat.id, text=response, reply_markup=None)
        current_state = 'url_creation'
    elif current_state == 'initialized':
        context.bot.send_message(chat_id=update.effective_chat.id, text="What would your new url be?")
        state_changer(update, context, 'url_edit', current_state)
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Would be cool to visit that website someday!")


def create_desc(update, context):
    if current_state == 'initialized':
        context.bot.send_message(chat_id=update.effective_chat.id, text="What would your new description be?")
        state_changer(update, context, 'sending_desc', current_state)
    elif current_state == 'manage_website':
        state_changer(update, context, 'update_desc', current_state)
        context.bot.send_message(chat_id=update.effective_chat.id, text=f"Your current description is: {desc}\nWhat would your new description be?")
    else:
        response = "Alright, input a brief description to be displayed on the website."
        context.bot.send_message(chat_id=update.effective_chat.id, text=response)
        state_changer(update, context, 'sending_desc', current_state)

def state_changer(update, context, new_state, old_state):
    global current_state
    if old_state == 'initialized':
        if new_state == 'sending_desc':
            current_state = 'sending_desc'
        elif new_state == 'url_edit':
            current_state = 'url_edit'
    elif old_state == 'url_creation':
        if new_state == 'sending_desc':
            current_state = 'sending_desc'
    else:
        current_state = new_state

def url_desc_confirmation(update, context):
    global current_state
    if current_state == 'sending_desc':
        buttons = [[InlineKeyboardButton("That's right, I would like to proceed.", callback_data="send_url_desc")],
                   [InlineKeyboardButton("I want to edit my url.", callback_data="edit_url")],
                   [InlineKeyboardButton("I want to edit my description.", callback_data="edit_desc")],
                   [InlineKeyboardButton("I would like to stop creating a website.", callback_data="cancel")]]
        current_state = 'initialized'
        context.bot.send_message(chat_id=update.effective_chat.id,
                                text="Your desired url is: " + url + ", and your desired description is " + desc + ". Is that right?",
                                reply_markup=InlineKeyboardMarkup(buttons))
    elif current_state == 'update_desc':
        buttons = [[InlineKeyboardButton("Confirm update.", callback_data="manage_update_confirm")],
                   [InlineKeyboardButton("Cancel update.", callback_data="cancel")]]
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="Your new message is: \n" + desc + "\nPlease confirm the update.",
                                 reply_markup=InlineKeyboardMarkup(buttons))

def send_initialization_data(update, context):
    sa = gspread.service_account()
    sh = sa.open('ezWeb database')
    wks = sh.worksheet("Sheet1")
    row = 1
    while wks.acell('A' + str(row)).value is not None:
        row += 1
    wks.update('A' + str(row), url)
    wks.update('B' + str(row), desc)
    if wks.acell('C' + str(row)).value is None:
        print('here')
        wks.update('C' + str(row), update.effective_chat.id)
    context.bot.send_message(chat_id=update.effective_chat.id, text="Done!")
    global current_state
    current_state = ''
    requests.get(url='localhost:8080/generateSite', params='row')
    reset(update, context)

def send_data(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Confirmed. Sending data...")
    sa = gspread.service_account()
    sh = sa.open('ezWeb database')
    wks = sh.worksheet("Sheet1")
    row = target_row
    wks.update('B' + row, desc)
    context.bot.send_message(chat_id=update.effective_chat.id, text="Updated!")
    reset(update, context)


def manage_website(update, context):
    global current_state
    current_state = 'manage_website'
    sa = gspread.service_account()
    sh = sa.open('ezWeb database')
    wks = sh.worksheet("Sheet1")
    tg_id = update.effective_chat.id
    row = 1
    url_list = {}
    total_urls = 0
    while wks.acell('A' + str(row)).value is not None:
        row += 1
        if wks.acell('C' + str(row)).value == str(tg_id):
            url_list[wks.acell('A' + str(row)).value] = row
            total_urls += 1
    buttons = []
    counter = 1
    print("We are here right now! Number of rows = " + str(total_urls))
    for my_url in url_list:
        option = str(counter) + ". " + str(my_url)
        callback = "manage_choose_" + str(my_url) + "_" + str(url_list[my_url])
        buttons.append([InlineKeyboardButton(str(option), callback_data=str(callback))])
        counter += 1
    if row == 1:
        alt_buttons = [[InlineKeyboardButton("Yes! I'd like to create a website.", callback_data="create_website")],
                       [InlineKeyboardButton("I do not wish to create a website.", callback_data="cancel")]]
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="You haven't created a website with ezWeb. Would you like to proceed with creating a website instead?",
                                 reply_markup=InlineKeyboardMarkup(alt_buttons))
    else:
        buttons.append([InlineKeyboardButton("I no longer want to edit my websites.", callback_data="cancel")])
        context.bot.send_message(chat_id=update.effective_chat.id,
                            text="Certainly! Select a website to update.",
            reply_markup=InlineKeyboardMarkup(buttons))




def inline_query(update, context):
    query = update.callback_query.data
    update.callback_query.answer()
    context.bot.edit_message_reply_markup(
        message_id=update.callback_query.message.message_id,
        chat_id=update.callback_query.message.chat.id,
        reply_markup=None)
    if "create_website" in query:
        global current_state
        current_state = 'create_website'
        create_url(update, context)
    elif "manage_website" in query:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Sure, checking websites..")
        manage_website(update, context)
    elif "cat" in query:
        get_cat_fact(update, context)
    elif "send_url_desc" in query:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Sending data...")
        send_initialization_data(update, context)
    elif "edit_url" in query:
        create_url(update, context)
    elif "edit_desc" in query:
        create_desc(update, context)
    elif "cancel" in query:
        reset(update, context)
    elif "manage_update_confirm" in query:
        send_data(update, context)
    elif "manage_choose" in query:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Fetching data..")
        sa = gspread.service_account()
        sh = sa.open('ezWeb database')
        wks = sh.worksheet("Sheet1")
        ls = query.split("_")
        global url
        url = ls[2]
        global desc
        desc = str(wks.acell('B' + str(ls[3])).value)
        create_desc(update, context)
        global target_row
        target_row = ls[3]


def reset(update, context):
    global current_state
    current_state = ''
    context.bot.send_message(chat_id=update.effective_chat.id, text="Alright! Let me know if you need anything else :)")

def message_handler(update, context):
    global url
    if current_state == 'sending_desc' or current_state == 'update_desc':
        msg = update.message.text
        context.bot.send_message(chat_id=update.effective_chat.id, text="One moment...")
        global desc
        desc = msg
        url_desc_confirmation(update, context)
    elif current_state == 'url_edit':
        if '.com' or '.sg' in update.message.text:
            url = update.message.text.lower()
            url_desc_confirmation(update, context)
        else:
            context.bot.send_message(chat_id=update.effective_chat.id, text="Invalid url, please input a new url.")
    elif current_state == 'url_creation':
        if '.com' or '.sg' in update.message.text:
            url = update.message.text.lower()
            create_desc(update, context)
        elif 'cancel' in update.message.text:
            reset(update, context)
        else:
            context.bot.send_message(chat_id=update.effective_chat.id, text="That is not a valid url. Please input a valid url, or type 'Cancel' to cancel.")
    else:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="I'm not sure what you're looking for.. please be more specific.")


# Create and add command handlers
start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

catchall_handler = MessageHandler(Filters.text, message_handler)
dispatcher.add_handler(catchall_handler)

query_handler = CallbackQueryHandler(inline_query)
dispatcher.add_handler(query_handler)


updater.start_polling()
updater.idle()
