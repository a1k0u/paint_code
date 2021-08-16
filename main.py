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
			pygame.K_1: "rect",
			pygame.K_2: "ellipse"
		}
		self.log = []
		self.cursor = self.cursors_dct[pygame.K_1]
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
			self.draw_cursor()
			self.actions()
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

			if event.type == pygame.MOUSEBUTTONUP:
				if event.button == 1:
					self.drag = False

			self.actions()

	def actions(self):
		if self.cursor in ("rect", "ellipse"):
			if self.drag:
				self.draw_figure_obj()
			elif not self.drag:
				if self.drag_stop != (0, 0):
					self.create_object()

	def draw_cursor(self):
		if self.cursor in ("rect", "ellipse"):
			pygame.draw.rect(self.screen, colors.RED, (get_pos()[0] + 10, get_pos()[1] + 25, 30, 30),
			                 width=2, border_radius=100*(self.cursor == "ellipse"))

	def draw_figure_obj(self):
		if self.cursor in ("rect", "ellipse"):
			x1, y1 = self.dragging_coordinates
			x2, y2 = get_pos()
			start_point = [x2, y2]
			width_height = [abs(x1 - x2), abs(y2 - y1)]
			if x2 > x1:
				start_point[0] = x1
			if y2 > y1:
				start_point[1] = y1
			self.drag_start = start_point
			self.drag_stop = width_height
			if self.cursor == "rect":
				pygame.draw.rect(self.screen, self.current_color,
				                 (start_point[0], start_point[1],
				                  width_height[0], width_height[1]))
			else:
				pygame.draw.ellipse(self.screen, self.current_color,
				                    (start_point[0], start_point[1],
				                     width_height[0], width_height[1]))

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
			"type": self.cursor,
			"color": self.current_color,
			"position": get_pos()
		}

		if self.cursor in ("rect", "ellipse"):
			object_config["position"] = self.drag_start
			object_config["perimeter"] = self.drag_stop
			self.drag_stop = (0, 0)

		self.layers.append(object_config)
		self.log.append({"num_layer": self.current_layer})


if __name__ == "__main__":
	start = PaintCode(800, 600, "Test")
	start.loop()
