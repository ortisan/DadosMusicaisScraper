__author__ = 'marcelo'

from scrapy import cmdline
import sys, getopt

def main(argv):
    try:
        opts, args = getopt.getopt(argv, 's:')
        if len(opts) == 0:
            raise getopt.GetoptError(u'Argumento "-s" obrigatorio')
        for opt, arg in opts:
            if opt != '-s' or arg == '':
                raise getopt.GetoptError(u'Argumento "-s" obrigatorio')
            cmdline.execute(('scrapy crawl ' + arg).split())
            break
    except getopt.GetoptError:
        print 'Erro!\nUtilize o comando: main.py -s <nome do spider>'
        sys.exit(2)

if __name__ == "__main__":
   main(sys.argv[1:])