from OpenGL.GL import *      
from OpenGL.GLUT import *    
from OpenGL.GLU import *     
import math
import random

# ===== Global Variables =====
WINDOW_WIDTH, WINDOW_HEIGHT = 1000, 650
bg_r, bg_g, bg_b = 0.8, 0.8, 1.0 
rain_angle, rain_drop = 0, 0 
rain_particles = []
num_drops = 50    


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

def draw_shapes():

    glBegin(GL_TRIANGLES)

    #big ground
    glColor3f(102/255, 59/255, 14/255)
    glVertex2d(-250, -250)
    glVertex2d(-250, 70)
    glVertex2d(250, 70)

    glVertex2d(250, 70)
    glVertex2d(250, -250)
    glVertex2d(-250, -250)

    #1st one
    glColor3f(0, 102/255, 0)
    glVertex2d(-200, 50)
    glVertex2d(-250, 50)
    glColor3f(51/255, 1, 0)
    glVertex2d(-225, 120)
    #2nd one
    glColor3f(0, 102/255, 0)
    glVertex2d(-150, 50)
    glVertex2d(-200, 50)
    glColor3f(51/255, 1, 0)
    glVertex2d(-175, 120)
    #3rd one
    glColor3f(0, 102/255, 0)
    glVertex2d(-100, 50)
    glVertex2d(-150, 50)
    glColor3f(51/255, 1, 0)
    glVertex2d(-125, 120)
    #4th one
    glVertex2d(-50, 50)
    glVertex2d(-100, 50)
    glVertex2d(-75, 120)
    #5th one
    glVertex2d(0, 50)
    glVertex2d(-50, 50)
    glVertex2d(-25, 120)

    #5th one
    glVertex2d(50, 50)
    glVertex2d(0, 50)
    glVertex2d(25, 120)
    #7th one
    glVertex2d(100, 50)
    glVertex2d(50, 50)
    glVertex2d(75, 120)
    #8th one
    glColor3f(0, 102/255, 0)
    glVertex2d(150, 50)
    glVertex2d(100, 50)
    glColor3f(51/255, 1, 0)
    glVertex2d(125, 120)
    #9th one
    glColor3f(0, 102/255, 0)
    glVertex2d(200, 50)
    glVertex2d(150, 50)
    glColor3f(51/255, 1, 0)
    glVertex2d(175, 120)
    #10th one
    glColor3f(0, 102/255, 0)
    glVertex2d(250, 50)
    glVertex2d(200, 50)
    glColor3f(51/255, 1, 0)   
    glVertex2d(225, 120)

    #House
    glColor3f(204/255, 204/255, 255/255)
    glVertex2d(-120, -60)
    glVertex2d(-120, 80)
    glVertex2d(120, 80)
    glVertex2d(120, 80)
    glVertex2d(120, -60)
    glVertex2d(-120, -60)
    #Roof
    glColor3f(0/255, 51/255, 102/255)
    glVertex2d(-130, 80)
    glVertex2d(130, 80)
    glColor3f(0/255, 51/255, 204/255)
    glVertex2d(0, 175)
    #Door
    glColor3f(51/255, 0 , 51/255)
    glVertex2d(-20, -60)
    glVertex2d(-20, 30)
    glVertex2d(20, 30)
    glVertex2d(20, 30)
    glVertex2d(20, -60)
    glVertex2d(-20, -60)
    #Window
    glColor3f(51/255, 0 , 51/255)
    glVertex2d(-90, -20)
    glVertex2d(-90, 40)
    glVertex2d(-45, 40)
    glVertex2d(-45, 40)
    glVertex2d(-45, -20)
    glVertex2d(-90, -20)

    glVertex2d(45, 40)
    glVertex2d(90, 40)
    glVertex2d(90, -20)
    glVertex2d(90, -20)
    glVertex2d(45, -20)
    glVertex2d(45, 40)

    glEnd()
    
    #Door Knob
    glPointSize(7)
    glBegin(GL_POINTS)
    glColor3f(1, 1, 1)
    glVertex2f(15, -20)
    glEnd()

    #Window Grills
    glLineWidth(2)
    glBegin(GL_LINES)
    glColor3f(1, 1, 1)
    glVertex2f(-90, 10)
    glVertex2f(-45, 10)
    glVertex2f(-67.5, 40)
    glVertex2f(-67.5, -20)

    glVertex2f(90, 10)
    glVertex2f(45, 10)
    glVertex2f(67.5, 40)
    glVertex2f(67.5, -20)    
    glEnd()

def draw_rain():
    global rain_particles, rain_angle

    glLineWidth(2)
    glBegin(GL_LINES)

    for drop in rain_particles:

        x, y, color = drop
        r, g, b = color
        glColor3f(r, g, b)

        end_x = x + rain_angle
        end_y = y - 30

        glVertex2f(x, y)
        glVertex2f(end_x, end_y)

    glEnd()

# ===== Keyboard & Mouse Interaction =====
def keyboard_listener(key, x, y):
    """Handles normal keyboard inputs."""
    global bg_r, bg_g, bg_b
    if key == b'd':  
        bg_r = min(bg_r + 0.1, 1.0)
        bg_g = min(bg_g + 0.1, 1.0)
        bg_b = min(bg_b + 0.1, 1.0)
        print("lighing increased")
    elif key == b'n':  
        bg_r = max(bg_r - 0.1, 0.0)
        bg_g = max(bg_g - 0.1, 0.0)
        bg_b = max(bg_b - 0.1, 0.0)
        print("light darkened")
    glutPostRedisplay()


def special_key_listener(key, x, y):
    global rain_angle
    if key == GLUT_KEY_LEFT:
        rain_angle = max(rain_angle- 5, -10)
        print("Rain bend to left")
    elif key == GLUT_KEY_RIGHT:
        rain_angle = min(rain_angle + 5, 10)
        print("Rain bend to right")
    glutPostRedisplay()


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
    """Main display callback for rendering each frame."""
    global bg_r, bg_g, bg_b
    glClearColor(bg_r, bg_g, bg_b, 1.0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    setup_projection()
    draw_shapes()
    draw_rain()

    glutSwapBuffers()


def animate():
    global rain_particles

    for drop in rain_particles:
        drop[1] -= 5 

        if drop[1] < -250:
            drop[1] = 250
            drop[0] = random.uniform(-250, 250)

    glutPostRedisplay()


# ===== Main Function =====
def main():
    glutInit()
    glutInitDisplayMode(GLUT_RGBA)
    glutInitWindowSize(WINDOW_WIDTH, WINDOW_HEIGHT)
    glutInitWindowPosition(100, 100)
    glutCreateWindow(b"Cats and Dogs")

    glutDisplayFunc(display)
    glutIdleFunc(animate)
    glutKeyboardFunc(keyboard_listener)
    glutSpecialFunc(special_key_listener)

    for _ in range(num_drops):
        x = random.uniform(-250, 250)
        y = random.uniform(-250, 250)

        color_choice = random.choice([
            (0.6, 0.6, 1.0),      
            (0.0, 0.4, 1.0),      
            (0.8, 0.8, 0.9)       
        ])

        rain_particles.append([x, y, color_choice])

    glutMainLoop()


# ===== Entry Point =====
if __name__ == "__main__":
    main()
