# -*- coding: utf-8 -*-
"""
Interface do usuário e HUD do jogo
"""

import pygame
import os
from ..config import TELA_LARGURA, TELA_ALTURA


def desenhar_tela_cinematic(tela, cinematic_manager):
    """Desenha a tela de cinemática em tela cheia horizontal (1280x720)"""
    # Obtém o frame atual do vídeo
    frame_atual = cinematic_manager.obter_frame_atual()
    
    if frame_atual:
        # Garante que o frame seja do tamanho correto
        if frame_atual.get_size() != (TELA_LARGURA, TELA_ALTURA):
            frame_atual = pygame.transform.scale(frame_atual, (TELA_LARGURA, TELA_ALTURA))
        
        # Desenha o frame do vídeo em tela cheia
        tela.blit(frame_atual, (0, 0))
        
        # Overlay semi-transparente para melhorar legibilidade das instruções
        overlay = pygame.Surface((TELA_LARGURA, TELA_ALTURA), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 80))  # Fundo semi-transparente mais sutil
        tela.blit(overlay, (0, 0))
        
        # Instruções
        fonte_instrucoes = pygame.font.SysFont('Arial', 28, True)
        instrucoes = fonte_instrucoes.render('Pressione ESPAÇO para pular', True, (255, 255, 255))
        rect = tela.get_rect()
        tela.blit(instrucoes, (rect.centerx - instrucoes.get_width()//2, TELA_ALTURA - 60))
        
    else:
        # Modo fallback - fundo preto com texto para 1280x720
        tela.fill((0, 0, 0))
        
        # Texto central
        fonte = pygame.font.SysFont('Arial', 48, True)
        texto = fonte.render('🎬 CINEMÁTICA', True, (255, 255, 255))
        rect = tela.get_rect()
        tela.blit(texto, (rect.centerx - texto.get_width()//2, rect.centery - 120))
        
        # Status da cinemática
        fonte_status = pygame.font.SysFont('Arial', 32)
        status = fonte_status.render('Modo Fallback - Aguardando...', True, (255, 255, 0))
        tela.blit(status, (rect.centerx - status.get_width()//2, rect.centery - 50))
        
        # Instruções para fallback
        fonte_instrucoes = pygame.font.SysFont('Arial', 24)
        instrucoes1 = fonte_instrucoes.render('Coloque o arquivo "cinematic.mp4"', True, (200, 200, 200))
        instrucoes2 = fonte_instrucoes.render('na pasta "assets/videos/"', True, (200, 200, 200))
        tela.blit(instrucoes1, (rect.centerx - instrucoes1.get_width()//2, rect.centery + 20))
        tela.blit(instrucoes2, (rect.centerx - instrucoes2.get_width()//2, rect.centery + 50))
        
        # Instruções
        instrucoes = fonte_instrucoes.render('Pressione ESPAÇO para pular', True, (200, 200, 200))
        tela.blit(instrucoes, (rect.centerx - instrucoes.get_width()//2, rect.centery + 120))


def desenhar_tela_abertura(tela, img_abertura):
    """Desenha a tela de abertura"""
    tela.blit(img_abertura, (0, 0))


def desenhar_tela_gameover(tela, pontuacao, img_gameover, record_manager, novo_record=False):
    """Desenha a tela de game over"""
    tela.blit(img_gameover, (0, 0))
    
    # Pontuação
    fonte = pygame.font.SysFont('Arial', 40, True)
    score = fonte.render(f'Pontuação: {pontuacao}', True, (255,255,255))
    rect = tela.get_rect()
    tela.blit(score, (rect.centerx - score.get_width()//2, 300))
    
    # Record
    record_atual = record_manager.obter_record()
    fonte_record = pygame.font.SysFont('Arial', 32, True)
    
    if novo_record:
        # Novo record - destaque especial
        record_texto = fonte_record.render(f'🏆 NOVO RECORD! 🏆', True, (255, 215, 0))  # Dourado
        tela.blit(record_texto, (rect.centerx - record_texto.get_width()//2, 350))
        
        record_valor = fonte_record.render(f'{record_atual} pontos', True, (255, 215, 0))
        tela.blit(record_valor, (rect.centerx - record_valor.get_width()//2, 380))
    else:
        # Record atual
        record_texto = fonte_record.render(f'Record: {record_atual}', True, (200, 200, 200))
        tela.blit(record_texto, (rect.centerx - record_texto.get_width()//2, 350))
    
    # Instruções
    fonte_instrucoes = pygame.font.SysFont('Arial', 24)
    instrucoes = fonte_instrucoes.render('Pressione R para voltar ao menu', True, (150, 150, 150))
    tela.blit(instrucoes, (rect.centerx - instrucoes.get_width()//2, 450))


def desenhar_hud_jogo(tela, pontuacao, obstaculos, playlist_manager, record_manager, game_state=None):
    """Desenha o HUD durante o jogo"""
    # Pontuação
    fonte = pygame.font.SysFont('Arial', 28)
    tela.blit(fonte.render(f'Pontuação: {pontuacao}', True, (255,255,255)), (10, 10))
    
    # Record
    record_atual = record_manager.obter_record()
    fonte_record = pygame.font.SysFont('Arial', 20)
    record_texto = fonte_record.render(f'Record: {record_atual}', True, (200, 200, 200))
    tela.blit(record_texto, (10, 40))
    
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
        
        # Mostra status do mute
        if playlist_manager.mute_ativo or playlist_manager.volume == 0:
            texto_musica = fonte_musica.render(f'🔇 {nome_musica} (MUTADO)', True, (255, 100, 100))
        elif playlist_manager.pausado:
            texto_musica = fonte_musica.render(f'⏸️ {nome_musica} (PAUSADO)', True, (255, 165, 0))  # Laranja
        else:
            texto_musica = fonte_musica.render(f'🎵 {nome_musica}', True, (200, 200, 200))
        
        tela.blit(texto_musica, (10, TELA_ALTURA - 30))
        
        # Controles da playlist - MELHORADO
        if playlist_manager.mute_ativo or playlist_manager.volume == 0:
            controles = fonte_musica.render('N: Próxima | R: Aleatória | P: Pausar | M: Desmutar', True, (255, 150, 150))
        elif playlist_manager.pausado:
            controles = fonte_musica.render('N: Próxima | R: Aleatória | P: Despausar | M: Mutar', True, (255, 200, 150))
        else:
            controles = fonte_musica.render('N: Próxima | R: Aleatória | P: Pausar | M: Mutar', True, (150, 150, 150))
        
        tela.blit(controles, (10, TELA_ALTURA - 50))
        
        # Controles de volume
        fonte_volume = pygame.font.SysFont('Arial', 14)
        controles_volume = fonte_volume.render('+/-: Ajustar Volume | 0: Resetar Volume', True, (150, 150, 150))
        tela.blit(controles_volume, (10, TELA_ALTURA - 70))
        
        # Mostra volume atual
        if not playlist_manager.mute_ativo:
            volume_texto = fonte_volume.render(f'Volume: {int(playlist_manager.volume * 100)}%', True, (200, 200, 200))
            tela.blit(volume_texto, (TELA_LARGURA - volume_texto.get_width() - 10, TELA_ALTURA - 30))
        
        # Comando para resetar record
        fonte_record_controle = pygame.font.SysFont('Arial', 14)
        record_controle = fonte_record_controle.render('F1: Resetar Record', True, (100, 100, 100))
        tela.blit(record_controle, (10, TELA_ALTURA - 90)) 