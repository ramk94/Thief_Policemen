from object_detector import DarkNet
import logging
import sys
import zerorpc

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
logger.addHandler(handler)
weight_path = '../model/custom_tiny_yolov3.weights'
network_config_path = '../cfg/custom-tiny.cfg'
object_config_path = '../cfg/custom.data'

dark = DarkNet(weight_path, network_config_path, object_config_path)
s = zerorpc.Server(dark)
s.bind("tcp://0.0.0.0:4242")
s.run()
