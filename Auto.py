import telebot
import datetime

TOKEN = '774205504:AAFKTmHXrvmSmuDa5LZ-NY9UCEdyPKBBoFw'
bot = telebot.TeleBot(TOKEN)
chat = 551040176

bot.send_message(chat, 'автосообщение')
