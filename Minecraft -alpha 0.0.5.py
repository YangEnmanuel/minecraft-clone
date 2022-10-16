import perlin_noise
from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

from perlin_noise import PerlinNoise
import random


app = Ursina()

class Block(Button):
    def __init__(self, position = (0,0,0), texture = 'white_cube'):
        super().__init__(
            parent = scene,
            position = position,
            model = 'cube',
            texture = texture,
            origin_y = 0.5,
            color = color.white,
            scale = 1
            
        )

    def input(self, key):
        
        if self.hovered:

            if key == 'right mouse down': block = Block(position = self.position + mouse.normal) 
               
            if key == 'left mouse down' : destroy(self)
               
            if key == 'escape': app.stop()
            
noise = PerlinNoise(octaves=3, seed=random.randint(1, 1000000))

for z in range(-20, 20):
    for x in range(-20, 20):
        y = noise([x * 0.02, z * 0.02])
        y = math.floor(y*7.5)
        block = Block(position = (x,y,z))

player = FirstPersonController(
    gravity = 1,
    jump_duration = .2,
    jump_height = 1.85,
    
    )

player.position = (5,0,5)

player.speed = 5 

window.borderless = False
window.fps_counter.visible = True
window.cog_button.enabled = False
window.exit_button.visible = False
window.vsync = True

app.run()  