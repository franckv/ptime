from model import Project, Category, Task

def get_backend(config):
    if config.backend['type'] == 'DB':
        from .db import DB
        return DB(config.backend['engine'])
    elif config.backend['type'] == 'JSon':
        from .jsonbackend import JSon
        return JSon(config.backend['filename'])

class Backend(object):
    pass
