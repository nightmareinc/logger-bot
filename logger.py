import time
import sys
import telepot
import json
from sh import tail
from telepot.delegate import pave_event_space, per_chat_id, create_open
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, ForceReply
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
from telepot.namedtuple import InlineQueryResultArticle, InlineQueryResultPhoto, InputTextMessageContent
from credentials import tocken, adminID, password, location

message_with_inline_keyboard = None


def on_chat_message(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
                   [InlineKeyboardButton(text='login', callback_data='login')]
               ])
    global message_with_inline_keyboard

    if msg['text'] == password:
        remove_keyboard = ReplyKeyboardRemove(remove_keyboard= True)

        if message_with_inline_keyboard:
            msg_idf = telepot.message_identifier(message_with_inline_keyboard)
            bot.editMessageText(msg_idf, 'remove your password')
            sendLog(bot, chat_id)
        else:
            bot.answerCallbackQuery(query_id, text='No previous message to edit')
    else:
        message_with_inline_keyboard = bot.sendMessage(chat_id, 'Choose one of options below:', reply_markup=keyboard)


def on_callback_query(msg):
    query_id, from_id, data = telepot.glance(msg, flavor='callback_query')
    global message_with_inline_keyboard

    if data == 'login':
        if from_id == adminID:
            bot.answerCallbackQuery(query_id, text='Welcome Brian')
            if message_with_inline_keyboard:
                msg_idf = telepot.message_identifier(message_with_inline_keyboard)
                bot.editMessageText(msg_idf, 'Enter password:')
            else:
                bot.answerCallbackQuery(query_id, text='No previous message to edit')
        else:
            bot.answerCallbackQuery(query_id, text='You are not Brian')


class MessageCounter(telepot.helper.ChatHandler):
    def __init__(self, *args, **kwargs):
        super(MessageCounter, self).__init__(*args, **kwargs)
        self._count = 0

    def on_chat_message(self, msg):
        self._count += 1
        self.sender.sendMessage(self._count)

def sendLog(bot, chat_id):
    for line in tail("-F", location, _iter=True):
        bot.sendMessage(chat_id, line)


# deligate bot
bot = telepot.DelegatorBot(tocken, [
    pave_event_space()(
        per_chat_id(), create_open, MessageCounter, timeout=30),
])

# get messages
bot.message_loop({
                  'chat': on_chat_message,
                  'callback_query': on_callback_query},
                  run_forever='')
while 1:
	time.sleep(10)
