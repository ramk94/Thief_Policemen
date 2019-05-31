import zerorpc


class HelloRPC(object):
    def hello(self, name):
        return "Hello, %s" % name


s = zerorpc.Server(HelloRPC())
s.bind("tcp://0.0.0.0:4242")
s.run()
# import zerorpc

# c = zerorpc.Client()
# c.connect("tcp://127.0.0.1:4242")
# print c.hello("RPC")