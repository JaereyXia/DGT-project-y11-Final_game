from data import *


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.image = pygame.image.load(join('image', '0.png')).convert_alpha()
        self.rect = self.image.get_rect(center=pos)

        self.direction = pygame.Vector2()
        self.speed = 500

    def input(self):
        keys = pygame.key.get_pressed()
        #通过int()将按键转换为1(触发)和0(不触发)后减去K_right和K_left得到1或0
        """
        假设: 按下了K_right “int(keys[pygame.K_RIGHT])” = 1
        1-0=1 Vector2(1,0)
        假设: 按下了K_right “int(keys[pygame.K_LEFT])” = 1
        0-1=-1 Vector2(-1,0)      
        """
        self.direction.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
        self.direction.y = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])
        """
        如果self.direction发现正在按K_right和K_left按键，则用normalize将他们的变量变成1，
        否则Survivor的速度在斜着走时速度会比横竖着走时快 
        """
        #self.direction = self.direction.normalize() if self.direction else self.direction

    def move(self, dt):
        self.rect.center += self.direction * self.speed * dt

    def update(self, dt):
        self.input()
        self.move(dt)