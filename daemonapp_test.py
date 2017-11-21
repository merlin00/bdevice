from smart.building import AtomDevice
from smart.building import DaemonApp
import time
import argparse
import os


class SensorApp(DaemonApp):
    def run(self, path):
        path += path + '/'
        dev = AtomDevice(path + 'deamonapp.ini',
                         path + 'deamonapp_logger.json')

        info = dev.scan_network(10000)
        if dev.update(info):
            dev.register()

        while True:
            time.sleep(1)


app = SensorApp('test.pid', os.getcwd())

parser = argparse.ArgumentParser(description='Daemon')
parser.add_argument('cmd',
                    help='start, stop or restart',
                    choices=['start', 'stop', 'restart'])
args = vars(parser.parse_args())

if args['cmd'] == 'start':
    app.start()
elif args['cmd'] == 'stop':
    app.stop()
elif args['cmd'] == 'restart':
    app.stop()
    app.start()
