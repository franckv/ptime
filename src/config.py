#backend = {'type': 'DB', 'engine': 'sqlite:////home/franck/Dev/ptime/db/ptime.db'}
backend = {'type': 'JSon', 'filename': '/home/franck/Dev/ptime/db/ptime.json'}

log_file = '/tmp/ptime.log'

colors = {
    #'default': (0, 'WHITE', 'BLACK', 'NORMAL'),
    'default': (0, 'RED', 'BLACK', 'NORMAL'),
    'title': (1, 'YELLOW', 'BLUE', 'BOLD'),
    'status': (2, 'YELLOW', 'BLUE', 'BOLD'),
    'error': (3, 'RED', 'BLACK', 'BOLD'),
    'highlight': (4, 'YELLOW', 'MAGENTA', 'BOLD'),
    'deleted': (5, 'RED', 'BLACK', 'NORMAL'),
} 
