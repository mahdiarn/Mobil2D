import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from math import *

vertices = (
	(0, 1, 1),
	(3, 1, 1),
	(3, 2, 1),
	(5, 2, 1),
	(5, 1, 1),
	(7, 1, 1),
	(7, 2, 1),
	(9, 2, 1),
	(9, 1, 1),
	(11, 1, 1),
	(11, 4, 1),
	(10, 4, 1),
	(10, 7, 1),
	(3, 7, 1), 
	(3, 4, 1),
	(0, 4, 1))
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
	(0, 15)
	)
surfaces = (
	(0, 1, 14, 15),
	(2, 7, 12, 13),
	(8, 9, 10, 11),
	(3, 4, 5, 6))

def CarBody(time):

	glBegin(GL_LINES)
	for edge in edges:
		for vertex in edge:
			glVertex3fv(vertices[vertex])
	glEnd()
	glBegin(GL_QUADS)
	for surface in surfaces:
		for vertex in surface:
			glColor3fv((1, 0, 0))
			glVertex3fv(vertices[vertex])
	glEnd()
	radius = 0.9
	sides = 32
	posx, posy = 3.9,1
	glBegin(GL_POLYGON)
	for i in range(100):
		if ((i + time) % 4 >= 2) :
			cosine = radius * cos (i*2*pi/sides) + posx
			sine = radius * sin(i*2*pi/sides) + posy
			glVertex2f(cosine, sine)
	glEnd()

	posx, posy = 8.2,1
	glBegin(GL_POLYGON)
	for i in range(100):
		if ((i + time) % 4 >= 2) :
			cosine = radius * cos (i*2*pi/sides) + posx
			sine = radius * sin(i*2*pi/sides) + posy
			glVertex2f(cosine, sine)
	glEnd()

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
		CarBody(x)
		x+=1
		pygame.display.flip()
		pygame.time.wait(100)
main()
