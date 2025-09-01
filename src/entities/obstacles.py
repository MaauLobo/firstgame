# -*- coding: utf-8 -*-
"""
Classe para obstáculos do jogo
"""

import os
import random
import pygame
from ..config import (
    OBST_ALTURA, LANE_MARGIN, ALPHA_THRESHOLD, SHOW_HITBOX_DEBUG,
    POLICE_SPAWN_CHANCE, POLICE_LATERAL_SPEED, POLICE_LANE_CHANGE_INTERVAL,
    POLICE_AGGRESSIVE_MODE, OBST_VEL_INICIAL
)
from .police import SireneAnimacao
from ..managers.collision import create_hit_rect


class Obstaculo:
    inimigos_imgs = []
    inimigos_nomes = ["taxi.png", "audi.png", "car.png", "police.png"]

    @classmethod
    def carregar_imgs(cls):
        if not cls.inimigos_imgs:
            for nome in cls.inimigos_nomes:
                caminho = os.path.join("assets", "images", nome)
                img = pygame.image.load(caminho).convert_alpha()
                cls.inimigos_imgs.append(img)  # sem escala aqui

    def __init__(self, vel_px_s: float, lane_centers: list[int], lane_w: int):
        if not Obstaculo.inimigos_imgs:
            Obstaculo.carregar_imgs()

        # Escolhe uma imagem aleatória com chance especial para polícia
        if random.random() < POLICE_SPAWN_CHANCE:
            # Força spawn de carro da polícia
            img_index = Obstaculo.inimigos_nomes.index("police.png")
        else:
            # Escolhe aleatoriamente entre todos os carros (exceto polícia)
            carros_disponiveis = [i for i, nome in enumerate(Obstaculo.inimigos_nomes) if nome != "police.png"]
            img_index = random.choice(carros_disponiveis)
            
        base = Obstaculo.inimigos_imgs[img_index]
        self.nome_imagem = Obstaculo.inimigos_nomes[img_index]
        
        ow, oh = base.get_width(), base.get_height()

        # escala pela ALTURA alvo (OBST_ALTURA), preservando proporção
        scale = OBST_ALTURA / oh
        w = int(ow * scale)
        h = OBST_ALTURA

        # garante que cabe na faixa
        max_w = max(10, lane_w - 2*LANE_MARGIN)
        if w > max_w:
            s = max_w / w
            w = int(w * s)
            h = int(h * s)

        self.largura, self.altura = w, h
        self.img  = pygame.transform.smoothscale(base, (w, h)).convert_alpha()
        self.mask = pygame.mask.from_surface(self.img, ALPHA_THRESHOLD)

        self.vel = vel_px_s
        center = random.choice(lane_centers)
        self.x = center - self.largura // 2
        self.y = -self.altura
        
        # Guarda informações das faixas para movimento da polícia
        self.lane_centers = lane_centers
        self.lane_w = lane_w
        
        # Cria animação da sirene se for carro da polícia
        self.sirene = None
        self.eh_policia = False
        if self.nome_imagem == "police.png":
            self.sirene = SireneAnimacao(self.x, self.y, self.largura, self.altura)
            self.eh_policia = True
            
            # Variáveis para movimento lateral da polícia
            self.lane_change_timer = 0.0
            # Detecta a faixa inicial baseada na posição
            self.current_lane = self._detectar_faixa_atual()
            self.target_lane_x = self.x
            self.moving_lateral = False

    def mover(self, dt):
        self.y += self.vel * dt
        
        # Movimento lateral especial para polícia
        if self.eh_policia:
            self._mover_policia_lateral(dt)
        
        # Atualiza posição da sirene se existir
        if self.sirene:
            self.sirene.x = self.x
            self.sirene.y = self.y
            self.sirene.atualizar(dt)

    def desenhar(self, tela):
        tela.blit(self.img, (int(self.x), int(self.y)))
        
        # Desenha a sirene se for carro da polícia
        if self.sirene:
            self.sirene.desenhar(tela)
        
        # Efeito visual quando a polícia está se movendo lateralmente
        if self.eh_policia and self.moving_lateral:
            # Desenha uma seta indicando o movimento
            seta_surf = pygame.Surface((20, 20), pygame.SRCALPHA)
            if self.x < self.target_lane_x:
                # Movendo para direita
                pygame.draw.polygon(seta_surf, (255, 255, 0, 180), [(0, 10), (20, 10), (15, 5), (15, 15)])
            else:
                # Movendo para esquerda
                pygame.draw.polygon(seta_surf, (255, 255, 0, 180), [(20, 10), (0, 10), (5, 5), (5, 15)])
            
            tela.blit(seta_surf, (self.x + self.largura // 2 - 10, self.y - 25))
        
        if SHOW_HITBOX_DEBUG:
            pygame.draw.rect(tela, (255,0,0), self.hit_rect, 2)
            if hasattr(self, 'mask'):
                msurf = self.mask.to_surface(setcolor=(255,0,0,80), unsetcolor=(0,0,0,0))
                msurf.set_colorkey((0,0,0))
                tela.blit(msurf, (int(self.x), int(self.y)))
    
    def _mover_policia_lateral(self, dt):
        """Movimento lateral especial da polícia para tentar bloquear o jogador"""
        self.lane_change_timer += dt
        
        # Ajusta intervalo baseado na dificuldade e velocidade
        intervalo_atual = POLICE_LANE_CHANGE_INTERVAL
        if POLICE_AGGRESSIVE_MODE and hasattr(self, 'dificuldade_jogo'):
            # Reduz o intervalo conforme a dificuldade aumenta
            intervalo_atual = max(0.3, POLICE_LANE_CHANGE_INTERVAL - (self.dificuldade_jogo - 1) * 0.15)
        
        # Ajusta intervalo baseado na velocidade do jogo
        # Quanto mais rápido, mais frequentemente deve tentar manobrar
        velocidade_ratio = self.vel / OBST_VEL_INICIAL
        intervalo_atual = max(0.2, intervalo_atual / velocidade_ratio)
        
        # Decide se deve mudar de faixa
        if self.lane_change_timer >= intervalo_atual:
            self.lane_change_timer = 0.0
            
            # Comportamento inteligente: tenta bloquear o jogador se estiver próximo
            # Ativa mais cedo em velocidades altas
            altura_ativacao = 720 * 0.5  # 50% da tela (era 30%)
            if velocidade_ratio > 2.0:  # Se velocidade > 2x a inicial
                altura_ativacao = 720 * 0.7  # Ativa ainda mais cedo (70% da tela)
            
            if hasattr(self, 'jogador_x') and self.y > altura_ativacao:
                # Tenta se posicionar na faixa do jogador
                faixa_jogador = self._detectar_faixa_jogador()
                if faixa_jogador != self.current_lane:
                    nova_faixa = faixa_jogador
                else:
                    # Se já está na faixa do jogador, escolhe uma aleatória
                    nova_faixa = random.randint(0, 2)
            else:
                # Movimento aleatório normal
                nova_faixa = random.randint(0, 2)
            
            if nova_faixa != self.current_lane:
                self.current_lane = nova_faixa
                self.moving_lateral = True
                
                # Calcula a posição alvo na nova faixa
                target_center = self.lane_centers[self.current_lane]
                self.target_lane_x = target_center - self.largura // 2
        
        # Move lateralmente se estiver mudando de faixa
        if self.moving_lateral:
            # Ajusta velocidade lateral baseado na velocidade do jogo
            velocidade_lateral = POLICE_LATERAL_SPEED
            if velocidade_ratio > 1.5:  # Se velocidade > 1.5x a inicial
                velocidade_lateral = POLICE_LATERAL_SPEED * velocidade_ratio
            
            dx = velocidade_lateral * dt
            if abs(self.x - self.target_lane_x) < dx:
                self.x = self.target_lane_x
                self.moving_lateral = False
            else:
                # Move em direção ao alvo
                if self.x < self.target_lane_x:
                    self.x += dx
                else:
                    self.x -= dx
    
    def _detectar_faixa_atual(self):
        """Detecta em qual faixa o carro está baseado na posição X"""
        carro_center = self.x + self.largura // 2
        menor_distancia = float('inf')
        faixa_mais_proxima = 0
        
        for i, center in enumerate(self.lane_centers):
            distancia = abs(carro_center - center)
            if distancia < menor_distancia:
                menor_distancia = distancia
                faixa_mais_proxima = i
        
        return faixa_mais_proxima
    
    def _detectar_faixa_jogador(self):
        """Detecta em qual faixa o jogador está baseado na posição X"""
        if not hasattr(self, 'jogador_x'):
            return 1  # faixa central como padrão
        
        menor_distancia = float('inf')
        faixa_mais_proxima = 1
        
        for i, center in enumerate(self.lane_centers):
            distancia = abs(self.jogador_x - center)
            if distancia < menor_distancia:
                menor_distancia = distancia
                faixa_mais_proxima = i
        
        return faixa_mais_proxima
    
    def atualizar_posicao_jogador(self, jogador_x):
        """Atualiza a posição do jogador para comportamento inteligente"""
        self.jogador_x = jogador_x

    def fora_da_tela(self):
        return self.y > 720  # TELA_ALTURA

    @property
    def rect(self):
        return pygame.Rect(int(self.x), int(self.y), self.largura, self.altura)

    @property
    def hit_rect(self):
        return create_hit_rect(self.rect) 