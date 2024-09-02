# Imports
import sys

import pm
import pygame
import ctypes

from pygame.examples.moveit import WIDTH, HEIGHT

window = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
pygame.display.set_caption('DrawKei 1.0')  # Başlığı buradan değiştirin

# Load and set the icon
icon = pygame.image.load('icon.png')  # Burada 'icon.png' dosya adınız olmalı
pygame.display.set_icon(icon)

# Increas Dots Per inch so it looks sharper
ctypes.windll.shcore.SetProcessDpiAwareness(True)

# Pygame Configuration
pygame.init()
fps = 300
fpsClock = pygame.time.Clock()
width, height = 640, 480
screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)

font = pygame.font.SysFont('Arial', 20)

# Variables

# Our Buttons will append themself to this list
objects = []

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)

# Initial color
drawColor = [0, 0, 0]

# Initial brush size
brushSize = 30
brushSizeSteps = 3

# Drawing Area Size
canvasSize = [800, 800]

# Button Class
class Button():
    def __init__(self, x, y, width, height, buttonText='Button', onclickFunction=None, onePress=False):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.onclickFunction = onclickFunction
        self.onePress = onePress

        self.fillColors = {
            'normal': '#ffffff',
            'hover': '#666666',
            'pressed': '#333333',
        }

        self.buttonSurface = pygame.Surface((self.width, self.height))
        self.buttonRect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.buttonSurf = font.render(buttonText, True, (20, 20, 20))

        self.alreadyPressed = False

        objects.append(self)

    def process(self):

        mousePos = pygame.mouse.get_pos()

        self.buttonSurface.fill(self.fillColors['normal'])
        if self.buttonRect.collidepoint(mousePos):
            self.buttonSurface.fill(self.fillColors['hover'])

            if pygame.mouse.get_pressed(num_buttons=3)[0]:
                self.buttonSurface.fill(self.fillColors['pressed'])

                if self.onePress:
                    self.onclickFunction()

                elif not self.alreadyPressed:
                    self.onclickFunction()
                    self.alreadyPressed = True

            else:
                self.alreadyPressed = False

        self.buttonSurface.blit(self.buttonSurf, [
            self.buttonRect.width/2 - self.buttonSurf.get_rect().width/2,
            self.buttonRect.height/2 - self.buttonSurf.get_rect().height/2
        ])
        screen.blit(self.buttonSurface, self.buttonRect)

# Handler Functions

# Changing the Color
def changeColor(color):
    global drawColor
    drawColor = color

# Changing the Brush Size
def changebrushSize(dir):
    global brushSize
    if dir == 'greater':
        brushSize += brushSizeSteps
    else:
        brushSize -= brushSizeSteps

# Save the surface to the Disk
def save():
    pygame.image.save(canvas, "canvas.png")

# Button Variables.
buttonWidth = 120
buttonHeight = 35

# Colors
colors = {
    'Black': BLACK,
    'White': WHITE,
    'Red': RED,
    'Green': GREEN,
    'Blue': BLUE,
    'Yellow': YELLOW,
    'Cyan': CYAN,
    'Magenta': MAGENTA,
    'Orange': ORANGE,
    'Purple': PURPLE
}

# Changing the Color
def changeColor(color):
    global drawColor
    drawColor = color

# Buttons and their respective functions
buttons = [
    ['Siyah', lambda: changeColor(BLACK)],
    ['Beyaz', lambda: changeColor(WHITE)],
    ['Kırmızı', lambda: changeColor(RED)],
    ['Yeşil', lambda: changeColor(GREEN)],
    ['Mavi', lambda: changeColor(BLUE)],
    ['Sarı', lambda: changeColor(YELLOW)],
    ['Turkuaz', lambda: changeColor(CYAN)],
    ['Pembe', lambda: changeColor(MAGENTA)],
    ['Turuncu', lambda: changeColor(ORANGE)],
    ['Mor', lambda: changeColor(PURPLE)],
    ['Fırçayı Büyült', lambda: changebrushSize('greater')],
    ['Fırçayı Küçült', lambda: changebrushSize('smaller')],
    ['Kaydet', save],
]

# Making the buttons
for index, buttonName in enumerate(buttons):
    Button(index * (buttonWidth + 10) + 10, 10, buttonWidth,
           buttonHeight, buttonName[0], buttonName[1])

# Canvas
canvas = pygame.Surface(canvasSize)
canvas.fill((255, 255, 255))

# Game loop.
while True:
    screen.fill((30, 30, 30))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Save current canvas state before drawing
    if pygame.mouse.get_pressed()[0]:
        mx, my = pygame.mouse.get_pos()

        # Calculate Position on the Canvas
        dx = mx - x / 2 + canvasSize[0] / 2
        dy = my - y / 2 + canvasSize[1] / 2

        # Add current canvas state to history
        pygame.draw.circle(
            canvas,
            drawColor,
            [dx, dy],
            brushSize,
        )

    # Drawing the Buttons
    for object in objects:
        object.process()

    # Draw the Canvas at the center of the screen
    x, y = screen.get_size()
    screen.blit(canvas, [x / 2 - canvasSize[0] / 2, y / 2 - canvasSize[1] / 2])

    pygame.display.flip()
    fpsClock.tick(fps)


