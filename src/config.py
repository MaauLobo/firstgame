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
CINEMATICA = 1  # Novo estado para cinemática
JOGANDO = 2
GAME_OVER = 3
POWERUP_HELP = 4  # Novo estado para tela de ajuda dos power-ups

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
PLAYLIST_VOLUME = 0.2  # volume das músicas da playlist (0.0 a 1.0) - 20%
PLAYLIST_FADE_TIME = 1.0  # tempo de fade entre músicas (segundos)
PLAYLIST_AGGRESSIVE_MODE = False  # volume agressivo DESATIVADO - usuário tem controle total

# -------------------- Configurações do Record --------------------
RECORD_FILE = "record.txt"  # arquivo para salvar o record 

# -------------------- Configurações dos Power-ups --------------------
POWERUP_SPAWN_CHANCE = 0.08  # 8% de chance de spawnar power-up
POWERUP_ALTURA = 60  # altura dos power-ups
POWERUP_VELOCIDADE = 280  # velocidade de queda dos power-ups (px/s)

# Tipos de Power-ups disponíveis
POWERUP_TIPOS = {
    'shield': {
        'nome': 'Escudo',
        'duracao': 5.0,  # segundos
        'cor': (0, 255, 255),  # ciano
        'descricao': 'Proteção contra colisões'
    },
    'speed_boost': {
        'nome': 'Turbo',
        'duracao': 3.0,  # segundos
        'cor': (255, 255, 0),  # amarelo
        'descricao': 'Velocidade aumentada'
    },
    'slow_motion': {
        'nome': 'Câmera Lenta',
        'duracao': 4.0,  # segundos
        'cor': (128, 0, 255),  # roxo
        'descricao': 'Tempo desacelerado'
    },
    'magnet': {
        'nome': 'Ímã',
        'duracao': 6.0,  # segundos
        'cor': (255, 0, 255),  # magenta
        'descricao': 'Atrai power-ups próximos'
    },
    'double_points': {
        'nome': 'Pontos Duplos',
        'duracao': 8.0,  # segundos
        'cor': (0, 255, 0),  # verde
        'descricao': 'Pontuação duplicada'
    }
}

# Efeitos dos Power-ups
POWERUP_EFEITOS = {
    'shield': {
        'velocidade_jogador_mult': 1.0,  # não altera velocidade
        'velocidade_obstaculos_mult': 1.0,  # não altera velocidade dos obstáculos
        'pontos_mult': 1.0,  # não altera pontuação
        'imunidade_colisao': True
    },
    'speed_boost': {
        'velocidade_jogador_mult': 1.5,  # 50% mais rápido
        'velocidade_obstaculos_mult': 1.0,
        'pontos_mult': 1.0,
        'imunidade_colisao': False
    },
    'slow_motion': {
        'velocidade_jogador_mult': 1.0,
        'velocidade_obstaculos_mult': 0.5,  # obstáculos 50% mais lentos
        'pontos_mult': 1.0,
        'imunidade_colisao': False
    },
    'magnet': {
        'velocidade_jogador_mult': 1.0,
        'velocidade_obstaculos_mult': 1.0,
        'pontos_mult': 1.0,
        'imunidade_colisao': False,
        'raio_imã': 150  # pixels
    },
    'double_points': {
        'velocidade_jogador_mult': 1.0,
        'velocidade_obstaculos_mult': 1.0,
        'pontos_mult': 2.0,  # pontuação duplicada
        'imunidade_colisao': False
    }
} 