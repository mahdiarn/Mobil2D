#!/usr/bin/python
import random
import math
import json

from OpenGL.GL import *
from OpenGL.GLUT import *


class Utils2():
	def __init__(self):
		try:
			fp = open('./config2.json')
			self.params = json.load(fp)
		except:
			logging.exception("no config2.json")

	@property
	def config(self):
		return self.params

	@staticmethod
	def getRadians(x):
		return math.pi/180.0 * x

particleList = []
utils = Utils2()
params = utils.config


class Particle2(object):
	def __init__(self,x,y,z,vx,vy,vz,color,size):
		self.x = x	
		self.y = y		
		self.z = z
		self.vx = vx		
		self.vy = vy
		self.vz = vz

		self.age= 0		
		self.max_age=params['maxAge']

		self.wind = -20
		self.size = size	
		
		self.color=color
		self.is_dead = False

	def update(self,dx=0.05,dy=0.1,dz=0.05):
		#self.vx -= dx* self.wind 
		self.vz += dy* self.wind * -1

		#self.vx *= 1- params['dragFactor']/1000
		self.vz *= 1.098

		self.x += self.vx
		self.y += self.vy
		self.z += self.vz
		self.check_particle_age()		

	def draw(self):
		glColor4fv(self.color)
		glTexCoord2f(0.0, 0.25)
		glPushMatrix()
		glTranslatef(self.x,self.y,self.z)
		glutSolidSphere(self.size,20,20)
		glPopMatrix()
		glutPostRedisplay()

	def check_particle_age(self):		
		self.age +=1 
		self.is_dead = self.age >= self.max_age	

		#self.color[3]= 1.0 - float(self.age)/float(self.max_age)

class ParticleBurst2(Particle2):	
	def __init__(self,x,y,z,vx,vy,vz):
		color = params['launchColor']
		size = params['launchSize']		
		Particle2.__init__(self,x,y,z,vx,vy,vz,color,size)
		self.wind=1				

	def check_particle_age(self):
		
		self.age += 1
		
		if self.age > 140:
			self.is_dead = True			

class ParticleSystem2():
	def __init__(self):		
		self.x = round(random.uniform(-20.0,20.0),2)
		self.y = round(random.uniform(-3.0,3.0),2)
		self.z = 5
		self.timer = 0
		print self.x
		print self.y
		self.addParticle()

	def addParticle(self):
		speed = params['particleSpeed']
		angle = 270*3.14/180 + round(random.uniform(-0.5,0.5),2)
		vx = 0
		vz = 0
		vy = 0
		
		f = ParticleBurst2(self.x,self.y,self.z,vx,vy,vz )			
		particleList.append(f)

	def update(self):
		interval = params['launchIterval']
		self.timer += 1
		self.x = round(random.uniform(-20,20),2)
		self.y = round(random.uniform(-3,3),2)
		if self.timer % interval == 0 or self.timer < 2:		
			self.addParticle()
		
		for i in range(len(particleList)-1,0,-1):
			p = particleList[i]
			x = params['windX']
			y = params['windX']
			z = 100
			p.update(x,y,z)
			p.check_particle_age()			
			if p.is_dead:					
				p.color = [0.0,0.0,0.0,0.0]				
				particleList.pop(i)				
			else:
				p.draw()
