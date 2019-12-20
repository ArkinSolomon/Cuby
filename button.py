import pygame

class Button(pygame.sprite.Sprite):

    def __init__(self, coords, w, h, text, size, screen):
        super(Button, self).__init__()

        self.screen = screen
        self.color = pygame.Color('lightgreen')
        self.text_color = pygame.Color('black')
        self.coords = coords

        self.font = pygame.font.SysFont('Comic Sans MS', size)
        self.text = self.font.render(text, False, (0, 0, 0))
        self.t = text

        self.image = pygame.Surface([w, h])
        self.image.fill(self.color)
        pygame.draw.rect(screen, self.color, [coords[0], coords[1], w, h])
        self.rect = self.image.get_rect()
        self.rect.x = coords[0]
        self.rect.y = coords[1]

    def check_click(self, mouse_x, mouse_y):
        return mouse_x > self.rect.left and mouse_x < self.rect.right and mouse_y > self.rect.top and mouse_y < self.rect.bottom

    def draw(self):
        self.screen.blit(self.image, self.rect)
        self.screen.blit(self.text, (self.coords[0] + ((self.rect.width / 2) - self.font.size(self.t)[0] / 2), self.coords[1] + ((self.rect.height / 2) - self.font.size(self.t)[1] / 2)))
