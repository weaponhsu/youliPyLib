#! /usr/bin/python
# -*- coding:utf-8 -*-
# @author: weaponhsu
# @File:   RedisHash
# @Time:   2018/9/4 上午9:16
import time


class RedisSortedSet(object):
    def __init__(self, logger=None):
        super(RedisSortedSet, self).__init__()
        self.logger = logger
        self.redis = self.redis_pipeline = None

    def get_latest_item_from_sorted_set(self, key, desc=False, reset=False, delete=True):
        result = None
        try:
            result = self.redis.zrange(key, 0, 0, desc, True, score_cast_func=int)
            if len(result) != 1 and isinstance(result[0], tuple) is False:
                raise TypeError('%s数据有误' % key)

            # 拿出来就删除掉
            if delete is True:
                self.redis.zrem(key, result[0][0])

            # 从第一个拿出来放到最后去
            if reset is True:
                self.redis.zadd(key, result[0][0], int(time.time()))

        except Exception as e:
            self.logger.error(format(e))
        finally:
            return result

    def get_keys(self, keys):
        result = None
        try:
            if isinstance(keys, str) is False:
                raise TypeError('keys不是string')

            result = self.redis.keys(keys)
        except Exception as e:
            self.logger.error(format(e))
        finally:
            return result

    def get_sorted_set_by_score(self, key, start_score=0, end_score=-1, desc=True, with_score=True):
        result = None
        try:
            # 从start_score开始取到结束
            if end_score is -1:
                end_score = self.redis.zrange(name=key, start=-1, end=-1, withscores=True, score_cast_func=int)
                if isinstance(end_score, list) is False or isinstance(end_score[0], tuple) is False:
                    raise TypeError('zrange error')

                end_score = end_score[0][1]

            result = self.redis.zrangebyscore(name=key, min=start_score, max=end_score, withscores=True,
                                              score_cast_func=int)

            if isinstance(result, list) is False:
                raise TypeError('无效直播内容类型')

        except Exception as e:
            self.logger.error('get sorted set by score error: %s' % format(e))
        finally:
            return result

    def get_sorted_set_by_desc(self, key, start=0, end=-1, desc=True, with_score=True):
        result = None
        try:
            # result = self.redis.zcard(key)
            result = self.redis.zrange(key, start, end, desc, with_score, score_cast_func=int)
        except Exception as e:
            self.logger.error('get sorted set by desc error: %s' % format(e))
        finally:
            return result

    def put_item_into_sorted_set(self, **kwargs):
        """
        :param kwargs:
        :return:
        """
        result = None
        try:
            if self.redis_pipeline is None:
                result = self.redis.zadd(kwargs['key'], {kwargs['value']: kwargs['score']})
                self.redis.expire(name=kwargs['key'], time=kwargs['expire'] if 'expire' in kwargs else 43200)
            else:
                self.redis_pipeline.zadd(kwargs['key'], {kwargs['value']: kwargs['score']})
                self.redis_pipeline.expire(name=kwargs['key'], time=kwargs['expire'] if 'expire' in kwargs else 43200)

        except Exception as e:
            self.logger.error(format(e))
        finally:
            return result

    def delete_sorted_set(self, **kwargs):
        result = None
        try:
            if self.redis_pipeline is None:
                result = self.redis.delete(kwargs['key'])
            else:
                self.redis_pipeline.delete(kwargs['key'])
                result = 1
        except Exception as e:
            self.logger.error('delete sorted set: %s' % format(e))
        finally:
            return result

    def delete_item_by_item(self, key, value):
        result = None
        try:
            if isinstance(value, bytes) is False:
                raise TypeError('delete_item_by_item必须接收string类型的参数')

            if self.redis_pipeline is None:
                result = self.redis.zrem(key, value)
            else:
                self.redis_pipeline.zrem(key, value)
                result = 1
        except Exception as e:
            self.logger.error('delete item by item: %s' % format(e))
        finally:
            return result
