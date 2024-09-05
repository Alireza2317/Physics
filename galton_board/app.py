import math
import sys
import pygame as pg
import pymunk as pm
#import pymunk.pygame_util as pgutil
#pgutil.to_pygame()

WIDTH, HEIGHT = 1200, 900
FPS = 60

BG_COLOR = '#202020'


class Ball:
	def __init__(self, space: pm.Space, *, pos, mass, color, radius = None, btype = pm.Body.DYNAMIC) -> None:
		radius = radius or mass
		moment = pm.moment_for_circle(mass=mass, inner_radius=0, outer_radius=radius)
		self.body = pm.Body(mass=mass, moment=moment, body_type=btype)
		self.body.position = pos
		self.shape = pm.Circle(self.body, radius=radius)
		self.shape.color = color

		self.shape.density = 1
		self.shape.elasticity = 0.9
		self.shape.friction = 0.9

		space.add(self.body, self.shape)


	def draw(self, screen: pg.surface) -> None:
		self.pg = pg.draw.circle(screen, self.shape.color, center=self.body.position, radius=self.shape.radius)



class Segment:
	def __init__(self, space: pm.Space, *, pos_a, pos_b, mass = None, color, thickness = None, btype = pm.Body.STATIC) -> None:
		
		self.body = pm.Body(mass=mass, body_type=btype)
		self.shape = pm.Segment(self.body, a=pos_a, b=pos_b, radius=thickness)
		self.shape.color = color
		#self.shape.elasticity = 0.9

		space.add(self.body, self.shape)


	def calculate_polygon_points(self) -> tuple[tuple, tuple, tuple, tuple]:
		start = self.shape.a
		end = self.shape.b
		
		# Compute the direction vector and its length
		dx = end[0] - start[0]
		dy = end[1] - start[1]
		length = math.hypot(dx, dy)
	
		# Normalize the direction vector
		dx /= length
		dy /= length
		
		# Compute perpendicular vector
		perp_dx = -dy
		perp_dy = dx
		
		# Compute the four corners of the polygon
		offset = self.shape.radius
		p1 = (start[0] + offset * perp_dx, start[1])
		p2 = (start[0] - offset * perp_dx, start[1] - offset * perp_dy)
		p3 = (end[0] - offset * perp_dx, end[1] - offset * perp_dy)
		p4 = (end[0] + offset * perp_dx, end[1] )

		return (p1, p2, p3, p4)

	def draw(self, screen: pg.surface) -> None:
		self.pg = pg.draw.polygon(screen, color=self.shape.color, points=self.calculate_polygon_points())


class Simulation:
	def __init__(self) -> None:
		# pymunk settings
		self.space = pm.Space()
		self.space.gravity = (0, 200)
		self.space.damping = 0.93
		
		# pygame settings
		self.screen = pg.display.set_mode((WIDTH, HEIGHT))
		pg.display.set_caption('Pendulum Simulation')
		self.clock = pg.time.Clock()
		self.fps = FPS

		

	def draw(self) -> None:
		pass

	def step(self):
		for event in pg.event.get():
			if event.type == pg.QUIT:
				pg.quit()
				sys.exit()
		
		self.screen.fill(BG_COLOR)
		
		self.draw()
		
		pg.display.update()
		self.clock.tick(self.fps)
		self.space.step(1/self.fps)



if __name__ == '__main__':
	sim = Simulation()
	
	while True:
		sim.step()