import requests
from BeautifulSoup import BeautifulSoup


def read_file(filename):
    with open(filename) as input_file:
        text = input_file.read()
    return text

def parse_user_datafile_bs(filename):
    # results = []
    text = read_file(filename)

    soup = BeautifulSoup(text, convertEntities=BeautifulSoup.HTML_ENTITIES)
    date_text = soup.find('div', {'class': 'datebox'}).find('b').text
    print(date_text)
    result = {}
    result['title'] = date_text

    complexes = []
    menu_items = soup.findAll('div', {'class': 'panel panel-warning'})
    #print menu_items
    for item in menu_items:
        complex_item = ""
        title = item.find('div', {'class': 'panel-heading'}).find('h3').text
        # complex['title'] = title
        # print title
        complex_item = complex_item + title + "\n"

        content = item.find('div', {'class': 'entry-content'}).findAll('h4')
        complex_content = ""
        for meal in content:
            meal.decompose()
            # print meal.text
            complex_content = complex_content + meal.text + "\n"
        complex_item = complex_item + complex_content
        complexes.append(complex_item)
    result["complexes"] = complexes
    return result

def get_html():
    url = 'http://enode-cafe.ru'
    request = requests.get(url)
    with open('test.html', 'w') as output_file:
        output_file.write(request.text.encode('utf8'))
    #parse_user_datafile_bs('test.html')


import telebot
BOT_TOKEN = "339818089:AAEiYVFzGn3--Wo1P2fXiOTKJbfUclX7CyA"
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    print("hello")
    bot.reply_to(message, "Ты можешь узнать меню по команде /menu")

@bot.message_handler(commands=['menu'])
def send_menu(message):
    # bot.reply_to(message, "Howdy, how are you doing?")
    print("sending menu")
    get_html()
    menu = parse_user_datafile_bs('test.html')
    print(menu)
    bot.reply_to(message, menu['title'])
    for complex in menu['complexes']:
        bot.reply_to(message, complex)
        # for item in complex['content']:
        #     bot.reply_to(message, item)

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    print("print echo")
    bot.reply_to(message, message.text)


bot.polling()
