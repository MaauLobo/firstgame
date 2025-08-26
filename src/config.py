# -*- coding: utf-8 -*-
"""
Configurações e constantes do jogo
"""

# -------------------- Configurações da Tela --------------------
TELA_LARGURA = 1280
TELA_ALTURA = 720
FPS = 60

# Estados do jogo
MENU = 0
JOGANDO = 1
GAME_OVER = 2

# -------------------- Configurações dos Carros --------------------
CARRO_VEL = 380  # px/s
CARRO_ALTURA = 90

# Obstáculos
OBST_ALTURA = 90
OBST_VEL_INICIAL = 280  # px/s

# Faixas
LANE_COUNT = 3
LANE_MARGIN = 6  # folga lateral dentro da faixa

# -------------------- Configurações de Colisão --------------------
COLLISION_MODE = "mask"  # "shrink" ou "mask"
HITBOX_SHRINK_W = 0.15  # 15% na largura (modo shrink)
HITBOX_SHRINK_H = 0.18  # 18% na altura (modo shrink)
ALPHA_THRESHOLD = 50  # opacidade mínima p/ máscara
SHOW_HITBOX_DEBUG = False

# -------------------- Configurações da Sirene --------------------
SIRENE_FPS = 8  # frames por segundo da animação da sirene
SIRENE_COLOR = (255, 0, 0)  # cor vermelha da sirene
POLICE_SPAWN_CHANCE = 0.15  # 15% de chance de spawnar carro da polícia
POLICE_SPECIAL_EFFECTS = True  # ativa efeitos especiais para carros da polícia

# Movimento da polícia
POLICE_LATERAL_SPEED = 120  # velocidade de movimento lateral (px/s)
POLICE_LANE_CHANGE_INTERVAL = 1.5  # tempo entre mudanças de faixa (segundos)
POLICE_TARGETING_RANGE = 200  # distância para começar a mirar no jogador (px)
POLICE_AGGRESSIVE_MODE = True  # ativa modo agressivo que aumenta com dificuldade

# -------------------- Configurações da Playlist --------------------
PLAYLIST_VOLUME = 0.7  # volume das músicas da playlist (0.0 a 1.0)
PLAYLIST_FADE_TIME = 1.0  # tempo de fade entre músicas (segundos)
PLAYLIST_AGGRESSIVE_MODE = True  # aumenta volume conforme dificuldade 