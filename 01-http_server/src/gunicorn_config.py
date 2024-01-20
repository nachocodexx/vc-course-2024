from multiprocessing import cpu_count
from os import environ

def max_workers():    
    return cpu_count()


bind = '0.0.0.0:' + environ.get('PORT', '7777')
max_requests = 1000
# 
MAX_WORKERS = int(environ.get("MAX_WORKERS","2"))
mw = max_workers()
workers =  MAX_WORKERS if MAX_WORKERS < mw else mw