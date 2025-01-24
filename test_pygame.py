import pygame
 
pygame.init()
screen = pygame.display.set_mode((400, 300))
done = False
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
white = (255,255,255)
while not done:
   for event in pygame.event.get():
      if event.type == pygame.QUIT:
         done = True
   pygame.draw.circle(screen, red, (90,180), 60+20)
   pygame.draw.circle(screen, white, (90,180), 60)
   pygame.display.update()