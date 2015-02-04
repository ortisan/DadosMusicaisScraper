__author__ = 'marcelo'

import thread

from scrapy import cmdline
from concurrent.futures.process import ProcessPoolExecutor

def iniciar_spiders():
    x = "scrapy crawl cifraclub -a idx_batch=0".split()
    cmdline.execute(x)

iniciar_spiders()