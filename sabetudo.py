import configparser
import datetime
import logging
import logging.handlers
import random
import telebot
from telebot import types

config = configparser.ConfigParser()
config.sections()
config.read('/usr/local/bin/SabeTudoBot/bot.conf')

bot_token = config['DEFAULT']['bot_token']
bot = telebot.TeleBot(bot_token)

LOG_INFO_FILE = '/var/log/SabeTudoBot/sabetudobot.log'
logger_info = logging.getLogger('InfoLogger')
logger_info.setLevel(logging.DEBUG)
handler_info = logging.handlers.RotatingFileHandler(LOG_INFO_FILE,
    maxBytes=10240, backupCount=5, encoding='utf-8')
logger_info.addHandler(handler_info)

Start_msg = '''
<b>Bem vindo ao @SabeTudoBot!</b>

Use este bot para adivinhar respostas ou solucionar questionamentos impossíveis.

É o fim dos seus problemas!

Este bot funciona apenas em <i>modo inline</i>.
Ou seja, em qualquer chat digite na caixa de mensagens:
<code>@SabeTudoBot</code> 
e clique na opção de enviar uma resposta.
'''

respostas = ['Sim.', 'Não.', 'Talvez.']

@bot.message_handler(func=lambda m: True)
def send_welcome(message):
    try:
        log_msg = str(message.from_user.id) + ' ' + str(message.from_user.username)
    except:
        log_msg = str(message.from_user.id)
    logger_info.info(str(datetime.datetime.now()) + '\tMessage\t' + log_msg)
    bot.reply_to(message, Start_msg, parse_mode='HTML')

@bot.inline_handler(func=lambda m: True)
def query_text(inline_query):
    try:
        log_msg = str(inline_query.from_user.id) + ' ' + str(inline_query.from_user.username)
    except:
        log_msg = str(inline_query.from_user.id) 
    logger_info.info(str(datetime.datetime.now()) + '\tInline\t' + log_msg)
    try:
        r = types.InlineQueryResultArticle('1', 'Enviar resposta...', 
            types.InputTextMessageContent(random.choice(respostas)))
        bot.answer_inline_query(inline_query.id, [r])
    except Exception as e:
        print(e)

bot.polling()
