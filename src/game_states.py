# -*- coding: utf-8 -*-
"""
Gerenciamento dos estados do jogo
"""

import pygame
import os
from .config import MENU, JOGANDO, GAME_OVER, TELA_LARGURA, TELA_ALTURA
from .ui.hud import desenhar_tela_abertura, desenhar_tela_gameover, desenhar_hud_jogo
from .managers.collision import check_collision


class GameStateManager:
    def __init__(self, tela, playlist_manager):
        self.tela = tela
        self.playlist_manager = playlist_manager
        self.estado = MENU
        
        # Carrega imagens das telas
        self.img_abertura = self._carregar_imagem_abertura()
        self.img_gameover = self._carregar_imagem_gameover()
    
    def _carregar_imagem_abertura(self):
        """Carrega a imagem de abertura"""
        img = pygame.image.load(os.path.join("assets", "images", "abertura.png")).convert()
        return pygame.transform.scale(img, (TELA_LARGURA, TELA_ALTURA))
    
    def _carregar_imagem_gameover(self):
        """Carrega a imagem de game over"""
        img = pygame.image.load(os.path.join("assets", "images", "gameover.png")).convert()
        return pygame.transform.scale(img, (TELA_LARGURA, TELA_ALTURA))
    
    def processar_eventos(self, eventos, carro, obstaculos, trilha_abertura):
        """Processa eventos baseado no estado atual"""
        for e in eventos:
            if e.type == pygame.QUIT:
                return False  # Sinaliza para sair do jogo
            
            if self.estado == MENU and e.type == pygame.KEYDOWN and e.key == pygame.K_SPACE:
                self.iniciar_jogo()
                
            elif self.estado == GAME_OVER and e.type == pygame.KEYDOWN and e.key == pygame.K_r:
                self.voltar_ao_menu(trilha_abertura)
            
            # Controles da playlist durante o jogo
            elif self.estado == JOGANDO and e.type == pygame.KEYDOWN:
                self._processar_controles_playlist(e)
        
        return True  # Continua o jogo
    
    def iniciar_jogo(self):
        """Inicia o jogo"""
        self.estado = JOGANDO
        # Reseta flag para permitir que a música de abertura seja parada
        if hasattr(self, '_musica_abertura_parada'):
            delattr(self, '_musica_abertura_parada')
        print("🎮 Iniciando jogo...")
    
    def voltar_ao_menu(self, trilha_abertura):
        """Volta ao menu principal"""
        self.estado = MENU
        # Para playlist e volta para música do menu
        self.playlist_manager.parar_com_fade()
        # Reseta flag para permitir que a música de abertura seja tocada novamente
        if hasattr(self, '_musica_abertura_parada'):
            delattr(self, '_musica_abertura_parada')
        if os.path.exists(trilha_abertura):
            pygame.mixer.music.load(trilha_abertura)
            pygame.mixer.music.play(-1)
    
    def _processar_controles_playlist(self, evento):
        """Processa controles da playlist"""
        if evento.key == pygame.K_n:  # Próxima música
            self.playlist_manager.tocar_proxima()
        elif evento.key == pygame.K_r:  # Música aleatória
            self.playlist_manager.tocar_aleatoria()
        elif evento.key == pygame.K_p:  # Pausar/Despausar
            if pygame.mixer.music.get_busy():
                self.playlist_manager.pausar()
            else:
                self.playlist_manager.despausar()
        elif evento.key == pygame.K_m:  # Mudo/Desmudo
            if self.playlist_manager.volume > 0:
                self.playlist_manager.definir_volume(0.0)
            else:
                from .config import PLAYLIST_VOLUME
                self.playlist_manager.definir_volume(PLAYLIST_VOLUME)
    
    def verificar_colisao(self, carro, obstaculos, pontuacao_atual):
        """Verifica colisão entre carro e obstáculos"""
        for obst in obstaculos:
            if check_collision(carro, obst):
                self.game_over(pontuacao_atual)
                return True
        return False
    
    def game_over(self, pontuacao_final):
        """Define estado de game over"""
        # Para playlist quando perde
        self.playlist_manager.parar_com_fade()
        self.estado = GAME_OVER
        # Armazena a pontuação final
        self.pontuacao_final = pontuacao_final
    
    def desenhar(self, pontuacao=0, obstaculos=None):
        """Desenha o estado atual"""
        if self.estado == MENU:
            desenhar_tela_abertura(self.tela, self.img_abertura)
        elif self.estado == JOGANDO:
            if obstaculos:
                desenhar_hud_jogo(self.tela, pontuacao, obstaculos, self.playlist_manager)
        elif self.estado == GAME_OVER:
            # Usa a pontuação final armazenada no game over
            pontuacao_final = getattr(self, 'pontuacao_final', 0)
            desenhar_tela_gameover(self.tela, pontuacao_final, self.img_gameover)
    
    def atualizar_playlist(self, dt):
        """Atualiza o gerenciador de playlist"""
        if self.estado == JOGANDO:
            self.playlist_manager.atualizar(dt)
    
    def gerenciar_musica_jogo(self):
        """Gerencia a música durante o jogo"""
        if self.estado == JOGANDO:
            # Garante que a playlist esteja tocando
            if not self.playlist_manager.musica_atual:
                print("🚀 Iniciando playlist do jogo...")
                self.playlist_manager.tocar_aleatoria()
            
            # Verifica se a música atual terminou e toca a próxima
            if self.playlist_manager.musica_atual and not pygame.mixer.music.get_busy():
                print("🔄 Música terminou, tocando próxima...")
                self.playlist_manager.tocar_proxima()
    
    @property
    def estado_atual(self):
        return self.estado 