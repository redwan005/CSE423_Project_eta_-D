#Libraries & module ekhane
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import math

# Window-er dimensions
window_width, window_height = 500, 700

#========================================================================================================================================================================================
#========================================================================================================================================================================================
                                                                               # Box-er positions koi and dimensions koto (normalized mane [-1 to 1] <-- ei range-er moddhe houya lagbe)
boxes = [
    {"x": -0.8, "y": 0.5, "width": 0.5, "height": 0.3, "game": "Tennis!" } ,
    {"x": -0.2, "y": 0.5, "width": 0.5, "height": 0.3, "game": "Aim!" } ,
    {"x":  0.4, "y": 0.5, "width": 0.5, "height": 0.3, "game": "Asteroids!" } ,
        ]

current_game = None
                                                                               # Duita triangle aaka lagbe box shape-er jonne
def draw_filled_box(x, y, width, height):
    glBegin(GL_TRIANGLES)
    glVertex2f(x, y)                                                           # Top-left
    glVertex2f(x + width, y)                                                   # Top-right
    glVertex2f(x, y - height)                                                  # Bottom-left
    glVertex2f(x + width, y)                                                   # Top-right
    glVertex2f(x + width, y - height)                                          # Bottom-right
    glVertex2f(x, y - height)                                                  # Bottom-left
    glEnd()

                                                                               # Text print/show korar jonne
def draw_text(text, x, y) :
    glRasterPos2f(x, y)
    for char in text :
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(char))

                                                                               # Box call and oitar moddhe color & text add kora
def draw_menu():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    
    for box in boxes:
        glColor3f(0.8086, 0.7383, 0.5898)  #box-er
        draw_filled_box(box["x"], box["y"], box["width"], box["height"])
        
        glColor3f(0.3311, 0.0781, 0.0781)                 #border-er
        glBegin(GL_LINE_LOOP)
        glVertex2f(box["x"], box["y"])
        glVertex2f(box["x"] + box["width"], box["y"])
        glVertex2f(box["x"] + box["width"], box["y"] - box["height"])
        glVertex2f(box["x"], box["y"] - box["height"])
        glEnd()

        draw_text(box["game"], box["x"] + 0.1, box["y"] - 0.15)

    glutSwapBuffers()


def mouse_click(button, state, x, y) :
    global current_game
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN :
        # Convert mouse coordinates to OpenGL normalized coordinates
        normalized_x = (x / window_width) * 2 - 1
        normalized_y = -((y / window_height) * 2 - 1)

        # Check if the click is inside any box
        for box in boxes :
            if (box["x"] < normalized_x < box["x"] + box["width"] and
                box["y"] > normalized_y > box["y"] - box["height"]) :
                print(f"Starting {box['game']}...")
                current_game = box["game"]
                if current_game == "Tennis!" :
                    start_ping_pong()
                if current_game == "Aim!" :
                    start_aim_game() 
                if current_game == "Asteroids!" :
                    start_asteroids()


#================================================================================================================================================================================================
#================================================================================================================================================================================================


paddle_width = 0.09
paddle_height = 0.3
left_paddle_y = 0.0
right_paddle_y = 0.0
ball_x, ball_y = 0.0, 0.0
ball_dx, ball_dy = 0.01, 0.01
ball_size = 0.05
buttons = [
    {"x": -0.9, "y": 0.9, "width": 0.2, "height": 0.13, "action": "Restart", "label": "<- "}, 
    {"x": -0.1, "y": 0.9, "width": 0.2, "height": 0.13, "action": "Pause", "label": "| |"},    
    {"x": 0.7, "y": 0.9, "width": 0.2, "height": 0.13, "action": "Close", "label": "><"}, 
          ]
paused = False  

def start_ping_pong() :
    global ball_x, ball_y, ball_dx, ball_dy, left_paddle_y, right_paddle_y
    ball_x, ball_y = 0.0, 0.0
    ball_dx, ball_dy = random.choice([0.0002, -0.0002]), random.choice([0.0002, -0.0002])
    left_paddle_y, right_paddle_y = 0.0, 0.0
    
    glutDisplayFunc(draw_ping_pong)
    glutIdleFunc(draw_ping_pong) 
    glutKeyboardFunc(keyboard)
    glutMouseFunc(mouse)
    glutSpecialFunc(special_keys)

def draw_buttons() :
    for button in buttons :
        glColor3f(0.8398, 0.5703, 0.1953)  # box-er color
        draw_filled_box(button["x"], button["y"], button["width"], button["height"])
        
        glColor3f(0, 0, 0)                 # border-er color
        glBegin(GL_LINE_LOOP)
        glVertex2f(button["x"], button["y"])
        glVertex2f(button["x"] + button["width"], button["y"])
        glVertex2f(button["x"] + button["width"], button["y"] - button["height"])
        glVertex2f(button["x"], button["y"] - button["height"])
        glEnd()

        glColor3f(0, 0, 0)                 # text-er color
        draw_text(button["label"], button["x"] + 0.07, button["y"] - 0.06)

def mouse(button, state, x, y) :
    global paused, ball_x, ball_y, ball_dx, ball_dy, left_paddle_y, right_paddle_y

    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN :
                                                                               # Mouse-er cordinated OPENGL-er jonne normalize kora lagbe
        normalized_x = (x / window_width) * 2 - 1
        normalized_y = -((y / window_height) * 2 - 1)

        for button in buttons :
            if (button["x"] < normalized_x < button["x"] + button["width"] and button["y"] > normalized_y > button["y"] - button["height"]) :
                action = button["action"]
                if action == "Restart" :
                    print("Restarting game...")
                    start_ping_pong() 
                elif action == "Pause" :
                    paused = not paused  
                    if paused:
                        print("Game paused.")
                    else:
                        print("Game resumed.")
                elif action == "Close" :
                    print("Closing game...")
                    glutLeaveMainLoop()  
                return


def keyboard(key, x, y) :
    global left_paddle_y, right_paddle_y
    if key == b'w' :
        left_paddle_y = min(1.0 - paddle_height / 2, left_paddle_y + 0.05)
    elif key == b's' :
        left_paddle_y = max(-1.0 + paddle_height / 2, left_paddle_y - 0.05)


def special_keys(key, x, y) :
    global right_paddle_y
    if key == GLUT_KEY_UP :
        right_paddle_y = min(1.0 - paddle_height / 2, right_paddle_y + 0.05)
    elif key == GLUT_KEY_DOWN :
        right_paddle_y = max(-1.0 + paddle_height / 2, right_paddle_y - 0.05)


def draw_ping_pong() :
    global left_paddle_y, right_paddle_y, ball_x, ball_y, ball_dx, ball_dy, current_game, paused

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    draw_buttons()

    if not paused :
    
        glColor3f(0.4766, 0.6797, 0.7656)           #paddle-er color
        glRectf(-1.0, left_paddle_y - paddle_height / 2, -1.0 + paddle_width, left_paddle_y + paddle_height / 2)
        glRectf(1.0 - paddle_width, right_paddle_y - paddle_height / 2, 1.0, right_paddle_y + paddle_height / 2)

        glColor3f(0.3311, 0.0732, 0.0732)            #ball color
        glRectf(ball_x - ball_size / 2, ball_y - ball_size / 2, ball_x + ball_size / 2, ball_y + ball_size / 2)

        ball_x += ball_dx
        ball_y += ball_dy
                                                                               # upper & lower wall-e bounce korate hobe
        if ball_y + ball_size / 2 > 1 or ball_y - ball_size / 2 < -1 :
            ball_dy *= -1

                                                                               # paddle-eo bounce korbe
        if (ball_x - ball_size / 2 < -1.0 + paddle_width and
            left_paddle_y - paddle_height / 2 < ball_y < left_paddle_y + paddle_height / 2) :
            ball_dx *= -1
        elif (ball_x + ball_size / 2 > 1.0 - paddle_width and
            right_paddle_y - paddle_height / 2 < ball_y < right_paddle_y + paddle_height / 2) :
            ball_dx *= -1
                                                                               # left & right boundery cross korle respectively jitbe
        if ball_x - ball_size / 2 < -1 :
            print("Right Player Wins!")
            current_game = None
            glutDisplayFunc(draw_menu)
        elif ball_x + ball_size / 2 > 1 :
            print("Left Player Wins!")
            current_game = None
            glutDisplayFunc(draw_menu)
    
    if paused :
        glutTimerFunc(16, draw_ping_pong, 0)
        return 
 
    glutSwapBuffers()


#==================================================================================================================================================================================
#==================================================================================================================================================================================


circle_zones = []
player_score = 0
frame_count = 0
player_pos_x, player_pos_y = 250, 30
pause_btn_x, pause_btn_y = 250, 675
back_btn_x, back_btn_y = 0, 675
exit_btn_x, exit_btn_y = 450, 700
bullet_x, bullet_y = player_pos_x, 2*player_pos_y+5
miss_count = 0
missed_shots = 0
is_shooting = False
is_playing = True
is_game_over = False
falling_balls = []
ball_x = random.uniform(50, 450)
ball_y = random.randint(625, 640)
falling_balls.append([ball_x, ball_y, 650-ball_y])


def start_asteroids() :
    glutInit()
    glutInitWindowSize(window_width, window_height)
    glutInitWindowPosition(0, 0)
    glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGB)
    window = glutCreateWindow(b"Rocket Shooting Game")
    
    glutDisplayFunc(display)
    glutIdleFunc(animate)
    glutMouseFunc(handle_mouse)
    glutKeyboardFunc(handle_keyboard)
    
    glutMainLoop()

def convert_coordinates(cx, cy) :
    global window_width, window_height
    x = cx
    y = (window_height) - cy
    return x, y

def calculate_zone(start_x, start_y, zone_type) :
    if zone_type == 0 :
        return start_x, start_y
    elif zone_type == 1 :
        return start_y, start_x
    elif zone_type == 2 :
        return -start_y, start_x
    elif zone_type == 3 :
        return -start_x, start_y
    elif zone_type == 4 :
        return -start_x, -start_y
    elif zone_type == 5 :
        return -start_y, -start_x
    elif zone_type == 6 :
        return start_y, -start_x
    elif zone_type == 7 :
        return start_x, -start_y


def zone_switch_to_zero(x_val, y_val, zone_type) :
    if zone_type == 0 :
        return x_val, y_val
    elif zone_type == 1 :
        return y_val, x_val
    elif zone_type == 2 :
        return y_val, -x_val
    elif zone_type == 3 :
        return -x_val, y_val
    elif zone_type == 4 :
        return -x_val, -y_val
    elif zone_type == 5 :
        return -y_val, -x_val
    elif zone_type == 6 :
        return -y_val, x_val
    elif zone_type == 7 :
        return x_val, -y_val

                                                                               #drawing part
def draw_exit_button(exit_x, exit_y, exit_color) :
    draw_game_line(exit_x, exit_y, exit_x+50, exit_y-50, exit_color)
    draw_game_line(exit_x, exit_y-50, exit_x+50, exit_y, exit_color)

def draw_back_button(back_x, back_y, back_color) :
    draw_game_line(back_x, back_y, back_x+50, back_y, back_color)
    draw_game_line(back_x, back_y, back_x+20, back_y+25, back_color)
    draw_game_line(back_x, back_y, back_x+20, back_y-25, back_color) 
    
def draw_pause_play_button(pp_x, pp_y, pp_color) :
    if not is_playing :
        draw_game_line(pp_x-25, pp_y+25, pp_x-25, pp_y-25, pp_color)
        draw_game_line(pp_x-25, pp_y+25, pp_x+25, pp_y, pp_color)
        draw_game_line(pp_x-25, pp_y-25, pp_x+25, pp_y, pp_color)
    if is_playing :
        draw_game_line(pp_x-20, pp_y+25, pp_x-20, pp_y-25, pp_color)
        draw_game_line(pp_x+20, pp_y+25, pp_x+20, pp_y-25, pp_color)


def draw_game_line(x_start, y_start, x_end, y_end, line_color) :
    dx = x_end - x_start
    dy = y_end - y_start
    zone_type = 0

    if abs(dx) > abs(dy) :                                                     # zone type find kora
        if dx >= 0 and dy >= 0 :
            zone_type = 0
        elif dx < 0 and dy >= 0 :
            zone_type = 3
        elif dx < 0 and dy < 0 :
            zone_type = 4
        elif dx >= 0 and dy < 0 :
            zone_type = 7
    else :
        if dx >= 0 and dy >= 0 :
            zone_type = 1
        elif dx < 0 and dy >= 0 :
            zone_type = 2
        elif dx < 0 and dy < 0 : 
            zone_type = 5
        elif dx >= 0 and dy < 0 :
            zone_type = 6

    glColor3f(line_color[0], line_color[1], line_color[2])      # moving shob dots-er color
    glPointSize(3)
    glBegin(GL_POINTS)
    glVertex2f(x_start, y_start)

    x_start, y_start = zone_switch_to_zero(x_start, y_start, zone_type)        # midpoint circle drawing reflection use kore
    x_end, y_end = zone_switch_to_zero(x_end, y_end, zone_type)
    dx = x_end - x_start
    dy = y_end - y_start
    d = 2 * dy - dx
    dE = 2 * dy
    dNE = 2 * (dy - dx)
    x, y = x_start, y_start

    while x < x_end :
        if d <= 0 :
            d += dE
            x += 1
        else :
            d += dNE
            x += 1
            y += 1
        
        original_x , original_y = calculate_zone(x, y, zone_type)
        glVertex2f(original_x, original_y)
    
    glEnd()


def draw_bullet_at_center(center_point) :
    
    glBegin(GL_POINTS)
    
    for zone in circle_zones :
        x_val, y_val = shift_to_center(zone[0], zone[1], center_point)
        glVertex2f(x_val, y_val)
    
    glEnd()


def shift_to_center(x_coord, y_coord, center_point) :
    global window_width, window_height
    cx, cy = center_point[0], center_point[1]
    x_coord = x_coord + cx
    y_coord = y_coord + cy
    return x_coord, y_coord 

def compute_zones(cx, cy) :
    global circle_zones
    circle_zones.append((cx, cy))
    circle_zones.append((cy, cx))
    circle_zones.append((cy, -cx))
    circle_zones.append((cx, -cy))
    circle_zones.append((-cx, -cy))
    circle_zones.append((-cy, -cx))
    circle_zones.append((-cy, cx))
    circle_zones.append((-cx, cy))

def draw_circle_with_zones(c_center_x, c_center_y, radius) :
    global circle_zones
    x_circle = 0
    y_circle = radius
    circle_zones = []
    
    compute_zones(x_circle, y_circle)
    
    decision_param = 1-radius
    east_param = 2*x_circle + 3
    southeast_param = 2*x_circle - 2*y_circle + 5
    
    while x_circle < y_circle :
        east_param = 2*x_circle + 3
        southeast_param = 2*x_circle - 2*y_circle + 5
        
        if decision_param < 0 :
            decision_param += east_param
            x_circle += 1
        else:
            decision_param += southeast_param
            x_circle += 1
            y_circle -= 1
        
        compute_zones(x_circle, y_circle)
    
    draw_bullet_at_center((c_center_x, c_center_y))

def draw_rocket() :
    # Left side
    draw_game_line(player_pos_x - 10, player_pos_y - 20, player_pos_x - 10, player_pos_y + 20, [1, 1, 1])
    # Right side  
    draw_game_line(player_pos_x + 10, player_pos_y - 20, player_pos_x + 10, player_pos_y + 20, [1, 1, 1])
    # Top 
    draw_game_line(player_pos_x - 10, player_pos_y + 20, player_pos_x + 10, player_pos_y + 20, [1, 1, 1])
    # Bottom  
    draw_game_line(player_pos_x - 10, player_pos_y - 20, player_pos_x + 10, player_pos_y - 20, [1, 1, 1])  
    # Rocket top
    draw_game_line(player_pos_x - 10, player_pos_y + 20, player_pos_x, player_pos_y + 42, [1, 1, 1])  
    draw_game_line(player_pos_x + 10, player_pos_y + 20, player_pos_x, player_pos_y + 42, [1, 1, 1]) 
    # Left fin
    draw_game_line(player_pos_x - 10, player_pos_y, player_pos_x - 20, player_pos_y - 20, [1, 1, 1])
    draw_game_line(player_pos_x - 20, player_pos_y - 20, player_pos_x - 10, player_pos_y - 20, [1, 1, 1])
    # Right fin
    draw_game_line(player_pos_x + 10, player_pos_y , player_pos_x + 20, player_pos_y - 20, [1, 1, 1])
    draw_game_line(player_pos_x + 20, player_pos_y - 20, player_pos_x + 10, player_pos_y - 20, [1, 1, 1])

  
def handle_keyboard(key, mouse_x, mouse_y) :
    global is_playing, player_pos_x, bullet_x, is_shooting
    
    if not is_game_over and is_playing :
        if key == b'd' :
            if player_pos_x + player_pos_y != 500 :
                player_pos_x = player_pos_x + 10
        if key == b'a' :
            if player_pos_x - player_pos_y != 0 :
                player_pos_x = player_pos_x - 10
        if key == b' ' and is_shooting == False :
            bullet_x = player_pos_x
            is_shooting = True
    
    glutPostRedisplay()

def handle_mouse(button, state, mx, my) :	
    global is_playing, color, dmdX, dmdY, is_game_over, speed, player_score, falling_balls, frame_count, miss_count, missed_shots, bullet_x, bullet_y, player_pos_x, player_pos_y, is_shooting, circle_zones
    
    if button == GLUT_LEFT_BUTTON :
        if state == GLUT_DOWN :
            screen_x, screen_y = convert_coordinates(mx, my)

            if back_btn_x <= screen_x <= back_btn_x+50 and back_btn_y-25 <= screen_y <= back_btn_y+25 :
                
                if is_game_over :
                    is_playing = True
                    is_game_over = False
                    print("Starting Over!")
                    player_pos_x, player_pos_y = 250, 30
                    bullet_x, bullet_y = player_pos_x, 2*player_pos_y+5
                    circle_zones = []
                    is_shooting = False
                    falling_balls = []
                    player_score = 0
                    frame_count = 0
                    miss_count = 0
                    missed_shots = 0
                    ball_x = random.uniform(50, 450)
                    ball_y = random.randint(625, 640)
                    falling_balls.append([ball_x, ball_y, 650-ball_y])    
                
                else :
                    is_playing = True
                    print("Starting Over!")
                    player_pos_x, player_pos_y = 250, 30
                    bullet_x, bullet_y = player_pos_x, 2*player_pos_y+5
                    circle_zones = []
                    is_shooting = False
                    falling_balls = []
                    player_score = 0
                    frame_count = 0
                    miss_count = 0
                    missed_shots = 0
            
            if pause_btn_x-25 <= screen_x <= pause_btn_x+25 and pause_btn_y-25 <= screen_y <= pause_btn_y+25 :
                if not is_game_over :
                    if is_playing :
                        is_playing = False
                    else :
                        is_playing = True

            if exit_btn_x <= screen_x <= exit_btn_x+50 and exit_btn_y-50 <= screen_y <= exit_btn_y :
                print("GG! Total Score :", player_score)
                glutLeaveMainLoop()
    
    glutPostRedisplay()

  
def update_falling_balls() :
    global falling_balls, frame_count, miss_count, is_game_over, is_playing
    
    if is_playing and not is_game_over :
        if len(falling_balls) < 5 :
            if frame_count == 0 :
                frame_count += 0.07
            elif math.floor(frame_count) == 50 :
                ball_x = random.uniform(50, 450)
                ball_y = random.randint(625, 640)
                falling_balls.append([ball_x, ball_y, 650-ball_y])
                for i in range(len(falling_balls)) :
                    falling_balls[i][1] = falling_balls[i][1] - 0.08
                frame_count = 0
            else :
                for i in range(len(falling_balls)) :
                    falling_balls[i][1] = falling_balls[i][1] - 0.08
                frame_count += 0.07
        
        else :
            for i in range(len(falling_balls)) :
                falling_balls[i][1] = falling_balls[i][1] - 0.08
                if math.floor(falling_balls[i][1]) <= 0 :
                    miss_count += 1
                    falling_balls.pop(i)
                    break
            if miss_count == 3 :
                falling_balls = []
                miss_count = 0
                is_playing = False
                is_game_over = True
            if is_game_over :
                print("GG!")
                print("Total Score :", player_score)

                
def handle_shooting() :
    global is_playing, is_game_over, is_shooting, bullet_x, bullet_y, player_pos_x, player_pos_y, falling_balls, missed_shots, player_score 
    
    hit_index = -1
    if not is_game_over and is_playing and is_shooting : 
        if math.floor(bullet_y) < 650 :
            bullet_y += 1
        else :
            is_shooting = False
            bullet_y = 2*player_pos_y+5
            missed_shots += 1
    
    if not is_game_over and is_playing and is_shooting :
        for i in range(len(falling_balls)) :
            x_dist = (bullet_x - falling_balls[i][0])**2
            y_dist = (bullet_y - falling_balls[i][1])**2
            radius_squared = (falling_balls[i][2]+5)**2
            if (x_dist + y_dist) <= radius_squared :
                hit_index = i
                player_score += 1
                print("Score:", player_score)
    
    if not is_game_over and is_playing :
        for i in range(len(falling_balls)) :
            x_dist = (player_pos_x - falling_balls[i][0])**2
            y_dist = (player_pos_y - falling_balls[i][1])**2
            radius_squared = (falling_balls[i][2]+20)**2
            if (x_dist + y_dist) <= radius_squared :
                bullet_y = 2*player_pos_y+5
                falling_balls = []
                is_playing = False
                is_game_over = True
                break
        if is_game_over :
            print("Game Over!")
            print("Total Score:", player_score)
    
    if hit_index != -1 :
        falling_balls.pop(hit_index)
        is_shooting = False
        bullet_y = 2*player_pos_y+5
    
    if not is_game_over and missed_shots == 3 :
        falling_balls = []
        missed_shots = 0
        is_playing = False
        is_game_over = True
        print("Game Over!")
        print("Total Score:", player_score)
  
def display() :
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glClearColor(0.4141, 0.4648, 0.3438, 1)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glViewport(0, 0, 500, 700)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, 500, 0.0, 700, 0.0, 1.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    
    global player_pos_x, player_pos_y, bullet_x, bullet_y, pause_btn_x, pause_btn_y, back_btn_x, back_btn_y, exit_btn_x, exit_btn_y, frame_count, is_shooting, falling_balls

    if not is_game_over and is_shooting :
        draw_circle_with_zones(bullet_x, bullet_y, 3)
    draw_rocket()
    
    for ball in falling_balls :
        draw_circle_with_zones(ball[0], ball[1], ball[2])
    
    draw_exit_button(exit_btn_x, exit_btn_y, [1, 0, 0])
    draw_back_button(back_btn_x, back_btn_y, [0, 0, 1])
    draw_pause_play_button(pause_btn_x, pause_btn_y, [1, 0.7, 0.02])  
    glutSwapBuffers()


def animate() :
    glutPostRedisplay()
    global is_playing, is_game_over, is_shooting, bullet_x, bullet_y, player_pos_x, player_pos_y, falling_balls
    update_falling_balls()
    handle_shooting()


#=================================================================================================================================================================================
#=================================================================================================================================================================================


aim_circle_radius = 0.05
aim_circle_x, aim_circle_y = 0.0, 0.0  
aim_circle_dx, aim_circle_dy = 0.008, 0.008  

aim_circle_visible = True
hit_count = 0

def aim_draw_circle(aim_x, aim_y, aim_radius) :
    
    glBegin(GL_TRIANGLE_FAN)
    glVertex2f(aim_x, aim_y)
    
    for angle in range(361) :  # 0 to 360 degrees
        theta = angle * 3.14159 / 180  # Convert to radians
        glVertex2f(aim_x + aim_radius * math.cos(theta), aim_y + aim_radius * math.sin(theta))

    glEnd()


def aim_display() :
    global aim_circle_x, aim_circle_y, aim_circle_dx, aim_circle_dy, aim_circle_visible

    glClear(GL_COLOR_BUFFER_BIT)

    if aim_circle_visible :
        glColor3f(0.33, 0.078, 0.078)     # target-er color
        aim_draw_circle(aim_circle_x, aim_circle_y, aim_circle_radius)

    glColor3f(0.8086, 0.7383, 0.5898)     # points print-er color
    aim_draw_text(f"Hits: {hit_count}", -0.95, 0.9)

    glutSwapBuffers()


def aim_update(value) :
    global aim_circle_x, aim_circle_y, aim_circle_dx, aim_circle_dy
                                                                               # circle position change kora
    aim_circle_x += aim_circle_dx
    aim_circle_y += aim_circle_dy

                                                                               # boundery-er moddhe bounce back koranor jonne
    if aim_circle_x + aim_circle_radius > 1 or aim_circle_x - aim_circle_radius < -1 :
        aim_circle_dx *= - 1
    if aim_circle_y + aim_circle_radius > 1 or aim_circle_y - aim_circle_radius < -1 :
        aim_circle_dy *= -1

    glutPostRedisplay()
    glutTimerFunc(16, aim_update, 0)  # Approximately 60 FPS


def aim_mouse(aim_button, aim_state, aim_x, aim_y) :
    global aim_circle_visible, hit_count, window_height, window_width

    if aim_button == GLUT_LEFT_BUTTON and aim_state == GLUT_DOWN :
                                                                               # mouse cordinates-ke opengl-er jonne normalize kora
        aim_normalized_x = (aim_x / window_width) * 2 - 1
        aim_normalized_y = -((aim_y / window_height) * 2 - 1)
                                                                               # target-e mouse point hit koreche kina
        if ((aim_normalized_x - aim_circle_x) ** 2 + (aim_normalized_y - aim_circle_y) ** 2) ** 0.5 <= aim_circle_radius :
            
            aim_circle_visible = False  
            hit_count += 1 
            aim_respawn_circle()


def aim_respawn_circle() :
    global aim_circle_x, aim_circle_y, aim_circle_visible
    aim_circle_x = random.uniform(-1 + aim_circle_radius, 1 - aim_circle_radius)
    aim_circle_y = random.uniform(-1 + aim_circle_radius, 1 - aim_circle_radius)
    aim_circle_visible = True


def aim_draw_text(text, a_x, a_y) :
    glRasterPos2f(a_x, a_y)
    
    for char in text :
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(char)) 


def start_aim_game() :
    global circle_x, circle_y

    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(window_width, window_height)
    glutCreateWindow(b"Aim Testing Game")

    glutDisplayFunc(aim_display)
    glutMouseFunc(aim_mouse)
    glutTimerFunc(16, aim_update, 0)

    glClearColor(0.4141, 0.4648, 0.3438, 1)    #background color

    aim_respawn_circle()

    glutMainLoop()


#=================================================================================================================================================================================
#=================================================================================================================================================================================


                                                                               # Initialize OpenGL and GLUT
def main_call_eta() :
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(window_width, window_height)
    glutCreateWindow(b"Asho Game Kheli!!") 

    glutDisplayFunc(draw_menu)
    glutMouseFunc(mouse_click)
    
    glClearColor(0.4141, 0.4648, 0.3438, 1)   # background color

    glutMainLoop()

main_call_eta()
