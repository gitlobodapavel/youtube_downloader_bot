from telebot import types


func_markup = types.ReplyKeyboardMarkup(True, True)
func_markup.row('/download_mp4', '/convert_to_mp3')
