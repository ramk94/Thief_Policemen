import zerorpc
# Vikingbot 0
# Emma Smith
from time import sleep
import RPi.GPIO as GPIO

# from Adafruit_BNO055 import BNO055
global L298N_IN1
global L298N_IN2
global L298N_IN3
global L298N_IN4
global L298N_ENA
global L298N_ENB
global pwm_a
global pwm_b


def setup():
    global L298N_IN1
    global L298N_IN2
    global L298N_IN3
    global L298N_IN4
    global L298N_ENA
    global L298N_ENB
    global pwm_a
    global pwm_b

    # switches on the H-bridge
    L298N_IN1 = 26
    L298N_IN2 = 19
    L298N_IN3 = 13
    L298N_IN4 = 6
    L298N_ENA = 16
    L298N_ENB = 12

    GPIO.setmode(GPIO.BCM)

    # initializing GPIO pins to low outputs
    GPIO.setup(L298N_IN1, GPIO.OUT)
    GPIO.setup(L298N_IN2, GPIO.OUT)
    GPIO.setup(L298N_IN3, GPIO.OUT)
    GPIO.setup(L298N_IN4, GPIO.OUT)
    GPIO.setup(L298N_ENA, GPIO.OUT)
    GPIO.setup(L298N_ENB, GPIO.OUT)
    GPIO.output(L298N_IN1, GPIO.LOW)
    GPIO.output(L298N_IN2, GPIO.LOW)
    GPIO.output(L298N_IN3, GPIO.LOW)
    GPIO.output(L298N_IN4, GPIO.LOW)
    # Set duty cycle to 100%
    pwm_a = GPIO.PWM(L298N_ENA, 500)
    pwm_b = GPIO.PWM(L298N_ENB, 500)

    # Initial pwms
    pwm_a.start(50)
    pwm_b.start(50)


def RobotFWD(time):
    print("got to fwd")
    global L298N_IN1
    global L298N_IN2
    global L298N_IN3
    global L298N_IN4
    global L298N_ENA
    global L298N_ENB

    GPIO.output(L298N_IN1, GPIO.HIGH)
    GPIO.output(L298N_IN2, GPIO.LOW)
    GPIO.output(L298N_IN3, GPIO.HIGH)
    GPIO.output(L298N_IN4, GPIO.LOW)
    sleep(time)
    RobotSTOP()
    print("got to end of fwd")


def RobotRIGHT(time):
    global L298N_IN1
    global L298N_IN2
    global L298N_IN3
    global L298N_IN4
    global L298N_ENA
    global L298N_ENB

    GPIO.output(L298N_IN1, GPIO.LOW)
    GPIO.output(L298N_IN2, GPIO.HIGH)
    GPIO.output(L298N_IN3, GPIO.HIGH)
    GPIO.output(L298N_IN4, GPIO.LOW)
    sleep(time)
    RobotSTOP()


def RobotLEFT(time):
    global L298N_IN1
    global L298N_IN2
    global L298N_IN3
    global L298N_IN4
    global L298N_ENA
    global L298N_ENB

    GPIO.output(L298N_IN1, GPIO.HIGH)
    GPIO.output(L298N_IN2, GPIO.LOW)
    GPIO.output(L298N_IN3, GPIO.LOW)
    GPIO.output(L298N_IN4, GPIO.HIGH)
    sleep(time)
    RobotSTOP()


def RobotBACK(time):
    global L298N_IN1
    global L298N_IN2
    global L298N_IN3
    global L298N_IN4
    global L298N_ENA
    global L298N_ENB

    GPIO.output(L298N_IN1, GPIO.LOW)
    GPIO.output(L298N_IN2, GPIO.HIGH)
    GPIO.output(L298N_IN3, GPIO.LOW)
    GPIO.output(L298N_IN4, GPIO.HIGH)
    sleep(time)
    RobotSTOP()


def RobotSTOP():
    global L298N_IN1
    global L298N_IN2
    global L298N_IN3
    global L298N_IN4
    global L298N_ENA
    global L298N_ENB

    GPIO.output(L298N_IN1, GPIO.LOW)
    GPIO.output(L298N_IN2, GPIO.LOW)
    GPIO.output(L298N_IN3, GPIO.LOW)
    GPIO.output(L298N_IN4, GPIO.LOW)


def GetTurnAmount(new_direction):
    # heading, roll pitch = bno.read_euler()
    current_direction = 90

    turn_amount = int(new_direction) - current_direction
    turn_amount = (turn_amount + 180) % 360 - 180
    return turn_amount


def command_arbiter(command, time):
    if command is 'w':
        RobotFWD(time)
    elif command is 'a':
        RobotLEFT(time)
    elif command is 'd':
        RobotRIGHT(time)
    elif command is 's':
        RobotBACK(time)
    else:
        return -1


def cleanup():
    GPIO.cleanup()
import zerorpc
# Vikingbot 0
# Emma Smith
from time import sleep
import RPi.GPIO as GPIO

# from Adafruit_BNO055 import BNO055
global L298N_IN1
global L298N_IN2
global L298N_IN3
global L298N_IN4
global L298N_ENA
global L298N_ENB
global pwm_a
global pwm_b


def setup():
    global L298N_IN1
    global L298N_IN2
    global L298N_IN3
    global L298N_IN4
    global L298N_ENA
    global L298N_ENB
    global pwm_a
    global pwm_b

    # switches on the H-bridge
    L298N_IN1 = 26
    L298N_IN2 = 19
    L298N_IN3 = 13
    L298N_IN4 = 6
    L298N_ENA = 16
    L298N_ENB = 12

    GPIO.setmode(GPIO.BCM)

    # initializing GPIO pins to low outputs
    GPIO.setup(L298N_IN1, GPIO.OUT)
    GPIO.setup(L298N_IN2, GPIO.OUT)
    GPIO.setup(L298N_IN3, GPIO.OUT)
    GPIO.setup(L298N_IN4, GPIO.OUT)
    GPIO.setup(L298N_ENA, GPIO.OUT)
    GPIO.setup(L298N_ENB, GPIO.OUT)
    GPIO.output(L298N_IN1, GPIO.LOW)
    GPIO.output(L298N_IN2, GPIO.LOW)
    GPIO.output(L298N_IN3, GPIO.LOW)
    GPIO.output(L298N_IN4, GPIO.LOW)
    # Set duty cycle to 100%
    pwm_a = GPIO.PWM(L298N_ENA, 500)
    pwm_b = GPIO.PWM(L298N_ENB, 500)

    # Initial pwms
    pwm_a.start(50)
    pwm_b.start(50)


def RobotFWD(time):
    print("got to fwd")
    global L298N_IN1
    global L298N_IN2
    global L298N_IN3
    global L298N_IN4
    global L298N_ENA
    global L298N_ENB

    GPIO.output(L298N_IN1, GPIO.HIGH)
    GPIO.output(L298N_IN2, GPIO.LOW)
    GPIO.output(L298N_IN3, GPIO.HIGH)
    GPIO.output(L298N_IN4, GPIO.LOW)
    sleep(time)
    RobotSTOP()
    print("got to end of fwd")


def RobotRIGHT(time):
    global L298N_IN1
    global L298N_IN2
    global L298N_IN3
    global L298N_IN4
    global L298N_ENA
    global L298N_ENB

    GPIO.output(L298N_IN1, GPIO.LOW)
    GPIO.output(L298N_IN2, GPIO.HIGH)
    GPIO.output(L298N_IN3, GPIO.HIGH)
    GPIO.output(L298N_IN4, GPIO.LOW)
    sleep(time)
    RobotSTOP()


def RobotLEFT(time):
    global L298N_IN1
    global L298N_IN2
    global L298N_IN3
    global L298N_IN4
    global L298N_ENA
    global L298N_ENB

    GPIO.output(L298N_IN1, GPIO.HIGH)
    GPIO.output(L298N_IN2, GPIO.LOW)
    GPIO.output(L298N_IN3, GPIO.LOW)
    GPIO.output(L298N_IN4, GPIO.HIGH)
    sleep(time)
    RobotSTOP()


def RobotBACK(time):
    global L298N_IN1
    global L298N_IN2
    global L298N_IN3
    global L298N_IN4
    global L298N_ENA
    global L298N_ENB

    GPIO.output(L298N_IN1, GPIO.LOW)
    GPIO.output(L298N_IN2, GPIO.HIGH)
    GPIO.output(L298N_IN3, GPIO.LOW)
    GPIO.output(L298N_IN4, GPIO.HIGH)
    sleep(time)
    RobotSTOP()


def RobotSTOP():
    global L298N_IN1
    global L298N_IN2
    global L298N_IN3
    global L298N_IN4
    global L298N_ENA
    global L298N_ENB

    GPIO.output(L298N_IN1, GPIO.LOW)
    GPIO.output(L298N_IN2, GPIO.LOW)
    GPIO.output(L298N_IN3, GPIO.LOW)
    GPIO.output(L298N_IN4, GPIO.LOW)


def GetTurnAmount(new_direction):
    # heading, roll pitch = bno.read_euler()
    current_direction = 90

    turn_amount = int(new_direction) - current_direction
    turn_amount = (turn_amount + 180) % 360 - 180
    return turn_amount


def command_arbiter(command, time):
    if command is 'w':
        RobotFWD(time)
    elif command is 'a':
        RobotLEFT(time)
    elif command is 'd':
        RobotRIGHT(time)
    elif command is 's':
        RobotBACK(time)
    else:
        return -1


def cleanup():
    GPIO.cleanup()


class Policeman(object):
    def rotate(self, alpha):
        alpha=alpha%360
        if alpha>180:
            alpha-=360
        beta=135.0
        if alpha>0:
            seconds=alpha/beta
            RobotRIGHT(seconds)
        else:
            seconds=-alpha/beta
            RobotLEFT(seconds)
        print('rotate {}'.format(alpha))

    def move_forward(self, n):
        seconds=n / 2.0
        RobotFWD(seconds)
        print('move {}'.format(n))

    def get_sensor_data(self):
        data = {
            'orientation': {
                'base': (0, -1),
                'current': (1, 0)
            }
        }
        data = None
        return data


try:
    setup()
    s = zerorpc.Server(Policeman())
    s.bind("tcp://0.0.0.0:4242")
    s.run()
except:
    cleanup()


class Policeman(object):
    def rotate(self, alpha):
        alpha=alpha%360
        if alpha>180:
            alpha-=360
        beta=135.0
        if alpha>0:
            seconds=alpha/beta
        else:
            seconds=360/beta+alpha/beta
        RobotRIGHT(seconds)
        print('rotate {}'.format(alpha))

    def move_forward(self, n):
        seconds=n / 2.0
        RobotFWD(seconds)
        print('move {}'.format(n))

    def get_sensor_data(self):
        data = {
            'orientation': {
                'base': (0, -1),
                'current': (1, 0)
            }
        }
        data = None
        return data


try:
    setup()
    s = zerorpc.Server(Policeman())
    s.bind("tcp://0.0.0.0:4242")
    s.run()
except:
    cleanup()
