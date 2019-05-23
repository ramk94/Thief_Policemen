import darknet as dn

# dn.set_gpu(0)
net = dn.load_net(b"../cfg/custom-tiny.cfg", b"../model/custom_tiny_yolov3.weights", 0)
meta = dn.load_meta(b"../cfg/custom.data")
r = dn.detect(net, meta, b"../data/processed_images/001/IMG_0897.jpg")
print(r)
print(dn.network_height(net))
print(dn.network_width(net))