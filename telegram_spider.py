# -*- coding: utf-8 -*-
import os
import sys
from os.path import abspath, dirname, join
sys.path.append(abspath(join(dirname(__file__), "../")))
from telethon import TelegramClient, sync, events, utils
from spiders_telegram.config import *
import datetime
import time
import traceback
import collections
import unicodedata
import pymysql
import json
import requests

logger = get_logger(os.path.basename(__file__))


def remove_emoji(text):
    return ''.join(c if c <= '\uFFFF' else '[emoji]' for c in unicodedata.normalize('NFC', text))


class TelegramSpider(object):

    def __init__(self):
        self.client = TelegramClient(**TELEGRAM_CONFIG)
        self.cols = []
        self.start_time = time.time()


    async def handler(self, event):
        try:
            content = remove_emoji(event.message.message)
            flag = True
            if content.strip().startswith('/'):
                flag = False
        
            print(event.chat.title, event.message.date, utils.get_display_name(event.sender), event.message.message)
        
            if event.is_reply is False and flag and content:
                # 构建存储数据
                temp = {}
                temp['theme'] = theme_classify(event.chat.title)
                temp['source'] = 'Telegram'
                temp['from_user'] = remove_emoji(utils.get_display_name(event.sender))[:80]
                temp['content'] = content
                temp['message_time'] = event.message.date + datetime.timedelta(hours=8)
                temp['message_time'] = str(temp['message_time'])[:19]
                temp['created_time'] = str(datetime.datetime.now())[:19]
    
                self.cols.append(temp)
                elapse = time.time() - self.start_time
                if len(self.cols) >= MAX_CHUNK_SIZE or elapse >= MAX_ELAPSE:
                    msg_list = self.cols
                    self.cols = []
                    self.start_time = time.time()
                    self.post_request(msg_list)

        except Exception as e:
            traceback.print_exc()
            logger.info(e)


    @staticmethod
    def post_request(data):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        post_file_name = os.path.join(base_dir, 'post_file')
        with open(post_file_name, 'w') as f:
            f.write(json.dumps(data))

        post_file = {"telegram_msg" : open(post_file_name, "rb").read()}
        resp = requests.post(POST_TELEGRAM, files=post_file)
        resp_data = resp.json()
        if resp.status_code == 200:
            if resp_data["errstr"] == "totally inserted":
                logger.info("Inserted %d Telegram messages successfully" % len(data))
            elif resp_data["errstr"] == "partially inserted":
                success_count = resp_data["data"]["success_count"]
                fail_count = resp_data["data"]["fail_count"]
                fail_reasons = resp_data["data"]["fail_reasons"]
                logger.info("Partially Inserted %d Telegram messages, success_count %d, fail_count %d"
                 "" % (len(data), success_count, fail_count))
                for index, fail_reason in enumerate(fail_reasons):
                    logger.info("reason%d - %s" % (index + 1, fail_reason))

        else:
            logger.error("Failed to Insert %d Telegram messages"  % len(data))
        os.remove(post_file_name)


    def run(self):
        self.handler = self.client.on(events.NewMessage)(self.handler)
        with self.client.start():
            print('(Press Ctrl+C to stop this)')
            self.client.run_until_disconnected()


if __name__ == '__main__':
    tspider = TelegramSpider()
    tspider.run()