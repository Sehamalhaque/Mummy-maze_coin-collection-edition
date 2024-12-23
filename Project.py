from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import time
import math
import random
W_Width, W_Height = 500,500

score=0

pause=True


    

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

def convert_coordinate(x,y):
    global W_Width, W_Height
    a = x - (W_Width/2)
    b = (W_Height/2) - y 
    return a,b


def keyboardListener(key, x, y):

    glutPostRedisplay()
    

def specialKeyListener(key, x, y):
    global speed
    if key=='w':
        print(1)
    
    glutPostRedisplay()
    # if key==GLUT_KEY_RIGHT:
        
    # if key==GLUT_KEY_LEFT:
        

    #   


def mouseListener(button, state, x, y):
    global pause

    if button== GLUT_LEFT_BUTTON:
        if (state == GLUT_DOWN):
            x1,y1=convert_coordinate(x,y)
            #pause button
            if -20<=x1<=20 and 215<=y1<=245:
                pause=not pause
                


            #reset
            elif -245<=x1<=-210 and 215<=y1<=245:
                reset()
                
            #cross button
            elif 210<=x1<=245 and 215<=y1<=245:
                print("Exited game")
                glutLeaveMainLoop()
    glutPostRedisplay()
def draw_points(x, y):
    glPointSize(2) #pixel size. by default 1
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
    draw_line((215,245),(245,215))
    draw_line((215,215),(245,245))
    glColor3f(1, 1, 1)

def draw_pause_button():
    global pause
    if pause==False:
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


def draw_reset_button():
    glColor3f(0.3, 0.8, 0.3)
    draw_line((-205,230),(-245,230))
    draw_line((-245,230),(-230,245))
    draw_line((-245,230),(-230,215))
    #draw_line((12,230),(-12,245))
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


    #draw_line((0, -250), (0, -200))
    draw_pause_button()
    draw_cross_button()
    draw_reset_button()
    glutSwapBuffers()

def reset():
    return None
    
    
def animate():
    return None

                    
    

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
glutSpecialFunc(specialKeyListener)
glutMouseFunc(mouseListener)

glutMainLoop()		#The main loop of OpenGL
