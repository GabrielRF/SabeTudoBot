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

simnao = open('/usr/local/bin/SabeTudoBot/alt/simnao.txt').read().splitlines()
tempo = open('/usr/local/bin/SabeTudoBot/alt/tempo.txt').read().splitlines()
valor = open('/usr/local/bin/SabeTudoBot/alt/valor.txt').read().splitlines()
culpa = open('/usr/local/bin/SabeTudoBot/alt/culpa.txt').read().splitlines()

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
        s = types.InlineQueryResultArticle('1', 'Sim, Não ou Talvez.',
            types.InputTextMessageContent(str(u'\U0001F52E') + ' ' +random.choice(simnao)))
        d = types.InlineQueryResultArticle('2', 'Datas.',
            types.InputTextMessageContent(str(u'\U0001F52E') + ' ' +random.choice(tempo)))
        v = types.InlineQueryResultArticle('3', 'Valores.',
            types.InputTextMessageContent(str(u'\U0001F52E') + ' ' +random.choice(valor)))
        c = types.InlineQueryResultArticle('3', 'Culpados.',
            types.InputTextMessageContent(str(u'\U0001F52E') + ' ' +random.choice(culpa)))
        bot.answer_inline_query(inline_query.id, [s,d,v,c], cache_time=1, is_personal=True)
    except Exception as e:
        print(e)

bot.polling()
