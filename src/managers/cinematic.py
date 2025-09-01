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
from ..config import TELA_LARGURA, TELA_ALTURA


class CinematicManager:
    def __init__(self):
        self.video_path = os.path.join("assets", "videos", "cinematic.mp4")
        self.playing = False
        self.finished = False
        self.cap = None
        self.fps = 30
        self.frame_delay = 1.0 / self.fps
        self.frame_timer = 0.0
        self.current_frame = None

        self.audio_path = None     # caminho do .wav temporário (se usar ffmpeg)
        self.audio_extracted = False
        self.video_vertical = False

        if not os.path.exists(self.video_path):
            print(f"⚠️ Arquivo de cinemática não encontrado: {self.video_path}")
            print("📝 Coloque 'cinematic.mp4' em assets/videos/")
            self.available = False
        else:
            print(f"✅ Cinemática carregada: {self.video_path}")
            self.available = True

            video_dir = os.path.dirname(self.video_path)
            video_name = os.path.splitext(os.path.basename(self.video_path))[0]
            self.separate_audio_path = os.path.join(video_dir, f"{video_name}.wav")
            self.has_separate_audio = os.path.exists(self.separate_audio_path)
            if self.has_separate_audio:
                print(f"🎵 Áudio separado detectado: {self.separate_audio_path}")
            else:
                print("🔇 Nenhum WAV separado encontrado.")

    # ---- inicialização de áudio ----
    def _ensure_mixer(self):
        try:
            # Garante que o mixer casa com o WAV (44.1kHz, 16-bit, estéreo)
            if not pygame.mixer.get_init():
                pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=1024)
                pygame.mixer.init()
            pygame.mixer.music.set_volume(1.0)
            return True
        except Exception as e:
            print(f"🔇 Mixer não pôde iniciar: {e}")
            return False

    def _stop_any_music(self):
        try:
            if pygame.mixer.get_init() and pygame.mixer.music.get_busy():
                pygame.mixer.music.stop()
        except Exception:
            pass

    # ---- ciclo de vida da cinematic ----
    def iniciar_cinematic(self):
        if not self.available:
            print("❌ Cinemática não disponível - fallback.")
            self.iniciar_fallback()
            return True

        try:
            self.cap = cv2.VideoCapture(self.video_path)
            if not self.cap.isOpened():
                raise Exception("Não foi possível abrir o vídeo")

            self.fps = self.cap.get(cv2.CAP_PROP_FPS) or 30
            self.frame_delay = 1.0 / self.fps
            self.frame_timer = 0.0

            width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            if height > width:
                print(f"📱 Vídeo vertical detectado ({width}x{height})")
                self.video_vertical = True
            else:
                print(f"🖥️ Vídeo horizontal detectado ({width}x{height})")
                self.video_vertical = False

            self.playing = True
            self.finished = False
            print(f"🎬 Iniciando cinemática @ {self.fps:.2f} FPS")

            # Áudio
            if self._ensure_mixer():
                self._stop_any_music()
                self._extrair_ou_carregar_audio()
            else:
                print("⚠️ Sem mixer de áudio: cinemática rodará muda.")

            return True

        except Exception as e:
            print(f"❌ Erro na cinemática: {e}")
            self.iniciar_fallback()
            return True

    def iniciar_fallback(self):
        self.playing = True
        self.finished = False
        self.fallback_timer = 0.0
        self.fallback_duration = 8.0
        print("🎬 Modo fallback ativado (sem vídeo/áudio)")

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

                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w = frame_rgb.shape[:2]

                # Corrige orientação para vídeos verticais (gira 90° horário)
                if self.video_vertical or h > w:
                    frame_rgb = cv2.rotate(frame_rgb, cv2.ROTATE_90_CLOCKWISE)
                    h, w = frame_rgb.shape[:2]

                # Letterbox dentro de 1280x720
                scale = min(TELA_LARGURA / w, TELA_ALTURA / h)
                new_w, new_h = int(w * scale), int(h * scale)
                resized = cv2.resize(frame_rgb, (new_w, new_h), interpolation=cv2.INTER_LINEAR)

                canvas = np.zeros((TELA_ALTURA, TELA_LARGURA, 3), dtype=np.uint8)
                y = (TELA_ALTURA - new_h) // 2
                x = (TELA_LARGURA - new_w) // 2
                canvas[y:y+new_h, x:x+new_w] = resized

                # Converte para Surface (buffer direto evita giro indesejado)
                self.current_frame = pygame.image.frombuffer(
                    canvas.tobytes(), (TELA_LARGURA, TELA_ALTURA), "RGB"
                )
        else:
            # fallback
            self.fallback_timer += dt
            if self.fallback_timer >= self.fallback_duration:
                self.finalizar_cinematic()

    def pular_cinematic(self):
        if self.playing:
            self._stop_any_music()
            if self.cap and self.cap.isOpened():
                self.cap.release()
            self.playing = False
            self.finished = True
            self._limpar_audio_temp()
            print("⏭️ Cinemática pulada")

    def finalizar_cinematic(self):
        if self.playing:
            self._stop_any_music()
            if self.cap and self.cap.isOpened():
                self.cap.release()
            self.playing = False
            self.finished = True
            self._limpar_audio_temp()
            print("✅ Cinemática finalizada")

    # ---- áudio ----
    def _extrair_ou_carregar_audio(self):
        # 1) WAV separado
        if self.has_separate_audio:
            try:
                pygame.mixer.music.load(self.separate_audio_path)
                pygame.mixer.music.play()
                self.audio_extracted = True
                print(f"🔊 Reproduzindo WAV separado: {self.separate_audio_path}")
                return
            except Exception as e:
                print(f"⚠️ Falha ao tocar WAV separado: {e}")

        # 2) Extrair com ffmpeg
        try:
            tmp = tempfile.NamedTemporaryFile(suffix='.wav', delete=False)
            tmp.close()
            self.audio_path = tmp.name

            cmd = [
                'ffmpeg', '-i', self.video_path,
                '-vn', '-acodec', 'pcm_s16le',
                '-ar', '44100', '-ac', '2',
                '-y', self.audio_path
            ]
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0 and os.path.exists(self.audio_path):
                pygame.mixer.music.load(self.audio_path)
                pygame.mixer.music.play()
                self.audio_extracted = True
                print(f"🎵 Áudio extraído e reproduzido: {self.audio_path}")
                return
            else:
                print("⚠️ ffmpeg não conseguiu extrair o áudio:", result.stderr[:200])
        except FileNotFoundError:
            print("⚠️ ffmpeg não encontrado no PATH. Instale-o ou forneça um WAV separado.")
        except Exception as e:
            print(f"⚠️ Erro ao extrair/tocar áudio: {e}")

        self.audio_extracted = False
        print("🔇 Sem áudio na cinemática.")

    def _limpar_audio_temp(self):
        if self.audio_path and os.path.exists(self.audio_path):
            try:
                os.remove(self.audio_path)
                print(f"🗑️ WAV temporário removido: {self.audio_path}")
            except Exception as e:
                print(f"⚠️ Erro ao remover WAV temporário: {e}")

    # ---- consultas ----
    def obter_frame_atual(self):
        return self.current_frame

    def esta_reproduzindo(self):
        return self.playing

    def esta_finalizada(self):
        return self.finished

    def esta_disponivel(self):
        return self.available

    def esta_em_fallback(self):
        return self.playing and not self.cap
