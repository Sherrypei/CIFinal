import pygame
import time
import sys
import random
import math
 
pygame.init()
 
oppo = {"red":"blue", "blue":"red", "green":"green"}
FPS = 60
WIDTH = 900
HEIGHT = 600
RIGHT = 1
LEFT = 0
STAND = 1
MOVE = 0
CENTER = (WIDTH / 2, HEIGHT / 2)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (153, 229, 253)
RED = (255, 0, 0)
isend = False
total_level = 2
 
def xor(bool1, bool2):
	if (bool1 and bool2) or (not bool1 and not bool2):
		return False
	else:
		return True
 
def iscollide(obj1,obj2):
	if ((obj2.x + obj2.width > obj1.x >= obj2.x) or (obj1.x + obj1.width > obj2.x >= obj1.x)) and ((obj2.y + obj2.height > obj1.y >= obj2.y) or (obj1.y + obj1.height > obj2.y >= obj1.y)):
	# if xor(obj1.x + obj1.width > obj2.x, obj1.x > obj2.x + obj2.width) and xor(obj1.y + obj1.height > obj2.y, obj1.y > obj2.y + obj2.height):
		return True
	else:
		return False
 
# screen
raw_background = pygame.image.load('./image/background.jpg')
raw_background_darken = pygame.image.load('./image/background_darken.png')
raw_background_transparent = pygame.image.load('./image/background_transparent.png')
raw_black_transparent = pygame.image.load('./image/black_transparent.png')
starting_page = pygame.image.load('./image/starting_page.jpg')
winning_page = pygame.image.load('./image/winning_page.jpg')
information_button = pygame.image.load('./image/information.png')
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("fire and ice sisters")
 
# clock
clock = pygame.time.Clock()
 
# text
def write(text, size, x, y, font = None, color = BLACK):
	cur_font = pygame.font.SysFont(font, size)
	cur_text = cur_font.render(text, True, color)
	cur_text_rect = cur_text.get_rect(center = (WIDTH / 2 + x, y))
	return cur_text, cur_text_rect
 
class Player(pygame.sprite.Sprite):
	#constant
	DX = 3 
	DY = -9
	DDY = 0.3
 
	def __init__(self, x, y, color, img_stand_right, img_move_right, width, height):
		pygame.sprite.Sprite.__init__(self)
		stand_right = pygame.image.load(img_stand_right)
		move_right = pygame.image.load(img_move_right)
		stand_left = pygame.transform.flip(stand_right, True, False)
		move_left = pygame.transform.flip(move_right, True, False)
		self.image = pygame.transform.scale(stand_right.convert_alpha(), (width, height))
		self.img_stand_right = pygame.transform.scale(stand_right.convert_alpha(), (width, height))
		self.img_stand_left = pygame.transform.scale(stand_left.convert_alpha(), (width, height))
		self.img_jump_right = pygame.transform.scale(move_right.convert_alpha(), (width, height))
		self.img_jump_left = pygame.transform.scale(move_left.convert_alpha(), (width, height))
		self.color = color
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.x = x
		self.y = y
		self.dx = 0
		self.dy = 0
		self.width = width
		self.height = height
		self.direction = RIGHT
		self.movement = STAND
		self.move_count = 10
 
	def isabove(self,obj):
		if (self.y + self.height == obj.y) and ((obj.x + obj.width > self.x >= obj.x) or (self.x + self.width > obj.x >= self.x)):
			return True
		else:
			return False
 
	def willcollide_x(self,obj):
		self.x += self.dx
		is_collide = iscollide(self,obj)
		self.x -= self.dx
		if is_collide:
			if self.dx < 0:
				self.dx = -(self.x - obj.x - obj.width)  # set it to be right into the obj (after moving)
			else:
				self.dx = obj.x - self.x - self.width
			return True
		else:
			return False
 
	def willcollide_y(self,obj):
		self.y += self.dy
		is_collide = iscollide(self, obj)
		self.y -= self.dy
		if is_collide:
			if self.dy < 0:
				self.dy = -(self.y - obj.y - obj.height)
			else:
				self.dy = obj.y - self.y - self.height
			return True
		else:
			return False
 
	def jump(self,objs, key_pressed):
		if (self.color == 'red' and key_pressed[pygame.K_w]) or (self.color == 'blue' and key_pressed[pygame.K_UP]):
			for wall in objs.wall:
				if (wall.color == 'green' or oppo[wall.color] == self.color) and self.isabove(wall):
					self.dy = self.DY
					return
			for door in objs.door:
				if self.isabove(door):
					self.dy = self.DY
					return
			for plane in objs.plane:
				if self.isabove(plane):
					self.dy = self.DY
					return
 
	def move(self, key_pressed):
		if self.color == "red":
			if key_pressed[pygame.K_a]:
				self.direction = LEFT
				self.dx = -self.DX
				self.move_count -= 1
			elif key_pressed[pygame.K_d]:
				self.direction = RIGHT
				self.dx = self.DX
				self.move_count -= 1
			else:
				self.dx = 0
		else:
			if key_pressed[pygame.K_LEFT]:
				self.dx = -self.DX
				self.direction = LEFT
				self.move_count -= 1
			elif key_pressed[pygame.K_RIGHT]:
				self.dx = self.DX
				self.direction = RIGHT
				self.move_count -= 1
			else:
				self.dx = 0
 
	def update(self,objs):
		key_pressed = pygame.key.get_pressed()
		self.change_gesture()
		self.move(key_pressed)
		self.jump(objs, key_pressed)
		self.get_diamond(objs)
 
		willcollide_x = False
		for wall in objs.wall:
			if wall.color == 'green' or oppo[wall.color] == self.color:
				willcollide_x = self.willcollide_x(wall) or willcollide_x
 
		for door in objs.door:
			if door.isopen == False:
				willcollide_x = self.willcollide_x(door) or willcollide_x
 
		for plane in objs.plane:
			willcollide_x = self.willcollide_x(plane) or willcollide_x
 
		self.x += self.dx
 
		if willcollide_x:
			self.dx = 0
 
		willcollide_y = False
		for wall in objs.wall:
			if wall.color == 'green' or oppo[wall.color] == self.color:
				willcollide_y = self.willcollide_y(wall) or willcollide_y
 
		for door in objs.door:
			if door.isopen == False:
				willcollide_y = self.willcollide_y(door) or willcollide_y
 
		for plane in objs.plane:
			willcollide_y = self.willcollide_y(plane) or willcollide_y
 
		self.y += self.dy
 
		if willcollide_y:
			self.dy = 0
 
 
		self.dy += self.DDY
		self.rect.x = self.x
		self.rect.y = self.y
 
	def change_gesture(self):
		# flying in the sky
		if abs(self.dy) > self.DDY:
			if self.direction == RIGHT:
				self.image = self.img_jump_right
			else:
				self.image = self.img_jump_left
			self.movement = MOVE
			return
 
		if self.move_count > 0:
			return
		self.move_count = 10
 
		# moving on the ground
		if self.movement == STAND:
			if self.direction == RIGHT:
				self.image = self.img_jump_right
			else:
				self.image = self.img_jump_left
			self.movement = MOVE
		else:
			if self.direction == RIGHT:
				self.image = self.img_stand_right
			else:
				self.image = self.img_stand_left
			self.movement = STAND
 
 
	def get_diamond(self, objs):
		for diamond in objs.diamond:
			if self.color == diamond.color and iscollide(self, diamond):
				all_sprite.remove(diamond)
				objs.diamond.remove(diamond)
				return
 
class Wall(pygame.sprite.Sprite):
	def __init__(self, color, x, y, width, height, image):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.transform.scale(pygame.image.load(image).convert_alpha(), (width, height))
		self.color = color
		self.rect = self.image.get_rect()
		self.x = x
		self.y = y
		self.rect.x = x
		self.rect.y = y
		self.width = width
		self.height = height
 
class Water(pygame.sprite.Sprite):
	def __init__(self, color, x, y, width, height, image):
		pygame.sprite.Sprite.__init__(self)
		self.color = color
		self.image = pygame.transform.scale(pygame.image.load(image).convert_alpha(), (width, height))
		self.x = x
		self.y = y
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.width = width
		self.height = height
	def kill(self, players):
		global isend
		for player in players:
			if (oppo[player.color] == self.color or self.color == "green") and iscollide(self,player):
				isend = True
				return
 
class Door(pygame.sprite.Sprite):
	def __init__(self, x, y, isopen, width, height, ID, img_close, img_open1, img_open2, img_open3, direction, phase_num):
		pygame.sprite.Sprite.__init__(self)
		self.img_close = pygame.transform.scale(pygame.image.load(img_close).convert_alpha(), (width, height))
		self.img_open = list()
		self.img_open.append(pygame.transform.scale(pygame.image.load(img_open1).convert_alpha(), (width, height)))
		self.img_open.append(pygame.transform.scale(pygame.image.load(img_open2).convert_alpha(), (width, height)))
		self.img_open.append(pygame.transform.scale(pygame.image.load(img_open3).convert_alpha(), (width, height)))
 
		self.isopen = isopen
		self.image = self.img_close
		self.phase_count = 0
		self.phase_num = phase_num
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.direction = direction
		self.ID = ID
		if direction == 'right':
			self.x = x
			self.y = y
			self.width = width * 2 / 5
			self.height = height
		elif direction == 'left':
			self.x = x + width * 3 / 5
			self.y = y
			self.width = width * 2 / 5
			self.height = height
		elif direction == 'down':
			self.x = x
			self.y = y
			self.width = width
			self.height = self.height / 5
		elif direction == 'up':
			self.x = x
			self.y = y + height * 4 / 5
			self.width = width
			self.height = height / 5
 
	def update(self):
		if self.phase_count == 0:
			self.isopen = False
			self.image = self.img_close
		else:
			self.isopen = True
			for i in range(3):
				if self.phase_count <= (i + 1) * self.phase_num:
					self.image = self.img_open[i]
					break
 
	def kill(self,players):
		global isend
		if not self.isopen:
			return
		for player in players:
			if iscollide(self,player):
				isend = True
				return
 
class Plane(pygame.sprite.Sprite):
	def __init__(self, x, y, ID, width, height, image):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.transform.scale(pygame.image.load(image).convert_alpha(), (width, height))
		self.x = x
		self.y = y
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.ID = ID
		self.width = width
		self.height = height
 
class Button(pygame.sprite.Sprite):
	def __init__(self, x, y, activate, deactivate, width, height, image_unpressed, image_pressed):
		pygame.sprite.Sprite.__init__(self)
		self.img_pressed = pygame.transform.scale(pygame.image.load(image_pressed).convert_alpha(), (width, height))
		self.img_unpressed = pygame.transform.scale(pygame.image.load(image_unpressed).convert_alpha(), (width, height))		
		self.image = self.img_unpressed
		self.x = x 
		self.y = y 
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.activate = activate
		self.deactivate = deactivate
		self.width = width
		self.height = height
 
	def check(self, players):
		for player in players:
			if iscollide(self, player):
				self.activate(objs)
				self.image = self.img_pressed
				return
		self.image = self.img_unpressed
		self.deactivate(objs)
 
def moveplane(planes, ID, players, x, y, dx, dy):
	global isend, objs
	for plane in planes:
		if plane.ID == ID:
			if dx < 0 and plane.x + dx < x:
				dx =- (plane.x - x)
			elif dx > 0 and plane.x + dx > x:
				dx = x - plane.x
			if dy < 0 and plane.y + dy < y:
				dy =- (plane.y - y)
			elif dy > 0 and plane.y + dy > y:
				dy = y - plane.y
 
			for player in players:
				if player.isabove(plane):
					player.dx = dx
					willcollide_x = False
					for wall in objs.wall:
						if wall.color == 'green' or oppo[wall.color] == player.color:
							willcollide_x = player.willcollide_x(wall) or willcollide_x
					for door in objs.door:
						if door.isopen == False:
							willcollide_x = player.willcollide_x(door) or willcollide_x
					for plane_in_planes in objs.plane:
						willcollide_x = player.willcollide_x(plane_in_planes) or willcollide_x
					player.x += player.dx
					if willcollide_x:
						player.dx = 0
			plane.x += dx
			for player in players:
				if iscollide(plane, player):
					if dx < 0:
						player.x = plane.x - player.width
					else:
						player.x = plane.x + plane.width
 
			plane.y += dy
			for player in players:
				if iscollide(plane, player):
					if dy < 0:
						player.y = plane.y - player.height
					else:
						player.y = plane.y + plane.height
			for player in players:
				player.y += dy
				if player.isabove(plane):
					player.dy = dy
					player.y -= player.dy
					willcollide_y = False
					for wall in objs.wall:
						if wall.color == 'green' or oppo[wall.color] == player.color:
							willcollide_y = player.willcollide_y(wall) or willcollide_y
					for door in objs.door:
						if door.isopen == False:
							willcollide_y = player.willcollide_y(door) or willcollide_y
					for plane_in_planes in objs.plane:
						willcollide_y = player.willcollide_y(plane_in_planes) or willcollide_y
					player.y += player.dy
					if willcollide_y:
						player.dy = 0
					player.y += dy
				player.y -= dy
 
			plane.rect.x = plane.x
			plane.rect.y = plane.y
 
			for player in players:
				for wall in objs.wall:
					if (wall.color == 'green' or oppo[wall.color] == player.color) and iscollide(player, wall):
						isend = True
						return
 
				for door in objs.door:
					if door.isopen == False and iscollide(player, door):
						isend = True
						return
 
				for plane_in_planes in objs.plane:
					if iscollide(player, plane_in_planes):
						isend = True
						return
 
def opendoor(doors, ID, speed):
	for door in doors:
		if door.ID == ID:
			if door.phase_count < door.phase_num * 3:
				door.phase_count += speed
			return
 
def closedoor(doors, ID, players, speed):
	for door in doors:
		if door.ID == ID:
			if door.phase_count > 0:
				door.phase_count -= speed
				if door.phase_count == 0:
					door.kill(players)
			return
 
class Diamond(pygame.sprite.Sprite):
	def __init__(self, color, x, y, width, height, image):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.transform.scale(pygame.image.load(image).convert_alpha(), (width, height))
		self.color = color
		self.x = x
		self.y = y
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.width = width
		self.height = height
 
class Cloud(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, image):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load(image).convert_alpha(), (width, height))
        self.x = x
        self.y = y
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = width
        self.height = height
        self.move_count = 0
        self.dx = 0
        self.dy = 0
 
    def moving(self):
        global WIDTH, HEIGHT
        if self.move_count == 0:
        	self.dx = random.randrange(-1, 2)
        	self.dy = random.randrange(-1, 2)
        	self.move_count = 60
 
        if 0 <= self.x + self.dx <= WIDTH - self.width:
        	self.x += self.dx
        if 0 <= self.y + self.dy <= HEIGHT / 4:
        	self.y += self.dy
        self.rect.x = self.x
        self.rect.y = self.y
        self.move_count -= 1
 
class Destination(pygame.sprite.Sprite):
	def __init__(self, color, x, y, width, height, *imgs):
		pygame.sprite.Sprite.__init__(self)
		self.img = pygame.transform.scale(pygame.image.load(imgs[0]).convert_alpha(), (width, height))
		self.img_win = pygame.transform.scale(pygame.image.load(imgs[1]).convert_alpha(), (width, height)) 
		if len(imgs) > 2:
			self.img_win2 = pygame.transform.scale(pygame.image.load(imgs[2]).convert_alpha(), (width, height))
		else:
			self.img_win2 = None
		self.image = self.img
		self.rect = self.image.get_rect()
		self.color = color
		self.x = x
		self.y = y
		self.rect.x = x
		self.rect.y = y
		self.iswin = False
		self.width = width
		self.height = height
 
	def win(self, players):
		for player in players:
			if player.color == self.color:
				if iscollide(self,player):
					self.iswin = True
				else:
					self.iswin = False
				return
 
class Objects:
	def __init__(self):
		self.player = set()
		self.wall = set()
		self.water = set()
		self.door = set()
		self.plane = set()
		self.button = set()
		self.diamond = set()
		self.destination = set()
		self.cloud = set()
 
	def clear(self):
		self.player.clear()
		self.wall.clear()
		self.water.clear()
		self.door.clear()
		self.plane.clear()
		self.button.clear()
		self.diamond.clear()
		self.destination.clear()
		self.cloud.clear()
 
def add_obj(obj, typ):
	global all_sprite, objs
	all_sprite.add(obj)
	if typ == 'player':
		objs.player.add(obj)
	elif typ == 'wall':
		objs.wall.add(obj)
	elif typ == 'water':
		objs.water.add(obj)
	elif typ == 'door':
		objs.door.add(obj)
	elif typ == 'plane':
		objs.plane.add(obj)
	elif typ == 'button':
		objs.button.add(obj)
	elif typ == 'diamond':
		objs.diamond.add(obj)
	elif typ == 'destination':
		objs.destination.add(obj)
	elif typ == 'cloud':
		objs.cloud.add(obj)
 
all_sprite = pygame.sprite.Group()
objs = Objects()
 
def init_obj_1():
	all_sprite.empty()
	objs.clear()
 
	# clouds
	cloud1 = Cloud(100, 100, 150, 100, './image/cloud.png')
	add_obj(cloud1, 'cloud')
	cloud2 = Cloud(300, 80, 120, 80, './image/cloud.png')
	add_obj(cloud2, 'cloud')
	cloud3 = Cloud(500, 120, 180, 120, './image/cloud.png')
	add_obj(cloud3, 'cloud')
	cloud3 = Cloud(700, 100, 120, 80, './image/cloud.png')
	add_obj(cloud3, 'cloud')
 
	# boarder walls
	floor = Wall('green', 0, HEIGHT - 10, WIDTH, 10, './image/wall.jpg')
	add_obj(floor, 'wall')
	left_wall = Wall('green', 0, 0, 1, HEIGHT, './image/wall.jpg')
	add_obj(left_wall, 'wall')
	right_wall = Wall('green', WIDTH - 1, 0, 1, HEIGHT, './image/wall.jpg')
	add_obj(right_wall, 'wall')
	ceiling = Wall('green', 0, 0, WIDTH, 1, './image/wall.jpg')
	add_obj(ceiling, 'wall')
 
	# walls
	wall1 = Wall('green', 220, HEIGHT - 130, 330, 20, './image/wall.jpg')
	add_obj(wall1, 'wall')
	wall2 = Wall('green', 450, HEIGHT - 250, 200, 20, './image/wall.jpg')
	add_obj(wall2, 'wall')
	wall3 = Wall('green', 700, HEIGHT - 370, 200, 20, './image/wall.jpg')
	add_obj(wall3, 'wall')
	wall4 = Wall('green', 300, HEIGHT - 230, 20, 100, './image/wall_vertical.png')
	add_obj(wall4, 'wall')
	wall5 = Wall('red', 480, HEIGHT - 230, 20, 100, './image/wall_red_vertical.png')
	add_obj(wall5, 'wall')
	wall6 = Wall('blue', 650, HEIGHT - 125, 100, 15, './image/wall_blue.png')
	add_obj(wall6, 'wall')
	wall7 = Wall('red', 650, HEIGHT - 250, 100, 20, './image/wall_red.png')
	add_obj(wall7, 'wall')
 
	# planes
	plane1 = Plane(300, HEIGHT - 250, 1, 140, 20, './image/plane.jpg')
	add_obj(plane1,  'plane')
	plane2 = Plane(775, HEIGHT - 250, 2, 100, 20, './image/plane.jpg')
	add_obj(plane2, 'plane')
	plane3 = Plane(220, HEIGHT - 110, 3, 20, 100, './image/plane_vertical.png')
	add_obj(plane3, 'plane')
 
	# waters
	water1 = Water('blue', 170, HEIGHT - 15, 100, 15, './image/water_blue.png')
	add_obj(water1, 'water')
	water2 = Water('red', 500, HEIGHT - 15, 100, 15, './image/water_red.png')
	add_obj(water2, 'water')
 
	# doors
	door1 = Door(350, HEIGHT - 110, False, 80, 100, 1, './image/door_close.png', './image/door_open1.png', './image/door_open2.png', './image/door_open3.png', 'right', 10)
	add_obj(door1, 'door')
	# window1 = Door(600, HEIGHT - 100, False, 100, 40, 1, './image/window_close.png', './image/window_open1.png', './image/window_open2.png', './image/window_open3.png', 'up')
	# add_obj(window1, 'door')
 
	# diamonds
	diamond1 = Diamond('red', 65, HEIGHT - 420, 30, 20, './image/diamond_red.png')
	add_obj(diamond1, 'diamond')
	diamond2 = Diamond('red', 300, HEIGHT - 30, 30, 20, './image/diamond_red.png')
	add_obj(diamond2, 'diamond')
	diamond3 = Diamond('blue', 430, HEIGHT - 150, 30, 20, './image/diamond_blue.png')
	add_obj(diamond3, 'diamond')
	diamond4 = Diamond('blue', 440, HEIGHT - 30, 30, 20, './image/diamond_blue.png')
	add_obj(diamond4, 'diamond')
 
	#buttons
	def b1activate(objs):
		moveplane(objs.plane, 1, objs.player, 10, HEIGHT - 400, -4, -2)
		moveplane(objs.plane, 2, objs.player, 775, HEIGHT - 130, 0, 2)
	def b1deactivate(objs):
		moveplane(objs.plane, 1, objs.player, 300, HEIGHT - 250, 4, 2)
		moveplane(objs.plane, 2, objs.player, 775, HEIGHT - 250, 0, -2)
	button1 = Button(535, HEIGHT - 270, b1activate, b1deactivate, 30, 20, './image/button_unpressed.png', './image/button_pressed.png')
	add_obj(button1, 'button')
 
	def b2activate(objs):
		opendoor(objs.door, 1, 1)
	def b2deactivate(objs):
		closedoor(objs.door, 1, objs.player, 1)
	button2 = Button(350, HEIGHT - 150, b2activate, b2deactivate, 30, 20, './image/button_unpressed.png', './image/button_pressed.png')
	add_obj(button2, 'button')
 
	def b3activate(objs):
		moveplane(objs.plane, 3, objs.player, 100, HEIGHT - 110, -2, 0)
	def b3deactivate(objs):
		moveplane(objs.plane, 3, objs.player, 220, HEIGHT - 110, 2, 0)
	button3 = Button(240, HEIGHT - 150, b3activate, b3deactivate, 30, 20, './image/button_unpressed.png', './image/button_pressed.png')
	add_obj(button3, 'button')
 
	# destinations
	destination_blue = Destination('blue', 750, HEIGHT - 450, 60, 80, './image/cup_without_water.png', './image/cup_with_water.png', './image/cup_with_iceman.png')
	add_obj(destination_blue, 'destination')
	destination_red = Destination('red', 810, HEIGHT - 470, 40, 100, './image/torch_without_fire.png', './image/torch_with_fire.png')
	add_obj(destination_red, 'destination')
 
	# players
	iceman = Player(WIDTH - 100, HEIGHT - 120, 'blue', './image/iceman.png', './image/iceman_move.png', 50, 90)
	add_obj(iceman, 'player')
	fireman = Player(50, HEIGHT - 120, 'red', './image/fireman.png', './image/fireman_move.png', 50, 90)
	add_obj(fireman, 'player')
 
def init_obj_2():
	all_sprite.empty()
	objs.clear()
 
	# clouds
	cloud1 = Cloud(100, 100, 150, 100, './image/cloud.png')
	add_obj(cloud1, 'cloud')
	cloud2 = Cloud(300, 80, 120, 80, './image/cloud.png')
	add_obj(cloud2, 'cloud')
	cloud3 = Cloud(500, 120, 180, 120, './image/cloud.png')
	add_obj(cloud3, 'cloud')
	cloud3 = Cloud(700, 100, 120, 80, './image/cloud.png')
	add_obj(cloud3, 'cloud')
 
	# boarder walls
	floor = Wall('green', 0, HEIGHT - 10, WIDTH, 10, './image/wall.jpg')
	add_obj(floor, 'wall')
	left_wall = Wall('green', 0, 0, 1, HEIGHT, './image/wall.jpg')
	add_obj(left_wall, 'wall')
	right_wall = Wall('green', WIDTH - 1, 0, 1, HEIGHT, './image/wall.jpg')
	add_obj(right_wall, 'wall')
	ceiling = Wall('green', 0, 0, WIDTH, 1, './image/wall.jpg')
	add_obj(ceiling, 'wall')
 
	# walls
	wall1 = Wall('green', 80, HEIGHT - 490, 150, 20, './image/wall.jpg')
	add_obj(wall1, 'wall')
	wall2 = Wall('green', 100, HEIGHT - 370, 420, 20, './image/wall.jpg')
	add_obj(wall2, 'wall')
	wall3 = Wall('green', 700, HEIGHT - 490, 200, 20, './image/wall.jpg')
	add_obj(wall3, 'wall')
	wall4 = Wall('green', 700, HEIGHT - 130, 200, 20, './image/wall.jpg')
	add_obj(wall4, 'wall')
	wall5 = Wall('green', 100, HEIGHT - 250, 700, 20, './image/wall.jpg')
	add_obj(wall5, 'wall')
	wall6 = Wall('green', 160, HEIGHT - 130, 70, 20, './image/wall.jpg')
	add_obj(wall6, 'wall')
	wall7 = Wall('green', 500, HEIGHT - 130, 20, 20, './image/wall.jpg')
	add_obj(wall7, 'wall')
	wall8 = Wall('green', 0, HEIGHT - 490, 20, 20, './image/wall.jpg')
	add_obj(wall8, 'wall')
	wall9 = Wall('green', 500, HEIGHT - 130, 20, 20, './image/wall.jpg')
	add_obj(wall9, 'wall')
 
	wall10 = Wall('red', 700, HEIGHT - 470, 20, 100, './image/wall_red_vertical.png')
	add_obj(wall10, 'wall')
	wall11 = Wall('red', 160, HEIGHT - 230, 20, 100, './image/wall_red_vertical.png')
	add_obj(wall11, 'wall')
	wall12 = Wall('red', 580, HEIGHT - 110, 20, 100, './image/wall_red_vertical.png')
	add_obj(wall12, 'wall')
	wall13 = Wall('red', 520, HEIGHT - 370, 60, 20, './image/wall_red.png')
	add_obj(wall13, 'wall')
	wall14 = Wall('red', 420, HEIGHT - 490, 80, 20, './image/wall_red.png')
	add_obj(wall14, 'wall')
 
	wall15 = Wall('blue', 585, HEIGHT - 590, 15, 240, './image/wall_blue_vertical.png')
	add_obj(wall15, 'wall')
	wall16 = Wall('blue', 230, HEIGHT - 128, 270, 15, './image/wall_blue.png')
	add_obj(wall16, 'wall')
	wall17 = Wall('blue', 500, HEIGHT - 230, 15, 100, './image/wall_blue_vertical.png')
	add_obj(wall17, 'wall')
 
	# planes
	plane1 = Plane(610, HEIGHT - 370, 1, 80, 20, './image/plane.jpg')
	add_obj(plane1,  'plane')
	plane2 = Plane(580, HEIGHT - 130, 2, 110, 20, './image/plane.jpg')
	add_obj(plane2,  'plane')
	plane3 = Plane(100, HEIGHT - 350, 3, 20, 100, './image/plane_vertical.png')
	add_obj(plane3,  'plane')
	plane4 = Plane(400, HEIGHT - 590, 4, 20, 120, './image/plane_vertical.png')
	add_obj(plane4,  'plane')
 
 	# waters
	water1 = Water('red', 0, HEIGHT - 15, 100, 15, './image/water_red.png')
	add_obj(water1, 'water')
	#water2 = Water('red', 350, HEIGHT - 15, 100, 15, './image/water_red.png')
	#add_obj(water2, 'water')
	water2 = Water('red', 350, HEIGHT - 15, 50, 15, './image/water_red.png')
	add_obj(water2, 'water')
 
 	# doors
	door1 = Door(150, HEIGHT - 470, False, 80, 100, 1, './image/door_close.png', './image/door_open1.png', './image/door_open2.png', './image/door_open3.png', 'right', 10)
	add_obj(door1, 'door')
	door6 = Door(200, HEIGHT - 350, False, 80, 100, 6, './image/door_close.png', './image/door_open1.png', './image/door_open2.png', './image/door_open3.png', 'right', 10)
	add_obj(door6, 'door')
	door7 = Door(450, HEIGHT - 350, False, 80, 100, 7, './image/door_close.png', './image/door_open1.png', './image/door_open2.png', './image/door_open3.png', 'right', 10)
	add_obj(door7, 'door')
	door8 = Door(480, HEIGHT - 470, False, 80, 100, 8, './image/door_close.png', './image/door_open1.png', './image/door_open2.png', './image/door_open3.png', 'right', 10)
	add_obj(door8, 'door')
 
	# windows
	window2 = Door(100, HEIGHT - 130, True, 60, 20, 2, './image/window_close.png', './image/window_open1.png', './image/window_open2.png', './image/window_open3.png', 'up', 10)
	add_obj(window2, 'door')
	#window3 = Door(230, HEIGHT - 130, True, 60, 20, 3, './image/window_close.png', './image/window_open1.png', './image/window_open2.png', './image/window_open3.png', 'up', 10)
	#add_obj(window3, 'door')
	window4 = Door(20, HEIGHT - 490, False, 60, 20, 4, './image/window_close.png', './image/window_open1.png', './image/window_open2.png', './image/window_open3.png', 'up', 10)
	add_obj(window4, 'door')
	window5 = Door(520, HEIGHT - 370, False, 60, 20, 5, './image/window_close.png', './image/window_open1.png', './image/window_open2.png', './image/window_open3.png', 'up', 10)
	add_obj(window5, 'door')
 
	diamond1 = Diamond('red', 320, HEIGHT - 270, 30, 20, './image/diamond_red.png')
	add_obj(diamond1, 'diamond')
	diamond2 = Diamond('blue', 50, HEIGHT - 150, 30, 20, './image/diamond_blue.png')
	add_obj(diamond2, 'diamond')
 
	def b1activate(objs):
		moveplane(objs.plane, 1, objs.player, 610, HEIGHT - 490, 0, -2)
	def b1deactivate(objs):
		moveplane(objs.plane, 1, objs.player, 610, HEIGHT - 370, 0, 2)
	button1 = Button(500, HEIGHT - 30, b1activate, b1deactivate, 30, 20, './image/button_unpressed.png', './image/button_pressed.png')
	add_obj(button1, 'button')
	def b2activate(objs):
		moveplane(objs.plane, 2, objs.player, 10, HEIGHT - 130, -5, 0)
		opendoor(objs.door, 6, 1)
	def b2deactivate(objs):
		moveplane(objs.plane, 2, objs.player, 580, HEIGHT - 130, 5, 0)
		closedoor(objs.door, 6, objs.player, 1)
	button2 = Button(700, HEIGHT - 150, b2activate, b2deactivate, 30, 20, './image/button_unpressed.png', './image/button_pressed.png')
	add_obj(button2, 'button')
	def b3activate(objs):
		opendoor(objs.door, 1, 1)
	def b3deactivate(objs):
		closedoor(objs.door, 1, objs.player, 1)
	button3 = Button(735, HEIGHT - 510, b3activate, b3deactivate, 30, 20, './image/button_unpressed.png', './image/button_pressed.png')
	add_obj(button3, 'button')
	def b4activate(objs):
		closedoor(objs.door, 2, objs.player, 5)
	def b4deactivate(objs):
		opendoor(objs.door, 2, 1)
	button4 = Button(150, HEIGHT - 30, b4activate, b4deactivate, 30, 20, './image/button_unpressed.png', './image/button_pressed.png')
	add_obj(button4, 'button')
	def b5activate(objs):
		moveplane(objs.plane, 3, objs.player, 100, HEIGHT - 230, 0, 2)
		opendoor(objs.door, 4, 1)
	def b5deactivate(objs):
		moveplane(objs.plane, 3, objs.player, 100, HEIGHT - 350, 0, -2)
		closedoor(objs.door, 4, objs.player, 1)
	button5 = Button(190, HEIGHT - 150, b5activate, b5deactivate, 30, 20, './image/button_unpressed.png', './image/button_pressed.png')
	add_obj(button5, 'button')
	#def b6activate(objs):
	#	closedoor(objs.door, 3, objs.player, 5)
	#def b6deactivate(objs):
	#	opendoor(objs.door, 3, 1)
	#button6 = Button(270, HEIGHT - 30, b6activate, b6deactivate, 30, 20, './image/button_unpressed.png', './image/button_pressed.png')
	#add_obj(button6, 'button')
	def b7activate(objs):
		opendoor(objs.door, 5, 1)
	def b7deactivate(objs):
		closedoor(objs.door, 5, objs.player, 1)
	button7 = Button(535, HEIGHT - 270, b7activate, b7deactivate, 30, 20, './image/button_unpressed.png', './image/button_pressed.png')
	add_obj(button7, 'button')
	def b8activate(objs):
		opendoor(objs.door, 8, 1)
	def b8deactivate(objs):
		closedoor(objs.door, 8, objs.player, 1)
	button8 = Button(420, HEIGHT - 390, b8activate, b8deactivate, 30, 20, './image/button_unpressed.png', './image/button_pressed.png')
	add_obj(button8, 'button')
	def b9activate(objs):
		opendoor(objs.door, 7, 1)
		moveplane(objs.plane, 4, objs.player, 320, HEIGHT - 590, -3, 0)
		moveplane(objs.plane, 3, objs.player, 100, HEIGHT - 350, 0, -2)
	def b9deactivate(objs):
		closedoor(objs.door, 7, objs.player, 1)
	button9 = Button(390, HEIGHT - 270, b9activate, b9deactivate, 30, 20, './image/button_unpressed.png', './image/button_pressed.png')
	add_obj(button9, 'button')
 
	destination_blue = Destination('blue', 820, HEIGHT - 90, 60, 80, './image/cup_without_water.png', './image/cup_with_water.png', './image/cup_with_iceman.png')
	add_obj(destination_blue, 'destination')
	destination_red = Destination('red', 830, HEIGHT - 590, 40, 100, './image/torch_without_fire.png', './image/torch_with_fire.png')
	add_obj(destination_red, 'destination')
 
	iceman = Player(100, HEIGHT - 590, 'blue', './image/iceman.png', './image/iceman_move.png', 50, 90)
	add_obj(iceman, 'player')
	fireman = Player(50, HEIGHT - 590, 'red', './image/fireman.png', './image/fireman_move.png', 50, 90)
	add_obj(fireman, 'player')
 
def start_game(level):
	game_rule, game_rule_rect = write('GAME RULE', 70, 0, HEIGHT / 2 + 50)
	game_rule1, game_rule1_rect = write('1. Eat all the Diamonds', 40, 0, HEIGHT / 2 + 100)
	game_rule2, game_rule2_rect = write('2. Reach the Destinations', 40, 15, HEIGHT / 2 + 140)
	game_rule3, game_rule3_rect = write('3. YOU WIN!!', 40, -73, HEIGHT / 2 + 180)
	press_1, press_1_rect = write('-- press      to play level 1 --', 40, -225, HEIGHT / 2 + 250)
	letter_1, letter_1_rect = write('1', 50, -284, HEIGHT / 2 + 249, None, (255, 69, 0))
	press_2, press_2_rect = write('-- press      to play level 2 --', 40, 220, HEIGHT / 2 + 250)
	letter_2, letter_2_rect = write('2', 50, 161, HEIGHT / 2 + 249, None, (0, 128, 0))
	information_message, information_message_rect = write('-- press      for more information --', 40, -180, HEIGHT / 2 + 280)
	I_letter, I_letter_rect = write('I', 50, -284, HEIGHT / 2 + 279, None, (176, 96, 225))
	quit_ending_message, quit_ending_message_rect = write('-- press      to Quit --', 40, 268, HEIGHT / 2 + 280)
	Q_letter, Q_letter_rect = write('Q', 50, 259, HEIGHT / 2 + 279, None, (255, 69, 0))
 
	starting_page_img = pygame.transform.scale(starting_page.convert_alpha(), (WIDTH, HEIGHT))
	counter = 0
	if level == 1:
		init_obj_1()
	elif level == 2:
		init_obj_2()
 
	while level == 0:
		clock.tick(FPS)
		counter += 1
		key_pressed = pygame.key.get_pressed()
		for event in pygame.event.get():
			if key_pressed[pygame.K_1]:
				init_obj_1()
				level = 1
			elif key_pressed[pygame.K_2]:
				init_obj_2()
				level = 2
			elif key_pressed[pygame.K_q]:
				end_game()
			elif key_pressed[pygame.K_i]:
				more_information()
		screen.blit(starting_page_img, (0, 0))
		screen.blit(game_rule, game_rule_rect)
		screen.blit(game_rule1, game_rule1_rect)
		screen.blit(game_rule2, game_rule2_rect)
		screen.blit(game_rule3, game_rule3_rect)
		if counter % FPS >= FPS / 3:
			screen.blit(press_1, press_1_rect)
			screen.blit(press_2, press_2_rect)
			screen.blit(letter_1, letter_1_rect)
			screen.blit(letter_2, letter_2_rect)
			screen.blit(information_message, information_message_rect)
			screen.blit(I_letter, I_letter_rect)
			screen.blit(quit_ending_message, quit_ending_message_rect)
			screen.blit(Q_letter, Q_letter_rect)
		pygame.display.update()
	run_game(level)
 
def run_game(level):
	global isend
	pygame.mixer.music.load('./music/theme_song.mp3')
	pygame.mixer.music.play(-1, 0)
	background_img = pygame.transform.scale(raw_background.convert_alpha(), (WIDTH, HEIGHT))
	information_button_img = pygame.transform.scale(information_button.convert_alpha(), (30, 30))
	running = True
	time_start = time.time()
 
	while running:
		clock.tick(FPS)
		# get input
		for event in pygame.event.get():
			key_pressed = pygame.key.get_pressed()
			if event.type == pygame.QUIT or key_pressed[pygame.K_q]:
				end_game()
			if key_pressed[pygame.K_i]:
				more_information()
			# if key_pressed[pygame.K_q]:
			# 	time_taken = time.time() - time_start
			# 	win(time_taken, level)
 
		# update the game
		for player in objs.player:
			player.update(objs)
 
		for door in objs.door:
			door.update()
 
		for button in objs.button:
			button.check(objs.player)
 
		for water in objs.water:
			water.kill(objs.player)
 
		for cloud in objs.cloud:
			cloud.moving()
 
		for destination in objs.destination:
			destination.win(objs.player)
 
		if len(objs.diamond) == 0:
			win_game = True
			for destination in objs.destination:
				if destination.iswin == False:
					win_game = False
					break
			if win_game == True:
				time_taken = time.time() - time_start
				win(time_taken, level)
 
		if isend:
			isend = False
			pygame.mixer.music.load('./music/die.mp3')
			pygame.mixer.music.play(0, 0)
			replay()
			return
 
 
		# display the screen
		screen.blit(background_img, (0, 0))
		all_sprite.draw(screen)
		screen.blit(information_button_img, (10, 10))
		pygame.display.update()
 
def replay():
	background_darken_img = pygame.transform.scale(raw_background_darken.convert_alpha(), (WIDTH, HEIGHT))
	black_transparent_img = pygame.transform.scale(raw_black_transparent.convert_alpha(), (WIDTH + 10, HEIGHT + 10))
	restart = False
	color_fill = 0
	counter = 0
	while not restart:
		counter += 1
		if color_fill < 255:
			color_fill += 1
		failing_message, failing_message_rect = write('Failed', 70, 0, HEIGHT / 2, 'arial', (color_fill, 0, 0))
		press_key_to_replay, press_key_to_replay_rect = write('-- press any key to replay --', 40, 0, HEIGHT / 2 + 60, None, (150, 150, 150))
		for event in pygame.event.get():
			key_pressed = pygame.key.get_pressed()
			if event.type == pygame.KEYDOWN and color_fill == 255:
				restart = True
			# if key_pressed[pygame.K_q] and color_fill == 255:
			# 	restart = True
		screen.fill(WHITE)
		screen.blit(background_darken_img, (0, 0))
		all_sprite.draw(screen)
		screen.blit(black_transparent_img, (-5, -5))
		screen.blit(failing_message, failing_message_rect)
		if counter % (FPS * 3) >= FPS:
			screen.blit(press_key_to_replay, press_key_to_replay_rect)
		pygame.display.update()
	start_game(0)
 
def more_information():
 
	horizontal_shift = -20
 
	more_information_message, more_information_message_rect = write('MORE INFORMATION', 70, -10, 70 + horizontal_shift)
	diamond_message, diamond_message_rect = write('1. You can only eat diamonds with the same color as yours', 40, -3, 120 + horizontal_shift)
	wall_message1, wall_message1_rect = write('2. You cannot go through walls different from your color', 40, -18, 160 + horizontal_shift)
	wall_message2, wall_message2_rect = write('3. You can stand on walls different from your color', 40, -55, 200 + horizontal_shift)
	button_message, button_message_rect = write('4. You have to stand on the button to open doors or windows', 40, 13, 240 + horizontal_shift)
 
	warning_message, warning_message_rect = write('WARNING', 70, 0, 320 + horizontal_shift)
	water_message, water_message_rect = write("1. Stand on different color's water will send you to heaven", 40, -2, 370 + horizontal_shift)
	plane_message1, plane_message1_rect = write('2. Stand between a moving plane and other object will', 40, -25, 410 + horizontal_shift)
	plane_message2, plane_message2_rect = write('squeeze you to death', 40, -214, 450 + horizontal_shift)
	door_message, door_message_rect = write('3. A shutting door will also squeeze you to death', 40, -57, 490 + horizontal_shift)
 
	feel_free_message, feel_free_message_rect = write('BTW, falling from any height will not cause injury', 40, 0, 535)
	back_message, back_message_rect = write('-- press      to go back the game --', 40, -190, 570)
	B_letter, B_letter_rect = write('B', 50, -287, 569, None, (176, 96, 225))
	quit_ending_message, quit_ending_message_rect = write('-- press      to Quit --', 40, 250, 570)
	Q_letter, Q_letter_rect = write('Q', 50, 240, 569, None, (255, 69, 0))
 
	counter = 0
	while True:
		clock.tick(FPS)
		counter += 1
		for event in pygame.event.get():
			key_pressed = pygame.key.get_pressed()
			if key_pressed[pygame.K_b]:
				return
			if key_pressed[pygame.K_q]:
				end_game()
		screen.fill(BLUE)
		screen.blit(more_information_message, more_information_message_rect)
		screen.blit(diamond_message, diamond_message_rect)
		screen.blit(wall_message1, wall_message1_rect)
		screen.blit(wall_message2, wall_message2_rect)
		screen.blit(button_message, button_message_rect)
		screen.blit(warning_message, warning_message_rect)
		screen.blit(water_message, water_message_rect)
		screen.blit(plane_message1, plane_message1_rect)
		screen.blit(plane_message2, plane_message2_rect)
		screen.blit(door_message, door_message_rect)
		screen.blit(feel_free_message, feel_free_message_rect)
		if counter % FPS >= FPS / 3:
			screen.blit(back_message, back_message_rect)
			screen.blit(B_letter, B_letter_rect)
			screen.blit(quit_ending_message, quit_ending_message_rect)
			screen.blit(Q_letter, Q_letter_rect)
		pygame.display.update()
 
 
def win(time_taken, level):
	global objs
 
	quit_ending_message, quit_ending_message_rect = write('-- press      to Quit --', 40, 0, HEIGHT / 2 + 245)
	Q_letter, Q_letter_rect = write('Q', 50, -10, HEIGHT / 2 + 244, None, (255, 69, 0))
	restart_ending_message, restart_ending_message_rect = write('-- press      to Restart --', 40, 0, HEIGHT / 2 + 280)
	R_letter, R_letter_rect = write('R', 50, -30, HEIGHT / 2 + 279, None, (0, 128, 0))
	time_message, time_message_rect = write('Time:', 60, -55, HEIGHT / 2 + 200)
 
	background_img = pygame.transform.scale(raw_background.convert_alpha(), (WIDTH, HEIGHT))
	winning_page_img = pygame.transform.scale(winning_page.convert_alpha(), (WIDTH, HEIGHT * 4 / 5))	
	time_interval = 180  # time_interval / FPS = seconds
 
	# destination animation
	pygame.mixer.music.load('./music/touch_torch.mp3')
	for i in range(time_interval):
		clock.tick(FPS)
		if i == 60:
				pygame.mixer.music.play(0, 0)
		for destination in objs.destination:
			if destination.img_win2 == None:
				if i >= time_interval * 4 / 10:
					destination.image = destination.img_win
			else:
				if i >= time_interval * 4 / 10:
					destination.image = destination.img_win2
				elif i >= time_interval * 3 / 10:
					destination.image = destination.img_win
		screen.blit(background_img, (0, 0))
		all_sprite.draw(screen)
		pygame.display.update()
 
	if level != total_level:
		start_game(level + 1)
		return
	counter = 0
	pygame.mixer.music.load('./music/win.mp3')
	pygame.mixer.music.play(0, 0)
	while True:
		clock.tick(FPS)
		counter += 1
		for event in pygame.event.get():
			key_pressed = pygame.key.get_pressed()
			if key_pressed[pygame.K_r]:
				start_game(0)
				return
			elif key_pressed[pygame.K_q] or event.type == pygame.QUIT:
				end_game()
			elif key_pressed[pygame.K_1]:
				start_game(1)
				return
			elif key_pressed[pygame.K_2]:
				start_game(2)
				return
		time, time_rect = write('{:.2f}'.format(time_taken), 60, 50 + 10 * math.log10(time_taken), HEIGHT / 2 + 200)
		screen.fill(BLUE)
		screen.blit(winning_page_img, (0, 0))
		screen.blit(time_message, time_message_rect)
		screen.blit(time, time_rect)
		if counter % FPS >= FPS / 3:
			screen.blit(quit_ending_message, quit_ending_message_rect)
			screen.blit(restart_ending_message, restart_ending_message_rect)
			screen.blit(Q_letter, Q_letter_rect)
			screen.blit(R_letter, R_letter_rect)
		pygame.display.update()
 
def end_game():
	pygame.quit()
	sys.exit()
 
start_game(0)