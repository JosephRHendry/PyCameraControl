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

class SimpleSlider:
    def __init__(self, x, y, w, h, surf, bgColor=WHITE, sliderColor=BLACK, maxVal=255):
        self.rect = pygame.Rect(x, y, w, h)
        self.image = pygame.Surface((w, h))
        self.image.fill(GRAY)
        self.rad = h//2
        self.pwidth = w-self.rad*2
        self.surf = surf
        self.bgColor = bgColor
        self.sliderColor = sliderColor
        self.maxVal = maxVal
        for i in range(self.pwidth):
            pygame.draw.rect(self.image, self.bgColor, (i+self.rad, h//3, 1, h-2*h//3))
        self.p = 0

    def handleEvent(self, event):
        moude_buttons = pygame.mouse.get_pressed()
        mouse_pos = pygame.mouse.get_pos()
        if moude_buttons[0] and self.rect.collidepoint(mouse_pos):
            self.p = (mouse_pos[0] - self.rect.left - self.rad) / self.pwidth
            self.p = (max(0, min(self.p, 1)))
            colorVal = int(self.p * self.maxVal)
            return colorVal
    
    def draw(self):
        self.surf.blit(self.image, self.rect)
        center = self.rect.left + self.rad + self.p * self.pwidth, self.rect.centery
        pygame.draw.circle(self.surf, self.sliderColor, center, self.rect.height // 2)

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
