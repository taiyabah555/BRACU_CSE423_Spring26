from OpenGL.GL import *      # Core OpenGL functions
from OpenGL.GLUT import *    # GLUT library for window and input handling
from OpenGL.GLU import *     # OpenGL Utility library
import math
import random
import time

# ===== Global Variables =====
WINDOW_WIDTH, WINDOW_HEIGHT = 500, 500
points = []
ball_speed = 0.01
ball_size = 3
blink_enabled = False
blink_visible = True
last_blink_time = time.time()
freeze = False

# ===== Coordinate Conversion =====
def convert_coordinate(x, y):
    """
    Converts mouse (screen) coordinates to OpenGL (Cartesian) coordinates.
    Top-left of the window is (0,0) in screen space,
    but OpenGL center is (0,0).
    """
    a = x - (WINDOW_WIDTH / 2)
    b = (WINDOW_HEIGHT / 2) - y
    return a, b


# ===== Draw Functions =====
def draw_point(x, y, size):
    """Draws a single point at (x, y) with given size."""
    glPointSize(size)
    glBegin(GL_POINTS)
    glVertex2f(x, y)
    glEnd()



# ===== Keyboard & Mouse Interaction =====

def keyboard_listener(key, x, y):
    global freeze
    if key == b' ':
        freeze = not freeze
        if freeze:
            print("Frozen")
        else:
            print("Unfrozen")

    glutPostRedisplay()

def special_key_listener(key, x, y):
    global ball_speed, freeze
    if freeze:
        return
    if key == GLUT_KEY_UP:
        ball_speed *= 2
        print("Speed Increased")
    elif key == GLUT_KEY_DOWN:
        ball_speed /= 2
        print("Speed Decreased")

    glutPostRedisplay()


def mouse_listener(button, state, x, y):
    global points, blink_enabled, freeze
    if freeze:
        return
    if button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
        px, py = convert_coordinate(x, y)

        dx = random.choice([-1, 1])
        dy = random.choice([-1, 1])
        color = (random.random(), random.random(), random.random())
        points.append([px, py, dx, dy, color])
        print("New point created")

    elif button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:

        blink_enabled = not blink_enabled
        print("Blink toggled")


# ===== Projection Setup =====
def setup_projection():
    """Defines a 2D orthographic coordinate system."""
    glViewport(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-250, 250, -250, 250, 0, 1)
    glMatrixMode(GL_MODELVIEW)


# ===== Display & Animation =====
def display():

    glClearColor(0,0,0,1)  
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    setup_projection()

    for i in points:
        ball_x, ball_y, dx, dy, color =i
        if blink_enabled and not blink_visible:
            glColor3f(0, 0, 0)  
        else:
            glColor3f(*color)
        draw_point(ball_x, ball_y, ball_size)

    glutSwapBuffers()


import time

last_blink = time.time()

def animate():
    global points, ball_speed
    global blink_enabled, blink_visible, last_blink_time
    global freeze

    # If frozen → stop everything
    if freeze:
        glutPostRedisplay()
        return

    # Move points
    for p in points:
        p[0] += p[2] * ball_speed
        p[1] += p[3] * ball_speed

        # Bounce from walls
        if p[0] > 250 or p[0] < -250:
            p[2] *= -1

        if p[1] > 250 or p[1] < -250:
            p[3] *= -1

    # Handle blinking
    if blink_enabled:
        current = time.time()

        if current - last_blink_time >= 0.5:
            blink_visible = not blink_visible
            last_blink_time = current

    glutPostRedisplay()


# ===== Main Function =====
def main():
    glutInit()
    glutInitDisplayMode(GLUT_RGBA)
    glutInitWindowSize(WINDOW_WIDTH, WINDOW_HEIGHT)
    glutInitWindowPosition(100, 100)
    glutCreateWindow(b"Pointy points")

    # Register callback functions
    glutDisplayFunc(display)
    glutIdleFunc(animate)
    glutKeyboardFunc(keyboard_listener)
    glutSpecialFunc(special_key_listener)
    glutMouseFunc(mouse_listener)

    glutMainLoop()


# ===== Entry Point =====
if __name__ == "__main__":
    main()
