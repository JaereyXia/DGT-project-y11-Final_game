"""
Those code defines game entities like player-attached guns, bullets, enemies, and basic sprites with functionality for movement, rotation, collision detection, and animation.
"""
from settings import * 
from math import atan2, degrees

# Basic sprite that can represent any game object (e.g., ground).
class Sprite(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft = pos)
        self.ground = True # Indicates this sprite is on the ground.

# Sprite specifically for handling collisions.
class CollisionSprite(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft = pos)

# Gun class attached to the player, follows player's movements and rotates toward the mouse position.
class Gun(pygame.sprite.Sprite):
    def __init__(self, player, groups):
        # player connection 
        self.player = player 
        self.distance = 140 # Distance from player to gun.
        self.player_direction = pygame.Vector2(0,1)  # Initial gun direction.

        # sprite setup 
        super().__init__(groups)
        self.gun_surf = pygame.image.load(join('code', 'images', 'gun', 'gun.png')).convert_alpha()
        self.image = self.gun_surf
        self.rect = self.image.get_rect(center = self.player.rect.center + self.player_direction * self.distance)

    # Determine the direction of the gun based on the mouse position.
    def get_direction(self):
        mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
        player_pos = pygame.Vector2(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2) # Player is centered.
        self.player_direction = (mouse_pos - player_pos).normalize() # Normalize direction vector.

    # Rotate the gun to point toward the mouse.
    def rotate_gun(self):
        angle = degrees(atan2(self.player_direction.x, self.player_direction.y)) - 90
        # Rotate and flip the gun based on direction.
        if self.player_direction.x > 0:
            self.image = pygame.transform.rotozoom(self.gun_surf, angle, 1)
        else:
            self.image = pygame.transform.rotozoom(self.gun_surf, abs(angle), 1)
            self.image = pygame.transform.flip(self.image, False, True)

    # Update gun position and orientation every frame.
    def update(self, _):
        self.get_direction()
        self.rotate_gun()
        self.rect.center = self.player.rect.center + self.player_direction * self.distance

# Bullet class for projectiles fired from the gun.
class Bullet(pygame.sprite.Sprite):
    def __init__(self, surf, pos, direction, groups):
        super().__init__(groups)
        self.image = surf 
        self.rect = self.image.get_rect(center = pos)
        self.spawn_time = pygame.time.get_ticks() # Time the bullet was spawned.
        self.lifetime = 1000 # Lifetime of the bullet in milliseconds.

        self.direction = direction # Direction of bullet movement.
        self.speed = 1200 # Speed of the bullet.

    # Move the bullet and check if it should disappear after a certain time.
    def update(self, dt):
        self.rect.center += self.direction * self.speed * dt # Move bullet based on direction and time.
        if pygame.time.get_ticks() - self.spawn_time >= self.lifetime: 
            self.kill()# Remove bullet after its lifetime expires.

# Enemy class that moves toward the player and handles collisions.
class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, frames, groups, player, collision_sprites):
        super().__init__(groups)
        self.player = player # Reference to the player.

        # image 
        self.frames, self.frame_index = frames, 0 
        self.image = self.frames[self.frame_index]
        self.animation_speed = 6 # Speed of animation.

        # rect 
        self.rect = self.image.get_rect(center = pos)
        self.hitbox_rect = self.rect.inflate(-20,-40)
        self.collision_sprites = collision_sprites
        self.direction = pygame.Vector2()
        self.speed = 200 # Speed of the enemy.

        # Timer for handling enemy death.
        self.death_time = 0
        self.death_duration = 200 # Time it takes for the enemy to disappear after dying.

    
    # Animate the enemy by cycling through frames.
    def animate(self, dt):
        self.frame_index += self.animation_speed * dt
        self.image = self.frames[int(self.frame_index) % len(self.frames)]

    #Here I added a program that allows the monster to move towards the player. This will make the monster move to the player's coordinates.
    def move(self, dt):
        # get direction 
        player_pos = pygame.Vector2(self.player.rect.center)
        enemy_pos = pygame.Vector2(self.rect.center)
        self.direction = (player_pos - enemy_pos).normalize() # Move toward to the player.
        
        # update the rect position + collision
        self.hitbox_rect.x += self.direction.x * self.speed * dt
        self.collision('horizontal')
        self.hitbox_rect.y += self.direction.y * self.speed * dt
        self.collision('vertical')
        self.rect.center = self.hitbox_rect.center

    # Handle collision with obstacles in the game.
    def collision(self, direction):
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.hitbox_rect):
                if direction == 'horizontal':
                    if self.direction.x > 0: self.hitbox_rect.right = sprite.rect.left
                    if self.direction.x < 0: self.hitbox_rect.left = sprite.rect.right
                else:
                    if self.direction.y < 0: self.hitbox_rect.top = sprite.rect.bottom
                    if self.direction.y > 0: self.hitbox_rect.bottom = sprite.rect.top
    
    # Start the enemy's death process and change its appearance.
    def destroy(self):
        # start a timer 
        self.death_time = pygame.time.get_ticks()
        # change the image 
        surf = pygame.mask.from_surface(self.frames[0]).to_surface()
        surf.set_colorkey('black')
        self.image = surf
    
    # Check if enough time has passed for the enemy to disappear after dying.
    def death_timer(self):
        if pygame.time.get_ticks() - self.death_time >= self.death_duration:
            self.kill()

    # Update the enemy's behavior (moving or death) every frame.
    def update(self, dt):
        if self.death_time == 0:
            self.move(dt) # Move if not dead.
            self.animate(dt) # Animate.
        else:
            self.death_timer() # Handle death timer.