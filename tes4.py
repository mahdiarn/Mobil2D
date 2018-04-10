import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from math import *

vertices = (
	(0, 1, 1),
	(2, 1, 1),
	(3, 2, 1),
	(5, 2, 1),
	(6, 1, 1),
	(7, 1, 1),
	(8, 2, 1),
	(10, 2, 1),
	(11, 1, 1),
	(12, 1, 1),
	(12, 3, 1),
	(11, 4, 1),
	(10, 4, 1),
	(9, 5, 1),
	(4, 5, 1),
	(3, 4, 1),
	(1, 4, 1),
	(0, 3, 1),)
edges = (
	(0, 1),
	(1, 2),
	(2, 3),
	(3, 4),
	(4, 5),
	(5, 6),
	(6, 7),
	(7, 8),
	(8, 9),
	(9, 10),
	(10, 11),
	(11, 12),
	(12, 13),
	(13, 14),
	(14, 15),
	(15, 16),
	(16,17),
	(17,0),
	)

verticesColor = (
(0, 1, 1),
(2, 1, 1),
(2, 3, 1),
(0, 3, 1),
(3, 4, 1),
(1, 4, 1),
(11, 3, 1),
(9, 5, 1),
(4, 5, 1),
(3, 3, 1),
(3, 2, 1),
(10, 3, 1),
(10, 2, 1),
(11, 1, 1),
(12, 1, 1),
(12, 3, 1),
(11, 4, 1),
(10, 4, 1),
(5, 2, 1),
(6, 1, 1),
(7, 1, 1),
(8, 2, 1),
)
surfaces = (
	(0, 1, 2, 3),
	(2, 4, 5, 3),
	(2, 6, 7, 8),
	(2, 9, 10, 1),
	(9, 11, 12, 10),
	(11, 6, 13, 12),
	(6, 13, 14, 15),
	(6, 15, 16, 17),
	(18, 19, 20, 21),
	)

def drawCircle(radius,sides,posx,posy):

	glBegin(GL_POLYGON)
	for i in range(100):
		if ((i) % 4 >= 3) :
			cosine = radius * cos (i*2*pi/sides) + posx
			sine = radius * sin(i*2*pi/sides) + posy
			glVertex2f(cosine, sine)
	glEnd()

def drawCarBody():
	global surfaces
	global verticesColor
	glBegin(GL_QUADS)
	for surface in surfaces:
		for vertex in surface:
			glColor3fv((0, 0, 1))
			glVertex3fv(verticesColor[vertex])
	glEnd()

def drawCarOutline():
	global surfaces
	global verticesColor
	glBegin(GL_LINES)
	for edge in edges:
		for vertex in edge:
			glColor3fv((1, 0, 0))
			glVertex3fv(vertices[vertex])
	glEnd()

def CarBody(time):

	drawCarBody()
	drawCarOutline()

def main():
	pygame.init()
	display = (800, 600)
	pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
	gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)
	glTranslatef(-5.0, -5.0, -20.0)
	x = 0
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
		#glRotatef(1,3,1,1)
		glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
		#glRotatef(0, 0, 0, 0)
		glPushMatrix()
		CarBody(x)
		glColor3fv((1, 1, 1))
		glTranslatef(4, 0.8, -1.0)
		glRotatef(x*20, 0, 0, 1)
		radius,sides,posx, posy = 0.9,32,4,0.8
		glTranslatef(posx * -1, posy * -1, 1.0)
		drawCircle(radius,sides,posx,posy)
		glPopMatrix()
		glPushMatrix()
		posx, posy = 9.2,0.8
		glTranslatef(posx, posy, -1.0)
		glRotatef(x*20, 0, 0, 1)
		glTranslatef(posx * -1, posy * -1, 1.0)
		
		drawCircle(radius,sides,posx,posy)
		glPopMatrix()
		x+=1
		pygame.display.flip()
		pygame.time.wait(100)
main()
