# -*- coding: utf-8 -*-
"""
Classe para power-ups do jogo
"""

import os
import random
import pygame
import math
from ..config import (
    POWERUP_ALTURA, LANE_MARGIN, ALPHA_THRESHOLD, SHOW_HITBOX_DEBUG,
    POWERUP_VELOCIDADE, POWERUP_TIPOS, TELA_ALTURA
)
from ..managers.collision import create_hit_rect


class PowerUp:
    """Classe para representar um power-up no jogo"""
    
    def __init__(self, tipo: str, lane_centers: list[int], lane_w: int):
        """
        Inicializa um power-up
        
        Args:
            tipo: Tipo do power-up ('shield', 'speed_boost', etc.)
            lane_centers: Lista com as posições centrais das faixas
            lane_w: Largura de cada faixa
        """
        self.tipo = tipo
        self.config = POWERUP_TIPOS[tipo]
        
        # Posicionamento
        center = random.choice(lane_centers)
        self.x = center - POWERUP_ALTURA // 2
        self.y = -POWERUP_ALTURA
        
        # Dimensões
        self.largura = POWERUP_ALTURA
        self.altura = POWERUP_ALTURA
        
        # Velocidade
        self.vel = POWERUP_VELOCIDADE
        
        # Cria superfície do power-up
        self._criar_superficie()
        
        # Efeitos visuais
        self.animacao_timer = 0.0
        self.rotacao = 0.0
        self.escala = 1.0
        self.pulsando = True
        
    def _criar_superficie(self):
        """Cria a superfície visual do power-up"""
        # Cria uma superfície quadrada
        self.superficie = pygame.Surface((POWERUP_ALTURA, POWERUP_ALTURA), pygame.SRCALPHA)
        
        # Cor base do power-up
        cor = self.config['cor']
        
        # Desenha um círculo com gradiente
        raio = POWERUP_ALTURA // 2 - 5
        
        # Círculo externo (borda)
        pygame.draw.circle(self.superficie, (255, 255, 255), (POWERUP_ALTURA//2, POWERUP_ALTURA//2), raio + 2)
        
        # Círculo interno (cor principal)
        pygame.draw.circle(self.superficie, cor, (POWERUP_ALTURA//2, POWERUP_ALTURA//2), raio)
        
        # Círculo interno mais claro (brilho)
        pygame.draw.circle(self.superficie, tuple(min(255, c + 50) for c in cor), 
                          (POWERUP_ALTURA//2, POWERUP_ALTURA//2), raio - 5)
        
        # Adiciona símbolo baseado no tipo
        self._adicionar_simbolo()
        
        # Cria máscara para colisão
        self.mask = pygame.mask.from_surface(self.superficie, ALPHA_THRESHOLD)
        
    def _adicionar_simbolo(self):
        """Adiciona símbolo específico para cada tipo de power-up"""
        cor_simbolo = (255, 255, 255)  # branco
        centro = POWERUP_ALTURA // 2
        tamanho_simbolo = POWERUP_ALTURA // 4
        
        if self.tipo == 'shield':
            # Escudo - triângulo
            pontos = [
                (centro, centro - tamanho_simbolo),
                (centro - tamanho_simbolo, centro + tamanho_simbolo),
                (centro + tamanho_simbolo, centro + tamanho_simbolo)
            ]
            pygame.draw.polygon(self.superficie, cor_simbolo, pontos)
            
        elif self.tipo == 'speed_boost':
            # Turbo - seta para cima
            pontos = [
                (centro, centro - tamanho_simbolo),
                (centro - tamanho_simbolo//2, centro),
                (centro + tamanho_simbolo//2, centro)
            ]
            pygame.draw.polygon(self.superficie, cor_simbolo, pontos)
            
        elif self.tipo == 'slow_motion':
            # Câmera lenta - relógio
            pygame.draw.circle(self.superficie, cor_simbolo, (centro, centro), tamanho_simbolo//2, 2)
            # Ponteiros do relógio
            pygame.draw.line(self.superficie, cor_simbolo, 
                           (centro, centro), (centro, centro - tamanho_simbolo//3), 2)
            pygame.draw.line(self.superficie, cor_simbolo, 
                           (centro, centro), (centro + tamanho_simbolo//4, centro), 2)
            
        elif self.tipo == 'magnet':
            # Ímã - formato de U
            pygame.draw.rect(self.superficie, cor_simbolo, 
                           (centro - tamanho_simbolo//2, centro - tamanho_simbolo//2, 
                            tamanho_simbolo, tamanho_simbolo//2))
            pygame.draw.rect(self.superficie, cor_simbolo, 
                           (centro - tamanho_simbolo//3, centro, 
                            tamanho_simbolo*2//3, tamanho_simbolo//2))
            
        elif self.tipo == 'double_points':
            # Pontos duplos - dois círculos
            pygame.draw.circle(self.superficie, cor_simbolo, 
                             (centro - tamanho_simbolo//3, centro), tamanho_simbolo//3)
            pygame.draw.circle(self.superficie, cor_simbolo, 
                             (centro + tamanho_simbolo//3, centro), tamanho_simbolo//3)
    
    def mover(self, dt):
        """Move o power-up para baixo"""
        self.y += self.vel * dt
        
        # Atualiza animação
        self.animacao_timer += dt
        self.rotacao += 90 * dt  # rotação de 90 graus por segundo
        
        # Efeito de pulsação
        if self.pulsando:
            self.escala = 1.0 + 0.1 * math.sin(self.animacao_timer * 4)
    
    def desenhar(self, tela):
        """Desenha o power-up na tela"""
        if self.y + self.altura < 0 or self.y > TELA_ALTURA:
            return
            
        # Cria superfície rotacionada e escalada
        superficie_rot = pygame.transform.rotate(self.superficie, self.rotacao)
        superficie_final = pygame.transform.scale(superficie_rot, 
                                                (int(self.largura * self.escala), 
                                                 int(self.altura * self.escala)))
        
        # Centraliza a superfície rotacionada
        rect = superficie_final.get_rect()
        rect.centerx = self.x + self.largura // 2
        rect.centery = self.y + self.altura // 2
        
        tela.blit(superficie_final, rect)
        
        # Debug: mostra hitbox
        if SHOW_HITBOX_DEBUG:
            hit_rect = create_hit_rect(self.x, self.y, self.largura, self.altura)
            pygame.draw.rect(tela, (0, 255, 255), hit_rect, 2)  # ciano para power-ups
    
    def esta_na_tela(self):
        """Verifica se o power-up ainda está visível na tela"""
        return self.y < TELA_ALTURA and self.y + self.altura > 0
    
    def get_hit_rect(self):
        """Retorna o retângulo de colisão do power-up"""
        return create_hit_rect(self.x, self.y, self.largura, self.altura)


class PowerUpManager:
    """Gerenciador de power-ups ativos no jogador"""
    
    def __init__(self):
        self.powerups_ativos = {}  # {tipo: {'tempo_restante': float, 'config': dict}}
        self.efeitos_atuais = {
            'velocidade_jogador_mult': 1.0,
            'velocidade_obstaculos_mult': 1.0,
            'pontos_mult': 1.0,
            'imunidade_colisao': False,
            'raio_imã': 0
        }
    
    def adicionar_powerup(self, tipo: str):
        """Adiciona um power-up ativo"""
        from ..config import POWERUP_TIPOS, POWERUP_EFEITOS
        
        duracao = POWERUP_TIPOS[tipo]['duracao']
        self.powerups_ativos[tipo] = {
            'tempo_restante': duracao,
            'config': POWERUP_EFEITOS[tipo].copy()
        }
        
        print(f"🎁 Power-up ativado: {POWERUP_TIPOS[tipo]['nome']} ({duracao}s)")
    
    def atualizar(self, dt):
        """Atualiza os power-ups ativos e calcula efeitos"""
        # Remove power-ups expirados
        tipos_para_remover = []
        for tipo, dados in self.powerups_ativos.items():
            dados['tempo_restante'] -= dt
            if dados['tempo_restante'] <= 0:
                tipos_para_remover.append(tipo)
        
        for tipo in tipos_para_remover:
            del self.powerups_ativos[tipo]
            print(f"⏰ Power-up expirado: {POWERUP_TIPOS[tipo]['nome']}")
        
        # Calcula efeitos combinados
        self._calcular_efeitos_combinados()
    
    def _calcular_efeitos_combinados(self):
        """Calcula os efeitos combinados de todos os power-ups ativos"""
        from ..config import POWERUP_TIPOS
        
        # Reset para valores padrão
        self.efeitos_atuais = {
            'velocidade_jogador_mult': 1.0,
            'velocidade_obstaculos_mult': 1.0,
            'pontos_mult': 1.0,
            'imunidade_colisao': False,
            'raio_imã': 0
        }
        
        # Aplica efeitos de cada power-up ativo
        for tipo, dados in self.powerups_ativos.items():
            config = dados['config']
            
            # Multiplicadores são multiplicados entre si
            self.efeitos_atuais['velocidade_jogador_mult'] *= config.get('velocidade_jogador_mult', 1.0)
            self.efeitos_atuais['velocidade_obstaculos_mult'] *= config.get('velocidade_obstaculos_mult', 1.0)
            self.efeitos_atuais['pontos_mult'] *= config.get('pontos_mult', 1.0)
            
            # Imunidade é True se qualquer power-up der imunidade
            if config.get('imunidade_colisao', False):
                self.efeitos_atuais['imunidade_colisao'] = True
            
            # Raio do ímã é o maior entre todos
            self.efeitos_atuais['raio_imã'] = max(
                self.efeitos_atuais['raio_imã'], 
                config.get('raio_imã', 0)
            )
    
    def tem_powerup_ativo(self, tipo: str):
        """Verifica se um tipo específico de power-up está ativo"""
        return tipo in self.powerups_ativos
    
    def get_tempo_restante(self, tipo: str):
        """Retorna o tempo restante de um power-up específico"""
        if tipo in self.powerups_ativos:
            return self.powerups_ativos[tipo]['tempo_restante']
        return 0.0
    
    def get_efeitos_atuais(self):
        """Retorna os efeitos atuais combinados"""
        return self.efeitos_atuais.copy()
    
    def limpar_todos(self):
        """Remove todos os power-ups ativos"""
        self.powerups_ativos.clear()
        self._calcular_efeitos_combinados() 