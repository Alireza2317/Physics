import sys
import pygame as pg
import pymunk as pm

WIDTH = 600
HEIGHT = 400


class Pendulum:
	pass


class PendulumSimulation:
	def __init__(self) -> None:
		self.pendulum = Pendulum()
		self.screen = pg.display.set_mode((WIDTH, HEIGHT))
		pg.display.set_caption('Pendulum Simulation')
		

	def step(self):
		for event in pg.event.get():
			if event.type == pg.QUIT:
				pg.quit()
				sys.exit()

		return True



if __name__ == '__main__':
	simulation = PendulumSimulation()
	while True:
		done = simulation.step()
		
		if done:
			break