# -*- coding: utf-8 -*-
"""
Velozes e Assados - Jogo de Corrida
Arquivo principal simplificado usando arquitetura modular
"""

import pygame
import sys
import os
import random

# Importa módulos da nova arquitetura
from src.config import *
from src.utils.road_detection import detect_asphalt_bounds
from src.entities.player import CarroJogador
from src.entities.obstacles import Obstaculo
from src.managers.playlist import PlaylistManager
from src.game_states import GameStateManager


def main():
    pygame.init()
    pygame.mixer.init()
    tela = pygame.display.set_mode((TELA_LARGURA, TELA_ALTURA))
    pygame.display.set_caption('Velozes e Assados')
    clock = pygame.time.Clock()

    # Trilha do menu
    trilha_abertura = os.path.join("assets", "sounds", "abertura.mp3")
    if os.path.exists(trilha_abertura):
        pygame.mixer.music.load(trilha_abertura)
        pygame.mixer.music.play(-1)

    # Sprites
    img_carro_jogador = pygame.image.load(os.path.join("assets", "images", "carro_jogador.png")).convert_alpha()

    # Estrada
    img_road_orig = pygame.image.load(os.path.join("assets", "images", "road.png")).convert()
    road_width = min(img_road_orig.get_width(), int(TELA_LARGURA * 0.4))
    img_road = pygame.transform.smoothscale(img_road_orig, (road_width, img_road_orig.get_height()))
    H_tile = img_road.get_height()
    road_x = (TELA_LARGURA - road_width) // 2
    road_y1, road_y2 = 0, -H_tile
    road_speed = 200.0
    road_accel = 8.0

    # Detecta asfalto e define faixas
    inner_x, inner_w = detect_asphalt_bounds(img_road, road_x)
    lane_w = inner_w // LANE_COUNT
    lane_centers = [inner_x + lane_w//2 + i*lane_w for i in range(LANE_COUNT)]

    carro = CarroJogador(img_carro_jogador, inner_x, inner_w, lane_w)

    obstaculos = []
    spawn_timer = 0.0
    spawn_interval = 0.7
    vel_obst = OBST_VEL_INICIAL
    pontuacao = 0
    dificuldade = 1

    ultimo_t = pygame.time.get_ticks() / 1000.0

    # Gerenciadores
    playlist_manager = PlaylistManager()
    game_state = GameStateManager(tela, playlist_manager)
    
    # Debug: verifica se a playlist foi carregada
    print(f"🎵 Playlist inicializada com {len(playlist_manager.musicas)} músicas")
    if playlist_manager.musicas:
        print(f"🎵 Músicas disponíveis: {[os.path.basename(m) for m in playlist_manager.musicas]}")

    while True:
        agora = pygame.time.get_ticks() / 1000.0
        dt = agora - ultimo_t
        ultimo_t = agora
        dt = min(dt, 0.05)  # evita "teleporte" em quedas de FPS

        # Processa eventos
        eventos = pygame.event.get()
        if not game_state.processar_eventos(eventos, carro, obstaculos, trilha_abertura):
            break

        # Atualiza estado do jogo
        estado = game_state.estado_atual

        if estado == MENU:
            # Toca música de abertura apenas se não estiver tocando
            if not pygame.mixer.music.get_busy() and os.path.exists(trilha_abertura):
                pygame.mixer.music.load(trilha_abertura)
                pygame.mixer.music.play(-1)
                print("🎵 Tocando música de abertura")

        elif estado == JOGANDO:
            # Para trilha do menu apenas uma vez e inicia playlist do jogo
            if not hasattr(game_state, '_musica_abertura_parada'):
                if pygame.mixer.music.get_busy():
                    pygame.mixer.music.stop()
                    print("🛑 Parando música de abertura")
                game_state._musica_abertura_parada = True

            # Gerencia playlist
            game_state.gerenciar_musica_jogo()
            
            # Debug: mostra status da música
            if playlist_manager.musica_atual:
                print(f"🎵 Status: {os.path.basename(playlist_manager.musica_atual)} - Tocando: {pygame.mixer.music.get_busy()}")

            # LIMPAR A TELA DO FRAME ANTERIOR
            tela.fill((50, 150, 50))

            # Estrada infinita (duas cópias)
            road_y1 += road_speed * dt
            road_y2 += road_speed * dt
            if road_y1 >= TELA_ALTURA: road_y1 = road_y2 - H_tile
            if road_y2 >= TELA_ALTURA: road_y2 = road_y1 - H_tile
            tela.blit(img_road, (road_x, int(road_y1)))
            tela.blit(img_road, (road_x, int(road_y2)))
            road_speed += road_accel * dt

            # Jogador
            teclas = pygame.key.get_pressed()
            carro.mover(teclas, dt)
            carro.desenhar(tela)

            # Spawns (tempo real)
            spawn_timer += dt
            if spawn_timer >= spawn_interval:
                obstaculos.append(Obstaculo(vel_obst, lane_centers, lane_w))
                spawn_timer = 0.0
                spawn_interval = max(0.35, spawn_interval - 0.02)  # mais agressivo

            # Obstáculos + colisão
            for obst in obstaculos[:]:
                # Atualiza posição do jogador para polícia inteligente
                if obst.eh_policia:
                    obst.atualizar_posicao_jogador(carro.x + carro.largura // 2)
                    obst.dificuldade_jogo = dificuldade
                
                obst.mover(dt)
                obst.desenhar(tela)

                if obst.fora_da_tela():
                    obstaculos.remove(obst)
                    pontuacao += 1
                    if pontuacao % 10 == 0:
                        dificuldade += 1
                        vel_obst += 40  # aumento mais perceptível
                        
                        # Ajusta volume da playlist baseado na dificuldade
                        if PLAYLIST_AGGRESSIVE_MODE:
                            novo_volume = min(1.0, PLAYLIST_VOLUME + (dificuldade - 1) * 0.05)
                            playlist_manager.definir_volume(novo_volume)
                    continue

            # Verifica colisão
            if game_state.verificar_colisao(carro, obstaculos, pontuacao):
                # Reseta variáveis do jogo
                carro = CarroJogador(img_carro_jogador, inner_x, inner_w, lane_w)
                obstaculos.clear()
                spawn_timer = 0.0
                spawn_interval = 0.7
                vel_obst = OBST_VEL_INICIAL
                pontuacao = 0
                dificuldade = 1
                road_y1, road_y2 = 0, -H_tile
                road_speed = 200.0

        # Desenha interface baseada no estado
        game_state.desenhar(pontuacao, obstaculos if estado == JOGANDO else None)
        
        # Atualiza playlist
        game_state.atualizar_playlist(dt)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main() 