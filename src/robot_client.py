class Robot:
    """
    Robot class is a high-level abstraction of our real objects, and it has simple interfaces which are easy to manipulate.
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
        result = {
            'previous_direction': 0,
            'current_direction': alpha,
            'flag': True
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
        result = {
            'steps': n,
            'flag': True
        }
        return result
