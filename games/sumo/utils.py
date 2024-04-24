from math import sqrt, pi, asin, cos, sin
import os

FPS = 60
GENERAL_SPEED = 2000

# Set up the drawing window
WIDTH = 1000
HEIGHT = 800

# Set up the ground
DOJO_WIDTH = 800
DOJO_HIGHT = 600
DOJO_X = (WIDTH - DOJO_WIDTH) // 2
DOJO_Y = (HEIGHT - DOJO_HIGHT) // 2

# Set up the bots
BOT_SIZE = 5
BOT_OFFSET = BOT_SIZE // 2
BOT_LINEAR_SPEED = 200
BOT_ANGULAR_SPEED = 1

BACKWARD_FACTOR = 10
EPSILON = int(BOT_SIZE * 0.9)
EXPLOSION_TIME = 50

# Bot colors available
RED = "red.png"
BLUE = "blue.png"
#GREEN = "green.png"
#YELLOW = "yellow.png"
ORANGE = "ORANGEE.PNG"
PURPLE = "PURPLEE.PNG"
#BLACK = "black.png"
#BROWN = "brown.png"

# define the RGB values for some colors.
RGB_WHITE = (255, 255, 255)
RGB_BLACK = (0, 0, 0)
RGB_GREEN = (0, 255, 0)
RGB_BLUE = (0, 0, 128)


def calculate_distance(point1, point2):
    """Calculate distance between two points."""
    x1, y1 = point1
    x2, y2 = point2
    distance = sqrt((x2 - x1)**2 + (y2 - y1)**2)
    return distance


def calculate_angle(point1, point2):
    """Calculate angle between two points."""
    x1, y1 = point1[0], - point1[1]
    x2, y2 = point2[0], - point2[1]
    dist = calculate_distance(point1, point2)
    if dist == 0:
        return 0
    angle = asin((y2 - y1) / dist) * 180 / pi
    if x2 < x1:
        angle = 180 - angle
    return round(angle)


def calculate_scalar_product_two_angles(angle1, angle2):
    """Calculate scalar product between two angles."""
    return cos((angle1 - angle2) * pi / 180)
    

def calculate_impact_alligned(own_angle, point1, point2):
    """Calculate impact factor with the opponent."""
    angle_with_opponent = calculate_angle(point1, point2)
    scalar_product = calculate_scalar_product_two_angles(own_angle, angle_with_opponent)
    if scalar_product >= 0:
        return round(scalar_product, 2)
    return 0.1


def collision(point1, point2):
    """Check if two points are colliding."""
    x1, y1 = point1
    x2, y2 = point2
    if sqrt((x2 - x1)**2 + (y2 - y1)**2) <= EPSILON:
        return True
    return False


def calculate_impact(own_angle, point1, point2):
    """Calculate impact and return factor to move the opponent backwards."""
    impact_factor = calculate_impact_alligned(own_angle, point1, point2) * BACKWARD_FACTOR
    if collision(point1, point2):
        return round(impact_factor, 2)
    return 0


def calculate_point(point, angle, distance):
    """Calculate point from another point, angle and distance."""
    x, y = point
    x += distance * cos(angle * pi / 180)
    y += distance * sin(angle * pi / 180)
    return (x, y)


def calculate_point_from_origin(angle, distance):
    """Calculate point from origin, angle and distance."""
    x = distance * cos(angle * pi / 180)
    y = distance * sin(angle * pi / 180)
    return (x, y)


def calculate_angle_from_origin(point):
    """Calculate angle from origin."""
    x, y = point
    angle = asin(y / sqrt(x**2 + y**2)) * 180 / pi
    if x < 0:
        angle = 180 - angle
        return round(angle)


def pathto(f):
    '''open file relative to system'''
    return os.path.join(os.getcwd(), 'games', 'sumo', 'sprites', f)
