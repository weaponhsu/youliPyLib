#! /usr/bin/python
# -*- coding:utf-8 -*-
# @author: weaponhsu
# @File:   rdRedis
# @Time:   2018/9/4 上午11:41
from . import config
from . import RedisSortedSet, RedisList, RedisString
import redis


class RdRedis(RedisSortedSet.RedisSortedSet, RedisList.RedisList, RedisString.RedisString):
    def __init__(self, logger=None):
        super(RdRedis, self).__init__()
        self.logger = logger
        self.redis = redis.Redis(host=config.REDIS_HOST, port=config.REDIS_PORT, db=6) \
            if self.redis is None else self.redis
        self.redis_pipeline = None

    @property
    def redis_handle(self):
        return self.redis

    def start_transaction(self):
        self.redis_pipeline = self.redis.pipeline(transaction=False)

    def execute(self):
        return self.redis_pipeline if self.redis_pipeline is None \
            else self.redis_pipeline.execute()


