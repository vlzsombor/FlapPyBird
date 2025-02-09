# import pygame
 
# pygame.init()
# screen = pygame.display.set_mode((400, 300))
# done = False
# red = (255,0,0)
# green = (0,255,0)
# blue = (0,0,255)
# white = (255,255,255)
# i = 0
# while not done:

#    screen.fill(blue)

#    for event in pygame.event.get():
#       if event.type == pygame.QUIT:
#          done = True
#    c = white

#    b = pygame.draw.circle(screen, c, (90,180), 60)
#    if i < 5 or i >20:
#       c = green
#       b = pygame.draw.circle(screen, c, (90,180), 60)
#       pygame.display.update()

#    # else:
#    #    pygame.draw.circle(screen, red, (90,180), 60+20)
#    pygame.display.update(b)

#    clock=pygame.time.Clock()
#    clock.tick((1))

#    rotated_image = pygame.transform.rotate(self.image, self.rot)
#    rotated_rect = rotated_image.get_rect(center=self.rect.center)
#    screen.blit(rotated_image, rotated_rect)    

#    i+=1

#    if i == 100:
#       pygame.quit()


import random
import pygame

pygame.init()
screen = pygame.display.set_mode((400, 300))
pygame.display.set_caption("Blit Example")

# Load an image (Make sure you have 'example.png' in the same directory)
imageBird = pygame.image.load("assets/sprites/redbird-upflap.png")
imagePipe = pygame.image.load("assets/sprites/pipe-red.png")
clock=pygame.time.Clock()

running = True
while running:

   screen.fill((0,0,0))


   for event in pygame.event.get():
      if event.type == pygame.QUIT:
         running = False


   for i in range(10):
      screen.blit(imageBird, (random.randrange(0,100), random.randrange(0,200)))  # Draw image at position (100, 50)

      #pygame.display.update()


   screen.blit(imagePipe, (100, 50))  # Draw image at position (100, 50)
   
   pygame.display.update()
   
   clock.tick((1))

pygame.quit()
