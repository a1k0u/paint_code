import pygame
import sys
import colors

pygame.init()


def get_pos():
	return pygame.mouse.get_pos()


class PaintCode:
	def __init__(self, width: int, height: int, caption: str):
		pygame.display.set_caption(caption)
		self.screen = pygame.display.set_mode((width, height))
		self.layers = []
		self.cursors_dct = {
			pygame.K_1: ("brush", colors.GREEN),
			pygame.K_2: ("rubber", colors.RED)

		}
		self.log = []
		self.cursor = self.cursors_dct[pygame.K_1]
		self.radius = 25
		self.drag = False
		self.current_color = colors.BLACK
		self.current_layer = 0

	def loop(self):
		while True:
			self.handlers()
			self.draw_object()
			self.draw_cursor()
			pygame.display.update()
			pygame.time.Clock().tick(144)

	def handlers(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()

			if event.type == pygame.KEYDOWN:
				if event.key in self.cursors_dct.keys():
					self.cursor = self.cursors_dct[event.key]

			if event.type == pygame.MOUSEBUTTONDOWN:
				if event.button == 1:
					self.drag = True
					self.actions()
				if event.button == 4:
					self.radius += 1
				if event.button == 5:
					if self.radius >= 5:
						self.radius -= 1

			if event.type == pygame.MOUSEBUTTONUP:
				if event.button == 1:
					self.drag = False

			if event.type == pygame.MOUSEMOTION:
				if self.drag:
					self.actions()

	def actions(self):
		if self.cursor[0] in ("brush", "rubber"):
			self.create_object()

	def draw_cursor(self):
		if self.cursor[0] in ("brush", "rubber"):
			pygame.mouse.set_visible(False)
			pygame.draw.circle(self.screen, self.cursor[1], get_pos(), self.radius, width=2)

	def draw_object(self):
		self.screen.fill(colors.WHITE)
		for layer in self.layers:
			if layer["type"] in ("brush", "rubber"):
				pygame.draw.circle(self.screen, layer["color"],
				                   layer["position"], layer["radius"])

	def create_object(self):
		object_config = {
			"type": self.cursor[0],
			"color": self.current_color,
			"position": get_pos()
		}

		if self.cursor[0] in ("brush", "rubber"):
			object_config["radius"] = self.radius
		if self.cursor[0] == "rubber":
			object_config["color"] = colors.WHITE

		self.layers.append(object_config)


if __name__ == "__main__":
	start = PaintCode(800, 600, "Test")
	start.loop()
