import sys

import pygame
from settings import *
from functions import set_function
from entity import Entity


class Player(Entity):
    def __init__(self, pos, groups, obstacle_sprites, create_attack,
                 weapon_desappear):
        super().__init__(groups)
        self.image = pygame.image.load(
            '../graphics/test/player.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -20)
        self.import_player_assets()
        self.action = 'down'
        self.create_attack = create_attack
        self.attack = False
        self.attack_cooldown = 400
        self.attack_time = None
        self.obstacle_sprites = obstacle_sprites
        self.weapon_desappear = weapon_desappear
        self.arsenal_index = 0
        self.arsenal_weapon = list(weapon_information.keys())[self.arsenal_index]
        self.can_switch_weapon = True
        self.weapon_switch_time = None
        self.switch_duration_cooldown = 500
        self.stats = {'heath': 100, 'attack': 10, 'speed': 8}
        self.heath = self.stats['heath']
        self.attack1 = self.stats['attack']
        self.speed = self.stats['speed']
        self.vulnerable = True
        self.hurt_time = None
        self.invulnerability_duration = 500

    def import_player_assets(self):
        character_files = '../graphics/player/'
        self.animations = {'up': [], 'down': [], 'left': [], 'right': [],
                           'right_idle': [], 'left_idle': [], 'up_idle': [],
                           'down_idle': [],
                           'right_attack': [], 'left_attack': [],
                           'up_attack': [], 'down_attack': []}
        for animation in self.animations.keys():
            full_files = character_files + animation
            self.animations[animation] = set_function(full_files)

    def clicking(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP]:
            self.direction.y = -1
            self.action = 'up'
        elif keys[pygame.K_DOWN]:
            self.direction.y = 1
            self.action = 'down'
        else:
            self.direction.y = 0

        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
            self.action = 'right'
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
            self.action = 'left'
        else:
            self.direction.x = 0

        if keys[pygame.K_z] and not self.attack:
            self.attack = True
            self.attack_time = pygame.time.get_ticks()
            self.create_attack()

        if keys[pygame.K_c] and self.can_switch_weapon:
            self.can_switch_weapon = False
            self.weapon_switch_time = pygame.time.get_ticks()
            if self.arsenal_index < len(list(weapon_information.keys())) - 1:
                self.arsenal_index += 1
            else:
                self.arsenal_index = 0
            self.arsenal_weapon = list(weapon_information.keys())[
                self.arsenal_index]

    def action_get(self):
        if self.direction.x == 0 and self.direction.y == 0:
            if not 'idle' in self.action and not 'attack' in self.action:
                self.action = self.action + '_idle'

        if self.attack:
            self.direction.x = 0
            self.direction.y = 0
            if not 'attack' in self.action:
                if 'idle' in self.action:
                    self.action = self.action.replace('_idle', '_attack')
                else:
                    self.action = self.action + '_attack'
        else:
            if 'attack' in self.action:
                self.action = self.action.replace('_attack', '')

    def cooldowns(self):
        current_time = pygame.time.get_ticks()
        if self.attack:
            if current_time - self.attack_time >= self.attack_cooldown + \
                    weapon_information[self.arsenal_weapon]['cooldown']:
                self.attack = False
                self.weapon_desappear()
        if not self.can_switch_weapon:
            if current_time - self.weapon_switch_time >= \
                    self.switch_duration_cooldown:
                self.can_switch_weapon = True
        if not self.vulnerable:
            if current_time - self.hurt_time >= self.invulnerability_duration:
                self.vulnerable = True

    def animate(self):
        animation = self.animations[self.action]
        self.frame += self.animation_speed
        if self.frame >= len(animation):
            self.frame = 0
        self.image = animation[int(self.frame)]
        self.rect = self.image.get_rect(center=self.hitbox.center)
        if not self.vulnerable:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)

    def get_full_weapon_damage(self):
        base_damage = self.stats['attack']
        weapon_damage = weapon_information[self.arsenal_weapon]['damage']
        return base_damage + weapon_damage

    def update(self):
        if self.heath < 0:
            print('Ты неудачник')
            sys.exit()
        self.clicking()
        self.cooldowns()
        self.action_get()
        self.animate()
        self.move(self.speed)
