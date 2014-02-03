#!/usr/bin/python
# -*- coding: utf-8 -*-
# Programmed by Kaan Akşit

import sys,matplotlib
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.art3d as art3d
import scipy.linalg
from matplotlib.patches import Circle, PathPatch
from mpl_toolkits.mplot3d import axes3d
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from numpy import *
from numpy.fft import *

__author__  = ('Kaan Akşit')

class paraxialmatrix():
    def __init__(self):
        # See "Laser beams and resonators" from Kogelnik and Li for the theoratical explanation
        self.fig = plt.figure()
        return
    def createvector(self,x,angle):
        # Creates a paraxial ray, angle is in degrees, x is the distance of the point to the plane of direction of propagation
        angle  = radians(angle)
        vector = array([[x],[angle],[1]])
        return vector
    def freespace(self,vector,distance,deltax=0,deltafi=0):
        # Ray transfer matrix of free space propagation, distance is in meters
        # deltax is the spatial shift, deltafi is the angular shift
        space  = array([[1,distance,deltax],[0,1,deltafi],[0,0,1]])
        vector = dot(space,vector)
        return vector
    def plotvector(self,startvector,stopvector):
        # Method to plot paraxial vectors in 2D space
        plt.plot([startvector[0]/startvector[1],stopvector[0]/stopvector[1]],[startvector[0],stopvector[0]],'o-')
        plt.show()
        return True

class raytracing():
    def __init__(self):
        # See "General Ray tracing procedure" from G.H. Spencerand M.V.R.K Murty for the theoratical explanation
        self.fig = plt.figure()
        self.ax  = self.fig.gca(projection='3d')
        return
    def findangles(self,Point1,Point2):
        # Function to find angle between two points if there was a line intersecting at both of them.
        # Vector to hold angles is created.
        angles   = []
        # Find the distance in between points.
        distance = self.finddistancebetweentwopoints(Point1,Point2)
        # X axis rotation is calculated.
        angles.append(degrees(arccos( (Point2[0]-Point1[0])/distance )))
        # Y axis rotation is calculated.
        angles.append(degrees(arccos( (Point2[1]-Point1[1])/distance )))
        # Z axis rotation is calculated.
        angles.append(degrees(arccos( (Point2[2]-Point1[2])/distance )))
        # Angles are returned.
        return angles
    def finddistancebetweentwopoints(self,Point1,Point2):
        # Function to find the distance between two points if there was a line intersecting at both of them.
        distancex = Point1[0]-Point2[0]
        distancey = Point1[1]-Point2[1]
        distancez = Point1[2]-Point2[2]
        distance  = sqrt(pow(distancex,2)+pow(distancey,2)+pow(distancez,2))
        return distance
    def createvector(self,(x0,y0,z0),(alpha,beta,gamma)):
        # Create a vector with the given points and angles in each direction
        point = array([[x0],[y0],[z0]])
        alpha = cos(radians(alpha))
        beta  = cos(radians(beta))
        gamma = cos(radians(gamma))
        # Cosines vector
        cosin = array([[alpha],[beta],[gamma]])
        return array([point,cosin])
    def CalculateIntersectionOfTwoVectors(self,vector1,vector2):
        A = array([[vector1[1][0][0], vector2[1][0][0] ],
                   [vector1[1][1][0], vector2[1][1][0] ],
#                   [vector1[1][2][0], vector2[1][2][0] ]
                  ])
        B = array([vector1[0][0]-vector2[0][0],
                   vector1[0][1]-vector2[0][1],
#                   vector1[0][2]-vector2[0][2]
                  ])
        # LU decomposition solution.
        distances = scipy.linalg.solve(A, B)
        # Point vector created.
        Point     = [] 
        # Intersection point at X axis.
        Point.append((vector1[0][0][0]-distances[0]*vector1[1][0][0])[0])
        # Intersection point at Y axis.
        Point.append((vector1[0][1][0]-distances[0]*vector1[1][1][0])[0])
        # Intersection point at Z axis.
        Point.append((vector1[0][2][0]-distances[0]*vector1[1][2][0])[0])
        return Point,distances
    def createvectorfromtwopoints(self,(x0,y0,z0),(x1,y1,z1)):
        # Create a vector from two given points
        point = array([[x0],[y0],[z0]])
        # Distance between two points
        s     = sqrt( pow((x0-x1),2) + pow((y0-y1),2) + pow((z0-z1),2) )
        alpha = (x1-x0)/s
        beta  = (y1-y0)/s
        gamma = (z1-z0)/s
        # Cosines vector
        cosin = array([[alpha],[beta],[gamma]])
        return array([point,cosin])
    def multiplytwovectors(self,vector1,vector2):
        # Multiply two vectors and return the resultant vector
        # Used method described under: 
        # Cross-product: http://en.wikipedia.org/wiki/Cross_product
        angle = cross(vector1[1].transpose()[0],vector2[1].transpose()[0])
        return array([vector1[0],[[angle[0]],[angle[1]],[angle[2]]]])
    def anglebetweentwovector(self,vector0,vector1):
        # Finds angle between two vectors
        # Used method described under: http://www.wikihow.com/Find-the-Angle-Between-Two-Vectors
        angle = vector0[1]*vector1[1]
        angle = angle[0]+angle[1]+angle[2]
        s1    = sqrt(vector0[1][0]**2+vector0[1][1]**2+vector0[1][2]**2)
        s2    = sqrt(vector1[1][0]**2+vector1[1][1]**2+vector1[1][2]**2)
        angle = degrees(arccos(angle/(s1*s2)))
        return angle
    def isitontriangle(self,pointtocheck,point0,point1,point2,error=0.1):
        # Check if the given point is insight the triangle which represented 
        # by three corners of the triangle.
        # Used method described under: http://www.blackpawn.com/texts/pointinpoly/default.html
        # point0, point1 and point2 are the corners of the triangle
        # point is the point to check
        vector1 = self.createvectorfromtwopoints(pointtocheck,point0)
        vector2 = self.createvectorfromtwopoints(pointtocheck,point1)
        vector3 = self.createvectorfromtwopoints(pointtocheck,point2)
        angle0  = self.anglebetweentwovector(vector1,vector2)
        angle1  = self.anglebetweentwovector(vector2,vector3)
        angle2  = self.anglebetweentwovector(vector3,vector1)
        sum     = angle0+angle1+angle2
        if sum <= 360+error and sum >= 360-error:
            return True
        else:
            return False
    def transform(self,input,(alpha,beta,gamma),(x0,y0,z0)):
        # alpha; rotation angle (euler) of x axis 
        # beta; rotation angle (euler) of y axis
        # gamma; rotation angle (euler) of z axis
        # x0; x coordinate of origin measured in the reference system
        # y0; y coordinate of origin measured in the reference system
        # z0; z coordinate of origin measured in the reference system
        alpha  = radians(alpha)
        beta   = radians(beta)
        gamma  = radians(gamma)
        R1     = array([[cos(gamma),-sin(gamma),0],[sin(gamma),cos(gamma),0],[0,0,1]])
        R2     = array([[1,0,0],[0,cos(beta),-sin(beta)],[0,sin(beta),cos(beta)]])
        R3     = array([[cos(alpha),0,-sin(alpha)],[0,1,0],[sin(alpha),0,cos(alpha)]])
        R      = dot(dot(R1,R2),R3)
        output = dot(R,input-array([[x0],[y0],[z0]]))
        return output
    def reflect(self,vector,normvector):
        # Used method described in G.H. Spencer and M.V.R.K. Murty, "General Ray-Tracing Procedure", 1961
        mu     = 1 
        div   = pow(normvector[1,0],2)  + pow(normvector[1,1],2) + pow(normvector[1,2],2)
        a     = mu* (vector[1,0]*normvector[1,0] + vector[1,1]*normvector[1,1] + vector[1,2]*normvector[1,2]) / div
        vector[0,0] = normvector[0,0]
        vector[0,1] = normvector[0,1]
        vector[0,2] = normvector[0,2]
        vector[1,0] = vector[1,0] - 2*a*normvector[1,0]
        vector[1,1] = vector[1,1] - 2*a*normvector[1,1]
        vector[1,2] = vector[1,2] - 2*a*normvector[1,2]
        return vector
    def snell(self,vector,normvector,n1,n2,error=0.01):
        # Method for Snell's law
        # n1 refractive index of the medium which vector is coming from
        # n2 refractive index of the medium which vector tries to go into
        mu    = n1/n2
        div   = pow(normvector[1,0],2)  + pow(normvector[1,1],2) + pow(normvector[1,2],2)
        a     = mu* (vector[1,0]*normvector[1,0] + vector[1,1]*normvector[1,1] + vector[1,2]*normvector[1,2]) / div
        b     = (pow(mu,2)-1) / div
        to    = -b*0.5/a
        num   = 0
        eps   = error*2
        # Newton-Raphson method to find the correct root
        while eps > error:
           num   += 1
           oldto  = to
           v      = pow(to,2) + 2*a*to + b
           deltav = 2*(to+a)
           to     = to - v /deltav
           eps    = abs(oldto-to)
           # Iteration notifier
           #print 'Iteration number: %s, Error: %s' % (num,error)
           # Iteration limiter
           if num > 5000:
              return vector
        vector[0,0] = normvector[0,0]
        vector[0,1] = normvector[0,1]
        vector[0,2] = normvector[0,2]
        vector[1,0] = mu*vector[1,0] + to*normvector[1,0]
        vector[1,1] = mu*vector[1,1] + to*normvector[1,1]
        vector[1,2] = mu*vector[1,2] + to*normvector[1,2]
        return vector
    def findinterspher(self,vector,sphere,error=0.00000001,numiter=1000,iternotify='no'):
        # Method for finding intersection in between a vector and a spherical surface
        # There are things to be done to fix wrong root convergence
        number   = 0
        distance = 1
        olddist  = 0
        shift    = 0
        epsilon  = error*2
        k        = vector[0,0,0]
        l        = vector[0,1,0]
        m        = vector[0,2,0]
        FXYZ     = pow(k-sphere[0],2) + pow(l-sphere[1],2) + pow(m-sphere[2],2) - pow(sphere[3],2)
        if abs(FXYZ) < 0.01:
            shift = 1.5 * sphere[3]
            k     = shift * vector[1,0] + k
            l     = shift * vector[1,1] + l
            m     = shift * vector[1,2] + m
        while epsilon > error:
            number  += 1
            x        = olddist * vector[1,0] + k
            y        = olddist * vector[1,1] + l
            z        = olddist * vector[1,2] + m
            oldFXYZ  = pow(x-sphere[0],2) + pow(y-sphere[1],2) + pow(z-sphere[2],2) - pow(sphere[3],2)
            x        = distance * vector[1,0] + k
            y        = distance * vector[1,1] + l
            z        = distance * vector[1,2] + m
            FXYZ     = pow(x-sphere[0],2) + pow(y-sphere[1],2) + pow(z-sphere[2],2) - pow(sphere[3],2)
            # Secant method is calculated, see wikipedia article of the method for more
            newdist  = distance - FXYZ*(distance-olddist)/(FXYZ-oldFXYZ)
            epsilon  = abs(newdist-distance)
            oldFXYZ  = FXYZ
            olddist  = distance
            distance = newdist
            normang  = array([[(sphere[0]-x)/sphere[3]],[(sphere[1]-y)/sphere[3]],[(sphere[2]-z)/sphere[3]]])
            normpnt  = array([x,y,z])
            normvec  = array([normpnt,normang])
            # Iteration reminder
            if iternotify == 'yes':
                print 'Iteration number: %s, Calculated distance: %s, Error: %s, Points: %s %s %s, Function:  %s' % (number,distance,epsilon,x,y,z,FXYZ)
            # Check if the number of iterations are too much
            if number > numiter:
               return 0,normvec        
        return distance+shift,normvec
    def findintersurface(self,vector,(point0,point1,point2),error=0.00001,numiter=100,iternotify='no'):
        # Method to find intersection point inbetween a surface and a vector
        # See http://www.jtaylor1142001.net/calcjat/Solutions/VPlanes/VP3Pts.htm
        vector1  = self.createvectorfromtwopoints(point0,point1)
        vector2  = self.createvectorfromtwopoints(point0,point2)
        normvec  = self.multiplytwovectors(vector1,vector2)
        k        = vector[0,0,0]
        l        = vector[0,1,0]
        m        = vector[0,2,0]
        # See http://en.wikipedia.org/wiki/Normal_%28geometry%29
        a           = normvec[1][0]
        b           = normvec[1][1]
        c           = normvec[1][2]
        d           = -normvec[1][0]*normvec[0][0]-normvec[1][1]*normvec[0][1]-normvec[1][2]*normvec[0][2]
        distance    = 1 
        number      = 0
        olddistance = 0
        epsilon     = error*2
        while epsilon > error:
            number     += 1
            x1          = distance * vector[1,0] + k
            y1          = distance * vector[1,1] + l
            z1          = distance * vector[1,2] + m
            x2          = olddistance * vector[1,0] + k
            y2          = olddistance * vector[1,1] + l
            z2          = olddistance * vector[1,2] + m
            F1          = a*x1+b*y1+c*z1+d
            F2          = a*x2+b*y2+c*z2+d
            # Secant method: http://en.wikipedia.org/wiki/Secant_method
            newdistance = distance - F1*(distance-olddistance)/(F1-F2)
            epsilon     = abs(distance-olddistance)
            olddistance = distance
            distance    = newdistance
            normvec[0]  = array([x1,y1,z2])
            # Iteration reminder
            if iternotify == 'yes':
                print 'Iteration number: %s, Calculated distance: %s, Error: %s, F1: %s, F2: %s, Old distance: %s ' % (number,distance,error,F1,F2,olddistance)
            if number > numiter:
               return 0,normvec
        return olddistance, normvec
    def plotvector(self,vector,distance,color='g'):
        # Method to plot rays
        x = array([vector[0,0,0], distance * vector[1,0] + vector[0,0,0]])
        y = array([vector[0,1,0], distance * vector[1,1] + vector[0,1,0]])
        z = array([vector[0,2,0], distance * vector[1,2] + vector[0,2,0]])
        self.ax.plot(x,y,z,color)
        return True
    def PlotPoint(self,point,color='g*'):
        # Method to plot a single spot.
        self.ax.plot(array([point[0]]),array([point[1]]),array([point[2]]),color)
        return True
    def plotsphericallens(self,cx=0,cy=0,cz=0,r=10,c='none'):
        # Method to plot surfaces
        sampleno = 100
        v        = linspace(0, pi, sampleno)
        u        = linspace(0,2*pi,sampleno)
        x        = r * outer(cos(u), sin(v)) + cx
        y        = r * outer(sin(u), sin(v)) + cy
        z        = r * outer(ones(size(u)), cos(v)) + cz
        self.ax.plot_surface(x, y, z, rstride=6, cstride=6, color=c)
        return array([cx,cy,cz,r])
    def CalculateFocal(self,rx,ry,rz,n):
        # Method to calculate the focal length of the lens in different axes.
        for a in [rx,ry]:
            R         = (pow(a,2)+pow(rz,2))/(2*rz)
            LensMaker = (n-1)*(-2/R+(n-1)*rz*2/(n*R))
            f         = pow(LensMaker,-1)
            print 'Focal length of the lens: ',f
        return True
    def plotasphericallens(self,cx=0,cy=0,cz=0,rx=10,ry=10,rz=10,n=1.51,c='none'):
        # Method to plot surfaces
        sampleno = 50
        v        = linspace(0, pi, sampleno)
        u        = linspace(0,2*pi,sampleno)
        x        = rx * outer(cos(u), sin(v)) + cx
        y        = ry * outer(sin(u), sin(v)) + cy
        z        = rz * outer(ones(size(u)), cos(v)) + cz
        self.ax.plot_surface(x, y, z, rstride=6, cstride=6, color=c)
        self.CalculateFocal(rx,ry,rz,n)
        return array([cx,cy,cz,rx,ry,rz])
    def plotcircle(self,center,r,c='none'):
        # Method to plot circle.
        circle = Circle((center[0], center[1]), r, facecolor=c, edgecolor=(0,0,0), linewidth=3, alpha=0.5)
        self.ax.add_patch(circle)
        art3d.pathpatch_2d_to_3d(circle, z=center[2], zdir='z')
        return array([center,r]) 
    def plottriangle(self,point0,point1,point2):
        # Method to plot triangular surface
        x = array([ point0[0], point1[0], point2[0]])
        y = array([ point0[1], point1[1], point2[1]])
        z = array([ point0[2], point1[2], point2[2]])
        verts = [zip(x, y,z)]
        self.ax.add_collection3d(Poly3DCollection(verts))
        return array([point0,point1,point2])
    def plotcornercube(self,centerx,centery,centerz,pitch,revert=False):
        # Method to plot a single cornercube
        point00 = array([ centerx, centery, centerz])
        point10 = array([ centerx, centery, centerz])
        point20 = array([ centerx, centery, centerz])
        if revert == False:
            point01 = array([ centerx, centery-2*pitch/3, centerz+sqrt(2)*pitch/3 ])
            point11 = array([ centerx, centery-2*pitch/3, centerz+sqrt(2)*pitch/3 ])
            point21 = array([ centerx-pitch/sqrt(3), centery+pitch/3, centerz+sqrt(2)*pitch/3 ])
            point02 = array([ centerx-pitch/sqrt(3), centery+pitch/3, centerz+sqrt(2)*pitch/3 ])
            point12 = array([ centerx+pitch/sqrt(3), centery+pitch/3, centerz+sqrt(2)*pitch/3 ])
            point22 = array([ centerx+pitch/sqrt(3), centery+pitch/3, centerz+sqrt(2)*pitch/3 ])
        else:
            point01 = array([ centerx, centery+2*pitch/3, centerz+sqrt(2)*pitch/3 ])
            point11 = array([ centerx, centery+2*pitch/3, centerz+sqrt(2)*pitch/3 ]) 
            point21 = array([ centerx+pitch/sqrt(3), centery-pitch/3, centerz+sqrt(2)*pitch/3 ])
            point02 = array([ centerx+pitch/sqrt(3), centery-pitch/3, centerz+sqrt(2)*pitch/3 ])
            point12 = array([ centerx-pitch/sqrt(3), centery-pitch/3, centerz+sqrt(2)*pitch/3 ])
            point22 = array([ centerx-pitch/sqrt(3), centery-pitch/3, centerz+sqrt(2)*pitch/3 ])
        self.plottriangle(point00,point01,point02)
        self.plottriangle(point10,point11,point12)
        self.plottriangle(point20,point21,point22)
        return array([point00,point01,point02]),array([point10,point11,point12]),array([point20,point21,point22])
    def defineplotshape(self,(xmin,xmax),(ymin,ymax),(zmin,zmax)):
        self.ax.set_xlim3d(xmin,xmax)
        self.ax.set_ylim3d(ymin,ymax)
        self.ax.set_zlim3d(zmin,zmax)
        return True
    def showplot(self,title='Ray tracing'):
        # Shows the prepared plot
        plt.title(title)
        plt.show()
        return True

class jonescalculus():
    def __init__(self):
        return
    def linearpolarizer(self,input,rotation=0):
        # Linear polarizer, rotation is in degrees and it is counter clockwise
        rotation        = radians(rotation)
        rotmat          = array([[cos(rotation),sin(rotation)],[-sin(rotation),cos(rotation)]])
        linearpolarizer = array([[1,0],[0,0]])
        linearpolarizer = dot(rotmat.transpose(),dot(linearpolarizer,rotmat))
        return dot(linearpolarizer,input)
    def circullarpolarizer(self,input,type='lefthanded'):
        # Circullar polarizer
        if type == 'lefthanded':
            circullarpolarizer = array([[0.5,-0.5j],[0.5j,0.5]])
        if type == 'righthanded':
            circullarpolarizer = array([[0.5,0.5j],[-0.5j,0.5]])
        return dot(circullarpolarizer,input)
    def quarterwaveplate(self,input,rotation=0):
        # Quarter wave plate, type determines the placing of the fast axis
        rotation = radians(rotation)
        rotmat   = array([[cos(rotation),sin(rotation)],[-sin(rotation),cos(rotation)]])
        qwp = array([[1,0],[0,-1j]])
        qwp = dot(rotmat.transpose(),dot(qwp,rotmat))        
        return dot(qwp,input)
    def halfwaveplate(self,input,rotation=0):
        # Half wave plate
        rotation = radians(rotation)
        rotmat   = array([[cos(rotation),sin(rotation)],[-sin(rotation),cos(rotation)]])
        hwp      = array([[1,0],[0,-1]])
        hwp      = dot(rotmat.transpose(),dot(hwp,rotmat))
        return dot(hwp,input)
    def birefringentplate(self,input,nx,ny,d,wavelength,rotation=0):
        # Birefringent plate, d thickness, nx and ny refractive indices
        rotation = radians(rotation)
        rotmat   = array([[cos(rotation),sin(rotation)],[-sin(rotation),cos(rotation)]])
        delta    = 2*pi*(nx-ny)*d/wavelength
        bfp      = array([[1,0],[0,exp(-1j*delta)]])
        bfp      = dot(rotmat.transpose(),dot(bfp,rotmat))
        return dot(bfp,input)
    def nematicliquidcrystal(self,input,alpha,ne,n0,d,wavelength,rotation=0):
        # Nematic liquid crystal, d cell thickness, extraordinary refrative index ne, ordinary refractive index n0,
        # alpha helical twist per meter in right-hand sense along the direction of wave propagation
        # alpha is calculated is by dividing cell thickness to 1 meter length
        # alpha    =  1 /d
        rotation = radians(rotation)
        rotmat   = array([[cos(rotation),sin(rotation)],[-sin(rotation),cos(rotation)]])
        beta     = 2*pi*(ne-n0)/wavelength
        lrot     = array([[cos(alpha*d),-sin(alpha*d)],[sin(alpha*d),cos(alpha*d)]])
        lretard  = array([[1,0],[0,exp(-1j*beta*d)]])
        lc       = dot(lrot,lretard)
        lc       = dot(rotmat.transpose(),dot(lc,rotmat))
        return dot(lc,input)
    def ferroliquidcrystal(self,input,tetat,ne,n0,d,wavelength,fieldsign='+',rotation=0):
        # Ferroelectric liquid crystal, d cell thickness, extraordinary refrative index ne, ordinary refractive index n0
        # Applied field sign determines the rotation angle
        rotation = radians(rotation)
        tetat    = radians(tetat)
        rotmat   = array([[cos(rotation),sin(rotation)],[-sin(rotation),cos(rotation)]])
        beta     = 2*pi*(ne-n0)/wavelength
        lrot1    = array([[cos(tetat),-sin(tetat)],[sin(tetat),cos(tetat)]])
        lrot2    = array([[cos(tetat),sin(tetat)],[-sin(tetat),cos(tetat)]])
        lretard  = array([[1,0],[0,exp(-1j*beta*d)]])
        if fieldsign == '+':
            lc = dot(dot(lrot1,lretard),lrot2)
        elif fieldsign == '-':
            lc = dot(dot(lrot2,lretard),lrot1)    
        lc       = dot(rotmat.transpose(),dot(lc,rotmat))
        return dot(lc,input)
    def electricfield(self,a1,a2):        
        return array([[a1],[a2]])

class aperture():
    def __init__(self):
        return
    def twoslits(self,nx,ny,X,Y,delta):
        # Creates a matrix that contains two slits
        obj=zeros((nx,ny),dtype=complex)
        for i in range(int(nx/2-X/2),int(nx/2+X/2)):
            for j in range(int(ny/2+delta/2-Y/2),int(ny/2+delta/2+Y/2)):
                obj[ny/2-abs(ny/2-j),i] = 1
                obj[j,i] = 1      
        return obj
    def rectangle(self,nx,ny,side):
        # Creates a matrix that contains rectangle
        obj=zeros((nx,ny),dtype=complex)
        for i in range(int(nx/2-side/2),int(nx/2+side/2)):
            for j in range(int(ny/2-side/2),int(ny/2+side/2)):
                obj[j,i] = 1 
        return obj
    def circle(self,nx,ny,radius):
        # Creates a matrix that contains circle
        obj=zeros((nx,ny),dtype=complex)
        for i in range(int(nx/2-radius/2),int(nx/2+radius/2)):
            for j in range(int(ny/2-radius/2),int(ny/2+radius/2)):
                if (abs(i-nx/2)**2+abs(j-ny/2)**2)**(0.5)< radius/2:
                    obj[j,i] = 1 
        return obj
    def sinamgrating(self,nx,ny,grating):
        # Creates a sinuosidal grating matrix
        obj=zeros((nx,ny),dtype=complex)
        for i in xrange(nx):
            for j in xrange(ny):
                obj[i,j] = 0.5+0.5*cos(2*pi*j/grating)
        return obj
    def lens(self,nx,ny,focal,wavelength):
        # Creates a lens matrix
        obj = zeros((nx,ny),dtype=complex)
        k   = 2*pi/wavelength
        for i in xrange(nx):
            for j in xrange(ny):
                obj[i,j] = exp(-1j*k*(pow(i,2)+pow(j,2))/2/focal)    
        return obj
    def gaussian(self,nx,ny,sigma):
        # Creates a 2D gaussian matrix
        obj = zeros((nx,ny),dtype=complex)
        for i in xrange(nx):
            for j in xrange(ny):   
                obj[i,j] = 1/pi/pow(sigma,2)*exp(-float(pow(i-nx/2,2)+pow(j-ny/2,2))/2/pow(sigma,2))
        return obj
    def retroreflector(self,nx,ny,wavelength,pitch,type='normal'):
        if nx != ny:
           nx = max([nx,ny])
           ny = nx
        part  = zeros((pitch,int(pitch/2)))
        for i in xrange(int(sqrt(3)*pitch/6)):
            for j in xrange(int(pitch/2)):
                if float(j)/(int(sqrt(3)*pitch/6)-i) < sqrt(3): 
                    part[i,j]       = int(sqrt(3)*pitch/6)-i
                    part[pitch-i-1,int(pitch/2)-j-1] = part[i,j]
        for i in xrange(int(pitch)):
            for j in xrange(int(pitch/2)):
                if j != 0:
                    if float(j)/(int(pitch)-i) < 0.5 and (int(sqrt(3)*pitch/6)-i)/float(j) < 1./sqrt(3):
                        # Distance to plane determines the level of the amplitude 
                        # Plane as a line y = slope*x+ pitch 
                        # Perpendicula line  y = -(1/slope)*x+n
                        slope     = -0.5
                        n         = j + (1/slope) * (i)
                        x1        = (n - pitch/2)/(slope+1/slope)
                        y1        = -(1/slope)*x1+n 
                        part[i,j] = int(sqrt(3)*pitch/6) - sqrt( pow(i-x1,2) + pow(j-y1,2) )
                        part[pitch-i-1,int(pitch/2)-j-1] = part[i,j]
                else:
                    if i > int(sqrt(3)*pitch/6):
                        slope     = -0.5
                        n         = j + (1/slope) * (i)
                        x1        = (n - pitch/2)/(slope+1/slope)
                        y1        = -(1/slope)*x1+n
                        part[i,j] = int(sqrt(3)*pitch/6) - sqrt( pow(i-x1,2) + pow(j-y1,2) )
                        part[pitch-i-1,int(pitch/2)-j-1] = part[i,j]
        left  = part
        right = part[::-1]
        part  = append(left,right,axis=1)
        obj   = tile(part,(nx/pitch,ny/pitch))
        for i in xrange(nx/pitch/2):
           obj[(2*i+1)*pitch:(2*i+1)*pitch+pitch,:] = roll(obj[(2*i+1)*pitch:(2*i+1)*pitch+pitch,:],pitch/2)    
        k     = 2*pi/wavelength
        D     = 5
        obj   = pow(obj,3)*exp(1j*k*obj)
        return obj
    def show(self,obj,pixeltom,wavelength,title='Detector',type='normal',filename=None,xlabel=None,ylabel=None):
        # Plots a detector showing the given object
        plt.figure(),plt.title(title)
        nx,ny = obj.shape
        # Number of the ticks to be shown both in x and y axes
        if type == 'normal':
            obj = abs(obj)
        elif type == 'log':
            obj = log(abs(obj))
        img = plt.imshow(obj,cmap=matplotlib.cm.jet,origin='lower')
        plt.colorbar(img,orientation='vertical')
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        if filename != None:
            plt.savefig(filename)
        plt.show()
        return True
    def show3d(self,obj):
        nx,ny   = obj.shape
        fig     = plt.figure()
        ax      = fig.gca(projection='3d')
        X,Y     = mgrid[0:nx,0:ny]
        surf    = ax.plot_surface(X,Y,abs(obj), rstride=1, cstride=1, cmap=matplotlib.cm.jet,linewidth=0, antialiased=False)
        fig.colorbar(surf, shrink=0.5, aspect=5)
        plt.show()
        return True
    def showrow(self,obj,wavelength,pixeltom,distance):
        # Plots row crosssection of the given object
        nx,ny = obj.shape
        a     = 5
        plt.figure()
        plt.plot(arange(-nx/2,nx/2)*pixeltom,abs(obj[nx/2,:]))
        plt.show()
        return True

class beams():
    def __init(self):
        return
    def spherical(self,nx,ny,distance,wavelength,pixeltom,focal,amplitude=1):
        # Spherical wave
        distance = abs(focal-distance)
        k        = 2*pi/wavelength
        X,Y      = mgrid[-nx/2:nx/2,-ny/2:ny/2]*pixeltom
        r        = sqrt(pow(X,2)+pow(Y,2)+pow(distance,2)) 
        U        = amplitude/r*exp(-1j*k*r)
        return U
    def gaussian(self,nx,ny,distance,wavelength,pixeltom,amplitude,waistsize,focal=0):
        # Gaussian beam
        distance = abs(distance-focal)
        X,Y      = mgrid[-nx/2:nx/2,-ny/2:ny/2]*pixeltom
        ro       = sqrt(pow(X,2)+pow(Y,2))
        z0       = pow(waistsize,2)*pi/wavelength
        A0       = amplitude/(1j*z0)
        if distance == 0:
            U = A0*exp(-pow(ro,2)/pow(waistsize,2))
            return U
        k        = 2*pi/wavelength
        R        = distance*(1+pow(z0/distance,2))
        W        = waistsize*sqrt(1+pow(distance/z0,2))
        ksi      = 1./arctan(distance/z0)
        U        = A0*waistsize/W*exp(-pow(ro,2)/pow(W,2))*exp(-1j*k*distance-1j*pow(ro,2)/2/R+1j*ksi)
        return U

class diffractions():
    def __init__(self):
        return
    def fft(self,obj):
        return fftshift(fft2(obj))
    def fresnelfraunhofer(self,wave,wavelength,distance,pixeltom,aperturesize):
        nu,nv  = wave.shape
        k      = 2*pi/wavelength
        X,Y    = mgrid[-nu/2:nu/2,-nv/2:nv/2]*pixeltom
        Z      = pow(X,2)+pow(Y,2)
        distancecritical = pow(aperturesize*pixeltom,2)*2/wavelength
        print 'Critical distance of the system is %s m. Distance of the detector is %s m.' % (distancecritical,distance)
        # Convolution kernel for free space
        h      = exp(1j*k*distance)/sqrt(1j*wavelength*distance)*exp(1j*k*0.5/distance*Z)
        qpf    = exp(-1j*k*0.5/distance*Z)
        if distancecritical < distance:
            wave = wave*qpf
        result = fftshift(ifft2(fft2(wave)*fft2(h)))
        return result
    def fresnelnumber(self,aperturesize,pixeltom,wavelength,distance):
        return  pow(aperturesize*pixeltom,2)/wavelength/distance
    def intensity(self,obj,pixeltom):
        return abs(pow(obj,2))*pow(pixeltom,2)*0.5*8.854*pow(10,-12)*299792458

def main():
    print 'Odak by %s' % __author__
    return True

if __name__ == '__main__':
    sys.exit(main())
