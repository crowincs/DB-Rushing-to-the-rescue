from csv import reader
from os import walk
import pygame


def csv_maps(files):
    maps_edges = []
    with open(files) as level_map:
        layout = reader(level_map, delimiter=',')
        for row in layout:
            maps_edges.append(list(row))
        return maps_edges


def set_function(files):
    surface_list = []
    for _, __, img_files in walk(files):
        for image in img_files:
            full_path = files + '/' + image
            image_surf = pygame.image.load(full_path).convert_alpha()
            surface_list.append(image_surf)

    return surface_list
