from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import time


WINDOW_WIDTH, WINDOW_HEIGHT = 500, 600
HALF_WIDTH = WINDOW_WIDTH / 2
HALF_HEIGHT = WINDOW_HEIGHT / 2
# catcher
x1,x2,x3,x4 = -70,-35,35,70
y1,y2 = -295,-270
catcher_cx = 0.0
CATCHER_SPEED = 200 

# for diamond
DIAMOND_HALF_W = 15        
DIAMOND_HALF_H = 20        

diamond_x   = 0.0
diamond_y   = 230 
diamond_color = (1.0, 0.0, 0.5)
diamond_arr = []
default_speed = 80
fall_speed = default_speed
acceleration = 5

# for play/pause button & left_arrow button
paused = False 
start = False 
game_over = False 
cheat = False

score_count = 0
last_time   = time.time()

def draw_points(x,y) :
    glPointSize(2)
    glBegin(GL_POINTS)
    glVertex2f(x,y)
    glEnd()

def find_zone(x0, y0, x1, y1):
    dx = x1 - x0
    dy = y1 - y0

    zone = -1
    if abs(dx) >= abs(dy):  
        if dx >= 0 and dy >= 0:
            zone = 0
        elif dx < 0 and dy >= 0:
            zone = 3
        elif dx < 0 and dy < 0:
            zone = 4
        else:
            zone = 7

    else:                  
        if dx >= 0 and dy > 0:
            zone = 1
        elif dx < 0 and dy > 0:
            zone = 2
        elif dx < 0 and dy < 0:
            zone = 5
        else:
            zone = 6   
    return zone

def convert(original_zone,x,y) :

    if (original_zone == 0) :
        return x,y
    elif (original_zone == 1) :
        return y,x
    elif (original_zone == 2) :
        return -y,x
    elif (original_zone == 3) :
        return -x,y
    elif (original_zone == 4) :
        return -x,-y
    elif (original_zone == 5) :
        return -y,-x
    elif (original_zone == 6) :
        return y,-x
    elif (original_zone == 7) :
        return x,-y

def convert_original(original_zone,x,y) :

    if (original_zone == 0) :
        return x,y
    elif (original_zone == 1) :
        return y,x
    elif (original_zone == 2) :
        return y,-x
    elif (original_zone == 3) :
        return -x,y
    elif (original_zone == 4) :
        return -x,-y
    elif (original_zone == 5) :
        return -y,-x
    elif (original_zone == 6) :
        return -y,x
    elif (original_zone == 7) :
        return x,-y  

def midpoint(zone,x0,y0, x1,y1) :

    dx = x1-x0
    dy = y1-y0
    d = (2*dy) - dx
    forE = 2*dy
    forNE = 2*(dy-dx)
    x = x0
    y = y0

    while (x < x1) :

        org_x, org_y = convert_original(zone,x,y)
        draw_points(org_x,org_y)
        if (d<=0) :
            x += 1
            d += forE
        else :
            x += 1
            y += 1
            d += forNE

def eight_way_symmetry(x0,y0,x1,y1) :

    zone = find_zone(x0,y0,x1,y1)
    conv_x0, conv_y0 = convert(zone,x0,y0)
    conv_x1, conv_y1 = convert(zone,x1,y1)
    if conv_x0 > conv_x1:
        conv_x0, conv_x1 = conv_x1, conv_x0
        conv_y0, conv_y1 = conv_y1, conv_y0

    midpoint(zone,conv_x0,conv_y0,conv_x1,conv_y1) 

def specialKeyListener(key,x,y) :

    global catcher_cx, last_time
    if paused or game_over or cheat:
        return
    step = CATCHER_SPEED * (time.time() - last_time + 0.016)
    if key == GLUT_KEY_LEFT:
        catcher_cx -= step * 3  
    elif key == GLUT_KEY_RIGHT:
        catcher_cx += step * 3
    boundary_controller_catcher()
    glutPostRedisplay()

def draw_catcher():

    global x1,x2,x3,x4,y1,y2
    cx = catcher_cx
    if game_over:
        glColor3f(1.0, 0.0, 0.0)
    else:
        glColor3f(1.0, 1.0, 1.0)
    eight_way_symmetry(cx+x2, y1, cx+x3, y1)
    eight_way_symmetry(cx+x1, y2, cx+x2, y1)
    eight_way_symmetry(cx+x3, y1, cx+x4, y2)
    eight_way_symmetry(cx+x1, y2, cx+x4, y2) 

def play_pause():
    glColor3f(255/255, 191/255, 0)
    if paused:
        eight_way_symmetry(-7.5,280,-7.5,230)
        eight_way_symmetry(-7.5,280,15,255)
        eight_way_symmetry(-7.5,230,15,255)
    else:
        eight_way_symmetry(-7.5,280,-7.5,230)
        eight_way_symmetry(7.5,280,7.5,230)
 
def left_arrow():
    glColor3f(0.0,128/255,128/255)
    eight_way_symmetry(-200,280,-220,255)
    eight_way_symmetry(-220,255,-170,255) #Stright line
    eight_way_symmetry(-220,255,-200,230)
    
def cross():
    glColor3f(1.0,0.0,0.0)
    eight_way_symmetry(170,280,220,230)
    eight_way_symmetry(220,280,170,230)

def reset_game():
    global catcher_cx, score_count, fall_speed, game_over, paused, cheat
    catcher_cx = 0.0
    score_count = 0
    fall_speed = default_speed
    game_over = False
    paused = False
    cheat = False
    spawn_diamond()


def mouseListener(button, state, x, y):
    global x1, x2, x3, x4, score_count, start, game_over, paused, cheat, fall_speed, catcher_cx

    new_x = x - HALF_WIDTH
    new_y = HALF_HEIGHT - y

    if (button == GLUT_LEFT_BUTTON) and (state == GLUT_DOWN):

        if (-15 <= new_x <= 15) and (230 <= new_y <= 280):
            if not game_over:
                paused = not paused
                print("Paused" if paused else "Resumed")

        if (170 <= new_x <= 220) and (230 <= new_y <= 280):
            game_over = True
            print(f"Goodbye! Total Score:{score_count}")
            glutLeaveMainLoop() #Game theke exit hoy

        if (-220 <= new_x <= -170) and (230 <= new_y <= 280):
            reset_game()
            print(f"Starting Over! Score:{score_count}")

    glutPostRedisplay()
    

def keyboard(key, x, y):
    global cheat
    if key == b'c' or key == b'C':
        cheat = not cheat
        state = "ON" if cheat else "OFF"
        print(f"Cheat mode {state}")
    glutPostRedisplay()


def check_collision() :

    global score_count, fall_speed, game_over

    d_left   = diamond_x - DIAMOND_HALF_W
    d_right  = diamond_x + DIAMOND_HALF_W
    d_top    = diamond_y + DIAMOND_HALF_H
    d_bottom = diamond_y - DIAMOND_HALF_H

    c_left  = catcher_cx + x1
    c_right = catcher_cx + x4
    c_top   = y2
    c_bottom= y1

    hit = (d_left  < c_right  and
           d_right > c_left   and
           d_top   > c_bottom and
           d_bottom < c_top)

    if hit:
        score_count+= 1
        fall_speed += acceleration
        print(f"Score: {score_count}")
        spawn_diamond()
        return

    if d_top < c_bottom:
        game_over = True
        print(f"Game Over! Total Score: {score_count}")

def draw_diamond(c_x,c_y) :

    check_collision()

    glColor3f(*diamond_color)
    hw, hh = DIAMOND_HALF_W, DIAMOND_HALF_H

    eight_way_symmetry(c_x - hw, c_y,      c_x,       c_y + hh)
    eight_way_symmetry(c_x,      c_y + hh, c_x + hw,  c_y)
    eight_way_symmetry(c_x - hw, c_y,      c_x,       c_y - hh)
    eight_way_symmetry(c_x,      c_y - hh, c_x + hw,  c_y)

def random_color():
    while True:
        r = random.random()
        g = random.random()
        b = random.random()
        if r + g + b > 1.5:   
            return (r, g, b)

def spawn_diamond():
    global diamond_x, diamond_y, diamond_color
    diamond_x     = random.uniform(-HALF_WIDTH + DIAMOND_HALF_W,
                                    HALF_WIDTH - DIAMOND_HALF_W)
    diamond_y     = 230 - DIAMOND_HALF_H
    diamond_color = random_color()

def update():
    global diamond_x, diamond_y, catcher_cx, last_time

    now = time.time()
    dt  = now - last_time
    last_time = now

    if paused or game_over:
        return
    diamond_y -= fall_speed * dt

    if cheat:
        diff = diamond_x - catcher_cx
        step = CATCHER_SPEED * 2 * dt
        if abs(diff) <= step:
            catcher_cx = diamond_x
        else:
            catcher_cx += step if diff > 0 else -step
        boundary_controller_catcher()

    check_collision()

def boundary_controller_catcher():
    global catcher_cx
    lo = -HALF_WIDTH - x1
    hi =  HALF_WIDTH - x4
    catcher_cx = max(lo, min(hi, catcher_cx))

def animation() :

    global paused
    if (paused == False)  :
        glutPostRedisplay()

def idle():
    glutPostRedisplay()

# ===== Projection Setup =====
def setup_projection():
    """Defines a 2D orthographic coordinate system."""
    glViewport(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-HALF_WIDTH, HALF_WIDTH, -HALF_HEIGHT, HALF_HEIGHT, 0, 1)
    glMatrixMode(GL_MODELVIEW)


def display() :
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    setup_projection()

    update()
    draw_catcher()
    play_pause()     
    left_arrow()
    cross()

    if not game_over:
        draw_diamond(diamond_x, diamond_y)
    
    # if pause == True:
    #     draw_pause()
    # else:
    #     play()
    #     for d in diamond_arr :
    #         d[1] += fall_speed
    
    # draw_diamond(d[0],d[1])

    # if d[1] > HALF_HEIGHT:
    #     d[1] = 0

    # if (over == True) :
    #     glutLeaveMainLoop()

    glutSwapBuffers()

def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(WINDOW_WIDTH, WINDOW_HEIGHT)
    glutInitWindowPosition(100,100)
    glutCreateWindow(b"Catch The Diamonds!")
    spawn_diamond()

    # Register callback functions
    glutDisplayFunc(display)
    glutSpecialFunc(specialKeyListener)
    glutKeyboardFunc(keyboard)
    glutMouseFunc(mouseListener)
    glutIdleFunc(idle)

    glutMainLoop()

if __name__ == "__main__":
    main()