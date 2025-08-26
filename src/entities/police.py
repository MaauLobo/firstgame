# -*- coding: utf-8 -*-
"""
Classe para animação da sirene da polícia
"""

import os
import pygame
from ..config import SIRENE_FPS, SIRENE_COLOR, POLICE_SPECIAL_EFFECTS


class SireneAnimacao:
    def __init__(self, x: int, y: int, largura: int, altura: int):
        self.x = x
        self.y = y
        self.largura = largura
        self.altura = altura
        
        # Carrega os frames da animação
        self.frames = []
        for i in range(1, 4):  # 1.png, 2.png, 3.png
            caminho = os.path.join("assets", "images", "Police_animation", f"{i}.png")
            if os.path.exists(caminho):
                img = pygame.image.load(caminho).convert_alpha()
                # Escala para o tamanho do carro da polícia
                img_scaled = pygame.transform.smoothscale(img, (largura, altura))
                self.frames.append(img_scaled)
        
        self.frame_atual = 0
        self.timer = 0.0
        self.frame_delay = 1.0 / SIRENE_FPS
        
        # Efeito de brilho da sirene
        self.brilho_timer = 0.0
        self.brilho_delay = 0.1  # 100ms para o efeito de brilho
        
    def atualizar(self, dt):
        # Atualiza animação dos frames
        self.timer += dt
        if self.timer >= self.frame_delay:
            self.timer = 0.0
            self.frame_atual = (self.frame_atual + 1) % len(self.frames)
        
        # Atualiza efeito de brilho
        self.brilho_timer += dt
        if self.brilho_timer >= self.brilho_delay:
            self.brilho_timer = 0.0
    
    def desenhar(self, tela):
        if self.frames:
            # Desenha o frame atual
            tela.blit(self.frames[self.frame_atual], (self.x, self.y))
            
            # Efeito de brilho da sirene (pisca)
            if self.brilho_timer < self.brilho_delay * 0.5:
                # Cria uma superfície para o efeito de brilho
                brilho_surf = pygame.Surface((self.largura, self.altura), pygame.SRCALPHA)
                pygame.draw.rect(brilho_surf, (*SIRENE_COLOR, 30), (0, 0, self.largura, self.altura))
                tela.blit(brilho_surf, (self.x, self.y))
                
            # Efeito de luz da sirene (raio de luz)
            if POLICE_SPECIAL_EFFECTS:
                # Cria um efeito de luz circular
                luz_surf = pygame.Surface((self.largura * 2, self.altura * 2), pygame.SRCALPHA)
                centro_x, centro_y = self.largura, self.altura
                raio = min(self.largura, self.altura) // 2
                
                # Gradiente radial para simular luz
                for r in range(raio, 0, -2):
                    alpha = max(0, 40 - (raio - r) * 2)
                    cor = (*SIRENE_COLOR, alpha)
                    pygame.draw.circle(luz_surf, cor, (centro_x, centro_y), r)
                
                tela.blit(luz_surf, (self.x - self.largura//2, self.y - self.altura//2)) 