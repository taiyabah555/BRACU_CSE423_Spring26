from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

import math
import random

cam_angle = 0          
cam_height = 500
cam_radius = 500
camera_follow = False  

player_pos = [0.0, 0.0, 0.0]
gun_angle = 0.0      
bullets = []           
BULLET_SPEED = 8.0
MAX_MISS = 10
ENEMY_COUNT = 5
enemies = []           
ENEMY_SPEED = 0.06

life = 5
score = 0
missed = 0
last_shot_time = 0.0
game_over= False
cheat_mode = False
cheat_vision= False  

GRID_LENGTH = 600
TILE_SIZE= 100
fovY = 80
WALL_HEIGHT= 100
HIT_RADIUS = 60      
PLAYER_RADIUS= 55      
time_elapsed = 0.0     


def spawn_enemy():
    side = random.randint(0, 3)
    if side == 0:
        x = random.uniform(-GRID_LENGTH, GRID_LENGTH)
        y = GRID_LENGTH
    elif side == 1:
        x = random.uniform(-GRID_LENGTH, GRID_LENGTH)
        y = -GRID_LENGTH
    elif side == 2:
        x = GRID_LENGTH
        y = random.uniform(-GRID_LENGTH, GRID_LENGTH)
    else:
        x = -GRID_LENGTH
        y = random.uniform(-GRID_LENGTH, GRID_LENGTH)
    return {'pos': [x, y, 0.0], 'phase': random.uniform(0, 2 * math.pi)}


def init_enemies():
    global enemies
    enemies = [spawn_enemy() for _ in range(ENEMY_COUNT)]


def fire_bullet():
    global missed
    if game_over:
        return
    rad = math.radians(gun_angle - 90)
    dx= math.cos(rad)
    dy= math.sin(rad)
    bx= player_pos[0] + dx*50
    by= player_pos[1] + dy*50
    bullets.append({'pos': [bx, by, 30.0], 'dir': [dx, dy, 0.0]})
    print(f"Bullet is Fired!")

def reset_game():
    global life, score, missed, game_over, cheat_mode, cheat_vision
    global player_pos, gun_angle, bullets, time_elapsed, last_shot_time
    global cam_angle, cam_height, cam_radius, camera_follow
    life = 5
    score = 0
    missed= 0
    game_over = False
    cheat_mode = False
    cheat_vision = False
    player_pos = [0.0, 0.0, 0.0]
    gun_angle= 0.0
    bullets = []
    time_elapsed= 0.0
    cam_angle= 0.0
    cam_height = 500
    cam_radius = 500
    camera_follow = False
    init_enemies()


def draw_text(x, y, text, font= GLUT_BITMAP_HELVETICA_18):
    glColor3f(1, 1, 1)
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, 1000, 0, 800)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    glRasterPos2f(x, y)
    for ch in text:
        glutBitmapCharacter(font, ord(ch))
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)


def draw_grid():
    #chessboard
    n = GRID_LENGTH //TILE_SIZE #6x6
    glBegin(GL_QUADS)
    for i in range(-n, n):
        for j in range(-n, n):
            if (i+j)%2 == 0:
                glColor3f(153/255, 51/255, 204/255)
            else:
                glColor3f(1., 1., 1)
            x0, x1= i*TILE_SIZE, (i + 1)*TILE_SIZE
            y0, y1= j*TILE_SIZE, (j + 1)*TILE_SIZE
            glVertex3f(x0,y0,0)
            glVertex3f(x1,y0,0)
            glVertex3f(x1,y1,0)
            glVertex3f(x0,y1,0)
    glEnd()


def draw_walls():
    L =GRID_LENGTH
    H = WALL_HEIGHT
    walls = [
        ((-L,-L,0), (L,-L, 0), ( L,-L, H), (-L,-L,H), (0,1,1)), # cyan border
        ((-L,L,0), (L, L,0), (L,L,H), (-L,L,H), (1,1,1)), # white border
        ((-L,-L,0), (-L,L,0), (-L,L,H), (-L,-L,H), (0,1,0)), # green border
        ((L,-L,0), (L,L,0), (L,L,H), (L,-L,H), (0,0,204/255)), # blue border
    ]
    glBegin(GL_QUADS)
    for w in walls:
        glColor3f(*w[4])
        for v in w[:4]:
            glVertex3f(*v)
    glEnd()


def draw_player():
    glPushMatrix()
    glTranslatef(*player_pos)
    glRotatef(gun_angle, 0, 0, 1)

    if game_over:
        glRotatef(90, 1, 0, 0)

    #head
    glPushMatrix()
    glTranslatef(0, 0, 75)
    glColor3f(0, 0., 0)
    gluSphere(gluNewQuadric(), 15, 16, 16)
    glPopMatrix()

    #body
    glPushMatrix()
    glTranslatef(0, 0, 40)
    glColor3f(0.25, 0.45, 0.2)
    glScalef(2.0, 1.0, 1.5)
    glutSolidCube(20)
    glPopMatrix()

    #left arm
    glPushMatrix()
    glTranslatef(-12, 0, 55)
    glColor3f(1, 204/255, 53/255)
    glRotatef(90, 1, 0, 0)          
    gluCylinder(gluNewQuadric(), 12, 2, 35, 8, 4)
    glPopMatrix()

    #right arm
    glPushMatrix()
    glTranslatef(12, 0, 55)
    glColor3f(1, 204/255, 53/255)
    glRotatef(90, 1, 0, 0)
    gluCylinder(gluNewQuadric(), 12, 2, 35, 8, 4)
    glPopMatrix()

    #gun
    glPushMatrix()
    glTranslatef(0, 0, 52)
    glColor3f(153/255, 153/255, 153/255)
    glRotatef(90, 1, 0, 0)  
    gluCylinder(gluNewQuadric(), 15, 2, 70, 8, 4)
    glPopMatrix()

    #left leg
    glPushMatrix()
    glTranslatef(-10, 0, 25)
    glColor3f(0.1, 0.2, 0.85)
    glRotatef(180, 1, 0, 0)
    gluCylinder(gluNewQuadric(), 12, 4, 35, 8, 4)
    glPopMatrix()

    #right leg
    glPushMatrix()
    glTranslatef(10, 0, 25)
    glColor3f(0.1, 0.2, 0.85)
    glRotatef(180, 1, 0, 0)
    gluCylinder(gluNewQuadric(), 12, 4, 35, 8, 4)
    glPopMatrix()

    glPopMatrix()


def draw_bullets():
    glColor3f(153/255, 0, 51/255)
    for b in bullets:
        glPushMatrix()
        glTranslatef(*b['pos'])
        glutSolidCube(10)
        glPopMatrix()


def draw_enemies():
    for e in enemies:
        scale = 1.0 + 0.25 * math.sin(e['phase'] + time_elapsed * 2.0)
        glPushMatrix()
        glTranslatef(*e['pos'])
        glScalef(scale, scale, scale)

        # Main body
        glColor3f(201/255, 0, 51/255)
        gluSphere(gluNewQuadric(), 28, 12, 12)

        #head
        glColor3f(0,0,0)
        glPushMatrix()
        glTranslatef(0, 0, 35)
        gluSphere(gluNewQuadric(), 14, 10, 10)
        glPopMatrix()

        glPopMatrix()


def draw_textBox():
    if game_over:
        draw_text(10, 775, f"GAME OVER!")
        draw_text(10, 748, f"Press R to restart")
    else:
        draw_text(10, 775, f"Player Life Remaining: {life}")
        draw_text(10, 748, f"Game Score: {score} ")
        draw_text(10, 721, f"Player Bullet Missed: {missed}")


def setupCamera():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(fovY, 1.25, 0.1, 3000)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    if camera_follow and not game_over:
        # 1st person view
        rad = math.radians(gun_angle-90)
        ex = player_pos[0]
        ey = player_pos[1]
        ez = player_pos[2]+ 100
        lx = ex + math.cos(rad)*200
        ly = ey + math.sin(rad)*200
        lz = ez
        gluLookAt(ex, ey, ez, lx, ly, lz, 0, 0, 1)
    else:
        #3rd person view
        rad = math.radians(cam_angle)
        cx = cam_radius*math.sin(rad)
        cy = cam_radius*math.cos(rad)
        cz = cam_height
        gluLookAt(cx + player_pos[0], cy + player_pos[1], cz,
                  player_pos[0], player_pos[1], 0,
                  0, 0, 1)


def keyboardListener(key, x, y):
    global gun_angle, cheat_mode, cheat_vision, game_over, camera_follow

    if key == b'r':
        reset_game()
        return

    if game_over:
        return

    step = 8.0
    if key == b'w':
        if not (cheat_mode and camera_follow):
            rad = math.radians(gun_angle - 90)
            player_pos[0] += math.cos(rad) * step
            player_pos[1] += math.sin(rad) * step
            # Keep within grid
            player_pos[0] = max(-GRID_LENGTH + 30, min(GRID_LENGTH - 30, player_pos[0]))
            player_pos[1] = max(-GRID_LENGTH + 30, min(GRID_LENGTH - 30, player_pos[1]))

    elif key == b's':
        if not (cheat_mode and camera_follow):
            rad = math.radians(gun_angle - 90)
            player_pos[0] -= math.cos(rad) * step
            player_pos[1] -= math.sin(rad) * step
            player_pos[0] = max(-GRID_LENGTH + 30, min(GRID_LENGTH - 30, player_pos[0]))
            player_pos[1] = max(-GRID_LENGTH + 30, min(GRID_LENGTH - 30, player_pos[1]))

    elif key == b'a' and not cheat_mode:
        if not (cheat_mode and camera_follow):
            gun_angle += 3.0

    elif key == b'd' and not cheat_mode:
        if not (cheat_mode and camera_follow):
            gun_angle -= 3.0

    elif key == b'c':
        cheat_mode = not cheat_mode

    elif key == b'v':
        if cheat_mode:
            cheat_vision = not cheat_vision
        else: 
            camera_follow = not camera_follow

    glutPostRedisplay()


def specialKeyListener(key, x, y):
    global cam_angle, cam_height

    if key == GLUT_KEY_LEFT:
        cam_angle -= 2
    elif key == GLUT_KEY_RIGHT:
        cam_angle += 2
    elif key == GLUT_KEY_UP:
        cam_height = min(1200, cam_height + 15)
    elif key == GLUT_KEY_DOWN:
        cam_height = max(50, cam_height - 15)

    glutPostRedisplay()


def mouseListener(button, state, x, y):
    global camera_follow

    if not cheat_mode:
        if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
            fire_bullet()

        elif button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
            camera_follow = not camera_follow


def update_bullets():
    global missed
    to_remove = []
    for b in bullets:
        b['pos'][0] += b['dir'][0]*BULLET_SPEED
        b['pos'][1] += b['dir'][1]*BULLET_SPEED

        if (abs(b['pos'][0])> GRID_LENGTH or abs(b['pos'][1])> GRID_LENGTH):
            to_remove.append(b)
            missed += 1
            print(f"Bullet Missed : {missed}")

    for b in to_remove:
        if b in bullets:
            bullets.remove(b)


def check_bullet_enemy_collision():
    global score
    for b in list(bullets):
        for e in enemies:            
            dx = b['pos'][0]-e['pos'][0]
            dy = b['pos'][1]-e['pos'][1]
            dist = math.sqrt(dx*dx + dy*dy)
            if dist<HIT_RADIUS:
                if b in bullets:
                    bullets.remove(b)
                e['pos'] = spawn_enemy()['pos']
                score += 1
                break


def check_enemy_player_collision():
    global life
    for e in enemies:
        dx = e['pos'][0]-player_pos[0]
        dy = e['pos'][1]-player_pos[1]
        dist = math.sqrt(dx*dx + dy*dy)
        if dist<PLAYER_RADIUS:
            life -= 1
            e['pos'] = spawn_enemy()['pos']


def update_enemies():
    for e in enemies:
        dx = player_pos[0]-e['pos'][0]
        dy = player_pos[1]-e['pos'][1]
        dist = math.sqrt(dx*dx + dy*dy)
        if dist > 5:
            e['pos'][0] += (dx/dist)*ENEMY_SPEED
            e['pos'][1] += (dy/dist)*ENEMY_SPEED


def update_cheat_mode():
    global gun_angle, last_shot_time
    gun_angle += 0.2  

    rotation_angle = gun_angle - 90
    for e in enemies:
        dx = e['pos'][0]-player_pos[0]
        dy = e['pos'][1]-player_pos[1]
        dist = math.sqrt(dx*dx + dy*dy)
        if dist < 5:
            continue
        enemy_angle = math.degrees(math.atan2(dy, dx))
        diff = (enemy_angle - rotation_angle) % 360
        if diff>180:
            diff -=360
        if abs(diff) < .3:  
            if (time_elapsed-last_shot_time) > 0.5:
                fire_bullet()
                last_shot_time = time_elapsed
            break
        

def idle():
    global game_over, time_elapsed

    time_elapsed += 0.016  

    if not game_over:
        update_bullets()
        update_enemies()
        check_bullet_enemy_collision()
        check_enemy_player_collision()

        if cheat_mode:
            update_cheat_mode()

        if life <= 0 or missed >= MAX_MISS:
            life_capped = max(life, 0)
            game_over = True

    glutPostRedisplay()

def showScreen():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glViewport(0, 0, 1000, 800)
    glEnable(GL_DEPTH_TEST)

    setupCamera()

    draw_grid()
    draw_walls()
    draw_player()
    draw_bullets()
    draw_enemies()
    draw_textBox()

    glutSwapBuffers()


def main():
    init_enemies()
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(1000, 800)
    glutInitWindowPosition(0, 0)
    glutCreateWindow(b"Bullet Frenzy-3D Game")

    glutDisplayFunc(showScreen)
    glutKeyboardFunc(keyboardListener)
    glutSpecialFunc(specialKeyListener)
    glutMouseFunc(mouseListener)
    glutIdleFunc(idle)

    glutMainLoop()


if __name__ == "__main__":
    main()