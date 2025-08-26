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


def create_hit_rect(rect: pygame.Rect) -> pygame.Rect:
    """Cria um retângulo de colisão reduzido"""
    hit_rect = rect.copy()
    hit_rect.inflate_ip(-rect.w * HITBOX_SHRINK_W, -rect.h * HITBOX_SHRINK_H)
    return hit_rect


def check_collision(obj_a, obj_b) -> bool:
    """Verifica colisão entre dois objetos baseado no modo configurado"""
    if COLLISION_MODE == "mask":
        return collide_mask(obj_a, obj_b)
    else:  # "shrink"
        return collide_shrink(obj_a.hit_rect, obj_b.hit_rect) 