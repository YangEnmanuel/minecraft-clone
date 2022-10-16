# Import the game engine
from ursina import *

#Import a first person game pluggin
from ursina.prefabs.first_person_controller import FirstPersonController

from perlin_noise import PerlinNoise
import random

app = Ursina()

#Set the texture of every block
grass_texture = load_texture('assets/grass_block.png')
stone_texture = load_texture('assets/stone_block.png')
brick_texture = load_texture('assets/brick_block.png')
dirt_texture  = load_texture('assets/dirt_block.png')
sky_texture   = load_texture('assets/skybox.png')
arm_texture   = load_texture('assets/arm_texture.png')
punch_sound   = Audio('assets/punch_sound',loop = False, autoplay = False, volume = .7)
ambient_music = Audio('assets/music', loop = True, autoplay = True, volume = 5)


#Disable the FPS counter, the dot in the bottom of the screen and exit button (it will not be usefull)
window.fps_counter.enabled = True
window.fps_counter.color = color.black
window.exit_button.visible = False
window.borderless = False
window.title = 'Minecraft v-beta 0.1 by @yangenmanuel'
window.cog_button.enabled = False

player = FirstPersonController(
	gravity = .9,
    jump_duration = .2,
    jump_height = 1.85
)

block_pick = 1

#Defines wich block I have in my hand  !!! The update function is called automatically
def update():
	global block_pick 

	if held_keys['left mouse'] or held_keys['right mouse']:
		hand.active()
	else:
		hand.passive()

	if held_keys['1']: block_pick = 1
	if held_keys['2']: block_pick = 2
	if held_keys['3']: block_pick = 3
	if held_keys['4']: block_pick = 4


# The blocks class
class Block(Entity):
	def __init__(self, position = (0,0,0), texture = ('assets/grass_block.png')):
		super().__init__(
			parent = scene,
			position = position,
			model = 'assets/block',
			origin_y = 0.5,
			texture = texture,
			color = color.color(0,0,1),
			scale = 0.5,
			collider = 'mesh'
			)

	# Putting and destroying blocks
	def input(self, key):
		
		if self.hovered:
			if key == 'right mouse down':

				punch_sound.play()

				if block_pick == 1: block = Block(position = self.position + mouse.normal, texture = grass_texture)
				if block_pick == 2: block = Block(position = self.position + mouse.normal, texture = stone_texture)
				if block_pick == 3: block = Block(position = self.position + mouse.normal, texture = brick_texture)
				if block_pick == 4: block = Block(position = self.position + mouse.normal, texture = dirt_texture)

			if key == 'left mouse down':
				punch_sound.play()
				destroy(self)

			if key == 'escape': app.stop()
			
			# Speed changes with shift and ctrl
			if key == 'shift' : 
				player.speed += 5
				if player.speed > 10:
					player.speed =  5
			
			if key == 'control':
				player.speed -= 3
				if player.speed < 2:
					player.speed = 5


# Set the sky as a masive sphere
class Sky(Entity):
	def __init__(self):
		super().__init__(
			parent = scene,
			model = 'sphere',
			texture = sky_texture,
			scale = 150,
			double_sided = True,
			collider = 'mesh'
			)

# The hand of the player
class Hand(Entity):
	def __init__(self):
		super().__init__(
			parent = camera.ui,
			model = 'assets/arm',
			texture = arm_texture,
			scale = 0.2,
			rotation = Vec3(150, -7, 0),
			position = Vec2(0.4,-0.6))

	def active(self):
		self.position = Vec2(0.3,-0.5)

	def passive(self):
		self.position = Vec2(0.4,-0.6)

# Set the floor
noise = PerlinNoise(octaves=3, seed=random.randint(1, 1000000))

for z in range(-20, 20):
    for x in range(-20, 20):
        y = noise([x * 0.02, z * 0.02])
        y = math.floor(y*7.5)
        block = Block(position = (x,y,z))

player.position = (0,0,0)

sky = Sky()
hand = Hand()


app.run()