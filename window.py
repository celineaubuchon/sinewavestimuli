import OpenGL
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from Camera import Camera
from parameters import *
from rds import *
from texturedSinewave import TexturedSinewave

# This file is a short demo of the stimuli used in Jovan's experiment
    # Run 'python window.py' to open a window which can present the stimuli with
    # random depths from the experiment.

    # The window begins with a drawing of a small sphere
    # press 't' to generate a textured sinewave ( this can take some time with high levels of subdivs)
    # press 's' to generate a rds sinewave
    # press 'm' for a monocular (or middle eye) view
    # press 'r' for a right eye view
    # press 'l' for a left eye view
    # pressing 't' or 's' multiple times will generate new stimuli (with random depths and wave offsets)

    # this files uses parameters defined in 'parameters.py'. Edit that file to change experimental parameters
    # and display information

global texturedSinewave
global stimType # 0 is textured sinewave, 1 is rds sinewave, 2 is draw nothing
stimType = 2
global eye # 0 is monocular (middle eye), 1 is left, 2 is right
eye = 0

def drawAperture():
    size = 0.97 * stimulus_width/2
    width = -20

    glLoadIdentity()
    glLoadMatrixd(camera.view)

    glColor3fv((0, 0, 0))
    glBegin(GL_QUADS)
    glVertex3f(-size,-size - 10, 0)
    glVertex3f(-size + width, -size - 10, 0)
    glVertex3f(-size + width, size + 10, 0)
    glVertex3f(-size, size + 10, 0)
    glEnd()
    glBegin(GL_QUADS)
    glVertex3f(size,-size - 10, 0)
    glVertex3f(size - width, -size - 10, 0)
    glVertex3f(size - width, size + 10, 0)
    glVertex3f(size, size+ + 10, 0)
    glEnd()
    glBegin(GL_QUADS)
    glVertex3f(-size - 10,-size, 0)
    glVertex3f(-size - 10 , -size + width, 0)
    glVertex3f(size + 10, -size + width, 0)
    glVertex3f(size + 10, -size, 0)
    glEnd()
    glBegin(GL_QUADS)
    glVertex3f(-size - 10,size, 0)
    glVertex3f(-size -10, size - width, 0)
    glVertex3f(size + 10, size - width, 0)
    glVertex3f(size + 10, size, 0)
    glEnd()

def dot():
    glLoadIdentity()
    glLoadMatrixd(camera.view)
    glutSolidSphere(5, 15, 15)
    glFlush()

def initLighting():
    glShadeModel(GL_SMOOTH)
    glEnable(GL_LIGHTING)
    glEnable(GL_NORMALIZE)
    glEnable(GL_COLOR_MATERIAL)

    glLightfv(GL_LIGHT1, GL_AMBIENT, LightAmbient)
    glLightfv(GL_LIGHT1, GL_DIFFUSE, LightDiffuse)
    glLightfv(GL_LIGHT1, GL_SPECULAR, LightSpecular)
    glLightf(GL_LIGHT1, GL_CONSTANT_ATTENUATION, 1)

    glLightfv(GL_LIGHT1, GL_POSITION, LightPosition)
    glEnable(GL_LIGHT1)
    glLightModeli(GL_LIGHT_MODEL_LOCAL_VIEWER, GL_TRUE)

def initRendering():

    # set up camera
    global camera 
    camera = Camera(IOD, focal_distance, display_wide_size, display_height_size)

    # set background color
    glClearColor(0.0, 0.0, 0.0, 0.0)

def keyPressed(key, x, y):
    global stimType
    global eye 

    if key == b'l':
        eye = 1
    if key == b'r':
        eye = 2
    if key == b'm':
        eye = 0

    if key == b't': # build and draw a new textured sinewave
        print("generate textured sinewave")
        depth = depths[random.randint(0, int(len(depths)-1))]
        wave_offset = random.randint(0, int(2*math.pi*period*100))/100.0
        global texturedSinewave
        texturedSinewave = TexturedSinewave(depth = depth, 
                                            width = stimulus_width,
                                            period = period,
                                            offset = wave_offset, 
                                            dot_radius=polka_width, 
                                            focal_distance=focal_distance, 
                                            subdivs=subdivs, 
                                            polka_density=polka_density)
        stimType = 0

    if key == b's': # build and draw a new rds sinewave
        print("generate rds sinewave")
        depth = depths[random.randint(0, int(len(depths)-1))]
        wave_offset = random.randint(0, int(2*math.pi*period*100))/100.0
        buildSinewaveRDS(depth, period, wave_offset, stimulus_width, num_dots)
        stimType = 1



def drawGLScene():

    if eye == 0:
        camera.setEye(camera.eyeMiddle)
    elif eye == 1:
        camera.setEye(camera.eyeLeft)
    elif eye == 2:
        camera.setEye(camera.eyeRight)

    glColor3fv((1, 0, 0))
    camera.project()
    glFlush()
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT) 
    glClearColor(0.0, 0.0, 0.0, 0.0)
    if(stimType == 0):
        glLoadIdentity()
        glLoadMatrixd(camera.view)
        texturedSinewave.drawTexturedSinewave(focal_distance, camera.view)
    if(stimType == 1):
        drawSinewaveRDS(0.1, focal_distance, camera.view)
    if(stimType == 2):
        dot()

    drawAperture()
    glutSwapBuffers()

def main():
    global window
 
    glutInit(sys.argv)
    glutSetOption(GLUT_MULTISAMPLE, 6)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH | GLUT_MULTISAMPLE)
    glutInitWindowSize(display_width, display_height)
    glutInitWindowPosition(0,0)

    window = glutCreateWindow('OpenGL Window')
    initRendering()
    initLighting()
    glutDisplayFunc(drawGLScene)
    glutIdleFunc(drawGLScene)
    glutKeyboardFunc(keyPressed)
    glutMainLoop()

if __name__ == "__main__":
    main()