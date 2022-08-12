import math
import random
import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

## This file contains the necessary functions to generate and draw a random-dot-stereogram of the sinewave
    # stimulus

dot_centers = [] # container for the dot xyz coordinates that make up the rds

def buildSinewaveRDS(depth, period, offset, width, num_dots):
    dot_centers.clear()
    for d in range(num_dots):
        x = random.randint(0, 1000)/1000.0*width - 0.5*width
        y = random.randint(0, 1000)/1000.0*width - 0.5*width
        z = math.sin(y*period + offset) * depth*0.5

        dot_centers.append((x,y,z))

def drawSinewaveRDS(dot_size, focal_distance, viewMat):
    glColor3fv((1, 0, 0))

    for c in dot_centers:
        glLoadIdentity()
        translation = np.identity(4)
        translation[3] = [c[0], c[1], c[2], 1]
        glLoadMatrixd(np.matmul(viewMat, translation))

        # dots should be scaled to be the same visual angle (image size) regardless of distance
        size = (focal_distance + c[2]) * math.tan(math.radians(0.5*dot_size))
        glutSolidSphere(size, 10, 10)
        
