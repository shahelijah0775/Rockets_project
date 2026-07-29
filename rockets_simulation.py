import turtle
import math
from scipy import constants
import re
from sympy import symbols, Eq, solve, parse_expr
import os
from PIL import Image

ENEMY_IMAGE_OFFSET = -90  
ISRAELI_IMAGE_OFFSET = -90

script_dir = os.path.dirname(__file__)
icon_path_e = os.path.join(script_dir, "enemy rocket.gif")
icon_path_i = os.path.join(script_dir, "israeli_rocket.gif")
icon_path_e_small = os.path.join(script_dir, "enemy_rocket_small.gif")
icon_path_i_small = os.path.join(script_dir, "israeli_rocket_small.gif")
blow_path = os.path.join(script_dir, "blow_icon.gif")
TARGET_SIZE = (40, 40)

for src, dest in [(icon_path_e, icon_path_e_small), (icon_path_i, icon_path_i_small)]:
    if os.path.exists(src):
        with Image.open(src) as img:
            img_small = img.resize(TARGET_SIZE, Image.Resampling.LANCZOS)
            img_small.save(dest)
    else:
        print(f"Warning: {src} not found.")

screen = turtle.Screen()
screen.setup(width=1000, height=600)

def update_rocket_rotation(turt, base_image_path, angle_degrees, shape_name):
    if os.path.exists(base_image_path):
        with Image.open(base_image_path) as img:
            rotated_img = img.rotate(angle_degrees, resample=Image.Resampling.BICUBIC)
            temp_path = os.path.join(script_dir, f"temp_{shape_name}.gif")
            rotated_img.save(temp_path)
            screen.addshape(temp_path)
            turt.shape(temp_path)

enemy = turtle.Turtle()
enemy.color("red")
enemy.penup()
screen.addshape(blow_path)
params = {}
testing_file = os.path.join(script_dir, 'enemy_testing.txt')
if os.path.exists(testing_file):
    with open(testing_file, 'r') as epf:
        for line in epf:
            line = line.strip()
            if not line or '=' not in line:
                continue
            key, value = line.split('=')
            params[key.strip()] = float(value.strip())

x0 = params.get('x', 400.0)
v0 = params.get('v', 150.0)
angle = params.get('angle', 45.0)
latency = params.get('latency', 1.0)
a = params.get('a', 5.0)
g = constants.g

angle_rad = math.radians(angle)
cos_component = abs(math.cos(angle_rad))
sin_component = abs(math.sin(angle_rad))

def enemy_eq(t):
    x = x0 - (v0 * cos_component * t)
    y = (v0 * sin_component * t) + (0.5 * (a - g) * t**2)
    return x, y

def enemy_velocity(t):
    vx = -v0 * cos_component
    vy = v0 * sin_component + (a - g) * t
    return vx, vy

def solve_quadratic_from_string(equation_str):
    equation_str = equation_str.replace('^', '**')
    equation_str = re.sub(r'(\d+)([a-zA-Z])', r'\1*\2', equation_str)
    if '=' in equation_str:
        lhs_str, rhs_str = equation_str.split('=')
    else:
        lhs_str, rhs_str = equation_str, '0'
    lhs = parse_expr(lhs_str)
    rhs = parse_expr(rhs_str)
    equation = Eq(lhs, rhs)
    var = list(lhs.free_symbols) if lhs.free_symbols else symbols('t')
    roots = solve(equation, var)
    real_roots = [float(root) for root in roots if root.is_real and root > 0]
    return real_roots

def enemy_eq2str():
    v_comp = v0 * sin_component
    t2_comp = 0.5 * (a - g)
    return f"{v_comp}*t + {t2_comp}*t^2 = 0"

enemy_roots = solve_quadratic_from_string(enemy_eq2str())
max_t = max(enemy_roots) if enemy_roots else 10.0

t_impact = latency + (max_t - latency) / 2
t_travel_pro = t_impact - latency
x_impact, y_impact = enemy_eq(t_impact)

class Israeli(turtle.Turtle):
    def __init__(self, start_x, start_y):
        super().__init__()
        self.color("blue")
        self.penup()
        self.start_x = start_x
        self.start_y = start_y
        self.goto(start_x, start_y)
        self.ax = (2 * (x_impact - self.start_x)) / (t_travel_pro ** 2)
        self.ay = ((2 * (y_impact - self.start_y)) / (t_travel_pro ** 2)) + g

    def isr_eq(self, t):
        if t < latency:
            return self.start_x, self.start_y
        t_rel = t - latency
        x = self.start_x + 0.5 * self.ax * (t_rel ** 2)
        y = self.start_y + 0.5 * (self.ay - g) * (t_rel ** 2)
        return x, y

    def isr_velocity(self, t):
        if t < latency:
            return 0, 0
        t_rel = t - latency
        vx = self.ax * t_rel
        vy = (self.ay - g) * t_rel
        return vx, vy

israeli = Israeli(-400.0, 0.0)

enemy.goto(enemy_eq(0))
enemy.pendown()

dt = 0.05
current_t = 0.0

screen.tracer(0)
while current_t <= t_impact:
    ex, ey = enemy_eq(current_t)
    evx, evy = enemy_velocity(current_t)
    
    enemy_angle = math.degrees(math.atan2(evy, evx)) + ENEMY_IMAGE_OFFSET
    update_rocket_rotation(enemy, icon_path_e_small, enemy_angle, "enemy")
    enemy.goto(ex, ey)
    
    if current_t >= latency:
        israeli.pendown()
        px, py = israeli.isr_eq(current_t)
        ivx, ivy = israeli.isr_velocity(current_t)
        israeli_angle = math.degrees(math.atan2(ivy, ivx)) + ISRAELI_IMAGE_OFFSET
        update_rocket_rotation(israeli, icon_path_i_small, israeli_angle, "israeli")
        israeli.goto(px, py)
        
    screen.update()
    current_t += dt

screen.tracer(1)
screen.clearscreen()

blow = turtle.Turtle()
blow.hideturtle()
blow.penup()
blow.speed(0)
blow.pencolor("") 
blow.shape(blow_path)
blow.goto(x_impact, y_impact)
blow.showturtle()

writing = turtle.Turtle()
writing.hideturtle()
writing.penup()
writing.goto(-200, -100)
writing.write('Boom, we saved our nation from this rocket!', move=False, align='left', font=('Arial', 15, 'normal'))
turtle.done()

