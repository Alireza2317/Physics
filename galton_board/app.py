import math
import sys
import pygame as pg
import pymunk as pm
import random

WIDTH, HEIGHT = 1200, 1000
FPS = 60

BG_COLOR = '#202020'
BOX_COLOR = (200, 200, 200)

class Ball:
	def __init__(self, space: pm.Space, *, pos, mass, color, radius = None, btype = pm.Body.DYNAMIC) -> None:
		radius = radius or mass
		moment = pm.moment_for_circle(mass=mass, inner_radius=0, outer_radius=radius)
		self.body = pm.Body(mass=mass, moment=moment, body_type=btype)
		self.body.position = pos
		self.shape = pm.Circle(self.body, radius=radius)
		self.shape.color = color

		self.shape.density = 3
		self.shape.elasticity = 0.3
		self.shape.friction = 0.6

		space.add(self.body, self.shape)


	def draw(self, screen: pg.surface) -> None:
		self.pg = pg.draw.circle(screen, self.shape.color, center=self.body.position, radius=self.shape.radius)



class Segment:
	def __init__(self, space: pm.Space, *, pos_a, pos_b, mass = None, color, thickness = None, btype = pm.Body.STATIC) -> None:
		
		self.body = pm.Body(mass=mass, body_type=btype)
		self.shape = pm.Segment(self.body, a=pos_a, b=pos_b, radius=thickness)
		self.shape.color = color
		self.shape.elasticity = 0.4
		self.shape.friction = 0.1

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
		self.space.gravity = (0, 1000)
		self.space.damping = 0.93
		
		# pygame settings
		self.screen = pg.display.set_mode((WIDTH, HEIGHT))
		pg.display.set_caption('Pendulum Simulation')
		self.clock = pg.time.Clock()
		self.fps = FPS


		self.funnel = [
			Segment(self.space, pos_a=(0, 0), pos_b=(0, 120), color=BOX_COLOR, thickness=5),
			Segment(self.space, pos_a=(0, 120), pos_b=(WIDTH/2 - 30, 200), color=BOX_COLOR, thickness=5),
			Segment(self.space, pos_a=(WIDTH/2 - 30, 200), pos_b=(WIDTH/2 - 30, 260), color=BOX_COLOR, thickness=2.5),

			Segment(self.space, pos_a=(WIDTH, 0), pos_b=(WIDTH, 120), color=BOX_COLOR, thickness=5),
			Segment(self.space, pos_a=(WIDTH, 120), pos_b=(WIDTH/2 + 30, 200), color=BOX_COLOR, thickness=5),
			Segment(self.space, pos_a=(WIDTH/2+30, 200), pos_b=(WIDTH/2 + 30, 260), color=BOX_COLOR, thickness=2.5),
		]
		NUM_BARS = 17
		self.bars = [
			Segment(self.space, pos_a=(0, HEIGHT), pos_b=(WIDTH, HEIGHT), color=BOX_COLOR, thickness=4),
			
		]

		for i in range(NUM_BARS+1):
			self.bars.append(
				Segment(
					self.space, 
					pos_a=(i*WIDTH/NUM_BARS, HEIGHT), 
					pos_b=(i*WIDTH/NUM_BARS, HEIGHT - 350), 
					color=BOX_COLOR, 
					thickness=2
				),
			)

		NUM_PEGS_ROWS = 10
		DPEGS = WIDTH//16
		self.pegs = [
			[
				Ball(self.space, pos=(i, r*30 + 310), mass=10, color=BOX_COLOR, btype=pm.Body.STATIC)
				for i in range(DPEGS//2 if r%2 else DPEGS, WIDTH, DPEGS)
			]
			for r in range(NUM_PEGS_ROWS)
		]
		NUM_BALLS = 720
		self.balls = [
			Ball(self.space, pos=(n * WIDTH//NUM_BALLS-45, n//6), color=(200, 170, 0), mass=5)
			for n in range(1, NUM_BALLS+1)
		]

	def draw(self) -> None:
		for seg in self.funnel:
			seg.draw(self.screen)
		for bar in self.bars:
			bar.draw(self.screen)

		for pegs in self.pegs:
			for peg in pegs:
				peg.draw(self.screen)

		for ball in self.balls:
			ball.draw(self.screen)

	def step(self):
		for event in pg.event.get():
			if event.type == pg.QUIT:
				pg.quit()
				sys.exit()
			if event.type == pg.MOUSEBUTTONDOWN:
				pos = event.pos
				self.balls.extend([Ball(self.space, pos=pos, color=(200, 170, 0), mass=5) for _ in range(50)])
	
			
		self.screen.fill(BG_COLOR)
		
		self.draw()
		
		pg.display.update()
		self.clock.tick(self.fps)
		self.space.step(1/self.fps)



if __name__ == '__main__':
	sim = Simulation()
	
	while True:
		sim.step()