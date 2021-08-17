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
			pygame.K_2: "ellipse",
			pygame.K_3: "line",
			pygame.K_4: "rubber"
		}
		self.log = []
		self.cursor = self.cursors_dct[pygame.K_1]
		self.drag = False
		self.dragging_coordinates = (0, 0)
		self.drag_start = (0, 0)
		self.drag_stop = (0, 0)
		self.line_width = 3
		self.clicked_coordinates = [self.dragging_coordinates]
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
		if self.cursor in ("rect", "ellipse", "line"):
			if self.drag:
				self.draw_figure_obj()
			elif not self.drag:
				if self.drag_stop != (0, 0):
					self.create_object()
		if self.cursor == "rubber":
			if self.drag:
				self.delete_object()

	def draw_cursor(self):
		if self.cursor in ("rect", "ellipse"):
			pygame.draw.rect(self.screen, colors.RED, (get_pos()[0] + 10, get_pos()[1] + 25, 30, 30),
			                 width=2, border_radius=100*(self.cursor == "ellipse"))

	def draw_figure_obj(self):
		x1, y1 = self.dragging_coordinates
		x2, y2 = get_pos()
		if self.cursor in ("rect", "ellipse"):
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
		if self.cursor == "line":
			self.drag_start = [x1, y1]
			self.drag_stop = [x2, y2]
			pygame.draw.line(self.screen, self.current_color, [x1, y1], [x2, y2], self.line_width)

	def draw_object(self):
		# TODO refactoring
		self.screen.fill(colors.WHITE)
		for layer in self.layers:
			if layer["type"] in ("rect", "ellipse", "line"):
				x1, y1 = layer["position"]
				width, height = layer["perimeter"]
				if layer["type"] == "rect":
					pygame.draw.rect(self.screen, layer["color"],
					                 (x1, y1, width, height))
				elif layer["type"] == "ellipse":
					pygame.draw.ellipse(self.screen, layer["color"],
					                    (x1, y1, width, height))
				elif layer["type"] == "line":
					pygame.draw.line(self.screen, self.current_color, [x1, y1], [width, height], self.line_width)

	def create_object(self):
		object_config = {
			"type": self.cursor,
			"color": self.current_color,
			"position": get_pos()
		}

		if self.cursor in ("rect", "ellipse", "line"):
			object_config["position"] = self.drag_start
			object_config["perimeter"] = self.drag_stop
			self.drag_stop = (0, 0)

		self.layers.append(object_config)
		self.log.append({"num_layer": self.current_layer})

	def delete_object(self):
		for layer in range(len(self.layers)-1, -1, -1):
			if self.layers[layer]["type"] in ("rect", "ellipse"):
				x1, y1 = self.layers[layer]["position"]
				width, height = self.layers[layer]["perimeter"]
				mouse_x, mouse_y = get_pos()
				if x1 <= mouse_x <= x1 + width and y1 <= mouse_y <= y1 + height:
					self.layers.pop(layer)
					self.drag = False
					return


if __name__ == "__main__":
	start = PaintCode(800, 600, "Test")
	start.loop()
