# -*- coding: utf-8 -*-
"""
Interface do usuário e HUD do jogo
"""

import pygame
import os
from ..config import TELA_LARGURA, TELA_ALTURA


def desenhar_tela_abertura(tela, img_abertura):
    """Desenha a tela de abertura"""
    tela.blit(img_abertura, (0, 0))


def desenhar_tela_gameover(tela, pontuacao, img_gameover):
    """Desenha a tela de game over"""
    tela.blit(img_gameover, (0, 0))
    fonte = pygame.font.SysFont('Arial', 40, True)
    score = fonte.render(f'Pontuação: {pontuacao}', True, (255,255,255))
    rect = tela.get_rect()
    tela.blit(score, (rect.centerx - score.get_width()//2, 300))


def desenhar_hud_jogo(tela, pontuacao, obstaculos, playlist_manager):
    """Desenha o HUD durante o jogo"""
    # Pontuação
    fonte = pygame.font.SysFont('Arial', 28)
    tela.blit(fonte.render(f'Pontuação: {pontuacao}', True, (255,255,255)), (10, 10))
    
    # Mostra aviso de carro da polícia se houver algum
    for obst in obstaculos:
        if obst.nome_imagem == "police.png":
            fonte_police = pygame.font.SysFont('Arial', 24, True)
            aviso = fonte_police.render('🚨 CARRO DA POLÍCIA! 🚨', True, (255, 0, 0))
            tela.blit(aviso, (TELA_LARGURA - aviso.get_width() - 10, 10))
            break
    
    # Informações da playlist
    if playlist_manager.musica_atual:
        nome_musica = os.path.basename(playlist_manager.musica_atual)
        # Remove extensão do arquivo
        nome_musica = os.path.splitext(nome_musica)[0]
        fonte_musica = pygame.font.SysFont('Arial', 16)
        texto_musica = fonte_musica.render(f'🎵 {nome_musica}', True, (200, 200, 200))
        tela.blit(texto_musica, (10, TELA_ALTURA - 30))
        
        # Controles da playlist
        controles = fonte_musica.render('N: Próxima | R: Aleatória | P: Pausar | M: Mudo', True, (150, 150, 150))
        tela.blit(controles, (10, TELA_ALTURA - 50)) 