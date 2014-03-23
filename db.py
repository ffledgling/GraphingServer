import re
import sqlite3

import config

class GraphServerDBExecption(Exception):
    """ Generic Exception Class for DBErrors"""

    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return repr(self.msg)


def sanitize_name(name):
    new_name = name.strip()
    new_name = re.sub('[^\w]', '_', new_name)
    return new_name

def check_table_exists(name):
    table_name = sanitize_name(name)

    conn = sqlite3.connect(config.DBNAME)
    cur = conn.execute('SELECT name FROM sqlite_master WHERE type=\'table\' AND name=\'%s\';' % table_name)
    return True if cur.fetchone() else False


def init_table(server_name):
    """ Initialize a DB for a previously unknown server """

    if server_name:
        server_name = sanitize_name(server_name)
    else:
        raise GraphServerDBExecption('Server name cannot be an empty string!')

    conn = sqlite3.connect(config.DBNAME)

    # Check if table already exists
    if check_table_exists(server_name):
        #print "Table already exsits, not recreating"
        #or
        #raise exception
        raise GraphServerDBExecption('Database with name %s already exists' % server_name)

    #print 'CREATE TABLE IF NOT EXISTS %s (datapoint1 real, datapoint2 real, timestamp string);' % server_name
    conn.execute('CREATE TABLE IF NOT EXISTS %s (datapoint1 text, datapoint2 text, timestamp text);' % server_name)
    conn.close()

def read_all(server_name):
    """ Read all entries for `server_name` """

    if server_name:
        server_name = sanitize_name(server_name)
    else:
        raise GraphServerDBExecption('Server name cannot be an empty string!')

    conn = sqlite3.connect(config.DBNAME)
    #print 'SELECT * FROM %s;' % server_name
    cur = conn.execute('SELECT * FROM %s;' % server_name)
    result = cur.fetchall()
    conn.close()

    return result


def insert(server_name, values):

    if server_name:
        server_name = sanitize_name(server_name)
    else:
        raise GraphServerDBExecption('Server name cannot be an empty string!')

    if not check_table_exists(server_name):
        raise GraphServerDBExecption('Cannot insert into non-existant table %s' % server_name)

    conn = sqlite3.connect(config.DBNAME)
    #print 'INSERT INTO %s VALUES (%s, %s, \'%s\');' % (server_name, str(values[0]), str(values[1]), str(values[2]))
    conn.execute('INSERT INTO %s VALUES (%s, %s, \'%s\');' % (server_name, str(values[0]), str(values[1]), str(values[2])))
    conn.commit()
    conn.close()

