import ctypes
import os
import turtle
from PIL import ImageGrab

try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except Exception:
    try:
        ctypes.windll.user32.SetProcessDPIAware()
    except Exception:
        pass  
screen = turtle.Screen()
screen.setup(800, 600)

rocket = turtle.Turtle()
rocket.speed(0)
rocket.penup()
rocket.fillcolor('grey')
X_SCALE = 15
Y_COEFF = 0.01
START_X = -5
END_X = 5
start_y = 25 - Y_COEFF * (START_X * X_SCALE) ** 2 + 200
rocket.goto(START_X * X_SCALE, start_y)
rocket.pendown()
rocket.begin_fill()
for x in range(START_X, END_X + 1):
    pixel_x = x * X_SCALE
    pixel_y = 25 - Y_COEFF * (pixel_x**2) + 200
    rocket.goto(pixel_x, pixel_y)
rocket.goto(pixel_x, -100)
rocket.goto(-1 * pixel_x, -100)
rocket.goto(-1 * pixel_x, pixel_y)
rocket.end_fill()
rocket.fillcolor('red')
rocket.goto(-1 * pixel_x, -100)
rocket.begin_fill()
rocket.goto(-1 * pixel_x - 50, -200)
rocket.goto(pixel_x + 50, -200)
rocket.goto(pixel_x, -100)
rocket.end_fill()
rocket.hideturtle()
screen.update()
canvas = screen.getcanvas()
x = canvas.winfo_rootx()
y = canvas.winfo_rooty()
w = canvas.winfo_width()
h = canvas.winfo_height()

img = ImageGrab.grab(bbox=(x, y, x + w, y + h))
img.save('israeli_rocket.gif', 'GIF')
img.close()
screen.clearscreen()
