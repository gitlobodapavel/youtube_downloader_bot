import telebot
import pytube

import moviepy.editor as mp

import constants
import markups

bot = telebot.TeleBot(constants.API_KEY)


@bot.message_handler(commands=['start', 'help'])
def handle_start(message):
    bot.send_message(message.chat.id, constants.START_MESSAGE, reply_markup=markups.func_markup)


@bot.message_handler(commands=['download_mp4', ])
def ask_for_link(message):
    bot.send_message(message.chat.id, constants.GET_LINK)
    bot.register_next_step_handler(message, download_mp4)


def download_mp4(message):
    bot.send_message(message.chat.id, 'Downloading video...')
    link = message.text
    yt = pytube.YouTube(link)
    ys = yt.streams.get_highest_resolution()
    print('downloading...')
    ys.download('downloads/')
    print('downloaded!')
    send_mp4(message, title=ys.title)


def send_mp4(message, title):
    print('sending...')
    bot.send_message(message.chat.id, 'Downloaded ! Sending ( It may take a few minutes.. )')
    bot.send_video(message.chat.id, open('downloads/'+title+'.mp4', 'rb'), supports_streaming=True)
    bot.send_message(message.chat.id, constants.START_MESSAGE, reply_markup=markups.func_markup)
    print('sent!')


@bot.message_handler(commands=['convert_to_mp3', ])
def ask_for_link(message):
    bot.send_message(message.chat.id, constants.GET_LINK)
    bot.register_next_step_handler(message, download_mp3)


def download_mp3(message):
    bot.send_message(message.chat.id, 'Downloading video...')
    link = message.text
    yt = pytube.YouTube(link)
    ys = yt.streams.get_highest_resolution()
    print('downloading...')
    ys.download('downloads/')
    print('downloaded!')
    print('converting...')
    convert_to_mp3(message, ys.title)
    print('converted!')
    send_mp3(message, title=ys.title)


def convert_to_mp3(message, title):
    bot.send_message(message.chat.id, 'Converting video to mp3...')
    clip = mp.VideoFileClip("downloads/"+title+".mp4")
    clip.audio.write_audiofile("downloads/"+title+".mp3")


def send_mp3(message, title):
    print('sending...')
    bot.send_message(message.chat.id, 'Converted ! Sending ( It may take a few minutes.. )')
    bot.send_audio(message.chat.id, open('downloads/' + title + '.mp3', 'rb'))
    bot.send_message(message.chat.id, constants.START_MESSAGE, reply_markup=markups.func_markup)
    print('sent!')


if __name__ == '__main__':
    bot.polling(none_stop=True)