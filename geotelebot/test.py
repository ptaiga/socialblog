import os
import telebot

bot = telebot.TeleBot(os.getenv('TOKEN'))

@bot.message_handler(content_types=['photo'])
def handle_message(message):
    file_info = bot.get_file(message.photo[0].file_id)
    base_name = os.path.basename(file_info.file_path)
    file_name, file_ext = os.path.splitext(file_info.file_path)
    print()
    image = bot.download_file(file_info.file_path)
    with open(os.path.join('photos', file_info.file_unique_id + file_ext), 'wb') as f:
        f.write(image)
    bot.send_photo(message.chat.id, image)


if __name__ == '__main__':
    bot.polling()