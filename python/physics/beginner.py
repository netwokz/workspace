import pygame
import pymunk
import pymunk.pygame_util
import math

pygame.init()
WIDTH = 1000
HEIGHT = 800

window = pygame.display.set_mode((WIDTH, HEIGHT))

def draw(space, window, draw_options):
    window.fill("white")
    space.debug_draw(draw_options)
    pygame.display.update()

def create_boundries(space, width, height):
    rects = [
        [(width/2, height - 10), (width, 20)],
        [(width/2, 10), (width, 20)],
        [(10, height/2), (20, height)],
        [(width - 10, height/2), (20, height)],
    ]
    
    for pos, size in rects:
        body = pymunk.Body(body_type=pymunk.Body.STATIC)
        body.position = pos
        shape = pymunk.Poly.create_box(body, size)
        shape.elasticity = 0.4
        shape.friction = 0.5
        space.add(body, shape)

def create_ball(space, radius, mass, color):
    body = pymunk.Body()
    body.position = (300,300)
    shape = pymunk.Circle(body,radius)
    shape.mass = mass
    shape.color = color
    shape.elasticity = 0.9
    shape.friction = 0.3
    space.add(body, shape)
    return shape

def run(window, width, height):
    run = True
    clock = pygame.time.Clock()
    fps = 60
    dt = 1 / fps
    
    space = pymunk.Space()
    space.gravity = (0, 981)
    
    ball = create_ball(space,30,10,(255,0,0,255))
    create_boundries(space,width,height)
    
    draw_options = pymunk.pygame_util.DrawOptions(window)
    
    while run:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                ball.body.apply_impulse_at_local_point((10000, 0), (0, 0))
        
        draw(space, window,draw_options)
        space.step(dt)
        clock.tick(fps)
        
        
if __name__ == "__main__":
    run(window,WIDTH,HEIGHT)