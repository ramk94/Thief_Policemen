import zerorpc


class Robot:
    """
    Robot class is a high-level abstraction of our real objects, and it has simple interfaces which are easy to manipulate.
    Examples:
        robot = Robot(name, ip, port)
        robot.connect()
        robot.rotate(85)
        robot.move_forward(2)
        data = robot.get_sensor_data()
        robot.disconnect()
    """

    def __init__(self, name, ip, port):
        """
        Construct a robot with corresponding name, ip and port.

        Parameters
        ----------
        name: str
            one of the names of our objects(thief, policeman1 and policeman2)
        ip: str
            a string which indicates the ip address of our remote server, for example, "192.168.1.1"
        port: int
            an integer which indicates the port number of our remote server
        """
        self.name = name
        self.ip = ip
        self.port = port
        self.client = zerorpc.Client(heartbeat=None)

    def connect(self):
        address = 'tcp://{ip}:{port}'.format(ip=self.ip, port=self.port)
        self.client.connect(address)

    def disconnect(self):
        self.client.close()

    def get_sensor_data(self):
        try:
            data = self.client.get_sensor_data()
            result = {
                'flag': True,
                'data': data
            }
        except Exception as e:
            result = {
                'flag': False,
                'message': repr(e)
            }
        return result

    def rotate(self, alpha):
        """
        Rotate the robot with alpha degree clockwisely.

        Parameters
        ----------
        alpha: int
            the degree that the robot rotates(can be negative for counterclockwise rotation)

        Returns
        -------
        result: dict
            a dict consists of some feedback information
        """
        try:
            result = {
                'flag': True
            }
            self.client.rotate(int(alpha))
        except Exception as e:
            result = {
                'flag': False,
                'message': repr(e)
            }
        return result

    def move_forward(self, n):
        """
        Move forward n units.

        Parameters
        ----------
        n: int
            steps that a robot moves(can be negative for backward)

        Returns
        -------
        result: dict
            a dict consists of some feedback information
        """
        try:
            result = {
                'flag': True
            }
            self.client.move_forward(int(n))
        except Exception as e:
            result = {
                'flag': False,
                'message': repr(e)
            }
        return result


if __name__ == '__main__':
    robot_client = Robot('thief', '192.168.31.109', 4242)
    robot_client.connect()
    robot_client.move_forward(1)
    # robot_client.rotate(-60)
