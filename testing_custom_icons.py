import turtle
from PIL import Image, ImageTk

screen = turtle.Screen()
screen.setup(600, 600) 
screen.title("Rocket Simulation")

pil_image1 = Image.open("enemy rocket.gif")
resized_pil1 = pil_image1.resize((40, 40)) 
tk_image1 = ImageTk.PhotoImage(resized_pil1)
screen.addshape("enemy rocket", turtle.Shape("image", tk_image1))


pil_image2 = Image.open("israeli_rocket.gif")
resized_pil2 = pil_image2.resize((40, 40)) 
tk_image2 = ImageTk.PhotoImage(resized_pil2)
screen.addshape("israeli_rocket", turtle.Shape("image", tk_image2))

enemy = turtle.Turtle()
enemy.shape("enemy rocket")
enemy.penup()
enemy.goto(-200, 0)  
israeli = turtle.Turtle()
israeli.shape("israeli_rocket")
israeli.penup()
israeli.goto(200, 0)   
turtle.done()
