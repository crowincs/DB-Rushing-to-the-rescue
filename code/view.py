import pygame
from settings import *
from art import Art
from player import Player
from functions import *
from random import choice, randint
from weapons import Weapon
from interface import Interface
from enemy import Enemy
from particle import AnimationPlayer


class View:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.for_the_view = CameraGroup()
        self.density = pygame.sprite.Group()
        self.current_attack = None
        self.attack_sprites = pygame.sprite.Group()
        self.attackable_sprites = pygame.sprite.Group()
        self.create_map()
        self.interface = Interface()
        self.animation_player = AnimationPlayer()

    def create_map(self):
        layouts = {
            'boundary': csv_maps('../map/map_FloorBlocks.csv'),
            'grass': csv_maps('../map/map_Grass.csv'),
            'object': csv_maps('../map/map_Objects.csv'),
            'entities': csv_maps('../map/map_Entities.csv')
        }
        graphics = {
            'grass': set_function('../graphics/Grass'),
            'objects': set_function('../graphics/objects')
        }

        for style, layout in layouts.items():
            for row_index, row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != '-1':
                        x = col_index * TILESIZE
                        y = row_index * TILESIZE
                        if style == 'boundary':
                            Art((x, y),
                                [self.density],
                                'invisible')
                        if style == 'grass':
                            random_grass_image = choice(graphics['grass'])
                            Art((x, y),
                                 [self.for_the_view,
                                  self.density,
                                  self.attackable_sprites],
                                 'grass', random_grass_image)

                        if style == 'entities':
                            if col == '394':
                                self.player = Player((x, y),
                                                     [self.for_the_view],
                                                     self.density,
                                                     self.create_attack,
                                                     self.weapon_desappear)
                            else:
                                if col == '390':
                                    monster_name = 'bamboo'
                                elif col == '391':
                                    monster_name = 'spirit'
                                elif col == '392':
                                    monster_name = 'raccoon'
                                else:
                                    monster_name = 'squid'
                                Enemy(monster_name,
                                      (x, y),
                                      [self.for_the_view,
                                       self.attackable_sprites],
                                      self.density,
                                      self.damage_player)

                        if style == 'object':
                            surf = graphics['objects'][int(col)]
                            Art((x, y),
                                 [self.for_the_view, self.density],
                                 'object', surf)

    def create_attack(self):
        self.current_attack = Weapon(self.player, [self.for_the_view,
                                                   self.attack_sprites])

    def weapon_desappear(self):
        if self.current_attack:
            self.current_attack.kill()
        self.current_attack = None

    def player_attack_procces(self):
        if self.attack_sprites:
            for attack_sprites in self.attack_sprites:
                hit_sprites = pygame.sprite.spritecollide(attack_sprites,
                                            self.attackable_sprites,
                                            False)
                if hit_sprites:
                    for target_sprite in hit_sprites:
                        if target_sprite.sprite_type == 'grass':
                            pos = target_sprite.rect.center
                            offset = pygame.math.Vector2(0, 75)
                            for leaf in range(randint(3, 6)):
                                self.animation_player.create_grass_particles(
                                    pos - offset, [self.for_the_view])
                            target_sprite.kill()
                        else:
                            target_sprite.get_damage(self.player,
                                                     attack_sprites.sprite_type)

    def damage_player(self, amount, attack_type):
        if self.player.vulnerable:
            self.player.heath -= amount
            self.player.vulnerable = False
            self.player.hurt_time = pygame.time.get_ticks()

    def run(self):
        self.for_the_view.custom_draw(self.player)
        self.for_the_view.update()
        self.for_the_view.enemy_update(self.player)
        self.player_attack_procces()
        self.interface.display(self.player)


class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.movement = pygame.math.Vector2()
        self.floor = pygame.image.load('../graphics/tilemap/ground.png').convert()
        self.floor_rect = self.floor.get_rect(topleft=(0, 0))

    def custom_draw(self, player):
        self.movement.x = player.rect.centerx - self.half_width
        self.movement.y = player.rect.centery - self.half_height

        floor_movement_pos = self.floor_rect.topleft - self.movement
        self.display_surface.blit(self.floor, floor_movement_pos)
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            movement_position = sprite.rect.topleft - self.movement
            self.display_surface.blit(sprite.image, movement_position)

    def enemy_update(self, player):
        enemy_sprites = [sprite for sprite in self.sprites() if hasattr(sprite, 'sprite_type') and sprite.sprite_type == 'enemy']
        for enemy in enemy_sprites:
            enemy.enemy_update(player)