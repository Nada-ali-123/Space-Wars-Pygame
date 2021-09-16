# credit to Coding with Rus YouTube channel
import pygame

#image = pygame.image.load('assets/images/btn.png').convert_alpha()
class Button:
    def __init__(self, x, y, image, scalex, scaley):
        self.scalex = scalex
        self.scaley = scaley
        self.image = pygame.transform.scale((pygame.image.load(image)), (self.scalex, self.scaley))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False # button not clicked 

    def draw(self, surface):
        action = False

        #get x, y of cursor poaition
        pos = pygame.mouse.get_pos()

        # check if button is clicked
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True

        # can click again if needed
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        # draw btton on screen
        surface.blit(self.image, (self.rect.x, self.rect.y))

        return action
        
    def draw_no_img(self, win, font, color1, color2, text):

        pos = pygame.mouse.get_pos()

        # check if button is clicked
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True

        # can click again if needed
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
        # buuton elements
        pygame.draw.rect(win, color1, self.rect)
        pygame.draw.rect(win, color2, self.rect, 2)
        label =  font.render(text, 1, color2)
        # get width and height to center the text in the rect
        w =label.get_width()
        h = label.get_height()
        # draw button
        win.blit(label, (self.x + self.width//2 - w//2, self.y + self.height //2 -h // 2))

