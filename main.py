import pygame
import sys
import colors

pygame.init()


# TODO: Surface(YT), new brush(TY), optimization, new instruments, refactoring, pygame+tkinter??

def get_pos():
	return pygame.mouse.get_pos()


class PaintCode:
	def __init__(self, width: int, height: int, caption: str):
		pygame.display.set_caption(caption)
		self.screen = pygame.display.set_mode((width, height))
		self.screen.fill(colors.WHITE)
		self.layers = []
		self.cursors_dct = {
			pygame.K_1: ("rect", colors.RED),
			pygame.K_2: ("ellipse", colors.RED)
		}
		self.log = []
		self.cursor = self.cursors_dct[pygame.K_1]
		self.radius = 25
		self.drag = False
		self.dragging_coordinates = (0, 0)
		self.drag_start = (0, 0)
		self.drag_stop = (0, 0)
		self.current_color = colors.BLACK
		self.current_layer = 0

	def loop(self):
		while True:
			self.draw_object()
			self.handlers()
			if self.drag:
				self.actions()
			self.draw_cursor()
			pygame.display.update()
			pygame.time.Clock().tick()

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
					self.dragging_coordinates = get_pos()
					self.actions()
				if event.button == 4:
					self.radius += 1
				if event.button == 5:
					if self.radius >= 5:
						self.radius -= 1

			if event.type == pygame.MOUSEBUTTONUP:
				if event.button == 1:
					self.drag = False
					self.actions()

			if event.type == pygame.MOUSEMOTION:
				if self.drag:
					self.actions()

	def actions(self):
		if self.cursor[0] in ("rect", "ellipse"):
			if self.drag:
				self.draw_figure_obj()
			elif not self.drag:
				self.create_object()

	def draw_cursor(self):
		if self.cursor[0] in ("rect", "ellipse"):
			pygame.mouse.set_visible(True)
			bd_radius = 0
			if self.cursor[0] == "ellipse":
				bd_radius = 100
			pygame.draw.rect(self.screen, colors.RED, (get_pos()[0] + 10, get_pos()[1] + 25, 30, 30),
			                 width=2, border_radius=bd_radius)

	def draw_figure_obj(self):
		if self.cursor[0] in ("rect", "ellipse"):
			x1, y1 = self.dragging_coordinates
			x2, y2 = get_pos()
			start_point = [x2, y2]
			perimeter = [abs(x1 - x2), abs(y2 - y1)]
			if x2 > x1:
				start_point[0] = x1
			if y2 > y1:
				start_point[1] = y1
			self.drag_start = start_point
			self.drag_stop = perimeter
			if self.cursor[0] == "rect":
				pygame.draw.rect(self.screen, self.current_color,
				                 (start_point[0], start_point[1],
				                  perimeter[0], perimeter[1]))
			else:
				pygame.draw.ellipse(self.screen, self.current_color,
				                    (start_point[0], start_point[1],
				                     perimeter[0], perimeter[1]))

	def draw_object(self):
		self.screen.fill(colors.WHITE)
		for layer in self.layers:
			if layer["type"] in ("rect", "ellipse"):
				x1, y1 = layer["position"]
				width, height = layer["perimeter"]
				if layer["type"] == "rect":
					pygame.draw.rect(self.screen, layer["color"],
					                 (x1, y1, width, height))
				else:
					pygame.draw.ellipse(self.screen, layer["color"],
					                    (x1, y1, width, height))

	def create_object(self):
		object_config = {
			"type": self.cursor[0],
			"color": self.current_color,
			"position": get_pos()
		}

		if self.cursor[0] in ("rect", "ellipse"):
			object_config["position"] = self.drag_start
			object_config["perimeter"] = self.drag_stop

		self.layers.append(object_config)
		self.log.append({"num_layer": self.current_layer})


if __name__ == "__main__":
	start = PaintCode(800, 600, "Test")
	start.loop()
