"""
Jerry Shi
11DGT
plan: Create a playable game that allows basic gameplay such as surviving on this island
"""

#imports
from settings import *
from player import Player
from sprites import *
from pytmx.util_pygame import load_pygame
from groups import AllSprites
from random import randint, choice

"""
In this game class, I want to create a playable interface where players can move around, shoot monsters and cause damage to them.
I need to create collision and terrain so that the player can't walk on the hills and the monsters can't cross the terrain.
"""

#The game class
class Game:

#all variable that will need for codeing will be put in this variable.
    def __init__(self):
        # setup
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Survivor')
        self.clock = pygame.time.Clock()
        self.running = True
        
        #startpage
        self.start = pygame.image.load(join('code', 'images', 'startpage', 'start.png'))
        self.play = pygame.image.load(join('code', 'images', 'startpage', 'player1.png'))
        self.play2 = pygame.image.load(join('code', 'images', 'startpage', 'player2.png'))
        self.play_DIFF = True
        

        #health
        self.health = 100
        self.health_cold_down_timer = 100
        self.health_cold_down = True
        self.hurt_timer = 0

        # groups 
        self.all_sprites = AllSprites()
        self.collision_sprites = pygame.sprite.Group()
        self.bullet_sprites = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()

        # gun timer
        self.can_shoot = True
        self.shoot_time = 0 
        self.gun_cooldown = 100

        # enemy timer as
        self.enemy_event = pygame.event.custom_type()
        pygame.time.set_timer(self.enemy_event, 300)
        self.spawn_positions = []
        
        # audio 
        self.shoot_sound = pygame.mixer.Sound(join('code', 'audio', 'shoot.wav'))
        self.shoot_sound.set_volume(0.2)
        self.impact_sound = pygame.mixer.Sound(join('code', 'audio', 'impact.ogg'))
        self.music = pygame.mixer.Sound(join('code', 'audio', 'music.wav'))
        self.music.set_volume(0.5)
        self.music.play(loops = -1)

        # setup
        self.load_images()
        self.setup()
        

    #set up a health timer so that they is cold down to moster dealing damege to the player, this make sure that player's collision can work normally
    def health_timer(self):
        if self.health_cold_down == False:
            current_time = pygame.time.get_ticks()
            if current_time - self.hurt_time - 100 >= self.health_cold_down:
                self.health_cold_down = True

    #load every images
    def load_images(self):
        self.bullet_surf = pygame.image.load(join('code', 'images', 'gun', 'bullet.png')).convert_alpha()

        folders = list(walk(join('code', 'images', 'enemies')))[0][1]
        self.enemy_frames = {}
        for folder in folders:
            for folder_path, _, file_names in walk(join('code', 'images', 'enemies', folder)):
                self.enemy_frames[folder] = []
                for file_name in sorted(file_names, key = lambda name: int(name.split('.')[0])):
                    full_path = join(folder_path, file_name)
                    surf = pygame.image.load(full_path).convert_alpha()
                    self.enemy_frames[folder].append(surf)

    #gun shot
    def input(self):
        if pygame.mouse.get_pressed()[0] and self.can_shoot:
            self.shoot_sound.play()
            pos = self.gun.rect.center + self.gun.player_direction * 50
            Bullet(self.bullet_surf, pos, self.gun.player_direction, (self.all_sprites, self.bullet_sprites))
            self.can_shoot = False
            self.shoot_time = pygame.time.get_ticks()

    #setting timer for gun so it don't shot like a Machine Gun
    def gun_timer(self):
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
            if current_time - self.shoot_time >= self.gun_cooldown:
                self.can_shoot = True

    #backgound map load
    def setup(self):
        map = load_pygame(join('code','data', 'maps', 'world.tmx'))

        for x, y, image in map.get_layer_by_name('Ground').tiles():
            Sprite((x * TILE_SIZE,y * TILE_SIZE), image, self.all_sprites)
        
        for obj in map.get_layer_by_name('Objects'):
            CollisionSprite((obj.x, obj.y), obj.image, (self.all_sprites, self.collision_sprites))
        
        for obj in map.get_layer_by_name('Collisions'):
            CollisionSprite((obj.x, obj.y), pygame.Surface((obj.width, obj.height)), self.collision_sprites)

        for obj in map.get_layer_by_name('Entities'):
            if obj.name == 'Player':
                self.player = Player((obj.x,obj.y), self.all_sprites, self.collision_sprites)
                self.gun = Gun(self.player, self.all_sprites)
            else:
                self.spawn_positions.append((obj.x, obj.y))

    #bullet collision with monster
    def bullet_collision(self):
        if self.bullet_sprites:
            for bullet in self.bullet_sprites:
                collision_sprites = pygame.sprite.spritecollide(bullet, self.enemy_sprites, False, pygame.sprite.collide_mask)
                if collision_sprites:
                    self.impact_sound.play()
                    for sprite in collision_sprites:
                        sprite.destroy()
                    bullet.kill()

    def player_collision(self): #if player get hurt, minus the total health, and if healthe is 0, then game over
        if pygame.sprite.spritecollide(self.player, self.enemy_sprites, False, pygame.sprite.collide_mask):
            if self.health_cold_down:
                self.health -= 1
                self.impact_sound.play()
                self.health_cold_down = False
                
                self.hurt_time = pygame.time.get_ticks()
            if self.health == 0:
                self.running = False

    #draw text for start page
    def draw_text(self, text, x, y):
        text_font = pygame.font.SysFont("Arial", 30)
        screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        img = text_font.render(text, True, ("white"))
        screen.blit(img,(x, y))

    def startpage(self): #Game interface
            switch = True
            while switch:
                self.clock.tick(5)
                self.draw_text("W to move forward, S to move backward, A to move left, D to move right, click Mouse-left to shot", 290, 600)
                self.display_surface.blit(self.start, [655, 200])
                if self.play_DIFF == False:
                    self.display_surface.blit(self.play, [770, 300])
                else:
                    self.display_surface.blit(self.play2, [770, 300])
                pygame.display.update()
                eve = pygame.event.get()
                for i in eve:
                    self.display_surface.fill('black')
                    ps = pygame.mouse.get_pos()
                    if (ps[0] - 800) ** 2 + (ps[1] - 327) ** 2 <= 27 * 27:
                        self.play_DIFF = True
                    else:
                        self.play_DIFF = False
                    if i.type == pygame.MOUSEBUTTONDOWN:
                        if self.play_DIFF == True:
                            switch = False
                    if i.type == pygame.QUIT:
                        pygame.quit()
                        



    def run(self):
        while self.running:
            # dt 
            dt = self.clock.tick() / 1000

            # event loop 
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == self.enemy_event:
                    Enemy(choice(self.spawn_positions), choice(list(self.enemy_frames.values())), (self.all_sprites, self.enemy_sprites), self.player, self.collision_sprites)

            # update 
            self.gun_timer()
            self.health_timer()
            self.input()
            self.all_sprites.update(dt)
            self.bullet_collision()
            self.player_collision()
            
            

            # draw
            self.display_surface.fill('black')
            self.all_sprites.draw(self.player.rect.center)
            pygame.display.update()

        pygame.quit()

if __name__ == '__main__':
    game = Game()
    game.startpage()
    game.run()
    print()