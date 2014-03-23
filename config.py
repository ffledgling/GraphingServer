import functions

DBNAME='graphing_server.db'
SIZE=1024

SERVERLIST = [
        {'IP' : "127.0.0.1",
        'port': 9001,
        'func': functions.convert1,
        'labels': ("bandwidth", "time"),
        'name': 'Test Server 2',
        'outfile': '/var/www/html/example.png',
        'allowed_source_IPs': ['127.0.0.1'],
        'key':''},
        ]
