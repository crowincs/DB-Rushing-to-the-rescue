import pygame
from settings import *


class Interface:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)
        self.heath_bar_rect = pygame.Rect(10, 10, HEALTH_BAR_WIDTH, BAR_HEIGHT)
        self.weapon_view = []
        for weapon in weapon_information.values():
            file = weapon['graphic']
            weapon = pygame.image.load(file).convert_alpha()
            self.weapon_view.append(weapon)

    def show_bar(self, current, max_amount, bg_rect, color):
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, bg_rect)
        ratio = current / max_amount
        current_widht = bg_rect.width * ratio
        current_rect = bg_rect.copy()
        current_rect.width = current_widht
        pygame.draw.rect(self.display_surface, color, current_rect)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, bg_rect, 3)

    def selection_box(self, left, top, has_switched):
        bg_rect = pygame.Rect(left, top, ITEM_BOX_SIZE, ITEM_BOX_SIZE)
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, bg_rect)
        if has_switched:
            pygame.draw.rect(self.display_surface, UI_BORDER_COLOR_ACTIVE,
                             bg_rect, 3)
        else:
            pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, bg_rect, 3)
        return bg_rect

    def weapon_overlay(self, arsenal_index, has_switched):
        bg_rect = self.selection_box(10, 630, has_switched)
        weapon_surf = self.weapon_view[arsenal_index]
        weapon_rect = weapon_surf.get_rect(center=bg_rect.center)
        self.display_surface.blit(weapon_surf, weapon_rect)

    def display(self, player):
        self.show_bar(player.heath, player.stats['heath'], self.heath_bar_rect,HEALTH_COLOR)
        self.weapon_overlay(player.arsenal_index, has_switched=True)
