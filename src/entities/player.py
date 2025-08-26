# -*- coding: utf-8 -*-
"""
Classe para o carro do jogador
"""

import pygame
from ..config import CARRO_ALTURA, LANE_MARGIN, ALPHA_THRESHOLD, SHOW_HITBOX_DEBUG
from ..managers.collision import create_hit_rect


class CarroJogador:
    def __init__(self, img, inner_x: int, inner_w: int, lane_w: int):
        self.inner_x = inner_x
        self.inner_w = inner_w

        # escala mantendo proporção pela ALTURA
        orig_w, orig_h = img.get_width(), img.get_height()
        scale = CARRO_ALTURA / orig_h
        w = int(orig_w * scale)
        h = CARRO_ALTURA

        # se ficar maior que a faixa - margens, reduz proporcionalmente
        max_w = max(10, lane_w - 2*LANE_MARGIN)
        if w > max_w:
            s = max_w / w
            w = int(w * s)
            h = int(h * s)

        self.largura = w
        self.altura = h

        # posiciona no centro da faixa central
        self.x = inner_x + inner_w // 2 - self.largura // 2
        self.y = 720 - self.altura - 20  # 720 é TELA_ALTURA
        self.vel = 380  # CARRO_VEL

        self.img = pygame.transform.smoothscale(img, (self.largura, self.altura)).convert_alpha()
        self.mask = pygame.mask.from_surface(self.img, ALPHA_THRESHOLD)

    def mover(self, teclas, dt):
        if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
            self.x -= self.vel * dt
        if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
            self.x += self.vel * dt
        self.x = max(self.inner_x, min(self.inner_x + self.inner_w - self.largura, self.x))

    def desenhar(self, tela):
        tela.blit(self.img, (int(self.x), int(self.y)))
        if SHOW_HITBOX_DEBUG:
            pygame.draw.rect(tela, (0,255,0), self.hit_rect, 2)
            if hasattr(self, 'mask'):
                msurf = self.mask.to_surface(setcolor=(0,255,0,80), unsetcolor=(0,0,0,0))
                msurf.set_colorkey((0,0,0))
                tela.blit(msurf, (int(self.x), int(self.y)))

    @property
    def rect(self):
        return pygame.Rect(int(self.x), int(self.y), self.largura, self.altura)

    @property
    def hit_rect(self):
        return create_hit_rect(self.rect) 