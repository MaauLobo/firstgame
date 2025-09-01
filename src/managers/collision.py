# -*- coding: utf-8 -*-
"""
Sistema de colisão do jogo
"""

import pygame
from ..config import COLLISION_MODE, HITBOX_SHRINK_W, HITBOX_SHRINK_H


def collide_shrink(a_rect: pygame.Rect, b_rect: pygame.Rect) -> bool:
    """Colisão usando retângulos reduzidos"""
    return a_rect.colliderect(b_rect)


def collide_mask(a, b) -> bool:
    """Colisão usando máscaras de pixel"""
    offset = (int(b.x - a.x), int(b.y - a.y))
    return a.mask.overlap(b.mask, offset) is not None


def create_hit_rect(x: int, y: int, w: int, h: int) -> pygame.Rect:
    """Cria um retângulo de colisão reduzido a partir de coordenadas e dimensões"""
    rect = pygame.Rect(x, y, w, h)
    hit_rect = rect.copy()
    hit_rect.inflate_ip(-rect.w * HITBOX_SHRINK_W, -rect.h * HITBOX_SHRINK_H)
    return hit_rect


def create_hit_rect_from_rect(rect: pygame.Rect) -> pygame.Rect:
    """Cria um retângulo de colisão reduzido a partir de um pygame.Rect"""
    hit_rect = rect.copy()
    hit_rect.inflate_ip(-rect.w * HITBOX_SHRINK_W, -rect.h * HITBOX_SHRINK_H)
    return hit_rect


def check_collision(obj_a, obj_b) -> bool:
    """Verifica colisão entre dois objetos baseado no modo configurado"""
    if COLLISION_MODE == "mask":
        return collide_mask(obj_a, obj_b)
    else:  # "shrink"
        return collide_shrink(obj_a.hit_rect, obj_b.hit_rect)


def check_collision_with_powerup(jogador, powerup) -> bool:
    """Verifica colisão específica entre jogador e power-up"""
    if COLLISION_MODE == "mask":
        return collide_mask(jogador, powerup)
    else:  # "shrink"
        jogador_hit_rect = create_hit_rect_from_rect(jogador.hit_rect)
        powerup_hit_rect = powerup.get_hit_rect()
        return collide_shrink(jogador_hit_rect, powerup_hit_rect)


def check_distance_between_objects(obj_a, obj_b, max_distance: float) -> bool:
    """Verifica se dois objetos estão dentro de uma distância máxima"""
    dx = obj_a.x - obj_b.x
    dy = obj_a.y - obj_b.y
    distance = (dx * dx + dy * dy) ** 0.5
    return distance <= max_distance 