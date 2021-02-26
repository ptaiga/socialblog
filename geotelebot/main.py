import os
import telebot

from collections import defaultdict

from storage import Storage

INFO, LOCATION, IMAGE, CONFIRMATION = range(4)
USER_ADD_STATE = defaultdict(lambda: None)
ITEMS = defaultdict(dict)

bot = telebot.TeleBot(os.getenv('TOKEN'))
storage = Storage(os.getenv('DATABASE_URL'))
admin_id = os.getenv('ADMIN_ID', None)


def get_add_state(message):
    return USER_ADD_STATE[message.chat.id]

def update_add_state(message, state):
    USER_ADD_STATE[message.chat.id] = state

def get_item(user_id):
    return ITEMS[user_id]

def update_item(user_id, key, value):
    ITEMS[user_id][key] = value


@bot.message_handler(func=lambda message: get_add_state(message) == INFO)
def handle_info(message):
    update_item(message.chat.id, 'info', message.text)
    bot.send_message(message.chat.id, 'Attach location or enter "x, y" or "no":')
    if admin_id:
        bot.send_message(admin_id, f'{message.chat.id} Attach location or enter "x, y" or "no":')
    update_add_state(message, LOCATION)

@bot.message_handler(func=lambda message: get_add_state(message) == LOCATION)
@bot.message_handler(content_types=['location'], func=lambda message: get_add_state(message) == LOCATION)
def handle_location(message):
    if message.location:
        lat, lon = message.location.latitude, message.location.longitude
        update_item(message.chat.id, 'location', (lat, lon))
    else:
        try:
            lat, lon = [float(c.strip()) for c in message.text.split(',', 1)]
            if not (-90 < lat < 90) or not (-180 < lon < 180):
                raise ValueError
            update_item(message.chat.id, 'location', (lat, lon))
        except ValueError:
            update_item(message.chat.id, 'location', None)
    bot.send_message(message.chat.id, 'Attach foto or enter "no":')
    if admin_id:
        bot.send_message(admin_id, f'{message.chat.id} Attach foto or enter "no":')
    update_add_state(message, IMAGE)

@bot.message_handler(func=lambda message: get_add_state(message) == IMAGE)
@bot.message_handler(content_types=['photo'], func=lambda message: get_add_state(message) == IMAGE)
def handle_image(message):
    image = None
    update_item(message.chat.id, 'image', image)
    if message.photo:
        file_info = bot.get_file(message.photo[0].file_id)
        image = bot.download_file(file_info.file_path)
        update_item(message.chat.id, 'image', file_info.file_path)

    bot.send_message(
        message.chat.id,
        f'Confirm saving the information (yes/no):\n{get_item(message.chat.id)}.'
    )
    if admin_id:
        bot.send_message(
            admin_id,
            f'{message.chat.id} Confirm saving the information (yes/no):\n{get_item(message.chat.id)}.'
        )
    update_item(message.chat.id, 'image', image)
    update_add_state(message, CONFIRMATION)

@bot.message_handler(func=lambda message: get_add_state(message) == CONFIRMATION)
def handle_confirmation(message):
    if message.text.lower() == 'yes':
        storage.save_item(
            message.chat.id,
            get_item(message.chat.id)['info'],
            get_item(message.chat.id)['location'],
            get_item(message.chat.id)['image']
        )
        text = 'Saved!'
    else:
        text = 'Canceled!'
    bot.send_message(message.chat.id, text)
    if admin_id:
        bot.send_message(admin_id, f'{message.chat.id} {text}')
    update_add_state(message, None)


@bot.message_handler(commands=['add'])
def hangle_add(message):
    text = message.text.split(" ", 1)
    if len(text) == 2:
        storage.save_item(message.chat.id, text[1])
        bot.send_message(message.chat.id, f'Saved: "{text[1]}"')
        if admin_id:
            bot.send_message(admin_id, f'{message.chat.id} Saved: "{text[1]}"')
    else:
        bot.send_message(message.chat.id, 'Enter name and address:')
        if admin_id:
            bot.send_message(admin_id, f'{message.chat.id} Enter name and address:')
        update_add_state(message, INFO)

@bot.message_handler(commands=['list'])
def hangle_list(message):
    items = storage.get_all(message.chat.id)
    text = "Saved locations:\n"
    for i, item in enumerate(items[-10:]):
        point = f', {item[3]}' if item[3] else ''
        photo = ' + photo' if item[4] else ''
        text += f'\n{i+1}. "{item[2]}"{point}{photo}\n'
    if not items:
        text += '\nNot found.'
    bot.send_message(message.chat.id, text)
    if admin_id:
        bot.send_message(admin_id, f'{message.chat.id} {text}')

@bot.message_handler(commands=['reset'])
def hangle_reset(message):
    storage.reset(message.chat.id)
    bot.send_message(message.chat.id, 'All items are deleted!')
    if admin_id:
        bot.send_message(admin_id, f'{message.chat.id} All items are deleted!')

@bot.message_handler(commands=['more'])
def hangle_reset(message):
    item = storage.get_item(message.chat.id)
    if item:
        if item[4]:
            bot.send_photo(message.chat.id, item[4], caption=item[2])
        else:
            bot.send_message(message.chat.id, item[2])
        if item[3]:
            lat, lon = [float(c.strip()) for c in item[3][1:-1].split(',')]
            bot.send_location(message.chat.id, lat, lon)
    else:
        bot.send_message(message.chat.id, 'Not found.')
    if admin_id:
        bot.send_message(admin_id, f'{message.chat.id} /more')

@bot.message_handler(commands=['location'])
@bot.message_handler(content_types=['location'])
def hangle_location(message):
    if message.location:
        lat, lon = message.location.latitude, message.location.longitude
    else:
        try:
            text = message.text.split(" ", 1)[1]
            lat, lon = [float(c.strip()) for c in text.split(',', 1)]
        except (ValueError, IndexError):
            bot.send_message(
                message.chat.id,
                'Incorrect! Text format: "/location x,y" or attach location.')
            return
    items = storage.get_nearby_items(message.chat.id, (lat, lon), 0.5)
    if items:
        text = "Within a radius of 500 meters, there are the following saved locations:\n"
        text += ''.join([f'\n - {item[2]}\n' for item in items])
    else:
        text = "There are not saved locations within 500 meters radius."
    bot.send_message(message.chat.id, text)
    if admin_id:
        bot.send_message(admin_id, f'{message.chat.id} {text}')

@bot.message_handler(commands=['start'])
def hangle_reset(message):
    text = '''This bot will help you save interesting places and show you which ones are nearby.
You can use commands:
/add - New location item. "/add name and address" - quick addition or "/add" for step-by-step  dialog
/list - List of 10 last location items
/more - Show detailed information about last location item
/location - Locations within 500 meters radius. "/location x,y" or attach location
/reset - Delete all saved location items'''
    bot.send_message(message.chat.id, text)
    if admin_id:
        bot.send_message(admin_id, f'{message.chat.id} /start')

if __name__ == '__main__':
    storage.create_table()
    bot.polling()
