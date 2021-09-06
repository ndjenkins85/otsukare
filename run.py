import argparse

from otsukare import app

parser = argparse.ArgumentParser(description="Otsukare run parameters")
parser.add_argument("-host", dest="host", default="127.0.0.1")
parser.add_argument("-port", dest="port", default="5000")
parser.add_argument("-debug", dest="debug", default="True")
args = parser.parse_args()

app.run(host=args.host, port=int(args.port), debug=bool(args.debug))
