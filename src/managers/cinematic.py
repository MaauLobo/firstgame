# -*- coding: utf-8 -*-
"""
Gerenciador de cinemática
"""

import os
import pygame
import cv2
import numpy as np
import subprocess
import tempfile
import wave
import struct
from ..config import TELA_LARGURA, TELA_ALTURA


class CinematicManager:
    def __init__(self):
        self.video_path = os.path.join("assets", "videos", "cinematic.mp4")
        self.playing = False
        self.finished = False
        self.surface = None
        self.cap = None
        self.fps = 30
        self.frame_delay = 1.0 / self.fps
        self.frame_timer = 0.0
        self.current_frame = None
        self.audio_path = None
        self.audio_extracted = False
        
        # Verifica se o arquivo existe
        if not os.path.exists(self.video_path):
            print(f"⚠️ Arquivo de cinemática não encontrado: {self.video_path}")
            print("📝 Coloque o arquivo 'cinematic.mp4' na pasta 'assets/videos/'")
            self.available = False
        else:
            print(f"✅ Cinemática carregada: {self.video_path}")
            self.available = True
            
            # Verifica se existe um arquivo de áudio separado
            video_dir = os.path.dirname(self.video_path)
            video_name = os.path.splitext(os.path.basename(self.video_path))[0]
            self.separate_audio_path = os.path.join(video_dir, f"{video_name}.wav")
            
            if os.path.exists(self.separate_audio_path):
                print(f"🎵 Arquivo de áudio separado encontrado: {self.separate_audio_path}")
                self.has_separate_audio = True
            else:
                print("🔇 Nenhum arquivo de áudio separado encontrado")
                self.has_separate_audio = False
    
    def iniciar_cinematic(self):
        """Inicia a reprodução da cinemática"""
        if not self.available:
            print("❌ Cinemática não disponível - usando modo fallback")
            self.iniciar_fallback()
            return True
        
        try:
            # Abre o vídeo com OpenCV
            self.cap = cv2.VideoCapture(self.video_path)
            if not self.cap.isOpened():
                raise Exception("Não foi possível abrir o vídeo")
            
            # Obtém informações do vídeo
            self.fps = self.cap.get(cv2.CAP_PROP_FPS)
            if self.fps <= 0:
                self.fps = 30  # FPS padrão se não conseguir detectar
            
            # Detecta a orientação do vídeo
            width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            
            if height > width:
                print(f"📱 Vídeo vertical detectado ({width}x{height}) - será rotacionado para horizontal")
                self.video_vertical = True
            else:
                print(f"🖥️ Vídeo horizontal detectado ({width}x{height})")
                self.video_vertical = False
            
            self.frame_delay = 1.0 / self.fps
            self.frame_timer = 0.0
            self.playing = True
            self.finished = False
            
            print(f"🎬 Iniciando cinemática - FPS: {self.fps}")
            
            # Extrai o áudio do vídeo se disponível
            self._extrair_audio()
            
            return True
            
        except Exception as e:
            print(f"❌ Erro ao reproduzir cinemática: {e}")
            print("🔄 Usando modo fallback...")
            self.iniciar_fallback()
            return True
    
    def _extrair_audio(self):
        """Extrai o áudio do vídeo para reprodução"""
        try:
            # Primeiro tenta usar o arquivo de áudio separado se disponível
            if hasattr(self, 'has_separate_audio') and self.has_separate_audio:
                try:
                    pygame.mixer.music.load(self.separate_audio_path)
                    pygame.mixer.music.play()
                    self.audio_extracted = True
                    print(f"🔊 Reproduzindo áudio separado: {self.separate_audio_path}")
                    return
                except Exception as e:
                    print(f"⚠️ Erro ao reproduzir áudio separado: {e}")
            
            # Tenta usar ffmpeg se estiver disponível
            try:
                # Cria um arquivo temporário para o áudio
                temp_audio = tempfile.NamedTemporaryFile(suffix='.wav', delete=False)
                temp_audio.close()
                self.audio_path = temp_audio.name
                
                # Usa ffmpeg para extrair o áudio
                cmd = [
                    'ffmpeg', '-i', self.video_path, 
                    '-vn', '-acodec', 'pcm_s16le', 
                    '-ar', '44100', '-ac', '2', 
                    '-y', self.audio_path
                ]
                
                result = subprocess.run(cmd, capture_output=True, text=True)
                
                if result.returncode == 0 and os.path.exists(self.audio_path):
                    self.audio_extracted = True
                    print(f"🎵 Áudio extraído com ffmpeg: {self.audio_path}")
                    
                    # Carrega e reproduz o áudio
                    pygame.mixer.music.load(self.audio_path)
                    pygame.mixer.music.play()
                    print("🔊 Reproduzindo áudio da cinemática")
                    return
                    
            except FileNotFoundError:
                print("⚠️ ffmpeg não encontrado")
            
            # Se não conseguiu reproduzir áudio
            self.audio_extracted = False
            print("🔇 Cinemática sem áudio - apenas vídeo")
            print("💡 Para ter áudio:")
            print("   1. Instale o ffmpeg, ou")
            print("   2. Coloque um arquivo 'cinematic.wav' na pasta 'assets/videos/'")
                
        except Exception as e:
            print(f"⚠️ Erro ao configurar áudio: {e}")
            self.audio_extracted = False
    
    def iniciar_fallback(self):
        """Inicia o modo fallback (sem vídeo)"""
        self.playing = True
        self.finished = False
        self.fallback_timer = 0.0
        self.fallback_duration = 8.0
        print("🎬 Modo fallback ativado")
    
    def atualizar(self, dt):
        if not self.playing:
            return

        if self.cap and self.cap.isOpened():
            self.frame_timer += dt
            if self.frame_timer >= self.frame_delay:
                self.frame_timer = 0.0

                ret, frame = self.cap.read()
                if not ret:
                    self.finalizar_cinematic()
                    return

                # BGR -> RGB
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w = frame_rgb.shape[:2]

                # Corrige orientação: vídeos "em pé" giram 90° (não 180°)
                if h > w:
                    frame_rgb = cv2.rotate(frame_rgb, cv2.ROTATE_90_CLOCKWISE)
                    h, w = frame_rgb.shape[:2]

                # Mantém proporção (letterbox) dentro de 1280x720
                scale = min(TELA_LARGURA / w, TELA_ALTURA / h)
                new_w, new_h = int(w * scale), int(h * scale)
                resized = cv2.resize(frame_rgb, (new_w, new_h), interpolation=cv2.INTER_LINEAR)

                # Canvas preto 1280x720 com o vídeo centralizado
                canvas = np.zeros((TELA_ALTURA, TELA_LARGURA, 3), dtype=np.uint8)
                y = (TELA_ALTURA - new_h) // 2
                x = (TELA_LARGURA - new_w) // 2
                canvas[y:y+new_h, x:x+new_w] = resized

                # Converte para Surface sem girar (usa frombuffer ao invés de surfarray)
                self.current_frame = pygame.image.frombuffer(
                    canvas.tobytes(), (TELA_LARGURA, TELA_ALTURA), "RGB"
                )
        else:
            self.fallback_timer += dt
            if self.fallback_timer >= self.fallback_duration:
                self.finalizar_cinematic()
    
    def pular_cinematic(self):
        """Pula a cinemática"""
        if self.playing:
            # Para o áudio da cinemática
            if self.audio_extracted and pygame.mixer.music.get_busy():
                pygame.mixer.music.stop()
                print("🛑 Parando áudio da cinemática")
            
            if self.cap and self.cap.isOpened():
                self.cap.release()
            
            self.playing = False
            self.finished = True
            print("⏭️ Cinemática pulada")
    
    def finalizar_cinematic(self):
        """Marca a cinemática como finalizada"""
        if self.playing:
            # Para o áudio da cinemática
            if self.audio_extracted and pygame.mixer.music.get_busy():
                pygame.mixer.music.stop()
                print("🛑 Parando áudio da cinemática")
            
            if self.cap and self.cap.isOpened():
                self.cap.release()
            
            self.playing = False
            self.finished = True
            print("✅ Cinemática finalizada")
            
            # Limpa arquivo temporário de áudio
            self._limpar_audio_temp()
    
    def _limpar_audio_temp(self):
        """Remove arquivo temporário de áudio"""
        if self.audio_path and os.path.exists(self.audio_path):
            try:
                os.remove(self.audio_path)
                print(f"🗑️ Arquivo temporário removido: {self.audio_path}")
            except Exception as e:
                print(f"⚠️ Erro ao remover arquivo temporário: {e}")
    
    def obter_frame_atual(self):
        """Retorna o frame atual para desenhar"""
        return self.current_frame
    
    def esta_reproduzindo(self):
        """Retorna se a cinemática está sendo reproduzida"""
        return self.playing
    
    def esta_finalizada(self):
        """Retorna se a cinemática foi finalizada"""
        return self.finished
    
    def esta_disponivel(self):
        """Retorna se a cinemática está disponível"""
        return self.available
    
    def esta_em_fallback(self):
        """Retorna se está no modo fallback"""
        return self.playing and not self.cap 