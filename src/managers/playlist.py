# -*- coding: utf-8 -*-
"""
Gerenciador de playlist de músicas
"""

import os
import random
import pygame
from ..config import PLAYLIST_VOLUME, PLAYLIST_FADE_TIME


class PlaylistManager:
    def __init__(self):
        self.playlist_dir = os.path.join("assets", "sounds", "playlist")
        self.musicas = []
        self.musica_atual = None
        self.indice_atual = 0
        self.volume = PLAYLIST_VOLUME
        self.fade_timer = 0.0
        self.fade_duration = PLAYLIST_FADE_TIME
        self.fade_out = False
        self.mute_ativo = False  # Flag para controlar mute
        self.pausado = False  # Flag para controlar pausa
        
        self.carregar_playlist()
    
    def carregar_playlist(self):
        """Carrega todas as músicas da pasta playlist"""
        print(f"🔍 Procurando músicas em: {self.playlist_dir}")
        
        if os.path.exists(self.playlist_dir):
            arquivos = os.listdir(self.playlist_dir)
            print(f"📁 Arquivos encontrados: {arquivos}")
            
            for arquivo in arquivos:
                if arquivo.lower().endswith(('.mp3', '.wav', '.ogg')):
                    caminho_completo = os.path.join(self.playlist_dir, arquivo)
                    self.musicas.append(caminho_completo)
                    print(f"🎵 Adicionado: {arquivo}")
        
        # Embaralha a playlist para reprodução aleatória
        if self.musicas:
            random.shuffle(self.musicas)
            print(f"✅ Playlist carregada com {len(self.musicas)} músicas")
        else:
            print("❌ Nenhuma música encontrada na pasta playlist!")
    
    def tocar_proxima(self):
        """Toca a próxima música da playlist"""
        if not self.musicas:
            print("ERRO: Nenhuma música encontrada na playlist!")
            return
        
        # Para a música atual se estiver tocando
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()
        
        # Seleciona próxima música
        self.musica_atual = self.musicas[self.indice_atual]
        self.indice_atual = (self.indice_atual + 1) % len(self.musicas)
        
        try:
            pygame.mixer.music.load(self.musica_atual)
            # Aplica volume considerando mute
            volume_aplicar = 0.0 if self.mute_ativo else self.volume
            pygame.mixer.music.set_volume(volume_aplicar)
            pygame.mixer.music.play()
            self.pausado = False  # Reseta flag de pausa
            print(f"✅ Tocando próxima: {os.path.basename(self.musica_atual)}")
        except Exception as e:
            print(f"❌ Erro ao tocar música: {e}")
            self.musica_atual = None
    
    def tocar_aleatoria(self):
        """Toca uma música aleatória da playlist"""
        if not self.musicas:
            print("ERRO: Nenhuma música encontrada na playlist!")
            return
        
        # Escolhe uma música aleatória
        musica_aleatoria = random.choice(self.musicas)
        print(f"Tentando tocar: {musica_aleatoria}")
        
        # Para a música atual se estiver tocando
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()
        
        try:
            pygame.mixer.music.load(musica_aleatoria)
            # Aplica volume considerando mute
            volume_aplicar = 0.0 if self.mute_ativo else self.volume
            pygame.mixer.music.set_volume(volume_aplicar)
            pygame.mixer.music.play()
            self.musica_atual = musica_aleatoria
            self.pausado = False  # Reseta flag de pausa
            print(f"✅ Tocando aleatória: {os.path.basename(musica_aleatoria)}")
        except Exception as e:
            print(f"❌ Erro ao tocar música: {e}")
            self.musica_atual = None
    
    def atualizar(self, dt):
        """Atualiza o gerenciador de playlist"""
        # Gerencia fade out se necessário
        if self.fade_out:
            self.fade_timer += dt
            if self.fade_timer >= self.fade_duration:
                pygame.mixer.music.stop()
                self.fade_out = False
                self.fade_timer = 0.0
                # Não reseta musica_atual aqui para evitar problemas
            else:
                # Reduz volume gradualmente
                progresso = self.fade_timer / self.fade_duration
                volume_atual = self.volume * (1.0 - progresso)
                pygame.mixer.music.set_volume(volume_atual)
    
    def parar_com_fade(self):
        """Para a música com fade out suave"""
        print("🛑 Parando playlist com fade...")
        self.fade_out = True
        self.fade_timer = 0.0
    
    def definir_volume(self, volume):
        """Define o volume da playlist (0.0 a 1.0)"""
        self.volume = max(0.0, min(1.0, volume))
        # Só aplica o volume se não estiver mutado
        if pygame.mixer.music.get_busy() and not self.mute_ativo:
            pygame.mixer.music.set_volume(self.volume)
    
    def ativar_mute(self):
        """Ativa o mute"""
        self.mute_ativo = True
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.set_volume(0.0)
    
    def desativar_mute(self):
        """Desativa o mute"""
        self.mute_ativo = False
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.set_volume(self.volume)
    
    def pausar(self):
        """Pausa a música atual"""
        print(f"🔍 Tentando pausar - Status: pausado={self.pausado}, tocando={pygame.mixer.music.get_busy()}")
        if pygame.mixer.music.get_busy() and not self.pausado:
            pygame.mixer.music.pause()
            self.pausado = True
            print("⏸️ Música pausada com sucesso")
        else:
            if self.pausado:
                print("⚠️ Música já está pausada")
            else:
                print("⚠️ Música não está tocando")
    
    def despausar(self):
        """Despausa a música atual"""
        print(f"🔍 Tentando despausar - Status: pausado={self.pausado}")
        if self.pausado:
            pygame.mixer.music.unpause()
            self.pausado = False
            print("▶️ Música despausada com sucesso")
        else:
            print("⚠️ Música não está pausada") 