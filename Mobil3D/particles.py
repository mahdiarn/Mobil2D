#!/usr/bin/python
import random
import math
import json

from OpenGL.GL import *
from OpenGL.GLUT import *


class Utils():
	def __init__(self):
		try:
			fp = open('./config.json')
			self.params = json.load(fp)
		except:
			logging.exception("no config.json")

	@property
	def config(self):
		return self.params

	@staticmethod
	def getRadians(x):
		return math.pi/180.0 * x

particleList = []
utils = Utils()
params = utils.config


class Particle(object):
	def __init__(self,x,y,z,vx,vy,vz,color,size):
		self.x = x	
		self.y = y		
		self.z = z
		self.vx = vx		
		self.vy = vy
		self.vz = vz

		self.age= 0		
		self.max_age=params['maxAge']

		self.wind = 0.1
		self.size = size	
		
		self.color=color
		self.is_dead = False

	def update(self,dx=0.05,dy=0.05,dz=0.05):
		self.vx -= dx* self.wind 
		self.vy += dy* self.wind * -1

		self.vx *= 1- params['dragFactor']/1000
		self.vy *= 1- params['dragFactor']/1000

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

		self.color[3]= 1.0 - float(self.age)/float(self.max_age)

class ParticleBurst(Particle):	
	def __init__(self,x,y,z,vx,vy,vz):
		color = params['launchColor']
		size = params['launchSize']		
		Particle.__init__(self,x,y,z,vx,vy,vz,color,size)
		self.wind=1				

	def check_particle_age(self):
		
		if self.vy <0:
			self.age += 1

		temp = int ( 100*  random.random()) + params['particleVariation']
		
		if self.age > temp:
			self.is_dead = True			

class ParticleSystem():
	def __init__(self):		
		self.x = params['initPosX']
		self.y = params['initPosY']
		self.z = params['initPosZ']
		self.timer = 0
		self.addParticle()

	def addParticle(self):
		speed = params['particleSpeed']
		speed *= (1 - random.uniform(0,params['particleVariation'])/100)
		angle = 270*3.14/180 + round(random.uniform(-0.5,0.5),2)
		vx = speed * math.cos(angle) 
		vz = speed
		vy = speed * math.cos(angle) 
		
		f = ParticleBurst(-3.1,0,-2,vx,vy,vz )			
		particleList.append(f)

	def update(self):
		interval = params['launchIterval']
		self.timer += 1

		if self.timer % interval == 0 or self.timer < 2:		
			self.addParticle()
		
		for i in range(len(particleList)-1,0,-1):
			p = particleList[i]
			x = params['windX']
			y = params['windY']						
			z = params['windZ']
			p.update(x,y,z)
			p.check_particle_age()			
			if p.is_dead:					
				p.color = [0.0,0.0,0.0,0.0]				
				particleList.pop(i)				
			else:
				p.draw()