from telegram.ext import (Updater, CommandHandler, Defaults, DictPersistence)
from telegram import ParseMode

import logging
import pickle

import requests
import xml.etree.ElementTree as ET

import pprint
list1 = []


def feed_in():

    url1 = "https://www.autosport.com/rss/feed/f1"
    res = requests.get(url1)

    with open("f1feed.xml", 'wb') as f:
        f.write(res.content)

    tree = ET.parse('f1feed.xml')
    root = tree.getroot()

    feedlist = []

    for item in root.findall('./channel/item'):
        feed = {}
        for child in item:
            feed[child.tag] = child.text.encode('utf8')
        feedlist.append(feed)

    return feedlist
#pprint.pprint(feed_in())


def notif(context):
    list1_file = open('list1.db', 'rb+')

    try:
        list1 = pickle.load(list1_file)
    except:
        list1 = []

    list1_file.close()
    feed = feed_in()

    list1_file = open('list1.db', 'wb+')

    list2 = feed
    final_list = [i for i in list2 if i not in list1]
    pickle.dump(list2, list1_file)

    list1_file.close()

    for i in reversed(range(len(final_list))):
        link = final_list[i]['link'].decode('ASCII')
        try:
            context.bot.send_message(chat_id="@F1feed", text=link, parse_mode='markdown')
        except BaseException as e:
            print(e)


def main():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    defaults = Defaults(parse_mode=ParseMode.MARKDOWN)
    updater = Updater(
        use_context=True, defaults=defaults, token='1238373906:AAEurU8DFg3e6ldPg655D3UqCjLhJzQaxG4'
    )
    dispatcher = updater.dispatcher
    j = updater.job_queue

    #start_handler = CommandHandler('start', start)

    #dispatcher.add_handler(start_handler)

    j.run_repeating(notif, interval=300, first=0)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
