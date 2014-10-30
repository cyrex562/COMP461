import jsonpickle
import redis
from utils import log_msg


REDIS_KEY = 'ent_app_proj'

redis_ctx = None

table_names = []


def init_data_gateway():
    """
    Initialize the data gateway
    :return: void
    """
    global redis_ctx
    redis_ctx = redis.StrictRedis()
    log_msg('debug', 'init_data_gateway, flushing in-memory store')
    redis_ctx.flushdb()


def get_table(table_name):
    """
    Retrieve table
    :param table_name:
    :return: a list of decoded json objects
    """
    mod_table_name = '{0}:{1}'.format(REDIS_KEY, table_name)
    table_list = redis_ctx.lrange(mod_table_name, 0, -1)
    table = [jsonpickle.decode(tl) for tl in table_list]
    return table


def add_table_row(table_name, row):
    """
    Append a row to a table in the store
    :param table_name: the name of the table to append a row to.
    :param row a python object representation of a row
    :return: void
    """
    mod_table_name = '{0}:{1}'.format(REDIS_KEY, table_name)
    redis_ctx.rpush(mod_table_name, jsonpickle.encode(row))


def get_value(key):
    """
    Get value from the store
    :param key: the key for the value
    :return: the value as a string
    """
    value = redis_ctx.get(key)
    return value


def persist_table(table_name):
    # TODO implement
    pass


def persist_row(table_name, row):
    # TODO implement
    pass


def persist_db():
    # TODO implement
    pass

################################################################################
# END OF FILE
################################################################################



