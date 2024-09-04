import sys
import pygame as pg
import pymunk as pm
import pymunk.pygame_util as pgutil
from math import sin, cos


WIDTH = 900
HEIGHT = 800
FPS = 120

MASS = 60
BG_COLOR = '#212121'
BALL_COLOR = (220, 180, 0, 255)


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
		
		radius = mass / 2
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

	
class DoublePendulum:
	def __init__(
			self, 
			space: pm.Space, 
			*, 
			piv_pos: tuple,
			length1: int,
			theta1: float,
			length2: int,
			theta2: float,
			ball_color: tuple[int, int, int, int] 
	) -> None:
		"""
		Creates pendulum, based on length and angle theta(degrees), ball color and pivot point coordinate
		piv_pos, is based on positive y-axis going down
		"""
		piv_pos = piv_pos[0], HEIGHT - piv_pos[1]
		theta1 = theta1 / 180 * 3.1415
		theta2 = theta2 / 180 * 3.1415

		ball1_pos = piv_pos[0] -  length1 * sin(theta1), piv_pos[1] -  length1 * cos(theta1)
		ball2_pos = ball1_pos[0] -  length2 * sin(theta2), ball1_pos[1] -  length2 * cos(theta2)


		self.ball1 = Ball(space, pos=ball1_pos, color=ball_color)
		self.ball2 = Ball(space, pos=ball2_pos, color=ball_color)

		self.rod1 = Rod(space, body1=self.ball1.body, body2=piv_pos)
		self.rod2 = Rod(space, body1=self.ball1.body, body2=self.ball2.body)


class Simulation:
	def __init__(self) -> None:
		# pymunk settings
		self.space = pm.Space()
		self.space.gravity = (0, -1500)
		self.space.damping = 0.93
		
		# pygame settings
		self.screen = pg.display.set_mode((WIDTH, HEIGHT))
		pg.display.set_caption('Pendulum Simulation')
		self.clock = pg.time.Clock()
		self.fps = FPS

		# pymunk and pygame integration
		self.options = pgutil.DrawOptions(self.screen)
		pgutil.positive_y_is_up = True

		rod_color = (255, 255, 255, 255)
		self.options.constraint_color = rod_color
		

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



if __name__ == '__main__':
	sim = Simulation()
	DoublePendulum(sim.space, piv_pos=(1*WIDTH//2, 50), length1=300, theta1=0, length2=150, theta2=15, ball_color=BALL_COLOR)

	while True:
		sim.step()
		