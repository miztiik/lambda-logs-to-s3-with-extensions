# -*- coding: utf-8 -*-

import logging
import json
import os
import datetime
import time
import random
import boto3


class GlobalArgs:
    """ Global statics """
    OWNER = "Mystique"
    ENVIRONMENT = "production"
    MODULE_NAME = "greeter_lambda"
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
    RANDOM_SLEEP_SECS = int(os.getenv("RANDOM_SLEEP_SECS", 2))
    ANDON_CORD_PULLED = os.getenv("ANDON_CORD_PULLED", False)


def set_logging(lv=GlobalArgs.LOG_LEVEL):
    """ Helper to enable logging """
    logging.basicConfig(level=lv)
    logger = logging.getLogger()
    logger.setLevel(lv)
    return logger


logger = set_logging()


def random_sleep(max_seconds=10):
    if bool(random.getrandbits(1)):
        logger.info(f"sleep_start_time:{str(datetime.datetime.now())}")
        time.sleep(random.randint(0, max_seconds))
        logger.info(f"sleep_end_time:{str(datetime.datetime.now())}")


def lambda_handler(event, context):
    logger.debug(f"rcvd_evnt:\n{event}")
    _resp = {
        "statusCode": 200,
        "body": f'{{"message": "Hello Miztiikal World, It is {str(datetime.datetime.now())} here! How about there?"}}'
    }
    logger.info(f"rcvd_evnt:\n{_resp}")
    return _resp
