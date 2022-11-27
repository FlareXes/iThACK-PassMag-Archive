import sys
from  iThACK import cli

argv = sys.argv[1:]
argc = len(argv)

if __name__ == "__main__":
    cli.process(argv, argc)
