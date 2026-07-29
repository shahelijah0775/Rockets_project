import turtle
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
star = turtle.Turtle()
star.fillcolor('orange')
star.begin_fill()
for _ in range(17):
    star.left(78.75)
    star.fd(50)
    star.right(157.5)
    star.fd(50)
star.end_fill()
star.hideturtle()
screen.update()
canvas = screen.getcanvas()
x = canvas.winfo_rootx()
y = canvas.winfo_rooty()
w = canvas.winfo_width()
h = canvas.winfo_height()

img = ImageGrab.grab(bbox=(x, y, x + w, y + h))
img.save('blow_icon.gif', 'GIF')
img.close()
screen.clearscreen()
