# -*- coding: utf-8 -*-
import logging
import sys
import os

MAX_CHUNK_SIZE = 150 # 最多几条信息发一次存数据POST请求
MAX_ELAPSE = 180 # 最长过多久发一次存数据POST请求（单位：秒）
POST_TELEGRAM = YOUR_TELEGRAMP_API # 爬取的数据传送到服务器的API接口存储


# logging config
BASE_DIR = (os.path.dirname(os.path.abspath(__file__)))
def get_logger(spider_name):
    logger = logging.getLogger()
    formatter = logging.Formatter('%(asctime)s [%(levelname)-8s]: %(message)s')
    
    file_handler = logging.FileHandler(os.path.join(BASE_DIR,"logs/%s.log"%(".".join(spider_name.split('.')[:-1]))))
    file_handler.setFormatter(formatter)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.formatter = formatter
    
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    logger.setLevel(logging.INFO)
    return logger


def theme_classify(group_name):
    lower_name = group_name.lower()
    for theme, kw_list in THEMES_KEYWORDS.items():
        for kw in kw_list:
            if kw in lower_name:
                return theme
    return group_name


TELEGRAM_CONFIG = {
    "api_id": YOUR_TELEGRAM_API_ID,
    "session": "login.session",
    "api_hash": YOUR_TELEGRAM_API_HASH,
    "proxy": None
}

THEMES_KEYWORDS = {
    # 交易所
    "Binance": ["币安", "binance"],
    "Huobi": ["火币", "huobi"],
    "OKEx": ["okex"],
    "Bit-Z": ["bitz", "bit-z"],
    "ZB": ["zb.com", "zb"],
    "FCoin": ["fcoin"],
    "gate.io": ["gate.io"],
    "Bigone": ["bigone"],
    "KKCoin": ["kkcoin"],
    "AEX": ["aex"],
    "HitBTC": ["hitbtc"],
    "OCX": ["x网", "ocx"],

    # 货币
    "QUBE": ["qube"],
    "NEO": ["小蚁", "neo"],
    "Achain": ["achain"],
    "TRON": ["波场", "tron"],
    "Aeternity": ["aeternity", "æternity"],
    "OTCBTC": ["otcbtc"],
    "Bitshares": ["比特股", "bitshares"],
    "Nebulas": ["星云币", "nebulas"],
    "XRP": ["瑞波币", "xrp", "ripple"],
    "EOS": ["eos"],
    "Kcash": ["kcash"],
    "雪币": ["雪币", "verge"],
    "门罗币": ["门罗币", "monero"],
    "沃尔顿链": ["沃尔顿链", "waltonchain"],
    "量子链": ["量子链", "qtum"],
    "维基链": ["维基链", "wicc", "waykichain"],
    "唯链": ["唯链", "ven","vechain"],

    # 工具
    "币用": ["币用", "biyong"],
    "币牛牛": ["币牛牛", "biniubiu"],  
    "MyToken": ["mytoken"],
    "imToken": ["imtoken"],
    "趋势狂人": ["趋势狂人", "qushikuangren"],
    "TokenClub": ["token_club"]

}

