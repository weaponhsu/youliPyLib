#! /usr/bin/python
# -*- coding:utf-8 -*-
# @author: weaponhsu
# @File:   RedisList
# @Time:   2018/9/3 上午11:52


class RedisList(object):
    def __init__(self, logger=None):
        super(RedisList, self).__init__()
        self.logger = logger
        self.redis = self.redis_pipeline = None

    def get_list_len(self, key=None):
        """
        取出redis中名为key的list的长度
        :param key:
        :return:
        """
        result = None
        try:
            result = self.redis.llen(key)
        except Exception as e:
            self.logger.error(format(e))
        finally:
            return result

    def get_item_from_list(self, key=None):
        """
        从redis的list中取出第一个元素
        :param key:
        :return:
        """
        result = None
        try:
            result = self.redis.rpop(key)
        except Exception as e:
            self.logger.error(format(e))
        finally:
            return result

    def put_item_into_list(self, key=None, item='', add_to_tail=False, expire=43200):
        """
        向redis的名为key的list插入元素，元素可从队列尾部插入
        :param key: 队列的键明
        :param item: 添加到队列的元素
        :param add_to_tail: 是否添加到队列尾部
        :param expire: 超时时间
        :return:
        """
        result = False
        try:
            if self.redis_pipeline is not None:
                if add_to_tail is False:
                    self.redis_pipeline.lpushx(key, item)
                else:
                    self.redis_pipeline.rpushx(key, item)
                self.redis_pipeline.expire(name=key, time=expire)
            else:
                if add_to_tail is True:
                    self.redis.lpushx(key, item)
                else:
                    self.redis.rpushx(key, item)
                self.redis.expire(name=key, time=expire)
            result = True
        except Exception as e:
            self.logger.error(format(e))
        finally:
            return result

