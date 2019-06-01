import zerorpc


class FakeRobot(object):
    def rotate(self, alpha):
        print('rotate {}'.format(alpha))

    def move_forward(self, n):
        print('move {}'.format(n))

    def get_sensor_data(self):
        data = {
            'orientation': {
                'base': (0, -1),
                'current': (1, 0)
            }
        }
        return data


s = zerorpc.Server(FakeRobot())
s.bind("tcp://0.0.0.0:4242")
s.run()
