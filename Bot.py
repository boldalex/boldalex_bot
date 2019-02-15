import requests
import telebot

TOKEN = '774205504:AAFKTmHXrvmSmuDa5LZ-NY9UCEdyPKBBoFw'
bot = telebot.Telebot(TOKEN)

@bot.message_handler(func=lambda message: True)
def echo_all(message):
	bot.reply_to(message, message.text)

bot.polling(60)


