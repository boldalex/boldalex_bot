import requests
import telebot
import datetime
from bs4 import BeautifulSoup

#Определение постоянных переменных
TOKEN = '774205504:AAFKTmHXrvmSmuDa5LZ-NY9UCEdyPKBBoFw'
bot = telebot.TeleBot(TOKEN)
channel_url = {
'матч тв' : 'https://tv.yandex.ru/213/channels/match-1593',
'матч арена' : 'https://tv.yandex.ru/213/channels/match-arena-1667',
'евроспорт' : 'https://tv.yandex.ru/2/channels/eurosport-737'
}
shows = {'биатлон': u'\U0001F3BF',
        'футбол': u'\U000026BD',
        'бокс': u'\U0001F44A' ,
        'фигурное катание':u'\U0001F483',
        'снукер': u'\U0001F3B1'}

#Класс для поиска расписания телеканала
class Schedule:
    def __init__(self, channel):
        self.now = datetime.datetime.now()
        day = str(self.now.day)
        month = self.now.month
        year = str(self.now.year)
        if month < 10:
            month = '0' + str(month)
        self.date = year + '-' + month + '-' + day
        self.url = channel_url[channel]+'?date={}'.format(self.date)

    def get_html(self):
        responce = requests.get(self.url)
        return responce.text

    def parse(self):
        soup = BeautifulSoup(self.get_html(), 'html.parser')
        ul = soup.find('ul', class_='channel-schedule__list')
        programms = []
        for li in ul.find_all('li'):
            prog = li.find('span', class_='channel-schedule__text')
            programms.append(li.time.text + ' ' + prog.text)
        return programms

#обработка команды /help
@bot.message_handler(commands=['help',])
def help_handler(message):
    res = '<b>СПРАВКА</b> \n\n'
    res+= '<b>Расписание телеканалов:</b>\n'
    for channel in channel_url.keys():
        res+= '<b>{}</b> - расписание телеканала {}\n'.format(channel, channel)
    res+= '\n<b>Трансляции по категориям:</b>\n'
    for show in shows.keys():
        res+= '<b>{}</b> - трансляции по категории {}\n'.format(show, show)
    bot.send_message(message.chat.id, res, parse_mode='HTML')

#обработка сообщений
@bot.message_handler(content_types=['text'])
def schedule_handler(message):
    text = message.text.lower()

    #отправка расписания указанного телеканала:
    if text in channel_url.keys():
        res='<b>'+ text.upper() + '</b>'+'\n'
        for i in Schedule(text).parse():
            res+= i + '\n'
        bot.send_message(message.chat.id, res, parse_mode='HTML')
        print(message.chat.id)

    #отправка трансляций по указанной категории:
    elif text in shows.keys():
        res=''
        for chan in channel_url.keys():
            sched=''
            for show in Schedule(chan).parse():
                if text in show.lower():
                    sched += shows[text] + show + '\n'
            if sched != '':
                res+= '<b>' + chan.upper() + '</b>' + '\n' + sched
        if res == '':
            bot.send_message(message.chat.id, text.capitalize() + ' сегодня не показывают!')
        else:
            bot.send_message(message.chat.id, res, parse_mode='HTML')

    #ответ на неизвестную команду
    else:
        bot.send_message(message.chat.id, 'Неизвестная команда. Введите /help для получения справки')

def main():
    bot.polling(none_stop=True)
    

if __name__ == '__main__':
    main()