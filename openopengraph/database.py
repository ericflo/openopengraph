import functools

import redis
import simplejson


def _filter_fields(fields, obj):
    if not fields or fields == ['']:
        return obj
    new_obj = {}
    for field in fields:
        new_obj[field] = obj[field]
    return new_obj


class DB(object):
    
    def __init__(self, host='localhost', port=6379, db=0):
        self.host = host
        self.port = port
        self.db = db
        self.client = redis.Redis(self.host, self.port, self.db)
    
    def get_new_id(self):
        return self.client.incr('global:id')
    
    def get_object_by_id(self, object_id, fields):
        key = 'object:%s' % (object_id,)
        return _filter_fields(fields, simplejson.loads(self.client.get(key)))
    
    def get_objects_by_connection(self, object_id, connection_type, limit,
        offset, fields):
        key = 'connection:%s:%s' % (object_id, connection_type)
        object_ids = self.client.lrange(key, offset, offset + limit)
        if not object_ids:
            return []
        object_keys = map(lambda o: 'object:%s' % (o,), object_ids)
        raw_objects = filter(bool, self.client.mget(object_keys))
        partial = functools.partial(_filter_fields, fields)
        return map(partial, map(simplejson.loads, raw_objects))
    
    def create_object(self, obj):
        new_id = self.get_new_id()
        obj['id'] = new_id
        key = 'object:%s' % (new_id,)
        value = simplejson.dumps(obj)
        self.client.set(key, value)
        return obj
    
    def generic_post(self, generic_id, connection, obj):
        connection_key = 'connection:%s:%s' % (generic_id, connection)
        new_id = self.get_new_id()
        obj['id'] = new_id
        object_key = 'object:%s' % (new_id,)
        encoded = simplejson.dumps(obj)
        self.client.set(object_key, encoded)
        self.client.lpush(connection_key, str(new_id))
        return obj