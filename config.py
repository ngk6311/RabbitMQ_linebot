#!/usr/bin/env python3

import os
import logging

from typing import Dict

MQ_DEFAULTS: Dict[str, str] = {
    'HOST': '192.168.1.132',
    'PORT': '5672',
    'VHOST': '/',
    'USER': 'dinkle_test',
    'PASSWORD': 'dinkle123',
    'QUEUE': 'dataMining'
}


MYSQL_DEFAULTS: Dict[str, str] = {
    'HOST': '192.168.1.132',
    'PORT': '5431',
    'USER': 'dinkle',
    'PASSWORD': 'dinkle1341',
    'DATABASE': 'crmnlp'
}


def printdefaults() -> None:
    printdefault('MQ', MQ_DEFAULTS)
    printdefault('MYSQL', MYSQL_DEFAULTS)


def setdefaults() -> None:
    setdefault('MQ', MQ_DEFAULTS)
    setdefault('MYSQL', MYSQL_DEFAULTS)


def printdefault(prefix: str, map: Dict[str, str]) -> None:
    for k in map.keys():
        key = prefix + '_' + k
        if k == 'PASSWORD':
            logging.info('%s = %s', key, '*******')
        else:
            logging.info('%s = %s', key, os.environ.get(key, ''))


def setdefault(prefix: str, map: Dict[str, str]) -> None:
    for k, v in map.items():
        os.environ.setdefault(prefix + '_' + k, v)


if __name__ == "__main__":
    setdefaults()
    printdefaults()
