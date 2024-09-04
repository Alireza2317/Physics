import sys
import pygame as pg
import pymunk as pm
import pymunk.pygame_util as pgutil
from math import sin, cos


WIDTH = 1500
HEIGHT = 900
FPS = 120

MASS = 20
BG_COLOR = '#212121'


class Ball:
	"""
	Creates a ball, and holds many attributes like body, shape and mass and other physical properties.
	And also graphical properties like size(radius) and color
	"""
	def __init__(
			self, 
			space: pm.Space, 
			pos: tuple[int, int],
			color: str | tuple[int, int, int] | pg.Color,
			mass: int = MASS,
			body_type = pm.Body.DYNAMIC
	) -> None:

		self.body = pm.Body(mass=mass, body_type=body_type)
		self.body.position = pos
		
		radius = mass
		self.body.moment = pm.moment_for_circle(mass, inner_radius=0, outer_radius=radius)
		self.shape = pm.Circle(self.body, radius=radius)
		self.shape.color = color

		self.shape.density = 1
		self.shape.elasticity = 0.9
		
		space.add(self.body, self.shape)



class Rod:
	"""
	Creates a rod, connecting two given bodies(or a given body and a coordinate in space)
	Using a PinJoint
	"""
	def __init__(
			self, 
			space: pm.Space, 
			body1: pm.Body,
			body2: pm.Body | tuple[int, int], # a body or a coordinate
	) -> None:
		self.body1 = body1

		
		if isinstance(body2, pm.Body):
			self.body2 = body2
		else:
			self.body2 = space.static_body
			# using body2 as the position
			self.body2.position = body2

		self.joint = pm.PinJoint(self.body1, self.body2)

		space.add(self.joint)

	


class Pendulum:
	def __init__(
			self, 
			space: pm.Space, 
			*, 
			length: int,
			theta: float,
			ball_color: tuple[int, int, int, int], 
			ball_mass: int,
			piv_pos: tuple
	) -> None:
		"""
		Creates pendulum, based on length and angle theta(degrees), ball color and pivot point coordinate
		"""
		theta = theta / 180 * 3.1415
		ball_pos = length * sin(theta), length * cos(theta)
		self.ball = Ball(space, pos=ball_pos, color=ball_color, mass=ball_mass)
		self.rod = Rod(space, body1=self.ball.body, body2=piv_pos)




class PendulumSimulation:
	def __init__(self) -> None:
		self.space = pm.Space()
		self.screen = pg.display.set_mode((WIDTH, HEIGHT))
		self.options = pgutil.DrawOptions(self.screen)
		rod_color = (255,255,255, 255)
		self.options._use_chipmunk_debug_draw = 1
		self.options.constraint_color = rod_color
		self.clock = pg.time.Clock()
		self.config()

		#self.pendulum = Pendulum(
		#	self.space,
		#	ball_pos=(WIDTH//15, HEIGHT//6),
		#	piv_pos=(WIDTH//2, 50),
		#	ball_mass=200,
		#	ball_color=(255,255,0,255),
		#	rod_color=rod_color,
		#	ball_radius=60
		#)
		
	def config(self):
		pg.display.set_caption('Pendulum Simulation')
		self.fps = FPS
		self.space.gravity = (0, 1300)
		self.space.damping = 1



	def step(self):
		for event in pg.event.get():
			if event.type == pg.QUIT:
				pg.quit()
				sys.exit()
		
		self.screen.fill(BG_COLOR)
		
		self.space.debug_draw(self.options)
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