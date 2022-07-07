from telegram.ext import *
from telegram import *
import requests
import gspread
import os
from datetime import date
# Setting up our logger
import logging

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
               [InlineKeyboardButton("Edit listings", callback_data="edit_listing")],
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

def other_edits(update, context):
    buttons = [[InlineKeyboardButton("My Posts", callback_data="manage_posts")],
               [InlineKeyboardButton("My Listings", callback_data="manage_listings")],
               [InlineKeyboardButton("Manage Agent Details", callback_data="manage_agent_details")],
               [InlineKeyboardButton("Edit Website Description", callback_data="manage_edit_desc")],
               [InlineKeyboardButton("Exit/Pick another website to edit", callback_data="exit")]]
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Are there any other edits that you would like to make to " + current_user[update.effective_chat.id]['current_url'] + "?",
                             reply_markup=InlineKeyboardMarkup(buttons))


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
                             text="The current post content is: " + current_user[update.effective_chat.id]['current_post']['content'] + ", please input your new content. "
                                                                                   "(Type 'cancel' to cancel)")


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
    if current_user['state'] == 'create_property_details':
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
                            text="This is the photo received. Please confirm that this will be your new featured photo.",
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
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text=str(current_user[update.effective_chat.id]['current_listing']['num_extra_photos']) + " photos added. Type '**done' if you are done. Otherwise, continue uploading extra photos of the property.")
    else:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="Cool photo! Although..I'm not sure what to do with it..")

def confirm_extra_photos(update, context):
    buttons = [[InlineKeyboardButton("Yes, I would like to proceed.", callback_data='confirm_new_listing')],
               [InlineKeyboardButton("No, I would like to re-upload the extra photos",
                                     callback_data='send_extra_photos')],
               [InlineKeyboardButton("I would like to stop creating a new listing", callback_data='cancel')]]
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Here are the extra photos uploaded.")
    for i in range(current_user[update.effective_chat.id]['new_listing']['num_extra_photos']):
        context.bot.send_photo(chat_id=update.effective_chat.id,
                               photo=current_user[update.effective_chat.id]['new_listing']['extra_photos'][i]['file_id'])
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Are you happy with these photos?",
                             reply_markup=InlineKeyboardMarkup(buttons))


def confirm_new_listing(update, context):
    buttons = [[InlineKeyboardButton("Confirm upload.", callback_data='confirm_listing_upload')],
               [InlineKeyboardButton("Cancel upload.", callback_data='cancel')]]
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Please confirm that you would like to upload this new listing.",
                             reply_markup=InlineKeyboardMarkup(buttons))


def confirm_listing_upload(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Uploading listing... please wait...")
    requests.post(url='http://localhost:8080/createListing', json=current_user[update.effective_chat.id]['new_listing'])
    del current_user[update.effective_chat.id]['new_listing']
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Done!")
    other_edits(update, context)

def delete_listings(update, context):
    global current_user
    current_user[update.effective_chat.id]['listings'] = {}
    context.bot.send_message(chat_id=update.effective_chat.id,
                            text="Retrieving listings, please wait...")
    items = requests.get(url='http://localhost:8080/retrieveListing', params={'websiteName': str(current_user[update.effective_chat.id]['current_url'])})
    buttons = []
    items = items.json()
    for item in items:
        new_item = {
            'id': item['id'],
            'title': item['title']
        }
        current_user[update.effective_chat.id]['listings'][str(item['id'])] = new_item
        buttons.append([InlineKeyboardButton("Listing id# " + str(item['id']) + ": " + str(item['title']),
                                             callback_data="listing_delete/" + str(item['id']))])
    if len(buttons) == 0:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="You do not have any listings available right now. Type /start if there's anything else I can help you with.")
        other_edits(update, context)
    else:
        buttons.append([InlineKeyboardButton("I no longer want to delete my listings.", callback_data='cancel')])
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="Which of your listings do you want to delete?",
                                 reply_markup=InlineKeyboardMarkup(buttons))

def delete_listings_confirmation(update, context):
    buttons = [[InlineKeyboardButton("Confirm deletion", callback_data='confirm_listing_delete')],
               [InlineKeyboardButton("I no longer want to delete this listing.", callback_data='cancel')]]

    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="The listing you have chosen is: " + current_user[update.effective_chat.id]['current_listing']['title'] + "\n\n Please confirm that you want to delete this listing.",
                             reply_markup=InlineKeyboardMarkup(buttons))

def confirm_delete_listing(update, context):
    new_request = {
        'listingId': current_user[update.effective_chat.id]['current_listing']['id'],
        'title': current_user[update.effective_chat.id]['current_listing']['title'],
        'websiteName': current_user[update.effective_chat.id]['current_url']
    }
    requests.post('http://localhost:8080/deleteListing', json=new_request)
    del current_user[update.effective_chat.id]['current_listing']
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Listing has successfully been deleted.")
    other_edits(update, context)

def edit_listings(update, context):
    global current_user
    buttons = []
    to_check = requests.get(url='http://localhost:8080/retrieveListing', params={'websiteName': str(current_user[update.effective_chat.id]['current_url'])})
    current_user[update.effective_chat.id]['listings'] = {}
    for item in to_check.json():
        listing = {
            'id': str(item['id']),
            'title': str(item['title'])
        }
        current_user[update.effective_chat.id]['listings'][str(item['id'])] = listing
        buttons.append([InlineKeyboardButton("Listing id#" + str(item['id']) + ": " + str(item['title']),
                                             callback_data="listing_edit/" + str(item['id']))])
    if len(buttons) == 0:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="You do not have any listings right now :(")
        other_edits(update, context)
    else:
        buttons.append([InlineKeyboardButton("I no longer want to edit my listings.", callback_data="cancel")])
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="Which one of your listings would you like to edit?")

def choose_edit_listing(update, context):
    buttons = [[InlineKeyboardButton("Edit featured photo", callback_data="edit_listing_featured_photo")],
               [InlineKeyboardButton("Edit extra photos", callback_data="edit_listing_extra_photos")],
               [InlineKeyboardButton("Edit description", callback_data="edit_listing_description")],
               [InlineKeyboardButton("Edit title", callback_data="edit_listing_title")],
               [InlineKeyboardButton("Edit property details (Address, price, area, floor, etc.)", callback_data="edit_listing_property_details")]]
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="How would you like to edit '" + current_user[update.effective_chat.id]['current_listing']['title'] + "'?",
                             reply_markup=InlineKeyboardMarkup(buttons))


def edit_listing_featured_photo(update, context):
    global current_user
    current_user[update.effective]['state'] = 'edit_listing_featured_photo'
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Sure! Please upload a new featured photo for your listing. Otherwise, type 'cancel' to go back to the main menu.")

def edit_listing_extra_photo(update, context):
    global current_user
    current_user[update.effective_chat.id]['state'] = 'edit_listing_extra_photos'
    current_user[update.effective_chat.id]['extra_photos'] = []
    current_user[update.effective_chat.id]['current_listing']['num_extra_photos'] = 0
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Please upload up to 10 extra photos, and type **done once you are done.")


def confirm_edit_listing_extra_photos(update, context):
    buttons = [[InlineKeyboardButton("Confirm", callback_data="update_listing")],
               [InlineKeyboardButton("Resend extra photos", callback_data="edit_listing_extra_photos")],
               [InlineKeyboardButton("Stop editing this listing", callback_data="cancel")]]
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Here are the extra photos uploaded.")
    for i in range(current_user[update.effective_chat.id]['new_listing']['num_extra_photos']):
        context.bot.send_photo(chat_id=update.effective_chat.id,
                               photo=current_user[update.effective_chat.id]['current_listing']['extra_photos'][i][
                                   'file_id'])
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Are you happy with these photos?",
                             reply_markup=InlineKeyboardMarkup(buttons))

def update_listing(update, context):
    global current_user
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Sending data...This process may take up to thirty seconds...")
    state = current_user[update.effective_chat.id]['state']
    listing = current_user[update.effective_chat.id]['current_listing']
    if state == 'edit_listing_featured_photo':
        requests.post('http://localhost:8080/updateListingFeatured', json=listing)
    elif state == 'edit_listing_extra_photos':
        requests.post('http://localhost:8080/updateListingGallery', json=listing)
    elif state == 'edit_listing_description':
        requests.post('http://localhost:8080/updateListingDescription', json=listing)
    elif state == 'edit_listing_title':
        requests.post('http://localhost:8080/updateListingTitle', json=listing)
    elif state == 'edit_listing_property_details':
        requests.post('http://localhost:8080/updateListingPropertyDetails', json=listing)
    del current_user[update.effective_chat.id]['current_listing']
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Done!")

def edit_listing_description(update, context):
    global current_user
    current_user[update.effective]['state'] = 'edit_listing_description'
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Please input a new description for " + current_user[update.effective_chat.id]['current_listing']['title'] + "\nOtherwise, type 'cancel' to cancel.")

def confirm_edit_listing_description(update, context):
    buttons = [[InlineKeyboardButton("Confirm", callback_data="update_listing")],
               [InlineKeyboardButton("Send a new description", callback_data="edit_listing_description")],
               [InlineKeyboardButton("Stop editing this listing", callback_data="cancel")]]
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Your new description is:\n\n" + current_user[update.effective_chat.id]['current_listing']['description'] + "\n\nPlease confirm.",
                             reply_markup=InlineKeyboardMarkup(buttons))

def edit_listing_title(update, context):
    global current_user
    current_user[update.effective]['state'] = 'edit_listing_title'
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Please input a new title for " + current_user[update.effective_chat.id]['current_listing']['title'] + "\nOtherwise, type 'cancel' to cancel.")

def confirm_edit_listing_title(update, context):
    buttons = [[InlineKeyboardButton("Confirm", callback_data="update_listing")],
               [InlineKeyboardButton("Send a new description", callback_data="edit_listing_title")],
               [InlineKeyboardButton("Stop editing this listing", callback_data="cancel")]]
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Your new title is:\n\n" + current_user[update.update.effective_chat.id]['current_listing']['title'] + "\n\nPlease confirm.",
                             reply_markup=InlineKeyboardMarkup(buttons))

def edit_listing_property_details(update, context):
    global current_user
    to_send = """
        Please input your new property details in the following format:

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
    current_user[update.effective]['state'] = "edit_listing_property_details"
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=to_send)


def confirm_edit_listing_property_details(update, context):
    buttons = [[InlineKeyboardButton("Confirm", callback_data="update_listing")],
               [InlineKeyboardButton("Send a new description", callback_data="edit_listing_property_details")],
               [InlineKeyboardButton("Stop editing this listing", callback_data="cancel")]]

    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Here are your new property details: \n\n" + current_user[update.effective_chat.id]['current_listing'][
                                 'overall_info'] + "\n\nPlease confirm.",
                             reply_markup=InlineKeyboardMarkup(buttons))

def add_agent_pictures(update, context):
    global current_user
    current_user[update.effective_chat.id]['agent_details']['num_pictures'] = 0
    current_user[update.effective_chat.id]['agent_details']['pictures'] = []
    current_user[update.effective_chat.id]['state'] = "add_agent_pictures"
    context.bot.send_message(chat_id=update.effective_chat.id, text="Certainly! Upload two pictures of yourself of size 480 x 480 with a transparent background.")

def confirm_agent_pictures(update, context):
    buttons = [[InlineKeyboardButton("Confirm and proceed", callback_data="confirm_agent_pictures")],
               [InlineKeyboardButton("Upload new pictures", callback_data="re_add_agent_pictures")],
               [InlineKeyboardButton("I'd like to add agent details another time.", callback_data='cancel')]]
    for i in range(2):
        context.bot.send_photo(chat_id=update.effective_chat.id,
                               photo=current_user[update.effective_chat.id]['agent_details']['pictures'][i]['file_id'])
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Confirm upload?",
                             reply_markup=InlineKeyboardMarkup(buttons))

def add_about_me(update, context):
    global current_user
    current_user[update.effective_chat.id]['state'] = "add_about_me"
    context.bot.send_message(chat_id=update.effective_chat.id, text="Let's add an 'About me' section to your site."
                                                                    "\n\nFor example, [Your name] has a passion for real estate, and helping clients achieve [X goals]. "
                                                                    "[He/she/they] have been a licensed Realtor for [number of years] and a top-performing agent at [your agency]. [Your name] has dedicated [number of years] helping clients buy and sell property with [insert sales statistics].")
def confirm_about_me(update, context):
    buttons = [[InlineKeyboardButton("Confirm and proceed.", callback_data='confirm_about_me')],
               [InlineKeyboardButton("Enter new 'About Me' section.", callback_data='re_add_agent_details')],
               [InlineKeyboardButton("I'd like to add agent details another time.", callback_data='cancel')]]
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="The 'About Me' section that you have written is as follows:\n\n"
                             + current_user[update.effective_chat.id]['agent_details']['about_me'] + "\n\n Please confirm.",
                             reply_markup=InlineKeyboardMarkup(buttons))

def add_contact_details(update, context):
    global current_user
    current_user[update.effective_chat.id]['state'] = "add_contact_details"
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Please type your name, phone number, and email address in the format provided below:"
                                  "\n\nJoshua Lee\n98765432\njoshua@gmail.com")

def confirm_contact_details(update, context):
    buttons = [[InlineKeyboardButton("Confirm and proceed.", callback_data='confirm_contact_details')],
               [InlineKeyboardButton("Enter new contact details", callback_data='re_add_contact_details')],
               [InlineKeyboardButton("I'd like to add agent details another time.", callback_data='cancel')]]
    text = "Your displayed name will be: " + current_user[update.effective_chat.id]['agent_details']['name'] + ",\n" + "Your displayed phone number will be: " + current_user[update.effective_chat.id]['agent_details']['number'] + ",\n" + "Your displayed email address will be: " + current_user[update.effective_chat.id]['agent_details']['email']
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=text,
                             reply_markup=InlineKeyboardMarkup(buttons))

def add_agent_quote(update, context):
    global current_user
    current_user[update.effective_chat.id]['state'] = "add_agent_quote"
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Please input a quote that summarises your values and mission in the real estate industry.\n\n"
                                  "Example: \nI am dedicated to ensuring an efficient and effective transaction for each of my clients,"
                                  "with the goal of maximising their satisfaction and financial gain.")

def confirm_agent_quote(update, context):
    buttons = [[InlineKeyboardButton("Confirm and proceed.", callback_data='confirm_agent_quote')],
               [InlineKeyboardButton("Enter new agent quote", callback_data='re_add_agent_quote')],
               [InlineKeyboardButton("I'd like to cancel and add agent details another time instead.", callback_data='cancel')]]
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Your desired quote is: \n\n" + current_user[update.effective_chat.id]['agent_details']['quote'] + "\n\nPlease confirm.",
                             reply_markup=InlineKeyboardMarkup(buttons))

def confirm_agent_details(update, context):
    buttons = [[InlineKeyboardButton("Confirm and upload", callback_data='confirm_agent_details')],
               [InlineKeyboardButton("Cancel upload", callback_data='cancel')]]
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Please confirm that you would like to upload your agent details.",
                             reply_markup=InlineKeyboardMarkup(buttons))

def send_agent_details(update, context):
    details = current_user[update.effective_chat.id]['agent_details']
    to_send = {
        'websiteName': current_user[update.effective_chat.id]['current_url'],
        'agentPicture': details['pictures'],
        'aboutMe': details['about_me'],
        'agentNumber': details['number'],
        'agentName': details['name'],
        'agentEmail': details['email'],
        'agentQuote': details['quote']
    }
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Uploading details...")
    requests.post('http://localhost:8080/updateSiteSetting', json=to_send)
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Done!")

def reset(update, context):
    global current_user
    del current_user[update.effective_chat.id]
    context.bot.send_message(chat_id=update.effective_chat.id, text="Alright! Let me know if you need anything else! :)")


def inline_query(update, context):
    query = update.callback_query.data
    update.callback_query.answer()
    context.bot.edit_message_reply_markup(
        message_id=update.callback_query.message.message_id,
        chat_id=update.callback_query.message.chat.id,
        reply_markup=None)
    global current_user
    if "create_website" in query:
        create_url(update, context)
    elif "reload_websites" in query:
        get_my_urls(update, context)
        manage_website(update, context)
    elif "exit" in query:
        exit_bot(update, context)
    elif "manage_website" in query:
        manage_website(update, context)
    elif "manage_edit_desc" in query:
        create_desc(update, context)
    elif "cat" in query:
        get_cat_fact(update, context)
    elif "create_desc" in query:
        create_desc(update, context)
    elif "change_url" in query:
        create_url(update, context)
    elif "url_desc_confirmation" in query:
        url_desc_confirmation(update, context)
    elif "send_url_desc" in query:
        # proceed to payment
        payment(update, context)
        context.bot.send_message(chat_id=update.effective_chat.id, text="Proceeding with payment...")
        # send_initialization_data(update, context)
    elif "edit_url" in query:
        create_url(update, context)
    elif "edit_desc" in query:
        create_desc(update, context)
    elif "cancel" in query:
        other_edits(update, context)
    elif "manage_update_confirm" in query:
        send_data(update, context)
    elif "manage_choose" in query:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Fetching data..")
        ls = query.split("_")
        current_user[update.effective_chat.id]['current_url'] = ls[2]
        current_user[update.effective_chat.id]['website_desc'] = str(wks.acell('B' + str(ls[3])).value)
        current_user[update.effective_chat.id]['target_row'] = ls[3]
        website_edit(update, context)
    elif "manage_posts" in query:
        manage_posts(update, context)
    elif "manage_listings" in query:
        manage_listings(update, context)
    elif "manage_agent_details" in query:
        manage_agent_details(update, context)
    elif "edit_desc" in query:
        create_desc(update, context)
    elif "create_post" in query or "change_post_title" in query:
        create_post_title(update, context)
    elif "confirm_post_title" in query or "change_post_content" in query:
        create_post_content(update, context)
    elif "confirm_post_content" in query:
        send_post_confirmation(update, context)
    elif "confirm_post_submission" in query:
        confirm_post(update, context)
    elif "edit_post_content" in query:
        edit_post_content(update, context)
    elif "edit_post_title" in query:
        edit_post_title(update, context)
    elif "edit_posts" in query:
        edit_posts(update, context)
    elif "delete_post" in query:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Retrieving data...")
        delete_post(update, context)
    elif "post_delete/" in query:
        temp = query.split('/')
        current_user[update.effective_chat.id]['current_post'] = current_user[update.effective_chat.id]['posts'][temp[1]]
        del current_user[update.effective_chat.id]['posts']
        delete_confirmation(update, context)
    elif "confirm_post_deletion" in query:
        confirm_delete(update, context)
    elif "post_edit/" in query:
        temp = query.split('/')
        current_user[update.effective_chat.id]['current_post'] = current_user[update.effective_chat.id]['posts'][temp[1]]
        del current_user[update.effective_chat.id]['posts']
        edit_post_title_or_content(update, context)
    elif "confirm_post_edit" in query:
        confirm_edit(update, context)
    elif "create_listing" in query:
        create_listing(update, context)
    elif "confirm_listing_title" in query:
        create_property_details(update, context)
    elif "change_property_details" in query:
        create_property_details(update, context)
    elif "listing_description" in query or "change_listing_desc" in query:
        listing_description(update, context)
    elif "upload_featured_photo" in query:
        upload_featured_photo(update, context)
    elif "send_extra_photos" in query:
        upload_extra_photos(update, context)
    elif "confirm_new_listing" in query:
        confirm_new_listing(update, context)
    elif "confirm_listing_upload" in query:
        confirm_listing_upload(update, context)
    elif "delete_listing" in query:
        delete_listings(update, context)
    elif "listing_delete/" in query:
        info = query.split('/')
        current_user[update.effective_chat.id]['current_listing'] = current_user[update.effective_chat.id]['listings'][info[1]]
        del current_user[update.effective_chat.id]['listings']
        delete_listings_confirmation(update, context)
    elif "confirm_listing_delete" in query:
        confirm_delete_listing(update, context)


    elif "edit_listing_featured_photo" in query:
        edit_listing_featured_photo(update, context)
    elif "re_edit_listing_featured_photo" in query:
        context.bot.send_message(update.effective_chat.id, text="Please upload another featured photo.")
    elif "update_listing" in query:
        update_listing(update, context)
    elif "edit_listing_extra_photo" in query:
        edit_listing_extra_photo(update, context)
    elif "edit_listing_description" in query:
        edit_listing_description(update, context)
    elif "edit_listing_title" in query:
        edit_listing_title(update, context)
    elif "edit_listing_property_details" in query:
        edit_listing_property_details(update, context)
    elif "edit_listings" in query:
        edit_listings(update, context)
    elif "listing_edit" in query:
        info = query.split('/')
        current_user[update.effective_chat.id]['current_listings'] = current_user[update.effective_chat.id]['listings'][info[1]]
        del current_user[update.effective_chat.id]['listings']
        choose_edit_listing(update, context)



    elif "re_add_agent_details" in query:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Please input a new 'About Me' description.")
    elif "add_agent_details" in query:
        current_user[update.effective_chat.id]['agent_details'] = {}
        add_agent_pictures(update, context)
    elif "re_add_agent_pictures" in query:
        ##add message
        current_user[update.effective_chat.id]['agent_details']['num_pictures'] = 0
        current_user[update.effective_chat.id]['agent_details']['pictures'] = []
        context.bot.send_message(chat_id=update.effective_chat.id, text="Please upload two pictures of yourself with a transparent background and height-to-width ratio as close to 1:4 as possible.")
    elif "confirm_agent_pictures" in query:
        add_about_me(update, context)
    elif "confirm_about_me" in query:
        add_contact_details(update, context)
    elif "re_add_contact_details" in query:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Please input your new contact information with the required format. Type '**cancel' to cancel.")
    elif "confirm_contact_details" in query:
        add_agent_quote(update, context)
    elif "re_add_agent_quote" in query:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Please input your new desired agent quote. Alternatively, type '**cancel' to cancel.")
    elif "confirm_agent_quote" in query:
        confirm_agent_details(update,context)
    elif "confirm_agent_details" in query:
        send_agent_details(update, context)
    elif "edit_agent_details" in query:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Edited!")

def message_handler(update, context):
    global current_user
    if current_user[update.effective_chat.id]['state'] == 'sending_desc' or current_user[update.effective_chat.id]['state'] == 'update_desc':
        msg = update.message.text
        context.bot.send_message(chat_id=update.effective_chat.id, text="One moment...")
        current_user[update.effective_chat.id]['website_desc'] = msg
        url_desc_confirmation(update, context)
    elif current_user[update.effective_chat.id]['state'] == 'url_edit':
        if '.com' in update.message.text or '.sg' in update.message.text:
            # Must check if url is available
            current_user[update.effective_chat.id]['url'] = update.message.text.lower()
            url_confirmation(update, context)
        else:
            context.bot.send_message(chat_id=update.effective_chat.id, text="Invalid url, please input a new url.")
    elif current_user[update.effective_chat.id]['state'] == 'url_creation':
        print(update.message.text)
        if '.com' in update.message.text or '.sg' in update.message.text:
            current_user[update.effective_chat.id]['url'] = update.message.text.lower()
            url_confirmation(update, context)
        elif 'cancel' in update.message.text or 'Cancel' in update.message.text:
            other_edits(update, context)
        else:
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text="That is not a valid url. Please input a valid url, or type 'Cancel' to cancel.")
    elif current_user[update.effective_chat.id]['state'] == 'create_post':
        current_user[update.effective_chat.id]['new_post']['post_title'] = update.message.text
        create_post_title_confirmation(update, context)
    elif current_user[update.effective_chat.id]['state'] == 'create_post_content':
        # global post_content
        current_user[update.effective_chat.id]['new_post']['post_content'] = update.message.text
        create_post_content_confirmation(update, context)
    elif current_user[update.effective_chat.id]['state'] == 'edit_post_content' or current_user[update.effective_chat.id]['state'] == 'edit_post_title':
        if 'cancel' in update.message.text or 'Cancel' in update.message.text:
            other_edits(update, context)
        if current_user[update.effective_chat.id]['state'] == 'edit_post_content':
            current_user[update.effective_chat.id]['current_post']['content'] = update.message.text
        else:
            current_user[update.effective_chat.id]['current_post']['title'] = update.message.text
        edit_post_content_confirmation(update, context)
    elif current_user[update.effective_chat.id]['state'] == 'create_listing_title':
        current_user[update.effective_chat.id]['new_listing']['title'] = update.message.text
        listing_title_confirmation(update, context)
    elif current_user[update.effective_chat.id]['state'] == 'create_property_details':
        property_details = update.message.text
        if '**cancel' in property_details:
            other_edits(update, context)
        if len(property_details.split('\n')) != 9:
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text="Invalid input, please try again, or type '**cancel' to stop creating a listing")
        else:
            listing_details(update, property_details)
            property_details_confirmation(update, context)
    elif current_user[update.effective_chat.id]['state'] == 'edit_featured_photo':
        if 'cancel' in update.message.text or 'Cancel' in update.message.text:
            other_edits(update, context)
    elif current_user[update.effective_chat.id]['state'] == 'listing_description':
        current_user[update.effective_chat.id]['new_listing']['description'] = update.message.text
        listing_description_confirmation(update, context)
    elif current_user[update.effective_chat.id]['state'] == 'upload_extra_photos':
        if '**done' in update.message.text:
            confirm_extra_photos(update, context)
    elif current_user[update.effective]['state'] == 'edit_listing_featured_photo':
        if 'cancel' in update.message.text or 'Cancel' in update.message.text:
            other_edits(update, context)
    elif current_user[update.effective_chat.id]['state'] == 'edit_listing_extra_photos':
        if '**done' in update.message.text:
            confirm_edit_listing_extra_photos(update, context)
    elif current_user[update.effective_chat.id]['state'] == 'edit_listing_description':
        if '**cancel' in update.message.text:
            other_edits(update, context)
        else:
            current_user[update.effective_chat.id]['current_listing']['description'] = update.message.text
            confirm_edit_listing_description(update, context)
    elif current_user[update.effective]['state'] == 'edit_listing_title':
        if 'cancel' in update.message.text or 'Cancel' in update.message.text:
            other_edits(update, context)
        else:
            current_user[update.effective]['current_listing']['title'] = update.message.text
            confirm_edit_listing_title(update, context)
    elif current_user[update.effective_chat.id]['state'] == 'edit_listing_property_details':
        if 'cancel' in update.message.text or 'Cancel' in update.message.text:
            other_edits(update, context)
        else:
            property_details = update.message.text
            if len(property_details.split('\n')) != 9:
                context.bot.send_message(chat_id=update.effective_chat.id,
                                         text="Invalid input, please try again, or type '**cancel' to stop creating a listing")
            else:
                listing_details(update, property_details)
                confirm_edit_listing_property_details(update, context)

    elif current_user[update.effective_chat.id]['state'] == 'add_about_me':
        current_user[update.effective_chat.id]['agent_details']['about_me'] = update.message.text
        confirm_about_me(update, context)
    elif current_user[update.effective_chat.id]['state'] == 'add_contact_details':
        if '**cancel' in update.message.text:
            other_edits(update, context)
        info = update.message.text.split('\n')
        if len(info) < 3:
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text="Invalid input, please try again, or type '**cancel' to cancel.")
        else:
            current_user[update.effective_chat.id]['agent_details']['name'] = info[0]
            current_user[update.effective_chat.id]['agent_details']['number'] = info[1]
            current_user[update.effective_chat.id]['agent_details']['email'] = info[2]
            confirm_contact_details(update, context)
    elif current_user[update.effective_chat.id]['state'] == 'add_agent_quote':
        if '**cancel' in update.message.text:
            other_edits(update, context)
        current_user[update.effective_chat.id]['agent_details']['quote'] = update.message.text
        confirm_agent_quote(update, context)
    else:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="I'm not sure what you're looking for.. please be more specific.")


# Create and add command handlers
start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

create_website_handler = CommandHandler('create_website', create_url)
dispatcher.add_handler(create_website_handler)

restart_handler = CommandHandler('restart', restart)
dispatcher.add_handler(restart_handler)

help_handler = CommandHandler('help', help_me)
dispatcher.add_handler(help_handler)

manage_websites_handler = CommandHandler('manage_websites', manage_website)
dispatcher.add_handler(manage_websites_handler)

pre_checkout_handler = PreCheckoutQueryHandler(precheckout_callback)
dispatcher.add_handler(pre_checkout_handler)

successful_payment_handler = MessageHandler(Filters.successful_payment, successful_payment_callback)
dispatcher.add_handler(successful_payment_handler)

catchall_handler = MessageHandler(Filters.text, message_handler)
dispatcher.add_handler(catchall_handler)

photo_handler = MessageHandler(Filters.photo, photo_receiver)
dispatcher.add_handler(photo_handler)

query_handler = CallbackQueryHandler(inline_query)
dispatcher.add_handler(query_handler)

updater.start_polling()
updater.idle()
