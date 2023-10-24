from turtle import *

shape("turtle")
speed(0)

def tree(size, levels, angle):
    left(90)
    if levels == 0:
        color("green")
        dot(size * 0.75)
        color("black")
        return
    forward(size)
    right(angle)
    tree(size * 0.8, levels - 1, angle)
    
    left(angle * 2)
    
    tree(size * 0.8, levels - 1, angle)
    
    right(angle)
    backward(size)
# tree(70,5,30)

def draw_square(side,angle):
    forward(side)
    left(angle)
    forward(side)
    left(angle)
    forward(side)
    left(angle)
    forward(side)
    left(angle)
    forward(side)
    left(angle)
    forward(side)
    left(angle)
    forward(side)
    left(angle)
    forward(side)
# draw_square(100,45)

def create_snowflake_side(length, depth):
    if depth == 0:
        forward(length)
        return
    
    length /= 3.0
    create_snowflake_side(length, depth - 1)
    left(60)
    create_snowflake_side(length, depth - 1)
    right(120)
    create_snowflake_side(length, depth - 1)
    left(60)
    create_snowflake_side(length, depth - 1)

def create_snowflake(length, depth):
    for _ in range(depth):
        create_snowflake_side(length,depth)
        right(360 / depth)
    

create_snowflake(200, 4)
mainloop()