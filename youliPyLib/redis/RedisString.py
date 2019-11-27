#! /usr/bin/python
# -*- coding:utf-8 -*-
# @author: weaponhsu
# @File:   RedisString
# @Time:   2018/11/21 2:57 PM
import time


class RedisString(object):
    def __init__(self, logger=None):
        super(RedisString, self).__init__()
        self.logger = logger
        self.redis = self.redis_pipeline = None

    def set_into_string(self, **kwargs):
        result = None
        try:
            if self.redis_pipeline is None:
                result = self.redis.setex(name=kwargs['key'], value=kwargs['value'], time=kwargs['time'])
            else:
                self.redis_pipeline.setex(name=kwargs['key'], value=kwargs['value'], time=kwargs['time'])
                result = True

        except Exception as e:
            self.logger.error(format(e))
        finally:
            return result

    def delete_string(self, **kwargs):
        result = None
        try:
            if self.redis_pipeline is None:
                result = self.redis.delete(kwargs['key'])
            else:
                self.redis_pipeline.delete(kwargs['key'])
                result = True
        except Exception as e:
            self.logger.error(format(e))
        finally:
            return result

    def get_string(self, key):
        result = None
        try:
            # result = key
            res = self.redis.get(key)
            result = res.decode() if isinstance(res, bytes) else res
        except Exception as e:
            self.logger.error('get string error: %s' % format(e))
        finally:
            return result
