import math
import random
import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

class TexturedSinewave():
## Class representing a textured sinewave, including functions to generate the sinewave mesh, 
    # calculate the vertex colors to 'paint' the texture, and draw the sinewave

    def __init__(self, depth, width, period, offset, dot_radius, focal_distance, subdivs, polka_density):
        self.depth = depth
        self.width = width
        self.period = period
        self.offset = offset
        self.dot_radius = dot_radius
        self.focal_distance = focal_distance
        self.subdivs = max(subdivs, 1)
        self.num_dots = self.periodLength() * width * 0.5 * polka_density / (3*dot_radius)**2
        self.buildTexturedSinewave()

    def generateWave(self):
        vertices = []
        normals = []
        indices = []

        # generate vertices
        for x in range(self.subdivs + 2):
            for y in range(self.subdivs + 2):
                xx = x * (self.width/(self.subdivs + 1)) - 0.5 * self.width
                yy = y * (self.width/(self.subdivs + 1)) - 0.5 * self.width
                zz = math.sin(yy*self.period + self.offset) * self.depth*0.5
                vertices.append(np.array([xx, yy, zz])) 

        # generate indices
        for c in range(self.subdivs + 1):
            for r in range(self.subdivs + 1):
                p = c*(self.subdivs + 2) + r
                indices.append(p)
                indices.append(p+self.subdivs+3)
                indices.append(p + 1)

                indices.append(p)
                indices.append(p + self.subdivs + 2)
                indices.append(p + self.subdivs + 3)
        
        # generate normals
        for v in vertices:
            derivative_sine = math.cos(v[1] * self.period + self.offset) * self.depth/2 * self.period
            nx = 0
            ny = -derivative_sine / math.sqrt(pow(derivative_sine,2) + 1)
            nz = -1 / math.sqrt(pow(derivative_sine,2) + 1)
            norm = np.array([nx, ny, nz])
            norm = norm/np.linalg.norm(norm)
            normals.append(norm)

        return vertices, normals, indices

    def periodLength(self):
        dist = 0
        step_size = 0.001
        y = step_size
        while y < self.width:
            prev_y = y - step_size

            depth_curr = math.sin(y*self.period + self.offset) * self.depth*0.5
            depth_prev = math.sin(prev_y*self.period + self.offset) * self.depth*0.5

            dist = dist + math.sqrt((y - prev_y)**2 + (depth_curr - depth_prev)**2)
            y = y + step_size
        return dist

    def checkIntersection(self, point, radius, sphere_centers):
        intersect = False
        for center in sphere_centers:
            distsq = (center[0] - point[0])**2 + (center[1] - point[1])**2 + (center[2] - point[2])**2
            if(distsq < radius**2):
                intersect = True
                break
        return intersect

    def generateSphereCenters(self):
        sphere_centers = []
        i = 0
        rep = 0
        while i < self.num_dots:
            x = (random.randint(0, int(abs(1000*self.width))) - 500 * self.width)/1000.0
            y = (random.randint(0, int(abs(1000*self.width))) - 500 * self.width)/1000.0
            z = math.sin(y*self.period + self.offset) * self.depth*0.5

            if not self.checkIntersection([x, y, z], self.dot_radius * 2, sphere_centers):
                sphere_centers.append((x, y, z))
                i = i + 1
            else:
                rep = rep + 1
            
            if rep > 10:
                rep = 0
                i = i + 1
        return sphere_centers

    def generateVertexColors(self, vertices, sphere_centers):
        colors = []
        for v in vertices:
            if self.checkIntersection(v, self.dot_radius, sphere_centers):
                colors.append((0.4,0,0))
            else:
                colors.append((1,0,0))
        return colors

    def buildTexturedSinewave(self):
        self.vertices, self.normals, self.indices = self.generateWave()
        self.sphere_centers = self.generateSphereCenters()
        self.colors = self.generateVertexColors(self.vertices, self.sphere_centers)

    def drawTexturedSinewave(self, viewMat, focal_distance):
        specularMaterial = [0.25, 0.0, 0.0, 1.0]
        shininessMaterial = 16.0
        glMaterialfv(GL_FRONT, GL_SPECULAR, specularMaterial)
        glMaterialf(GL_FRONT, GL_SHININESS, shininessMaterial)

        glBegin(GL_TRIANGLES)
        for i in self.indices:
            glColor3fv(self.colors[i])
            glVertex3fv(self.vertices[i])
            glNormal3fv(self.normals[i])
        glEnd()
        glFlush()


        

        




