import OpenGL
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import numpy as np


class Camera():
## Class representing the 'camera', which can switch between monocular (or middle eye) view, left, or right eye view.
    # First, make an instance of the Camera class, then
    # call (for ex) camera.setEye(camera.eyeLeft) for left eye view
    def __init__(self, IOD, focal_distance, wide_size, height_size):
        self.eyeRight = np.array([IOD/2.0, 0.0, 0.0])
        self.eyeLeft = np.array([-IOD/2.0, 0.0, 0.0])
        self.eyeMiddle = np.array([0.0, 0.0, 0.0])
        self.focal_distance = focal_distance
        self.pa = np.array([wide_size/2.0, -height_size/2.0, focal_distance])
        self.pb = np.array([-wide_size/2.0, -height_size/2.0, focal_distance])
        self.pc = np.array([wide_size/2.0, height_size/2.0, focal_distance])

        self.n = 100
        self.f = 1800

        self.vR = (self.pb - self.pa) / np.linalg.norm(self.pb - self.pa)
        self.vU = (self.pc - self.pa) / np.linalg.norm(self.pc - self.pa)
        self.vN = np.cross(self.vR, self.vU)

    def setEye(self, eye):

        # Compute the screen corner vectors
        vA = self.pa - eye
        vB = self.pb - eye
        vC = self.pc - eye

        global d
        d = -np.dot(vA, self.vN)
        global l
        l = np.dot(self.vR, vA) * self.n/d
        global r 
        r = np.dot(self.vR, vB) * self.n/d
        global b 
        b = np.dot(self.vU, vA) * self.n/d
        global t 
        t = np.dot(self.vU, vC) * self.n/d

        # set current eye
        global curr_eye 
        curr_eye = eye

    def project(self):
        # handles perspective projection
        projection = np.zeros((4,4))

        # handles translation and rotation of view matrix
        rotComponent = np.zeros((4,4))
        transComponent = np.zeros((4,4))

        ## calculate projection matrix
        projection[0][0] = (2 * self.n) / (r - l) 
        projection[2][0] = (r + l) / (r - l)
        projection[1][1] = (2 * self.n) / (t - b)
        projection[2][1] = (t + b) / (t - b)
        projection[2][2] = -(self.f + self.n) / (self.f - self.n)
        projection[3][2] = -(2 * self.f * self.n) / (self.f - self.n)
        projection[2][3] = -1
        projection[3][3] = 0

        ## calculate view matrix

        # calculate translation component of view matrix
        transComponent[3] = [-curr_eye[0], -curr_eye[1], -curr_eye[2] + self.focal_distance, 1]
        transComponent[0][0] = 1; transComponent[1][1] = 1; transComponent[2][2] = 1

        # calculate rotation component of view matrix
        rotComponent[0] = [self.vR[0], self.vU[0], self.vN[0], 0]
        rotComponent[1] = [self.vR[1], self.vU[1], self.vN[1], 0]
        rotComponent[2] = [self.vR[2], self.vU[2], self.vN[2], 0]
        rotComponent[3][3] = 1

        self.view = np.matmul(rotComponent, transComponent)

        # send projection and modelview matrixes for opengl
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glLoadMatrixd(projection)

        glMatrixMode(GL_MODELVIEW)


        




