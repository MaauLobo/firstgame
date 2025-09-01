# -*- coding: utf-8 -*-
"""
Gerenciamento dos estados do jogo
"""

import pygame
import os
from .config import MENU, CINEMATICA, JOGANDO, GAME_OVER, POWERUP_HELP, TELA_LARGURA, TELA_ALTURA
from .ui.hud import desenhar_tela_abertura, desenhar_tela_gameover, desenhar_hud_jogo, desenhar_tela_cinematic, desenhar_tela_powerup_help
from .managers.collision import check_collision
from .managers.record import RecordManager
from .managers.cinematic import CinematicManager


class GameStateManager:
    def __init__(self, tela, playlist_manager):
        self.tela = tela
        self.playlist_manager = playlist_manager
        self.estado = MENU
        
        # Carrega imagens das telas
        self.img_abertura = self._carregar_imagem_abertura()
        self.img_gameover = self._carregar_imagem_gameover()
        
        # Sistema de mute melhorado
        self.mute_ativo = False
        self.volume_anterior = 0.7  # Volume antes de mutar
        
        # Sistema de record
        self.record_manager = RecordManager()
        self.novo_record_atingido = False
        
        # Sistema de cinemática
        self.cinematic_manager = CinematicManager()
        self.cinematic_timer = 0.0
        self.cinematic_duration = 10.0  # Duração da cinemática em segundos (fallback)
    
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
            
            if self.estado == MENU and e.type == pygame.KEYDOWN:
                if e.key == pygame.K_SPACE:
                    self.iniciar_cinematic()
                elif e.key == pygame.K_h:
                    self.mostrar_ajuda_powerups()
                
            elif self.estado == CINEMATICA and e.type == pygame.KEYDOWN and e.key == pygame.K_SPACE:
                self.pular_cinematic()
                
            elif self.estado == GAME_OVER and e.type == pygame.KEYDOWN and e.key == pygame.K_r:
                self.voltar_ao_menu(trilha_abertura)
            
            # Controles da playlist durante o jogo
            elif self.estado == JOGANDO and e.type == pygame.KEYDOWN:
                self._processar_controles_playlist(e)
                
                # Tecla H para mostrar ajuda dos power-ups
                if e.key == pygame.K_h:
                    self.mostrar_ajuda_powerups()
                    
            # Voltar do menu de ajuda dos power-ups
            elif self.estado == POWERUP_HELP and e.type == pygame.KEYDOWN and e.key == pygame.K_h:
                self.voltar_do_ajuda_powerups()
        
        return True  # Continua o jogo
    
    def iniciar_cinematic(self):
        """Inicia a cinemática"""
        if self.cinematic_manager.esta_disponivel():
            # Para a música de abertura antes de iniciar a cinemática
            if pygame.mixer.music.get_busy():
                pygame.mixer.music.stop()
                print("🛑 Parando música de abertura para cinemática")
            
            self.estado = CINEMATICA
            self.cinematic_timer = 0.0
            self.cinematic_manager.iniciar_cinematic()
            print("🎬 Iniciando cinemática...")
        else:
            # Se não há cinemática, vai direto para o jogo
            self.iniciar_jogo()
    
    def pular_cinematic(self):
        """Pula a cinemática e inicia o jogo"""
        self.cinematic_manager.pular_cinematic()
        self.iniciar_jogo()
    
    def atualizar_cinematic(self, dt):
        """Atualiza o estado da cinemática"""
        if self.estado == CINEMATICA:
            # Atualiza a cinemática
            self.cinematic_manager.atualizar(dt)
            
            # Verifica se a cinemática terminou
            if self.cinematic_manager.esta_finalizada():
                self.iniciar_jogo()
    
    def iniciar_jogo(self):
        """Inicia o jogo"""
        self.estado = JOGANDO
        # Reseta flag para permitir que a música de abertura seja parada
        if hasattr(self, '_musica_abertura_parada'):
            delattr(self, '_musica_abertura_parada')
        # Reseta flag de novo record
        self.novo_record_atingido = False
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
        print(f"🔍 Processando tecla: {evento.key} (P={pygame.K_p}, N={pygame.K_n}, R={pygame.K_r})")
        
        # Teste específico para tecla P
        if evento.key == pygame.K_p:
            print("🎯 TECLA P DETECTADA!")
            print(f"🔍 Status detalhado: pausado={self.playlist_manager.pausado}, tocando={pygame.mixer.music.get_busy()}")
            
            if self.playlist_manager.pausado:
                print("🔄 Tentando despausar...")
                self.playlist_manager.despausar()
            else:
                print("🔄 Tentando pausar...")
                self.playlist_manager.pausar()
            return  # Para garantir que não processe outras condições
        
        elif evento.key == pygame.K_n:  # Próxima música
            print("🔄 Próxima música...")
            self.playlist_manager.tocar_proxima()
        elif evento.key == pygame.K_r:  # Música aleatória
            print("🔄 Música aleatória...")
            self.playlist_manager.tocar_aleatoria()
        elif evento.key == pygame.K_m:  # Mudo/Desmudo - SISTEMA MELHORADO
            self._alternar_mute()
        elif evento.key == pygame.K_F1:  # Resetar record
            self.record_manager.resetar_record()
            print("🔄 Record resetado!")
        elif evento.key == pygame.K_PLUS or evento.key == pygame.K_EQUALS:  # Aumentar volume
            self._aumentar_volume()
        elif evento.key == pygame.K_MINUS:  # Diminuir volume
            self._diminuir_volume()
        elif evento.key == pygame.K_0:  # Resetar volume para padrão
            self._resetar_volume()
        else:
            print(f"🔍 Tecla não reconhecida: {evento.key}")
    
    def _aumentar_volume(self):
        """Aumenta o volume da música"""
        if not self.mute_ativo:
            volume_atual = self.playlist_manager.volume
            novo_volume = min(1.0, volume_atual + 0.1)  # Aumenta 10%
            self.playlist_manager.definir_volume(novo_volume)
            self.volume_anterior = novo_volume
            print(f"🔊 Volume aumentado: {novo_volume:.1f}")
        else:
            print("🔇 Não é possível ajustar volume quando mutado")
    
    def _diminuir_volume(self):
        """Diminui o volume da música"""
        if not self.mute_ativo:
            volume_atual = self.playlist_manager.volume
            novo_volume = max(0.0, volume_atual - 0.1)  # Diminui 10%
            self.playlist_manager.definir_volume(novo_volume)
            self.volume_anterior = novo_volume
            print(f"🔊 Volume diminuído: {novo_volume:.1f}")
        else:
            print("🔇 Não é possível ajustar volume quando mutado")
    
    def _resetar_volume(self):
        """Reseta o volume para o padrão"""
        if not self.mute_ativo:
            from .config import PLAYLIST_VOLUME
            self.playlist_manager.definir_volume(PLAYLIST_VOLUME)
            self.volume_anterior = PLAYLIST_VOLUME
            print(f"🔊 Volume resetado para padrão: {PLAYLIST_VOLUME:.1f}")
        else:
            print("🔇 Não é possível ajustar volume quando mutado")
    
    def _alternar_mute(self):
        """Alterna entre mute e desmute com um clique"""
        if not self.mute_ativo:
            # Ativa mute
            self.volume_anterior = self.playlist_manager.volume
            self.playlist_manager.ativar_mute()
            self.mute_ativo = True
            print("🔇 Música mutada")
        else:
            # Desativa mute e restaura volume anterior
            self.playlist_manager.desativar_mute()
            # Restaura o volume personalizado que estava antes
            self.playlist_manager.definir_volume(self.volume_anterior)
            self.mute_ativo = False
            print(f"🔊 Música desmutada (volume: {self.volume_anterior:.1f})")
    
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
        
        # Verifica se é um novo record
        if self.record_manager.verificar_novo_record(pontuacao_final):
            self.novo_record_atingido = True
            print(f"🏆 NOVO RECORD! {pontuacao_final} pontos!")
        else:
            self.novo_record_atingido = False
            print(f"📊 Pontuação: {pontuacao_final} | Record: {self.record_manager.obter_record()}")
    
    def desenhar(self, pontuacao=0, obstaculos=None, powerup_manager=None):
        """Desenha o estado atual"""
        if self.estado == MENU:
            desenhar_tela_abertura(self.tela, self.img_abertura)
        elif self.estado == CINEMATICA:
            desenhar_tela_cinematic(self.tela, self.cinematic_manager)
        elif self.estado == JOGANDO:
            if obstaculos:
                desenhar_hud_jogo(self.tela, pontuacao, obstaculos, self.playlist_manager, self.record_manager, powerup_manager, self)
        elif self.estado == POWERUP_HELP:
            desenhar_tela_powerup_help(self.tela)
        elif self.estado == GAME_OVER:
            # Usa a pontuação final armazenada no game over
            pontuacao_final = getattr(self, 'pontuacao_final', 0)
            desenhar_tela_gameover(self.tela, pontuacao_final, self.img_gameover, self.record_manager, self.novo_record_atingido)
    
    def atualizar_playlist(self, dt):
        """Atualiza o gerenciador de playlist"""
        if self.estado == JOGANDO:
            self.playlist_manager.atualizar(dt)
    
    def mostrar_ajuda_powerups(self):
        """Mostra a tela de ajuda dos power-ups"""
        self.estado_anterior = self.estado
        self.estado = POWERUP_HELP
        print("📖 Mostrando ajuda dos power-ups")
    
    def voltar_do_ajuda_powerups(self):
        """Volta do menu de ajuda dos power-ups para o estado anterior"""
        # Se estava no menu, volta para o menu. Se estava jogando, volta para o jogo
        if hasattr(self, 'estado_anterior'):
            self.estado = self.estado_anterior
        else:
            self.estado = MENU
        print("🎮 Voltando ao estado anterior")
    
    def gerenciar_musica_jogo(self):
        """Gerencia a música durante o jogo"""
        if self.estado == JOGANDO:
            # Garante que a playlist esteja tocando
            if not self.playlist_manager.musica_atual:
                print("🚀 Iniciando playlist do jogo...")
                self.playlist_manager.tocar_aleatoria()
            
            # Verifica se a música atual terminou e toca a próxima
            # SÓ se não estiver pausado
            if (self.playlist_manager.musica_atual and 
                not pygame.mixer.music.get_busy() and 
                not self.playlist_manager.pausado):
                print("🔄 Música terminou, tocando próxima...")
                self.playlist_manager.tocar_proxima()
    
    @property
    def estado_atual(self):
        return self.estado 