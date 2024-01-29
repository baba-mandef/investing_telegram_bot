#!usr/bin/env python5
# conding : utf-8

# Import libraries
from telegram.ext import Updater, CommandHandler
from telegram import Message
import logging

# Import core modules
from scraper import get_event


# Set Bot token
_token = ''


_updater = Updater(_token, use_context=True)
_dispatcher = _updater.dispatcher

# Set logger
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hello {} ! Ca cash j'espère. Je suis l'assistant Investing.tbot. Je t'aide à obtenir des informations relatifs aux marchés financier. \n 1 - Utilise la commande /calendar pour obtenir la liste des annonces économiques les plus importantes de la journée \n 2 - Utilise la commande full_calendar pour obtenir la liste complètes des annonces économiques de la journée".format(update.effective_user.first_name))


# set start command handler
start_handler = CommandHandler('start', start)
_dispatcher.add_handler(start_handler)


def calendar(update, context):

    events = get_event()
    data = ""
    for event in events:
        if int(event['intensity']['priority']) == 3:
            my_event = f" Devise : {event['currency'] } {get_flag(event['currency']) if get_flag(event['currency'])!=None else ''} \n Heure : {event['time']}\n Evenement : {event['event']}\n Priorité : {('⭐️'*int(event['intensity']['priority']))}  \n\n"
            data += my_event
    context.bot.send_message(chat_id=update.effective_chat.id, text=data)


calendar_handler = CommandHandler("calendar", calendar)
_dispatcher.add_handler(calendar_handler)


def full_calendar(update, context):
    events = get_event()
    data = ""
    for event in events:
        my_event = f" Devise : {event['currency'] } {get_flag(event['currency']) if get_flag(event['currency'])!=None else ''} \n Heure : {event['time']}\n Evenement : {event['event']}\n Priorité : {('⭐️'*int(event['intensity']['priority']))}  \n\n"
        data += my_event
    context.bot.send_message(chat_id=update.effective_chat.id, text=data)


full_calendar_handler = CommandHandler("full_calendar", full_calendar)
_dispatcher.add_handler(full_calendar_handler)


def get_flag(currency):
    if currency == 'EUR':
        return "🇪🇺"

    elif currency == 'USD':
        return "🇺🇸"

    elif currency == 'AUD':
        return "🇦🇺"

    elif currency == 'NZD':
        return "🇳🇿"

    elif currency == 'CAD':
        return "🇨🇦"

    elif currency == 'CHF':
        return "🇨🇭"

    elif currency == 'JPY':
        return "🇯🇵"
    elif currency == 'GBP':
        return "🇬🇧"


_updater.start_polling()
_updater.idle()
