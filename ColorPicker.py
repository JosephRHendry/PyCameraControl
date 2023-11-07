# Code adapted from: https://stackoverflow.com/questions/73517832/how-to-make-an-color-picker-in-pygame
import pygame

# 2 - Define constants 
BLACK = (0, 0, 0)
GRAY = (230, 230, 230)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
TEAL = (0, 255, 255)
PURPLE = (255, 0, 255)

class ColorPicker:
    def __init__(self, x, y, w, h, surf):
        self.rect = pygame.Rect(x, y, w, h)
        self.image = pygame.Surface((w, h))
        self.image.fill(GRAY)
        self.rad = h//2
        self.pwidth = w-self.rad*2
        self.surf = surf
        for i in range(self.pwidth):
            color = pygame.Color(0)
            color.hsla = (int(360*i/self.pwidth), 100, 50, 100)
            pygame.draw.rect(self.image, color, (i+self.rad, h//3, 1, h-2*h//3))
        self.p = 0

    def get_color(self):
        color = pygame.Color(0)
        color.hsla = (int(self.p * self.pwidth), 100, 50, 100)
        return color
    
    def get_rgb_color(self):
        color = pygame.Color(0)
        color.hsla = (int(self.p * self.pwidth), 100, 50, 100)
        color_rgb = {'R':color.r,
                     'G':color.g,
                     'B':color.b,
                     }
        return color_rgb

    def handleEvent(self, event):
        moude_buttons = pygame.mouse.get_pressed()
        mouse_pos = pygame.mouse.get_pos()
        if moude_buttons[0] and self.rect.collidepoint(mouse_pos):
            self.p = (mouse_pos[0] - self.rect.left - self.rad) / self.pwidth
            self.p = (max(0, min(self.p, 1)))
            return self.get_rgb_color()
        

    def draw(self):
        self.surf.blit(self.image, self.rect)
        center = self.rect.left + self.rad + self.p * self.pwidth, self.rect.centery
        pygame.draw.circle(self.surf, self.get_color(), center, self.rect.height // 2)

"""
pygame.init()
window = pygame.display.set_mode((500, 200))
clock = pygame.time.Clock()

cp = ColorPicker(50, 50, 400, 60)

run = True
while run:
    clock.tick(100)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False 

    cp.update()

    window.fill(0)
    cp.draw(window)
    pygame.display.flip()
    
pygame.quit()
exit()
"""
