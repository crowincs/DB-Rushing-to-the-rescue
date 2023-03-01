import pygame
from settings import *
from entity import Entity
from functions import *


class Enemy(Entity):
    def __init__(self, monster_name, pos, groups, obstacle_sprites,
                 damage_player):
        super().__init__(groups)
        self.sprite_type = 'enemy'
        self.parameters(monster_name)
        self.action = 'idle'
        self.image = self.animations[self.action][self.frame]
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -10)
        self.obstacle_sprites = obstacle_sprites
        self.monster_name = monster_name
        monster_info = monster_information[self.monster_name]
        self.health = monster_info['health']
        self.speed = monster_info['speed']
        self.attact_damage = monster_info['damage']
        self.attact_radius = monster_info['attack_radius']
        self.notice_radius = monster_info['notice_radius']
        self.attact_type = monster_info['attack_type']
        self.monster_can_attact = True
        self.attack_monster_time = None
        self.attack_monster_cooldown = 500
        self.damage_player = damage_player
        self.vulnerable = True
        self.hit_time = None
        self.invincibility_duration = 300

    def parameters(self, name):
        self.animations = {'idle': [], 'move': [], 'attack': []}
        main_path = f'../graphics/monsters/{name}/'
        for animation in self.animations.keys():
            self.animations[animation] = set_function(main_path + animation)

    def distance_to_the_player(self, player):
        enemy_vec = pygame.math.Vector2(self.rect.center)
        player_vec = pygame.math.Vector2(player.rect.center)
        distance = (player_vec - enemy_vec).magnitude()
        if distance > 0:
            direction = (player_vec - enemy_vec).normalize()
        else:
            direction = pygame.math.Vector2()
        return (distance, direction)

    def get_action(self, player):
        distance = self.distance_to_the_player(player)[0]
        if distance <= self.attact_radius and self.monster_can_attact:
            if self.action != 'attack':
                self.frame = 0
            self.action = 'attack'
        elif distance <= self.notice_radius:
            self.action = 'move'
        else:
            self.action = 'idle'

    def actions(self, player):
        if self.action == 'attack':
            self.attack_monster_time = pygame.time.get_ticks()
            self.damage_player(self.attact_damage, self.attact_type)
        elif self.action == 'move':
            self.direction = self.distance_to_the_player(player)[1]
        else:
            self.direction = pygame.math.Vector2()

    def animate(self):
        animation = self.animations[self.action]
        self.frame += self.animation_speed
        if self.frame >= len(animation):
            if self.action == 'attack':
                self.monster_can_attact = False
            self.frame = 0
        self.image = animation[int(self.frame)]
        self.rect = self.image.get_rect(center=self.hitbox.center)
        if not self.vulnerable:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)

    def cooldown(self):
        current_time = pygame.time.get_ticks()
        if not self.monster_can_attact:
            if current_time - self.attack_monster_time >= self.attack_monster_cooldown:
                self.monster_can_attact = True
        if not self.vulnerable:
            if current_time - self.hit_time >= self.invincibility_duration:
                self.vulnerable = True

    def get_damage(self, player, attack_type):
        if self.vulnerable:
            self.direction = self.distance_to_the_player(player)[1]
            if attack_type == 'weapon':
                self.health -= player.get_full_weapon_damage()
        self.hit_time = pygame.time.get_ticks()
        self.vulnerable = False

    def check_death(self):
        if self.health <= 0:
            self.kill()

    def reaction(self):
        if not self.vulnerable:
            self.direction *= -3

    def update(self):
        self.reaction()
        self.move(self.speed)
        self.animate()
        self.cooldown()
        self.check_death()

    def enemy_update(self, player):
        self.get_action(player)
        self.actions(player)