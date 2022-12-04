import sys

from iThACK import cli
from iThACK.database.database import Database

argv = sys.argv[1:]
argc = len(argv)

Database().init_database()

if __name__ == "__main__":
    cli.process(argv, argc)
