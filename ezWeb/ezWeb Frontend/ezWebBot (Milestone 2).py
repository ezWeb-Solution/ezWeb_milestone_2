#Importing python-telegram-bot's library functions
from telegram.ext import *
from telegram import *
import requests
import gspread
import os
from datetime import date
# Setting up our logger
import logging
import re
from ExcelParser import *

bot_token = os.environ.get('ezWeb_bot_token')

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

# polls
updater = Updater(token=bot_token, use_context=True)
dispatcher = updater.dispatcher
current_user = {}

# for updating
target_row = ''
target_col = ''
wks = None
num = 1000
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
# access cell: wks.acell('A9').value or wks.cell(3, 4).value
# if access multiple cells: wks.get('A7:E9'), wks.get_all_records())
# wks.update('F2', ='UPPER(E2)', raw=False)
# wks.delete_rows(25)

# Functions to handle each command
def start(update, context):
    buttons = [[InlineKeyboardButton("Create new website.", callback_data="create_website")],
               [InlineKeyboardButton("Manage my websites.", callback_data="manage_website")],
               [InlineKeyboardButton("Random cat fact.", callback_data="cat_fact")]]
    welcome_text = "Welcome! I'm Tim, the bot designed by ezWeb that will service all your needs. How can I help you today?"
    global current_user
    if current_user.get(update.effective_chat.id) is None:
        current_user[update.effective_chat.id] = {}
    if current_user[update.effective_chat.id].get('state') is None:
        current_user[update.effective_chat] = {}
    current_user[update.effective_chat.id]['state'] = ''
    context.bot.send_message(chat_id=update.effective_chat.id, text=welcome_text,
                             reply_markup=InlineKeyboardMarkup(buttons))


def file_downloader(update, context):
    if current_user.get(update.effective_chat.id) is None or current_user[update.effective_chat.id].get('state') is None:
        context.bot.send_message("Cool file! Although, I don't really know what to do with it.")
    elif current_user[update.effective_chat.id]['state'] == 'add_mass_listings':
        context.bot.get_file(update.message.document).download()
        mass_listing_checker(update, context)


def help_me(update, context):
    to_send = """
    Welcome! I'm the ezWeb bot, and I am designed to help you create beautiful websites and maintain them.
    **Creating a website**
    Click on the menu, and select the "Create website" option to get started. Or, type '/create_website' to begin creating your own site.
    
    **Managing your website**
    Click on the menu, and select the "Manage_websites" option to edit your websites. Or, type 'manage_websites' to begin creating your own site.
    
    **FAQ
    I don't see my site in the list of options after clicking on 'Manage Websites', what do I do?
    __Click on 'Manage Websites', then choose the 'Reload websites' option. Your site should be shown now.
    
    What currency are payments made in?
    __Payments are made in SGD.__
 
    What level of customisability can I expect from ezBot?
    __You will be able to create, edit, and delete listings, posts, testimonials, clients, and services. In addition, you will be able to upload your contact details and photo to allow visitors to contact you.__
    """
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=to_send)

def create_url(update, context):
    global current_user
    current_user[update.effective_chat.id] = {}
    current_user[update.effective_chat.id]['state'] = 'url_creation'
    if current_user[update.effective_chat.id]['state'] == 'initialized':
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="What would your new url be? Type 'cancel' to cancel.")
        state_changer(update, context, 'url_edit')
    else:
        current_user[update.effective_chat.id]['state'] = 'url_creation'
        response = "Certainly! Please input your desired domain name: \n(Must end with .com/.sg, \nE.g. seanrealestate.com)"
        context.bot.send_message(chat_id=update.effective_chat.id, text=response, reply_markup=None)
        current_user[update.effective_chat.id]['state'] = 'url_creation'

def url_confirmation(update, context):
    global current_user
    to_check = requests.get('http://localhost:8080/checkURL', params={'urlToCheck': str(current_user[update.effective_chat.id]['url'])})
    print(to_check.json())
    if to_check.json()["availability"]:
        price = to_check.json()['price']
        print(price)
        current_user[update.effective_chat.id]['url_price'] = price

        if current_user[update.effective_chat.id]['state'] == 'url_creation':
            buttons = [[InlineKeyboardButton("Yes, I would like to proceed.", callback_data="create_desc")],
                       [InlineKeyboardButton("No, I would like to change my url.", callback_data="change_url")],
                       [InlineKeyboardButton("I would like to stop creating a website.", callback_data="cancel")]]
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text="This url is currently available. The price of hosting this url will be $" + str(
                                         price) + ". Would you like to proceed?",
                                     reply_markup=InlineKeyboardMarkup(buttons))
        elif current_user[update.effective_chat.id]['state'] == 'url_edit':
            buttons = [[InlineKeyboardButton("Yes, I would like to proceed with payment.",
                                             callback_data="url_desc_confirmation")],
                       [InlineKeyboardButton("No, I would like to change my url.", callback_data="edit_url")],
                       [InlineKeyboardButton("No, I would like to change my description.", callback_data="edit_desc")],
                       [InlineKeyboardButton("I would like to stop creating a website.", callback_data="cancel")]]
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text="This url is current available. The price of hosting this url will be $" + str(
                                         price) + ". Would you like to proceed?",
                                     reply_markup=InlineKeyboardMarkup(buttons))

    else:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="This url is currently unavailable. Please enter another url.")


def create_desc(update, context):
    if current_user[update.effective_chat.id]['state'] == 'initialized':
        context.bot.send_message(chat_id=update.effective_chat.id, text="What would your new description be?")
        state_changer(update, context, 'sending_desc')
    elif current_user[update.effective_chat.id]['state'] == 'manage_website':
        state_changer(update, context, 'update_desc')
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=f"Your current description is: {current_user[update.effective_chat.id]['website_desc']}\nWhat would your new description be?")
    else:
        response = "Alright, input a brief description to be displayed on the website."
        context.bot.send_message(chat_id=update.effective_chat.id, text=response)
        state_changer(update, context, 'sending_desc')


def state_changer(update, context, new_state):
    global current_user
    current_user[update.effective_chat.id]['state'] = new_state


def url_desc_confirmation(update, context):
    global current_user
    print("I'm here, current state = " + current_user[update.effective_chat.id]['state'])
    if current_user[update.effective_chat.id]['state'] == 'sending_desc' or current_user[update.effective_chat.id]['state'] == 'url_edit':
        buttons = [[InlineKeyboardButton("That's right, I would like to proceed with payment.",
                                         callback_data="send_url_desc")],
                   [InlineKeyboardButton("I want to edit my url.", callback_data="edit_url")],
                   [InlineKeyboardButton("I want to edit my description.", callback_data="edit_desc")],
                   [InlineKeyboardButton("I would like to stop creating a website.", callback_data="cancel")]]
        current_user[update.effective_chat.id]['state'] = 'initialized'
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="Your desired url is: " + current_user[update.effective_chat.id]['url'] + ", and your desired description is " + current_user[update.effective_chat.id]['website_desc'] + ". Is that right?",
                                 reply_markup=InlineKeyboardMarkup(buttons))
    elif current_user[update.effective_chat.id]['state'] == 'update_desc':
        buttons = [[InlineKeyboardButton("Confirm update.", callback_data="manage_update_confirm")],
                   [InlineKeyboardButton("Cancel update.", callback_data="cancel")]]
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="Your new message is: \n" + current_user[update.effective_chat.id]['website_desc'] + "\nPlease confirm the update.",
                                 reply_markup=InlineKeyboardMarkup(buttons))


def send_initialization_data(update, context):
    global current_user
    context.bot.send_message(chat_id=update.effective_chat.id, text="Sending data...")
    global wks
    sa = gspread.service_account()
    sh = sa.open('ezWeb database')
    wks = sh.worksheet("Sheet1")
    row = 1
    while wks.acell('A' + str(row)).value is not None:
        row += 1
    wks.update('A' + str(row), current_user[update.effective_chat.id]['url'])
    wks.update('B' + str(row), current_user[update.effective_chat.id]['website_desc'])
    if wks.acell('C' + str(row)).value is None:
        wks.update('C' + str(row), update.effective_chat.id)
    wks.update('D' + str(row), '0')
    context.bot.send_message(chat_id=update.effective_chat.id, text="Almost done...")
    current_user[update.effective_chat.id]['state'] = ''
    requests.get(url='http://localhost:8080/generateSite', params={'rownumber': str(row)})
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Data sent, site will be generated after 10 minutes.")
    reset(update, context)

def payment(update, context):
    prices = [LabeledPrice(current_user[update.effective_chat.id]['url'], int(current_user[update.effective_chat.id]['url_price']) * 100)]
    context.bot.send_invoice(chat_id=update.effective_chat.id,
                             title="Your new url will be: " + current_user[update.effective_chat.id]['url'],
                             description="New URL",
                             payload="test" + str(date.today()),
                             provider_token='284685063:TEST:NWFjNzdhNjIzNTk2',
                             currency="SGD",
                             prices=prices)

def precheckout_callback(update, context):
    query = update.pre_checkout_query
    if query.invoice_payload != "test" + str(date.today()):
        query.answer(ok=False, error_messages="Something went wrong...")
    else:
        print("Initializing pre-checkout process..")
        query.answer(ok=True)


def successful_payment_callback(update, context):
    print("Payment processing...")
    context.bot.send_message(chat_id=update.effective_chat.id, text="Thank you for your payment!")
    send_initialization_data(update, context)


def send_data(update, context):
    global wks
    context.bot.send_message(chat_id=update.effective_chat.id, text="Confirmed. Sending data...")
    # sa = gspread.service_account()
    # sh = sa.open('ezWeb database')
    # wks = sh.worksheet("Sheet1")
    # row = current_user[update.effective_chat.id]['target_row']
    # wks.update('B' + row, current_user[update.effective_chat.id]['website_desc'])
    context.bot.send_message(chat_id=update.effective_chat.id, text="Updated!")
    item = {'websiteName': current_user[update.effective_chat.id]['current_url'],
            'text': current_user[update.effective_chat.id]['website_desc']
    }
    requests.post('http://localhost:8080/updateDescription', json=item)
    other_edits(update, context)

def get_my_urls(update, context):
    global wks
    global current_user
    if wks is None:
        sa = gspread.service_account()
        sh = sa.open('ezWeb database')
        wks = sh.worksheet("Sheet1")
    tg_id = update.effective_chat.id
    row = 1
    current_user[update.effective_chat.id]['urls'] = {}
    total_urls = 0
    while wks.acell('A' + str(row)).value is not None:
        row += 1
        if wks.acell('C' + str(row)).value == str(tg_id) or wks.acell('A' + str(row)).value == 'orbitaltest1.com':
            current_user[update.effective_chat.id]['urls'][wks.acell('A' + str(row)).value] = row
            total_urls += 1

def manage_website(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Sure, checking websites..")
    global current_user
    if current_user.get(update.effective_chat.id) is None:
        current_user[update.effective_chat.id] = {}
    if current_user[update.effective_chat.id].get('state') is None:
        current_user[update.effective_chat] = {}
    current_user[update.effective_chat.id]['state'] = 'manage_website'
    to_check = current_user[update.effective_chat.id].get('urls')
    if to_check is None or to_check == {}:
        get_my_urls(update, context)
    buttons = []
    counter = 1
    for my_url in current_user[update.effective_chat.id]['urls']:
        option = str(counter) + ". " + str(my_url)
        callback = "manage_choose_" + str(my_url) + "_" + str(current_user[update.effective_chat.id]['urls'][my_url])
        buttons.append([InlineKeyboardButton(str(option), callback_data=str(callback))])
        counter += 1
    if counter == 1:
        alt_buttons = [[InlineKeyboardButton("Yes! I'd like to create a website.", callback_data="create_website")],
                       [InlineKeyboardButton("I do not wish to create a website.", callback_data="cancel")]]
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="You haven't created a website with ezWeb. Would you like to proceed with creating a website instead?",
                                 reply_markup=InlineKeyboardMarkup(alt_buttons))
    else:
        buttons.append([InlineKeyboardButton("Reload my websites (Click this option if you do not see your website)", callback_data='reload_websites')])
        buttons.append([InlineKeyboardButton("I no longer want to edit my websites.", callback_data="cancel")])
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="Select a website to update.",
                                 reply_markup=InlineKeyboardMarkup(buttons))

def exit_bot(update, context):
    del current_user[update.effective_chat.id]
    context.bot.send_message(chat_id=update.effective_chat.id, text="Exiting now... Choose the 'Manage Websites' option if you'd like to continue editing your websites.")

def restart(update, context) :
    current_user[update.effective_chat.id] = {}
    context.bot.send_message(chat_id=update.effective_chat.id, text="Bot restarted!")

def website_edit(update, context):
    current_user[update.effective_chat.id]['state'] = 'manage_website'
    buttons = [[InlineKeyboardButton("My Posts", callback_data="manage_posts")],
                    [InlineKeyboardButton("My Listings", callback_data="manage_listings")],
                    [InlineKeyboardButton("Manage Agent Details", callback_data="manage_agent_details")],
                    [InlineKeyboardButton("Manage Services", callback_data="manage_services")],
                    [InlineKeyboardButton("Manage Testimonials", callback_data="manage_testimonials")],
                    [InlineKeyboardButton("Edit Website Description", callback_data="manage_edit_desc")],
                    [InlineKeyboardButton("Exit/Pick another website to edit", callback_data="exit")]]
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Which part of your site would you like to edit?",
                             reply_markup=InlineKeyboardMarkup(buttons))

def manage_posts(update, context):
    buttons = [[InlineKeyboardButton("Create a new post", callback_data="create_post")],
               [InlineKeyboardButton("Edit posts", callback_data="edit_posts")],
               [InlineKeyboardButton("Delete post", callback_data="delete_post")],
               [InlineKeyboardButton("Manage another section of my website", callback_data="edit_website")],
               [InlineKeyboardButton("Stop managing " + current_user[update.effective_chat.id]['current_url'] + ".", callback_data="manage_website")]]
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Choose a following action:",
                             reply_markup=InlineKeyboardMarkup(buttons))

def manage_listings(update, context):
    buttons = [[InlineKeyboardButton("Create a new listing", callback_data="create_listing")],
               [InlineKeyboardButton("Upload mass listings (via Excel file)", callback_data="mass_listing")]
               [InlineKeyboardButton("Edit listings", callback_data="edit_listings")],
               [InlineKeyboardButton("Delete listing", callback_data="delete_listing")],
               [InlineKeyboardButton("Manage another section of my website", callback_data="edit_website")],
               [InlineKeyboardButton("Stop managing " + current_user[update.effective_chat.id]['current_url'] + ".", callback_data="manage_website")]]
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Choose a following action:",
                             reply_markup=InlineKeyboardMarkup(buttons))

def manage_agent_details(update, context):
    buttons = [[InlineKeyboardButton("Add agent details", callback_data="add_agent_details")],
               [InlineKeyboardButton("Manage another section of my website", callback_data="edit_website")],
               [InlineKeyboardButton("Stop managing " + current_user[update.effective_chat.id]['current_url'] + ".", callback_data="manage_website")]]
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Choose a following action:",
                             reply_markup=InlineKeyboardMarkup(buttons))

def manage_services(update, context):
    buttons = [[InlineKeyboardButton("Edit Service #1", callback_data="edit_service_1")],
               [InlineKeyboardButton("Edit Service #2", callback_data="edit_service_2")],
               [InlineKeyboardButton("Edit Service #3", callback_data="edit_service_3")],
               [InlineKeyboardButton("Get more info about the 'My Services' section.", callback_data="my_services_info")],
               [InlineKeyboardButton("Manage another section of my website", callback_data="edit_website")],
               [InlineKeyboardButton("Stop managing " + current_user[update.effective_Chat.id]['current_url'] + ".", callback_data="manage_website")]]
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Which of your three services would you like to edit?",
                             reply_markup=InlineKeyboardMarkup(buttons))

def manage_testimonials(update, context):
    buttons = [[InlineKeyboardButton("Add Testimonials", callback_data="edit_testimonials")],
               [InlineKeyboardButton("Delete Testimonials", callback_data="delete_testimonials")],
               [InlineKeyboardButton("Get more info about the 'My Testimonials' section.", callback_data="my_testimonials_info")]]
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Choose a following action",
                             reply_markup=InlineKeyboardMarkup(buttons))

def my_testimonials_info(update, context):
    to_send = """
    The 'My Testimonials' section allows you to add testimonials provided by your clients. Testimonials have a similar function to reviews, where your clients would provide a general description of how you helped them, and which aspects of your service they appreciated the most.

    You can upload up to 10 testimonials in total, and you can decide whether or not you would like to include a photo of your client for your testimonial.
    """
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=to_send)
    other_edits(update, context)

def choose_testimonial(update, context):
    buttons = [[InlineKeyboardButton("Edit Testimonial 1", callback_data="choose_testimonial/1")],
               [InlineKeyboardButton("Edit Testimonial 2", callback_data="choose_testimonial/2")],
               [InlineKeyboardButton("Edit Testimonial 3", callback_data="choose_testimonial/3")],
               [InlineKeyboardButton("Edit Testimonial 4", callback_data="choose_testimonial/4")],
               [InlineKeyboardButton("Edit Testimonial 5", callback_data="choose_testimonial/5")]]
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Which one of your testimonials would you like to edit?",
                             reply_markup=InlineKeyboardMarkup(buttons))

def edit_testimonial(update, context):
    global current_user
    current_user[update.effective_chat.id]['state'] = 'add_testimonial_photo'
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Please send a photo of the person whose testimonial you would like to add.\nOtherwise, type '**skip' to skip adding a photo or type '**cancel' to stop adding a testimonial.")

def add_testimonial_name(update, context):
    global current_user
    current_user[update.effective_chat.id]['state'] = 'add_testimonial_name'
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Please type in the name of the person who is providing you with a testimony, or type '**cancel' to cancel.")

def confirm_testimonial_name(update, context):
    buttons = [[InlineKeyboardButton("Confirm", callback_data="confirm_testimonial_name")],
               [InlineKeyboardButton("Resend name", callback_data="re_send_testimonial_name")],
               [InlineKeyboardButton("Stop creating new testimonial", callback_data="website_edit")]]
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Please confirm that the testimonial name that you want to add is:\n\n " + current_user[update.effective_chat.id]['new_testimonial']['testimonial_name'],
                             reply_markup=InlineKeyboardMarkup(buttons))

def add_testimonial_text(update, context):
    global current_user
    current_user[update.effective_chat.id]['state'] = 'add_testimonial_text'
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Please type in the text of the testimony.")

def confirm_testimonial_text(update, context):
    buttons = [[InlineKeyboardButton("Confirm", callback_data="confirm_testimonial_text")],
               [InlineKeyboardButton("Resent text", callback_data="re_send_testimonial_text")],
               [InlineKeyboardButton("Stop creating new testimonial", callback_data="website_edit")]]
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Please confirm that the testimonial text that you want to add is:\n\n " + current_user[update.effective_chat.id]['new_testimonial']['testimonial_text'],
                             reply_markup=InlineKeyboardMarkup(buttons))

def confirm_new_testimonial(update, context):
    buttons = [[InlineKeyboardButton("Confirm", callback_data="confirm_send_new_testimonial")],
               [InlineKeyboardButton("Cancel", callback_data="website_edit")]]
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Please confirm that you would like to upload this testimonial.",
                             reply_markup=InlineKeyboardMarkup(buttons))

def send_new_testimonial(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Confirmed... sending update...")
    new_request = {'name': current_user[update.effective_chat.id]['new_testimonial']['testimonial_name'],
                   'text': current_user[update.effective_chat.id]['new_testimonial']['testimonial_text'],
                   'photo': current_user[update.efffective_chat.id]['current_service']['testimonial_photo'],
                   'websiteName': current_user[update.effective_chat.id]['current_url'],
                   }
    r = requests.post('http://localhost:8080/addTestimonial', json=new_request)
    context.bot.send_message(chat_id=update.effective_chat,
                             text="Update sent successfully!")
    other_edits(update, context)

def other_edits(update, context):
    buttons = [[InlineKeyboardButton("My Posts", callback_data="manage_posts")],
               [InlineKeyboardButton("My Listings", callback_data="manage_listings")],
               [InlineKeyboardButton("Manage Agent Details", callback_data="manage_agent_details")],
               [InlineKeyboardButton("Manage Services", callback_data="manage_services")],
               [InlineKeyboardButton("Edit Website Description", callback_data="manage_edit_desc")],
               [InlineKeyboardButton("Exit/Pick another website to edit", callback_data="exit")]]
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Are there any other edits that you would like to make to " + current_user[update.effective_chat.id]['current_url'] + "?",
                             reply_markup=InlineKeyboardMarkup(buttons))

def my_services_info(update, context):
    to_send = """
    The 'My Services' section allows you to list three different services that you offer for your clients.
    
    During the website generation process, this section has been auto-generated for you, and if you would like to edit them, you can pick the select them individually in the 'Edit My Services' option.
    
    The services are numbered #1 to #3 from left to right, in increasing order."""
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=to_send)
    other_edits(update, context)

def edit_service_title(update, context):
    global current_user
    current_user[update.effective_chat.id]['state'] = 'edit_service_title'
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Please type in your new service title, or type '**cancel* to cancel.")


def edit_service_title_confirmation(update, context):
    buttons = [[InlineKeyboardButton("Confirm", callback_data="confirm_service_title")],
               [InlineKeyboardButton("Resend service title", callback_data="re_edit_service_title")]]
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Please confirm that your new service title would be " + current_user[update.effective_chat.id]['current_service']['service_title'] + ".",
                             reply_markup=InlineKeyboardMarkup(buttons))

def edit_service_description(update, context):
    global current_user
    current_user[update.effective_chat.id]['state'] = 'edit_service_description'
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Please type in your new service description, or type '**cancel' to cancel.")

def edit_service_description_confirmation(update, context):
    buttons = [[InlineKeyboardButton("Confirm", callback_data="confirm_service_description")],
               [InlineKeyboardButton("Resend service description", callback_data="re_edit_service_description")]]
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Please confirm that your new service title would be " + current_user[update.effective_chat.id]['current_service']['service_description'],
                             reply_markup=InlineKeyboardMarkup(buttons))

def confirm_send_service(update, context):
    buttons = [[InlineKeyboardButton("Confirm", callback_data="confirm_send_service")],
               [InlineKeyboardButton("I no longer want to edit my services.",  callback_data="cancel")]]
    to_send = "Please confirm that your new service would have have the following details:\n\nTitle: " + current_user[update.effective_chat.id]['current_service']['service_title'] + "\n" + "Description: " + current_user[update.effective_chat.id]['current_service']['service_description']
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=to_send,
                             reply_markup=InlineKeyboardMarkup(buttons))

def send_service_update(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Confirmed... sending update...")
    new_request = {'title': current_user[update.effective_chat.id]['current_service']['service_title'],
                   'text': current_user[update.effective_chat.id]['current_service']['service_description'],
                   'serviceNumber': current_user[update.efffective_chat.id]['current_service']['service_number'],
                   'websiteName': current_user[update.effective_chat.id]['current_url'],
                   }
    r = requests.post('http://localhost:8080/editService', json=new_request)
    context.bot.send_message(chat_id=update.effective_chat,
                             text="Update sent successfully!")
    other_edits(update, context)

def create_post_title(update, context):
    global current_user
    current_user[update.effective_chat.id]['state'] = 'create_post'
    current_user[update.effective_chat.id]['new_post'] = {}
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="I can help you out with that! What would the title of your new post be? (Type 'cancel' to exit)")


def create_post_title_confirmation(update, context):
    buttons = [[InlineKeyboardButton("Confirm title.", callback_data="confirm_post_title")],
               [InlineKeyboardButton("I would like to change my title.", callback_data="change_post_title")],
               [InlineKeyboardButton("I would like to stop creating a post.", callback_data="cancel")]]
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="The title of your new post will be " + current_user[update.effective_chat.id]['new_post']['post_title'] + ". Please confirm.",
                             reply_markup=InlineKeyboardMarkup(buttons))


def create_post_content(update, context):
    global current_user
    current_user[update.effective_chat.id]['state'] = 'create_post_content'
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Input the content of your new post.")


def create_post_content_confirmation(update, context):
    buttons = [[InlineKeyboardButton("Confirm content.", callback_data="confirm_post_content")],
               [InlineKeyboardButton("I would like to change the content of this post.",
                                     callback_data="change_post_content")],
               [InlineKeyboardButton("I would like to stop creating a post.", callback_data="cancel")]]
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="The content of your new post will be " + current_user[update.effective_chat.id]['new_post']['post_content'] + ". Please confirm.",
                             reply_markup=InlineKeyboardMarkup(buttons))

def send_post_confirmation(update, context):
    buttons = [[InlineKeyboardButton("Confirm post.", callback_data="confirm_post_submission")],
               [InlineKeyboardButton("I would like to change my title and content.", callback_data="create_post")],
               [InlineKeyboardButton("I would like to stop creating this post.", callback_data="cancel")]]
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="The title of your new post is " + current_user[update.effective_chat.id]['new_post']['post_title'] + ", and the content of your new post is "
                                  + current_user[update.effective_chat.id]['new_post']['post_content'], reply_markup=InlineKeyboardMarkup(buttons))

def confirm_post(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="One moment...")

    new_request = {'title': current_user[update.effective_chat.id]['new_post']['post_title'],
                   'content': current_user[update.effective_chat.id]['new_post']['post_content'],
                   'websiteName': current_user[update.effective_chat.id]['current_url'],
                   }
    r = requests.post('http://localhost:8080/createPost', json=new_request)
    del current_user[update.effective_chat.id]['new_post']
    context.bot.send_message(chat_id=update.effective_chat.id, text="Done!")
    other_edits(update, context)

def create_post_photo(update, context):
    global current_user
    current_user[update.effective_chat.id]['state'] = 'create_post_photo'
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Please upload a photo for your post if you'd like. Otherwise, type '**skip' to skip adding a photo.")
    
def delete_post(update, context):
    global current_user
    current_user[update.effective_chat.id]['posts'] = {}
    buttons = []
    to_check = requests.get(url='http://localhost:8080/retrievePost', params={'websiteName': str(current_user[update.effective_chat.id]['url'])})
    to_check = to_check.json()
    for item in to_check:
        post = {
            'id': str(item['id']),
            'title': item['title'],
            'content': item['content']
        }
        current_user[update.effective_chat.id]['posts'][str(item['id'])] = post

        buttons.append([InlineKeyboardButton("Post id #" + str(item['id']) + ": " + item['title'],
                                                 callback_data="post_delete/" + str(item['id']))])
    if len(buttons) == 0:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="You do not have any posts available right now.")
        other_edits(update, context)
    buttons.append([InlineKeyboardButton("I no longer want to delete my posts.", callback_data="data")])
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Which of your posts do you want to delete?",
                             reply_markup=InlineKeyboardMarkup(buttons))

def delete_confirmation(update, context):
    buttons = [[InlineKeyboardButton("Confirm deletion.", callback_data="confirm_post_deletion")],
               [InlineKeyboardButton("I changed my mind.", callback_data="cancel")]]
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Please confirm that you would like to delete the following post: " + current_user[update.effective_chat.id]['current_post']['title'],
                             reply_markup=InlineKeyboardMarkup(buttons))

def confirm_delete(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Deleting post...")
    to_delete = current_user[update.effective_chat.id]['current_post']
    new_request = {'title': to_delete['title'],
                   'content': to_delete['content'],
                   'websiteName': current_user[update.effective_chat.id]['current_url'],
                   'postId': to_delete['id']
                   }
    requests.post('http://localhost:8080/deletePost', json=new_request)
    del current_user[update.effective_chat.id]['current_post']
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Done!")
    other_edits(update, context)

def edit_posts(update, context):
    global current_user
    buttons = []
    to_check = requests.get(url='http://localhost:8080/retrievePost', params={'websiteName': str(current_user[update.effective_chat.id]['url'])})
    counter = 0
    current_user[update.effective_chat.id]['posts'] = {}
    for item in to_check.json():
        post = {
            'id': str(item['id']),
            'title': item['title'],
            'content': item['content']
        }
        current_user[update.effective_chat.id]['posts'][str(item['id'])] = post
        buttons.append([InlineKeyboardButton("Post id #" + str(item['id']) + ": " + str(item['title']),
                                            callback_data="post_edit/" + str(item['id']))])
        counter += 1
    if len(buttons) == 0:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="You do not have any posts available right now. Type /start if there's anything else I can help you with.")
        other_edits(update, context)
    else:
        buttons.append([InlineKeyboardButton("I no longer want to edit my posts.", callback_data="cancel")])
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="Which of your posts do you want to edit?",
                                 reply_markup=InlineKeyboardMarkup(buttons))

def edit_post_title_or_content(update, context):
    buttons = [[InlineKeyboardButton("Post title", callback_data="edit_post_title")],
               [InlineKeyboardButton("Post content", callback_data="edit_post_content")],
               [InlineKeyboardButton("Cancel editing", callback_data="cancel")]]
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="How would you like to edit this post?",
                             reply_markup=InlineKeyboardMarkup(buttons))

def edit_post_content(update, context):
    global current_user
    current_user[update.effective_chat.id]['state'] = 'edit_post_content'
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="The current post content is: " + current_user[update.effective_chat.id]['current_post']['content'] + ", please input your new content. " + "(Type 'cancel' to cancel)")

def edit_post_title(update, context):
    global current_user
    current_user[update.effective_chat.id]['state'] = 'edit_post_title'
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="The current post content is " + current_user[update.effective_chat.id]['current_post']['title'] + ", please input your new title. (Type 'cancel to cancel)")

def edit_post_content_confirmation(update, context):
    buttons = [[InlineKeyboardButton("Confirm update.", callback_data='confirm_post_edit')],
               [InlineKeyboardButton("Cancel.", callback_data='cancel')]]
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Your updated post is Title: " + current_user[update.effective_chat.id]['current_post']['title'] + ", and Content: " + current_user[update.effective_chat.id]['current_post']['content'] + ". Please confirm.",
                             reply_markup=InlineKeyboardMarkup(buttons))

def confirm_edit(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Updating post...")
    to_update = current_user[update.effective_chat.id]['current_post']
    new_request = {'title': to_update['title'],
                   'content': to_update['content'],
                   'websiteName': current_user[update.effective_chat.id]['current_url'],
                   'postId': to_update['id']
                   }
    # 'postId' : post_id
    requests.post('http://localhost:8080/updatePost', json=new_request)
    del current_user[update.effective_chat.id]['current_post']
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Done!")
    other_edits(update, context)

def mass_listing(update, context):
    global num
    global current_user
    num += 1
    file_name = create_excel_template(num)
    current_user[update.effective_chat.id]['mass_listing_file'] = file_name
    current_user[update.effective_chat.id]['state'] = 'add_mass_listings'
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Please input the details of each new listing in consecutive rows in this excel sheet.\n\nFor featured and other photos, you will have to upload the photos onto http://imgbb.com and add the link to the excel sheet accordingly.\n\nOtherwise, type 'Cancel' to exit.")
    context.bot.send_document(chat_id=update.effective_chat.id,
                              document=open(file_name, "rb"))

def mass_listing_checker(update, context):
    global current_user
    res = validate_inputs(current_user[update.effective_chat.id]['mass_listing_file'])
    if not res == "Valid":
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=res)
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="Please reupload the excel file, or type 'Cancel' to exit.")
    else:
        current_user[update.effective_chat.id]['mass_listings'] = parse_excel_file(current_user[update.effective_chat.id]['mass_listing_file'])
        upload_mass_listing(update, context, current_user[update.effective_chat.id]['mass_listings'])

def upload_mass_listing(update, context, listings):
    counter = 1
    for listing in listings:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="Uploading listing #" + str(counter))
        requests.post(url='http://localhost:8080/createListing',
                      json=listing)
        counter +=1
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Done!")


def create_listing(update, context):
    global current_user
    current_user[update.effective_chat.id]['state'] = 'create_listing_title'
    current_user[update.effective_chat.id]['new_listing'] = {}
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Input a title description of your listing (Eg. Blk 382 4br/Cuscaden Reserve Freehold/Braddell Heights Bungalow)")

def listing_title_confirmation(update, context):
    buttons = [[InlineKeyboardButton("Proceed with property details", callback_data='confirm_listing_title')],
               [InlineKeyboardButton("Cancel.", callback_data='cancel')]]
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Are you happy with the following title? '" + current_user[update.effective_chat.id]['new_listing']['title'] + "'",
                             reply_markup=InlineKeyboardMarkup(buttons))

def create_property_details(update, context):
    global current_user
    current_user[update.effective_chat.id]['state'] = 'create_property_details'
    to_send = """
    Please input your property details in the following format:
    
    *If unit is sold, please type 'Sold for ...' for Price.
    *For fields that are not applicable, please type 'Not applicable'
    
    Property type
    Number of rooms
    Year built
    Address
    Tenure
    Total Area
    Floor
    Number of Storeys
    Price
    
    Example input #1:
    Condominium
    4 Rooms
    2017
    9 Kallang Pudding Rd, #14-18
    Freehold
    1400 sq ft
    14th floor
    2
    $1,100,000
    
    Example input #2:
    Bungalow
    6 Rooms
    Not applicable
    Braddell Heights Estate
    Freehold
    6000 sq ft
    Not applicable
    3
    Sold for $15,000,000
    """
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=to_send)

def listing_details(update, property_details):
    global current_user
    if current_user[update.effective_chat.id]['state'] == 'create_property_details':
        listing = current_user[update.effective_chat.id]['new_listing']
    else:
        listing = current_user[update.effective_chat.id]['current_listing']

    details = property_details.split('\n')
    listing['websiteName'] = current_user[update.effective_chat.id]['current_url']
    listing['property_type'] = details[0]
    listing['num_rooms'] = details[1]
    listing['year_built'] = details[2]
    listing['address'] = details[3]
    listing['tenure'] = details[4]
    listing['total_area'] = details[5]
    listing['floor'] = details[6]
    listing['number_of_storeys'] = details[7]
    listing['price'] = details[8]
    listing['overall_info'] = property_details

def property_details_confirmation(update, context):
    buttons = [[InlineKeyboardButton("Proceed to add property description.", callback_data="listing_description")],
               [InlineKeyboardButton("Change property details.", callback_data="change_property_details")],
               [InlineKeyboardButton("Stop creating a listing.", callback_data='cancel')]]
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Here are your property details: \n\n" + current_user[update.effective_chat.id]['new_listing'][
                                 'overall_info'] + "\n\nWould you like to proceed or change your property details?",
                             reply_markup=InlineKeyboardMarkup(buttons))

def listing_description(update, context):
    global current_user
    current_user[update.effective_chat.id]['state'] = 'listing_description'
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Input the description for this property listing.")

def listing_description_confirmation(update, context):
    buttons = [[InlineKeyboardButton("Proceed with uploading featured photo", callback_data='upload_featured_photo')],
               [InlineKeyboardButton("Change description", callback_data='change_listing_desc')],
               [InlineKeyboardButton("Stop creating a listing", callback_data='cancel')]]
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Your description is: " + current_user[update.effective_chat.id]['new_listing'][
                                 'description'] + "\nWould you like to proceed with uploading a featured photo?",
                             reply_markup=InlineKeyboardMarkup(buttons))

def upload_featured_photo(update, context):
    global current_user
    current_user[update.effective_chat.id]['state'] = 'upload_featured_photo'
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Please upload a featured photo for this property listing.")


def upload_extra_photos(update, context):
    global current_user
    current_user[update.effective_chat.id]['state'] = 'upload_extra_photos'
    current_user[update.effective_chat.id]['new_listing']['num_extra_photos'] = 0
    current_user[update.effective_chat.id]['new_listing']['extra_photos'] = []
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Please upload up to ten extra photos for this property listing, and type '**done' after you are done")

def photo_receiver(update, context):
    if current_user[update.effective_chat.id]['state'] == 'upload_featured_photo':
        buttons = [[InlineKeyboardButton("Proceed to send extra photos.", callback_data='send_extra_photos')],
                   [InlineKeyboardButton("Resend featured photo", callback_data='upload_featured_photo')],
                   [InlineKeyboardButton("Stop creating a listing", callback_data='cancel')]]
        photo_file = update.message.photo[-1].get_file()
        file_path = photo_file['file_path']
        file_id = photo_file['file_id']
        current_user[update.effective_chat.id]['new_listing']['featured_photo_file_path'] = file_path
        current_user[update.effective_chat.id]['new_listing']['featured_photo_file_id'] = file_id
        context.bot.send_photo(chat_id=update.effective_chat.id,
                               photo=file_id)
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="This is the photo received. Would you like to proceed to sending extra photos of the property?",
                                 reply_markup=InlineKeyboardMarkup(buttons))
    elif current_user[update.effective_chat.id]['state'] == 'upload_extra_photos':
        photo_file = update.message.photo[-1].get_file()
        photo_file.download()
        to_add = current_user[update.effective_chat.id]['new_listing']['num_extra_photos']
        current_user[update.effective_chat.id]['new_listing']['num_extra_photos'] += 1
        current_user[update.effective_chat.id]['new_listing']['extra_photos'].append({})
        current_user[update.effective_chat.id]['new_listing']['extra_photos'][to_add]['file_path'] = photo_file['file_path']
        current_user[update.effective_chat.id]['new_listing']['extra_photos'][to_add]['file_id'] = photo_file['file_id']
        if current_user[update.effective_chat.id]['new_listing']['num_extra_photos'] == 10:
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text="Photo upload limit reached. Proceeding to confirm listing upload...")
            confirm_extra_photos(update, context)
        else:
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text=str(
                                         current_user[update.effective_chat.id]['new_listing']['num_extra_photos']) + " photos added. Type '**done' if you are done. Otherwise, continue uploading extra photos of the property.")
    elif current_user[update.effective_chat.id]['state'] == 'add_agent_pictures':
        photo_file = update.message.photo[-1].get_file()
        current_user[update.effective_chat.id]['agent_details']['pictures'].append({})
        curr_num = current_user[update.effective_chat.id]['agent_details']['num_pictures']
        current_user[update.effective_chat.id]['agent_details']['pictures'][curr_num]['file_path'] = photo_file['file_path']
        current_user[update.effective_chat.id]['agent_details']['pictures'][curr_num]['file_id'] = photo_file['file_id']
        current_user[update.effective_chat.id]['agent_details']['num_pictures'] += 1
        if current_user[update.effective_chat.id]['agent_details']['num_pictures'] == 2:
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text="Two pictures uploaded. Proceeding...")
            confirm_agent_pictures(update, context)
        else:
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text="1 picture added. Add one more of yourself with the same requirement.")
    elif current_user[update.effective_chat.id]['state'] == 'edit_listing_featured_photo':
        buttons = [[InlineKeyboardButton("Confirm", callback_data="update_listing")],
                   [InlineKeyboardButton("Resend featured photo", callback_data="re_edit_listing_featured_photo")],
                   [InlineKeyboardButton("Stop editing the current listing", callback_data="cancel")]]
        photo_file = update.message.photo[-1].get_file()
        file_path = photo_file['file_path']
        file_id = photo_file['file_id']
        current_user[update.effective_chat.id]['current_listing']['featured_photo_file_path'] = file_path
        current_user[update.effective_chat.id]['current_listing']['featured_photo_file_id'] = file_id
        context.bot.send_photo(chat_id=update.effective_chat.id,
                               photo=file_id)
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="This is the photo received. Please confirm that you would like this to be your new featured photo.",
                                 reply_markup=InlineKeyboardMarkup(buttons))
    elif current_user[update.effective_chat.id]['state'] == 'edit_listing_extra_photos':
        photo_file = update.message.photo[-1].get_file()
        to_add = current_user[update.effective_chat.id]['current_listing']['num_extra_photos']
        current_user[update.effective_chat.id]['current_listing']['num_extra_photos'] += 1
        current_user[update.effective_chat.id]['current_listing']['extra_photos'].append({})
        current_user[update.effective_chat.id]['current_listing']['extra_photos'][to_add]['file_path'] = photo_file['file_path']
        current_user[update.effective_chat.id]['current_listing']['extra_photos'][to_add]['file_id'] = photo_file['file_id']
        if current_user[update.effective_chat.id]['current_listing']['num_extra_photos'] == 10:
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text="Photo upload limit reached. Proceeding to confirm extra photos...")
            confirm_edit_listing_extra_photos(update, context)
        else:
            cont
