from smart.building import AtomDevice
from smart.building import DaemonApp
from time import sleep
import argparse
import os

from pi_sht1x import SHT1x, SHT1xError


class SensorApp(DaemonApp):
    def run(self, path):
        path += '/'
        dev = AtomDevice(path + 'rpi.ini',
                         path + 'logger.json')

        info = dev.scan_network(10000)
        dev.update(info)
        #if dev.update(info):
        #    dev.register()

        logger = dev.get_logger()
        with SHT1x(13, 11) as s:
            while True:
                try:
                    t = s.read_temperature()
                    h = s.read_humidity(t)
                    logger.info('Temperature: %f, Humidity: %f', t, h)
                    sleep(1)
                except SHT1xError as e:
                    logger.error(e)



app = SensorApp('rpi_test.pid', os.getcwd())

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
