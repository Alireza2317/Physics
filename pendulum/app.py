import sys
import pygame as pg
import pymunk as pm
from math import sin, cos

WIDTH = 1500
HEIGHT = 900
FPS = 120

BALL_SIZE = 20
MASS = 200

class Ball:
	def __init__(
			self, 
			space: pm.Space, 
			pos: tuple[int, int], 
			radius: int = BALL_SIZE, 
			body_type = pm.Body.DYNAMIC
	) -> None:
		self.body = pm.Body(mass=MASS, body_type=body_type)
		self.body.position = pos
		self.shape = pm.Circle(self.body, radius)
		self.shape.density = 1
		self.shape.elasticity = 1
		self.radius = radius

		space.add(self.body, self.shape)


class Rod:
	def __init__(
			self, 
			space: pm.Space, 
			body: pm.Body,
			attachment: pm.Body | tuple[int, int]
	) -> None:
		self.body = body

		if isinstance(attachment, tuple):
			self.body2 = pm.Body(body_type=pm.Body.STATIC)
			self.body2.position = attachment
		else:
			self.body2 = attachment

		self.joint = pm.PinJoint(self.body, self.body2)

		space.add(self.joint)



class Pendulum:
	def __init__(self, space: pm.Space, piv_point_pos: tuple[int, int], mass: int = 1, length: int = 1, theta: float = 0) -> None:
		pos = length * sin(theta), length * cos(theta)
		self.ball = Ball(space, pos=pos, radius=mass*10)
		self.rod = Rod(space, self.ball.body, attachment=piv_point_pos)
	
	

	

class PendulumSimulation:
	def __init__(self) -> None:
		self.space = pm.Space()
		self.screen = pg.display.set_mode((WIDTH, HEIGHT))
		self.clock = pg.time.Clock()
		self.config()

		self.pendulum = Pendulum(self.space, piv_point_pos=(WIDTH/2, 100), mass=2.5, length=1, theta=0.2)
		

	def draw(self):
		conv_pos = lambda pos: (int(pos[0]), int(pos[1]))
		
		pos1 = conv_pos(self.pendulum.rod.body.position)
		pos2 = conv_pos(self.pendulum.rod.body2.position)
		pg.draw.line(self.screen, (220, 220, 220), pos1, pos2, width=5)	
		
		pg.draw.circle(self.screen, color=(200, 200, 0), radius=self.pendulum.ball.radius, center=conv_pos(self.pendulum.ball.body.position))





	def config(self):
		pg.display.set_caption('Pendulum Simulation')
		self.screen.fill('#212121')
		self.fps = FPS
		self.space.gravity = (0, 1300)
		self.space.damping = 1


	def step(self):
		for event in pg.event.get():
			if event.type == pg.QUIT:
				pg.quit()
				sys.exit()
		
		self.screen.fill('#212121')
		self.draw()
		pg.display.update()
		self.clock.tick(self.fps)
		self.space.step(1/self.fps)

		return False



if __name__ == '__main__':
	simulation = PendulumSimulation()
	while True:
		done = simulation.step()
		
		if done:
			break