from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import time
import math
import random
W_Width, W_Height = 500,500
import math
import random
score=0
pause=False
circle_position = {"x": 207, "y": 177}
target_position = {"x": 207, "y": 177}
red_circle_position = {"x": -213, "y": -222}
red_target_position = {"x": -213, "y": -222}

animation_speed = 10 
step1=57    #for y axis movement
step2=60    #for x axis movement
level=1
centers=[[207 , 177], [207 , 120], [207 , 63], [207 , 6], [207 , -51], [207 , -108], [207 , -165], [207 , -222], [147 , 177], 
         [147 , 120], [147 , 63], [147 , 6], [147 , -51], [147 , -108], [147 , -165], [147 , -222], [87 , 177], [87 , 120], [87 , 63], 
         [87 , 6], [87 , -51], [87 , -108], [87 , -165], [87 , -222], [27 , 177], [27 , 120], [27 , 63], [27 , 6], [27 , -51], [27 , -108],
        [27 , -165], [27 , -222], [-33 , 177], [-33 , 120], [-33 , 63], [-33 , 6], [-33 , -51], [-33 , -108], [-33 , -165], [-33 , -222],
        [-93 , 177], [-93 , 120], [-93 , 63], [-93 , 6], [-93 , -51], [-93 , -108], [-93 , -165], [-93 , -222], [-153 , 177], [-153 , 120],
        [-153 , 63], [-153 , 6], [-153 , -51], [-153 , -108], [-153 , -165], [-153 , -222], [-213 , 177], [-213 , 120], [-213 , 63], 
        [-213 , 6], [-213 , -51], [-213 , -108], [-213 , -165], [-213 , -222]]
coin_pos = random.sample(range(63), 5)
coin_centers = [centers[i] for i in coin_pos]
death_zone=[]
death_zone_center=[]
class point:
    def __init__(self):
        self.x=0
        self.y=0
        self.z=0
def crossProduct(a, b):
    result=point()
    result.x = a.y * b.z - a.z * b.y
    result.y = a.z * b.x - a.x * b.z
    result.z = a.x * b.y - a.y * b.x
    return result
def do_lines_intersect(x1, y1, x2, y2, x3, y3, x4, y4):
    """Check if the line segment from (x1, y1) to (x2, y2) intersects with the line from (x3, y3) to (x4, y4)."""
    def ccw(Ax, Ay, Bx, By, Cx, Cy):
        return (Cy - Ay) * (Bx - Ax) > (By - Ay) * (Cx - Ax)
    # Check if the line segments (x1, y1) -> (x2, y2) and (x3, y3) -> (x4, y4) intersect
    return ccw(x1, y1, x3, y3, x4, y4) != ccw(x2, y2, x3, y3, x4, y4) and ccw(x1, y1, x2, y2, x3, y3) != ccw(x1, y1, x2, y2, x4, y4)
def restart():
    global circle_position,target_position,red_circle_position,red_target_position,score,level
    global death_zone,death_zone_center,coin_pos,coin_centers
    circle_position = {"x": 207, "y": 177}
    target_position = {"x": 207, "y": 177}
    red_circle_position = {"x": -213, "y": -222}
    red_target_position = {"x": -213, "y": -222}
    score=0
    level=1
    death_zone=[]
    death_zone_center=[]
    coin_pos = random.sample(range(63), 5)
    coin_centers = [centers[i] for i in coin_pos]
    time.sleep(2)
    print("Game has restarted")
    print("Point: ",score)
def path_crosses_wall(x1, y1, x2, y2):
    """Check if the path from (x1, y1) to (x2, y2) intersects any of the walls."""
    global maze  # Make sure maze is a global variable
    for wall in maze:
        x3, y3, x4, y4 = wall
        if do_lines_intersect(x1, y1, x2, y2, x3, y3, x4, y4):
            return True  # Path intersects a wall
    return False  # No intersection
def convert_coordinate(x,y):
    global W_Width, W_Height
    a = x - (W_Width/2)
    b = (W_Height/2) - y 
    return a,b
def draw_circle_with_points(cx, cy, r, color):
    glColor3f(*color)
    glBegin(GL_POINTS)
    for angle in range(360):  # Increment angle step for more or fewer points
        rad = math.radians(angle)
        x = cx + r * math.cos(rad)
        y = cy + r * math.sin(rad)
        glVertex2f(x, y)
    glEnd()

def increase_death_zones():
    global coin_pos,death_zone,death_zone_center,circle_position
    counter=0
    while counter<5:
        new_position=random.randint(0,63)
        if new_position not in coin_pos and new_position not in death_zone:
            death_zone.append(new_position)
            counter=counter+1
        if centers[new_position][0]==circle_position["x"] and centers[new_position][1]==circle_position["y"]:
            counter=counter-1
            death_zone.pop()
    death_zone_center = [centers[i] for i in death_zone]
def make_death_zone():
    global coin_pos,death_zone,death_zone_center,circle_position
    counter=0
    while counter<5:
        new_position=random.randint(0,63)
        if new_position not in coin_pos:
            death_zone.append(new_position)
            counter=counter+1
        if centers[new_position][0]==circle_position["x"] and centers[new_position][1]==circle_position["y"]:
            counter=counter-1
            death_zone.pop()
    death_zone_center = [centers[i] for i in death_zone]
        

def generate_coin(i):
    global coin_pos,coin_centers,death_zone
    new_pos=random.randint(0, 63)
    while (new_pos in coin_pos) or (new_pos in death_zone):
        new_pos = random.randint(0, 63)
    coin_pos[i]=new_pos
    coin_centers[i]=centers[coin_pos[i]]
    
def move_circle_smoothly(q=0):
    global circle_position, target_position,coin_centers,coin_pos,score,level,death_zone_center
    dx = target_position["x"] - circle_position["x"]
    dy = target_position["y"] - circle_position["y"]
    # Check if we need to keep moving
    if abs(dx) > animation_speed or abs(dy) > animation_speed:
        # Move in the direction of the target
        if abs(dx) > 0:
            circle_position["x"] += animation_speed if dx > 0 else -animation_speed
        if abs(dy) > 0:
            circle_position["y"] += animation_speed if dy > 0 else -animation_speed
        # Request the next frame
        glutPostRedisplay()
        glutTimerFunc(16, move_circle_smoothly, 0)  # Call this function again after 16ms
    else:
        # Snap to target to prevent overshooting
        circle_position["x"] = target_position["x"]
        circle_position["y"] = target_position["y"]
    for i in range(len(coin_centers)):
        if (coin_centers[i][0]==circle_position["x"] and coin_centers[i][1]==circle_position["y"] ):
            coin_pos[i]=None
            score=score+1
            print("Score: ",score)
            if score==6:
                level=2
                print("Entering level: 2")
                make_death_zone()
            if score==11:
                level=3
                print("Entering level: 3")
                increase_death_zones()
            if score==16:
                level=4
                print("Entering level: 4")
                increase_death_zones()
            generate_coin(i)
            break
    if level>1:
        for i in range(len(death_zone_center)):
           if (circle_position["x"]==death_zone_center[i][0] and circle_position["y"]==death_zone_center[i][1]):
               restart()
               break
    
    
    glutPostRedisplay()
def move_red_circle_smoothly(q=0):
    global red_circle_position, red_target_position,circle_position
    dx = red_target_position["x"] - red_circle_position["x"]
    dy = red_target_position["y"] - red_circle_position["y"]
    # Check if we need to keep moving
    if abs(dx) > animation_speed or abs(dy) > animation_speed:
        # Move in the direction of the target
        if abs(dx) > 0:
            red_circle_position["x"] += animation_speed if dx > 0 else -animation_speed
        if abs(dy) > 0:
            red_circle_position["y"] += animation_speed if dy > 0 else -animation_speed
        # Request the next frame
        glutPostRedisplay()
        glutTimerFunc(16, move_red_circle_smoothly, 0)  # Call this function again after 16ms
    else:
        # Snap to target to prevent overshooting
        red_circle_position["x"] = red_target_position["x"]
        red_circle_position["y"] = red_target_position["y"]
        glutPostRedisplay()
    if red_circle_position["x"]==circle_position["x"] and red_circle_position["y"]==circle_position["y"]:
        restart()
    glutPostRedisplay()

def keyboardListener(key, x, y):
    global target_position, red_target_position,step1,step2,level
    # Define the new position based on the key press
    new_x, new_y = target_position["x"], target_position["y"]
    r_new_x, r_new_y = red_target_position["x"], red_target_position["y"]
    # Check the movement direction
    if key == b'w' and new_y + step1 <= 180:  # Move up
        new_y += step1
    elif key == b's' and new_y - step1 >= -230:  # Move down
        new_y -= step1
    elif key == b'a' and new_x - step2 >= -220:  # Move left
        new_x -= step2
    elif key == b'd' and new_x + step2 <= 215:  # Move right
        new_x += step2
    # Check if the path to the new position intersects any walls
    if not path_crosses_wall(target_position["x"], target_position["y"], new_x, new_y):
        # If no intersection, update the target position
        if target_position["x"]!=new_x or target_position["y"]!=new_y:
            while (red_target_position["x"]==r_new_x and red_target_position["y"]==r_new_y):
                r_new_x, r_new_y = red_target_position["x"], red_target_position["y"]
                f= random.choice([1,2,3,4])
            
                if f==1 and (r_new_y + step1 <= 180):
                    r_new_y += step1
                elif f==2 and (r_new_y - step1 >= -230):
                    r_new_y -= step1
                elif f==3 and (r_new_x - step2 >= -220):
                    r_new_x -= step2
                elif f==4 and (r_new_x + step2 <= 215):
                    r_new_x += step2
                if path_crosses_wall(red_target_position["x"], red_target_position["y"], r_new_x, r_new_y):
                    r_new_x = red_target_position["x"]
                    r_new_y = red_target_position["y"]
            red_target_position["x"]=r_new_x
            red_target_position["y"]=r_new_y
            
        target_position["x"] = new_x
        target_position["y"] = new_y
    
    # Call for smooth circle movement after key press
    glutTimerFunc(16, move_circle_smoothly, 0)
    glutTimerFunc(16, move_red_circle_smoothly, 0)
def mouseListener(button, state, x, y):
    global pause
    if button== GLUT_LEFT_BUTTON:
        if (state == GLUT_DOWN):
            x1,y1=convert_coordinate(x,y)
            #pause button
            if -20<=x1<=20 and 215<=y1<=245:
                pause_function()
                
            #restart button
            elif -245<=x1<=-210 and 215<=y1<=245:
                restart()
                
            #cross button
            elif 210<=x1<=245 and 215<=y1<=245:
                print("Exited game")
                glutLeaveMainLoop()
    glutPostRedisplay()
def draw_points(x, y):
    
    glBegin(GL_POINTS)
    glVertex2f(x,y) #jekhane show korbe pixel
    glEnd()
def zone_finder(x,y):
    if (x>=0 and y>=0):     #first quadrent
        if x>=y:
            return 0
        else:
            return 1
    elif (x<0 and y>=0):   #2nd quad   
        if abs(x)>=y:
            return 3
        else:
            return 2
    elif (x<0 and y<0):
        if abs(x)>=abs(y):
            return 4
        else:
            return 5
    else:
        if x>abs(y):
            return 7
        else:
            return 6
def line_zone_finder(x1,y1,x2,y2):
    dx=x2-x1
    dy=y2-y1
    if (abs(dx)>=abs(dy)):  #possible zones 0,3,4,7
        if (dx>=0 and dy>=0):
            return 0
        elif (dx>=0 and dy<0):
            return 7
        elif (dx<0 and dy<0):
            return 4
        else:
            return 3
    else:                  #possible zones 1,2,5,6
        if (dx>=0 and dy>=0):
            return 1
        elif (dx>=0 and dy<0):
            return 2
        elif (dx<0 and dy<0):
            return 5
        else:
            return 6
        
def map_to_0(x,y,z):
    if z==0:
        return x,y
    elif z==1:
        return y,x
    elif z==2:
        return -y,x
    elif z==3:
        return -x,y
    elif z==4:
        return -x,-y
    elif z==5:
        return -y,-x
    elif z==6:
        return y,-x 
    elif z==7:
        return x,-y
def map_to_others(x,y,z):
    if z==0:
        return x,y
    elif z==1:
        return y,x
    elif z==2:
        return y,-x
    elif z==3:
        return -x,y
    elif z==4:
        return -x,-y
    elif z==5:
        return -y,-x
    elif z==6:
        return -y,x 
    elif z==7:
        return x,-y
def draw_line(start, end):
    x1, y1 = start
    x2, y2 = end
    
    line_zone=line_zone_finder(x1,y1,x2,y2)
    z0_x1,z0_y1=map_to_0(x1,y1,line_zone)    #after converting to zone 0
    z0_x2,z0_y2=map_to_0(x2,y2,line_zone)
    dx = z0_x2 - z0_x1
    dy = z0_y2 - z0_y1
    
 
    determiner=2*dy-dx    #d_init
    draw_points(x1,y1)
    while z0_x1<=z0_x2:
        if determiner<0:     #EAST
            determiner+=(2*dy)
            z0_x1+=1
        else:
            determiner+=(2*(dy-dx)) #NORTH EAST
            z0_x1+=1
            z0_y1+=1
        x_n,y_n=map_to_others(z0_x1,z0_y1,line_zone)
        draw_points(x_n,y_n)
        
def draw_circles(cx,cy,r):
    dis=1-r             #descition perameter basically
    x_0=r              #mapping on zone 0
    y_0=0
    
    while(y_0<=x_0):
        if dis<0:         #North
            y_0+=1
            dis+=(2*y_0)+3
        else:
                            #NORTH EAST
            x_0-=1
            y_0+=1
            dis+=(2*y_0)-(2*x_0)+5
        
        draw_points(x_0+cx,y_0+cy)
        a,b=map_to_others(x_0,y_0,1)
        draw_points(a+cx,b+cy)           #adding center after zone change
        a,b=map_to_others(x_0,y_0,2)
        draw_points(a+cx,b+cy)
        a,b=map_to_others(x_0,y_0,3)
        draw_points(a+cx,b+cy)
        a,b=map_to_others(x_0,y_0,4)
        draw_points(a+cx,b+cy)
        a,b=map_to_others(x_0,y_0,5)
        draw_points(a+cx,b+cy)
        a,b=map_to_others(x_0,y_0,6)
        draw_points(a+cx,b+cy)
        a,b=map_to_others(x_0,y_0,7)
        draw_points(a+cx,b+cy)
def draw_cross_button():
    glColor3f(0.8, 0.3, 0.3)
    glPointSize(3)
    draw_line((215,245),(245,215))
    draw_line((215,215),(245,245))
    glColor3f(1, 1, 1)

def draw_pause_button():
    glPointSize(3)
    global pause
    if pause==True:
        glColor3f(0.3, 0.3, 0.8)
        draw_line((-15,210),(-15,245))
        draw_line((-15,210),(15,230))
        draw_line((15,230),(-15,245))
        glColor3f(1, 1, 1)
    else:
        glColor3f(0.3, 0.3, 0.8)
        draw_line((-15,210),(-15,245))
        draw_line((15,210),(15,245))
        glColor3f(1, 1, 1)

maze=[[-120,145,-60,145],[-60,145,-60,90],[-60,90,-120,90],
      [-250,35,-125,35],[180,145,250,145],[180,35,250,35],
      [60,145,120,145],[120,145,120,90],[60,30,60,-20],[60,-20,115,-20],
      [0,-75,60,-75],[60,-75,60,-190],
      [-120,-135,0,-135],[-120,-135,-120,-190],[0,-135,0,-190],
      [-60,-250,-60,-195],[120,-190,180,-190]
      ]
def draw_blocks():
    x=-210
    
    glPointSize(65)
    tile=True
    
    for i in range(8):
        y=172
        tile=(not tile)
        for j in range(8):
            if (tile==True):
                glColor3f(0.92,0.68,0.26)
                tile=False
            else:
                glColor3f(0.66,0.43,0.03)
                tile=True
            draw_points(x,y)
            y-=57
        x+=60
        
def draw_maze():
    glPointSize(3)
    glColor3f(0,0,0)
    global maze
    for i in maze:
            glPointSize(7)
            draw_line((i[0],i[1]),(i[2],i[3]))
        
    glColor3f(1, 1, 1)
def draw_death_zone():
    glPointSize(20)
    glColor3f(0,0.8,0.5)
    if len(death_zone_center)>0:
        for i in death_zone_center:
            draw_circles(i[0],i[1],17)
    glColor3f(1, 1, 1)
    glPointSize(7)
def draw_restart_button():
    glColor3f(0.3, 0.8, 0.2)
    glPointSize(4)
    draw_line((-240,230),(-205,230))
    draw_line((-240,230),(-225,245))
    draw_line((-240,230),(-225,215))
    glColor3f(1, 1, 1)
def display():
    
    #//clear the display
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glClearColor(0,0,0,0);	#//color black
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    #//load the correct matrix -- MODEL-VIEW matrix
    glMatrixMode(GL_MODELVIEW)
    #//initialize the matrix
    glLoadIdentity()
    gluLookAt(0,0,200,	0,0,0,	0,1,0)
    glMatrixMode(GL_MODELVIEW)
    draw_pause_button()
    draw_cross_button()
    draw_restart_button()
    draw_blocks()
    draw_maze()
    draw_death_zone()
    draw_circle_with_points(circle_position["x"], circle_position["y"], 20, (1, 1, 1))  # White circle (upper-right)
    draw_circle_with_points(red_circle_position["x"], red_circle_position["y"], 20, (1, 0, 0))  # Red circle (lower-left)
    
    global coin_centers
    for i in range(len(coin_centers)):
        c_x=coin_centers[i][0]
        c_y=coin_centers[i][1]
        rad=8
        glPointSize(6)
        glColor3f(0.325, 0.592, 0.961)
        draw_circles(c_x,c_y,rad)
    
    glutPostRedisplay()
    glutSwapBuffers()

def pause_function():
    global pause,step1,step2,animation_speed
    pause = not pause
    if pause==True:
        step1=0
        step2=0
        animation_speed=0
    else:
        step1=57
        step2=60
        animation_speed=10
    glutPostRedisplay()
    
def animate():
    #if len(death_zone)>=5:
    None
                    
    
def init():
    #//clear the screen
    glClearColor(0,0,0,0)
    #//load the PROJECTION matrix
    glMatrixMode(GL_PROJECTION)
    #//initialize the matrix
    glLoadIdentity()
    #//give PERSPECTIVE parameters
    gluPerspective(104,	1,	1,	1000.0)
    # **(important)**aspect ratio that determines the field of view in the X direction (horizontally). The bigger this angle is, the more you can see of the world - but at the same time, the objects you can see will become smaller.
    #//near distance
    #//far distance
glutInit()
glutInitWindowSize(W_Width, W_Height)
glutInitWindowPosition(0, 0)
glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGB) #	//Depth, Double buffer, RGB color
# glutCreateWindow("My OpenGL Program")
wind = glutCreateWindow(b"OpenGL Coding Practice")
init()
glutDisplayFunc(display)	#display callback function
glutIdleFunc(animate)	#what you want to do in the idle time (when no drawing is occuring)
glutKeyboardFunc(keyboardListener)
glutMouseFunc(mouseListener)
glutMainLoop()	