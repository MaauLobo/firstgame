import pygame
import sys
import os
import random
import numpy as np  # detecção da faixa de asfalto

# -------------------- Configurações --------------------
tela_largura = 1280
tela_altura = 720
FPS = 60

MENU, JOGANDO, GAME_OVER = 0, 1, 2

# Carros (tamanho alvo pela ALTURA; a largura será proporcional)
CARRO_VEL     = 380  # px/s
CARRO_ALTURA  = 90

# Obstáculos (altura alvo; largura proporcional)
OBST_ALTURA       = 90
OBST_VEL_INICIAL  = 280  # px/s

LANE_COUNT = 3
LANE_MARGIN = 6   # folga lateral dentro da faixa

# Colisão
COLLISION_MODE      = "mask"   # "shrink" ou "mask"
HITBOX_SHRINK_W     = 0.15     # 15% na largura (modo shrink)
HITBOX_SHRINK_H     = 0.18     # 18% na altura  (modo shrink)
ALPHA_THRESHOLD     = 50       # opacidade mínima p/ máscara
SHOW_HITBOX_DEBUG   = False

# Sirene
SIRENE_FPS = 8  # frames por segundo da animação da sirene
SIRENE_COLOR = (255, 0, 0)  # cor vermelha da sirene
POLICE_SPAWN_CHANCE = 0.15  # 15% de chance de spawnar carro da polícia
POLICE_SPECIAL_EFFECTS = True  # ativa efeitos especiais para carros da polícia

# Movimento da polícia
POLICE_LATERAL_SPEED = 120  # velocidade de movimento lateral (px/s)
POLICE_LANE_CHANGE_INTERVAL = 1.5  # tempo entre mudanças de faixa (segundos)
POLICE_TARGETING_RANGE = 200  # distância para começar a mirar no jogador (px)
POLICE_AGGRESSIVE_MODE = True  # ativa modo agressivo que aumenta com dificuldade

# Playlist
PLAYLIST_VOLUME = 0.7  # volume das músicas da playlist (0.0 a 1.0)
PLAYLIST_FADE_TIME = 1.0  # tempo de fade entre músicas (segundos)
PLAYLIST_AGGRESSIVE_MODE = True  # aumenta volume conforme dificuldade

# -------------------- Classe PlaylistManager --------------------
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
            pygame.mixer.music.set_volume(self.volume)
            pygame.mixer.music.play()
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
            pygame.mixer.music.set_volume(self.volume)
            pygame.mixer.music.play()
            self.musica_atual = musica_aleatoria
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
                self.musica_atual = None  # Reseta música atual
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
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.set_volume(self.volume)
    
    def pausar(self):
        """Pausa a música atual"""
        pygame.mixer.music.pause()
    
    def despausar(self):
        """Despausa a música atual"""
        pygame.mixer.music.unpause()

# -------------------- Classe SireneAnimacao --------------------
class SireneAnimacao:
    def __init__(self, x: int, y: int, largura: int, altura: int):
        self.x = x
        self.y = y
        self.largura = largura
        self.altura = altura
        
        # Carrega os frames da animação
        self.frames = []
        for i in range(1, 4):  # 1.png, 2.png, 3.png
            caminho = os.path.join("assets", "images", "Police_animation", f"{i}.png")
            if os.path.exists(caminho):
                img = pygame.image.load(caminho).convert_alpha()
                # Escala para o tamanho do carro da polícia
                img_scaled = pygame.transform.smoothscale(img, (largura, altura))
                self.frames.append(img_scaled)
        
        self.frame_atual = 0
        self.timer = 0.0
        self.frame_delay = 1.0 / SIRENE_FPS
        
        # Efeito de brilho da sirene
        self.brilho_timer = 0.0
        self.brilho_delay = 0.1  # 100ms para o efeito de brilho
        
    def atualizar(self, dt):
        # Atualiza animação dos frames
        self.timer += dt
        if self.timer >= self.frame_delay:
            self.timer = 0.0
            self.frame_atual = (self.frame_atual + 1) % len(self.frames)
        
        # Atualiza efeito de brilho
        self.brilho_timer += dt
        if self.brilho_timer >= self.brilho_delay:
            self.brilho_timer = 0.0
    
    def desenhar(self, tela):
        if self.frames:
            # Desenha o frame atual
            tela.blit(self.frames[self.frame_atual], (self.x, self.y))
            
            # Efeito de brilho da sirene (pisca)
            if self.brilho_timer < self.brilho_delay * 0.5:
                # Cria uma superfície para o efeito de brilho
                brilho_surf = pygame.Surface((self.largura, self.altura), pygame.SRCALPHA)
                pygame.draw.rect(brilho_surf, (*SIRENE_COLOR, 30), (0, 0, self.largura, self.altura))
                tela.blit(brilho_surf, (self.x, self.y))
                
            # Efeito de luz da sirene (raio de luz)
            if POLICE_SPECIAL_EFFECTS:
                # Cria um efeito de luz circular
                luz_surf = pygame.Surface((self.largura * 2, self.altura * 2), pygame.SRCALPHA)
                centro_x, centro_y = self.largura, self.altura
                raio = min(self.largura, self.altura) // 2
                
                # Gradiente radial para simular luz
                for r in range(raio, 0, -2):
                    alpha = max(0, 40 - (raio - r) * 2)
                    cor = (*SIRENE_COLOR, alpha)
                    pygame.draw.circle(luz_surf, cor, (centro_x, centro_y), r)
                
                tela.blit(luz_surf, (self.x - self.largura//2, self.y - self.altura//2))

# -------------------- Util: detectar asfalto --------------------
def detect_asphalt_bounds(surf: pygame.Surface, road_x: int) -> tuple[int, int]:
    """Retorna (inner_x, inner_w) detectando a região de asfalto no sprite."""
    arr = pygame.surfarray.array3d(surf).astype(np.float32) / 255.0  # (W,H,3)
    W, H = arr.shape[0], arr.shape[1]

    # downscale p/ acelerar
    target_w = min(256, W)
    scale = target_w / W
    if scale < 1.0:
        small = pygame.transform.smoothscale(surf, (target_w, int(H * scale)))
        arr = pygame.surfarray.array3d(small).astype(np.float32) / 255.0
        W, H = arr.shape[0], arr.shape[1]

    r, g, b = arr[...,0], arr[...,1], arr[...,2]
    mx = np.max(arr, axis=2)
    mn = np.min(arr, axis=2)
    diff = mx - mn

    S = np.where(mx == 0, 0, diff / (mx + 1e-6))
    V = mx

    y0, y1 = int(H*0.30), int(H*0.70)
    S_line = S[:, y0:y1].mean(axis=1)
    V_line = V[:, y0:y1].mean(axis=1)

    # thresholds (ajustáveis)
    asphalt_mask = (S_line < 0.40) & (V_line < 0.65)

    # fechamento simples
    k = 5
    pad = np.pad(asphalt_mask, (k//2,), constant_values=False)
    for _ in range(2):
        dil = np.convolve(pad.astype(np.uint8), np.ones(k, dtype=np.uint8), mode='same') > 0
        ero = np.convolve(dil.astype(np.uint8), np.ones(k, dtype=np.uint8), mode='same') == k
        pad = ero
    asphalt_mask = pad[k//2: -k//2]

    # maior bloco contínuo
    best_len, best_l, cur_l = 0, 0, None
    for i, v in enumerate(asphalt_mask):
        if v and cur_l is None:
            cur_l = i
        elif (not v or i == len(asphalt_mask)-1) and cur_l is not None:
            rgt = i if not v else i+1
            if rgt - cur_l > best_len:
                best_len, best_l = rgt - cur_l, cur_l
            cur_l = None

    if best_len <= 0:
        l_small = int(W*0.15); r_small = int(W*0.85)
    else:
        l_small = best_l; r_small = best_l + best_len

    if scale < 1.0:
        l_src = int(l_small / scale); r_src = int(r_small / scale)
    else:
        l_src, r_src = l_small, r_small

    inner_w_sprite = max(1, r_src - l_src)
    inner_x_screen = road_x + l_src
    return inner_x_screen, inner_w_sprite

# -------------------- Colisão helpers --------------------
def collide_shrink(a_rect: pygame.Rect, b_rect: pygame.Rect) -> bool:
    return a_rect.colliderect(b_rect)

def collide_mask(a, b) -> bool:
    offset = (int(b.x - a.x), int(b.y - a.y))
    return a.mask.overlap(b.mask, offset) is not None

# -------------------- Classes --------------------
class Obstaculo:
    inimigos_imgs = []
    inimigos_nomes = ["taxi.png", "audi.png", "car.png", "police.png"]

    @classmethod
    def carregar_imgs(cls):
        if not cls.inimigos_imgs:
            for nome in cls.inimigos_nomes:
                caminho = os.path.join("assets", "images", nome)
                img = pygame.image.load(caminho).convert_alpha()
                cls.inimigos_imgs.append(img)  # sem escala aqui

    def __init__(self, vel_px_s: float, lane_centers: list[int], lane_w: int):
        if not Obstaculo.inimigos_imgs:
            Obstaculo.carregar_imgs()

        # Escolhe uma imagem aleatória com chance especial para polícia
        if random.random() < POLICE_SPAWN_CHANCE:
            # Força spawn de carro da polícia
            img_index = Obstaculo.inimigos_nomes.index("police.png")
        else:
            # Escolhe aleatoriamente entre todos os carros (exceto polícia)
            carros_disponiveis = [i for i, nome in enumerate(Obstaculo.inimigos_nomes) if nome != "police.png"]
            img_index = random.choice(carros_disponiveis)
            
        base = Obstaculo.inimigos_imgs[img_index]
        self.nome_imagem = Obstaculo.inimigos_nomes[img_index]
        
        ow, oh = base.get_width(), base.get_height()

        # escala pela ALTURA alvo (OBST_ALTURA), preservando proporção
        scale = OBST_ALTURA / oh
        w = int(ow * scale)
        h = OBST_ALTURA

        # garante que cabe na faixa
        max_w = max(10, lane_w - 2*LANE_MARGIN)
        if w > max_w:
            s = max_w / w
            w = int(w * s)
            h = int(h * s)

        self.largura, self.altura = w, h
        self.img  = pygame.transform.smoothscale(base, (w, h)).convert_alpha()
        self.mask = pygame.mask.from_surface(self.img, ALPHA_THRESHOLD)

        self.vel = vel_px_s
        center = random.choice(lane_centers)
        self.x = center - self.largura // 2
        self.y = -self.altura
        
        # Guarda informações das faixas para movimento da polícia
        self.lane_centers = lane_centers
        self.lane_w = lane_w
        
        # Cria animação da sirene se for carro da polícia
        self.sirene = None
        self.eh_policia = False
        if self.nome_imagem == "police.png":
            self.sirene = SireneAnimacao(self.x, self.y, self.largura, self.altura)
            self.eh_policia = True
            
            # Variáveis para movimento lateral da polícia
            self.lane_change_timer = 0.0
            # Detecta a faixa inicial baseada na posição
            self.current_lane = self._detectar_faixa_atual()
            self.target_lane_x = self.x
            self.moving_lateral = False

    def mover(self, dt):
        self.y += self.vel * dt
        
        # Movimento lateral especial para polícia
        if self.eh_policia:
            self._mover_policia_lateral(dt)
        
        # Atualiza posição da sirene se existir
        if self.sirene:
            self.sirene.x = self.x
            self.sirene.y = self.y
            self.sirene.atualizar(dt)

    def desenhar(self, tela):
        tela.blit(self.img, (int(self.x), int(self.y)))
        
        # Desenha a sirene se for carro da polícia
        if self.sirene:
            self.sirene.desenhar(tela)
        
        # Efeito visual quando a polícia está se movendo lateralmente
        if self.eh_policia and self.moving_lateral:
            # Desenha uma seta indicando o movimento
            seta_surf = pygame.Surface((20, 20), pygame.SRCALPHA)
            if self.x < self.target_lane_x:
                # Movendo para direita
                pygame.draw.polygon(seta_surf, (255, 255, 0, 180), [(0, 10), (20, 10), (15, 5), (15, 15)])
            else:
                # Movendo para esquerda
                pygame.draw.polygon(seta_surf, (255, 255, 0, 180), [(20, 10), (0, 10), (5, 5), (5, 15)])
            
            tela.blit(seta_surf, (self.x + self.largura // 2 - 10, self.y - 25))
        
        if SHOW_HITBOX_DEBUG:
            pygame.draw.rect(tela, (255,0,0), self.hit_rect, 2)
            if COLLISION_MODE == "mask":
                msurf = self.mask.to_surface(setcolor=(255,0,0,80), unsetcolor=(0,0,0,0))
                msurf.set_colorkey((0,0,0))
                tela.blit(msurf, (int(self.x), int(self.y)))
    
    def _mover_policia_lateral(self, dt):
        """Movimento lateral especial da polícia para tentar bloquear o jogador"""
        self.lane_change_timer += dt
        
        # Ajusta intervalo baseado na dificuldade (se ativado)
        intervalo_atual = POLICE_LANE_CHANGE_INTERVAL
        if POLICE_AGGRESSIVE_MODE and hasattr(self, 'dificuldade_jogo'):
            # Reduz o intervalo conforme a dificuldade aumenta
            intervalo_atual = max(0.5, POLICE_LANE_CHANGE_INTERVAL - (self.dificuldade_jogo - 1) * 0.1)
        
        # Decide se deve mudar de faixa
        if self.lane_change_timer >= intervalo_atual:
            self.lane_change_timer = 0.0
            
            # Comportamento inteligente: tenta bloquear o jogador se estiver próximo
            if hasattr(self, 'jogador_x') and self.y > tela_altura * 0.3:
                # Tenta se posicionar na faixa do jogador
                faixa_jogador = self._detectar_faixa_jogador()
                if faixa_jogador != self.current_lane:
                    nova_faixa = faixa_jogador
                else:
                    # Se já está na faixa do jogador, escolhe uma aleatória
                    nova_faixa = random.randint(0, 2)
            else:
                # Movimento aleatório normal
                nova_faixa = random.randint(0, 2)
            
            if nova_faixa != self.current_lane:
                self.current_lane = nova_faixa
                self.moving_lateral = True
                
                # Calcula a posição alvo na nova faixa
                target_center = self.lane_centers[self.current_lane]
                self.target_lane_x = target_center - self.largura // 2
        
        # Move lateralmente se estiver mudando de faixa
        if self.moving_lateral:
            dx = POLICE_LATERAL_SPEED * dt
            if abs(self.x - self.target_lane_x) < dx:
                self.x = self.target_lane_x
                self.moving_lateral = False
            else:
                # Move em direção ao alvo
                if self.x < self.target_lane_x:
                    self.x += dx
                else:
                    self.x -= dx
    
    def _detectar_faixa_atual(self):
        """Detecta em qual faixa o carro está baseado na posição X"""
        carro_center = self.x + self.largura // 2
        menor_distancia = float('inf')
        faixa_mais_proxima = 0
        
        for i, center in enumerate(self.lane_centers):
            distancia = abs(carro_center - center)
            if distancia < menor_distancia:
                menor_distancia = distancia
                faixa_mais_proxima = i
        
        return faixa_mais_proxima
    
    def _detectar_faixa_jogador(self):
        """Detecta em qual faixa o jogador está baseado na posição X"""
        if not hasattr(self, 'jogador_x'):
            return 1  # faixa central como padrão
        
        menor_distancia = float('inf')
        faixa_mais_proxima = 1
        
        for i, center in enumerate(self.lane_centers):
            distancia = abs(self.jogador_x - center)
            if distancia < menor_distancia:
                menor_distancia = distancia
                faixa_mais_proxima = i
        
        return faixa_mais_proxima
    
    def atualizar_posicao_jogador(self, jogador_x):
        """Atualiza a posição do jogador para comportamento inteligente"""
        self.jogador_x = jogador_x

    def fora_da_tela(self):
        return self.y > tela_altura

    @property
    def rect(self):
        return pygame.Rect(int(self.x), int(self.y), self.largura, self.altura)

    @property
    def hit_rect(self):
        r = self.rect.copy()
        r.inflate_ip(-r.w * HITBOX_SHRINK_W, -r.h * HITBOX_SHRINK_H)
        return r

class CarroJogador:
    def __init__(self, img, inner_x: int, inner_w: int, lane_w: int):
        self.inner_x = inner_x
        self.inner_w = inner_w

        # escala mantendo proporção pela ALTURA
        orig_w, orig_h = img.get_width(), img.get_height()
        scale = CARRO_ALTURA / orig_h
        w = int(orig_w * scale)
        h = CARRO_ALTURA

        # se ficar maior que a faixa - margens, reduz proporcionalmente
        max_w = max(10, lane_w - 2*LANE_MARGIN)
        if w > max_w:
            s = max_w / w
            w = int(w * s)
            h = int(h * s)

        self.largura = w
        self.altura  = h

        # posiciona no centro da faixa central
        self.x = inner_x + inner_w // 2 - self.largura // 2
        self.y = tela_altura - self.altura - 20
        self.vel = CARRO_VEL

        self.img  = pygame.transform.smoothscale(img, (self.largura, self.altura)).convert_alpha()
        self.mask = pygame.mask.from_surface(self.img, ALPHA_THRESHOLD)

    def mover(self, teclas, dt):
        if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
            self.x -= self.vel * dt
        if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
            self.x += self.vel * dt
        self.x = max(self.inner_x, min(self.inner_x + self.inner_w - self.largura, self.x))

    def desenhar(self, tela):
        tela.blit(self.img, (int(self.x), int(self.y)))
        if SHOW_HITBOX_DEBUG:
            pygame.draw.rect(tela, (0,255,0), self.hit_rect, 2)
            if COLLISION_MODE == "mask":
                msurf = self.mask.to_surface(setcolor=(0,255,0,80), unsetcolor=(0,0,0,0))
                msurf.set_colorkey((0,0,0))
                tela.blit(msurf, (int(self.x), int(self.y)))

    @property
    def rect(self):
        return pygame.Rect(int(self.x), int(self.y), self.largura, self.altura)

    @property
    def hit_rect(self):
        r = self.rect.copy()
        r.inflate_ip(-r.w * HITBOX_SHRINK_W, -r.h * HITBOX_SHRINK_H)
        return r

# -------------------- Telas --------------------
def desenhar_tela_abertura(tela, img_abertura):
    tela.blit(img_abertura, (0, 0))

def desenhar_tela_gameover(tela, pontuacao, img_gameover):
    tela.blit(img_gameover, (0, 0))
    fonte = pygame.font.SysFont('Arial', 40, True)
    score = fonte.render(f'Pontuação: {pontuacao}', True, (255,255,255))
    rect  = tela.get_rect()
    tela.blit(score, (rect.centerx - score.get_width()//2, 300))

# -------------------- Jogo --------------------
def main():
    pygame.init()
    pygame.mixer.init()
    tela = pygame.display.set_mode((tela_largura, tela_altura))
    pygame.display.set_caption('Velozes e Assados')
    clock = pygame.time.Clock()
    estado = MENU

    # Trilha do menu
    trilha_abertura = os.path.join("assets", "sounds", "abertura.mp3")
    if os.path.exists(trilha_abertura):
        pygame.mixer.music.load(trilha_abertura)
        pygame.mixer.music.play(-1)

    # Sprites
    img_carro_jogador = pygame.image.load(os.path.join("assets", "images", "carro_jogador.png")).convert_alpha()

    # Artes
    img_abertura = pygame.image.load(os.path.join("assets", "images", "abertura.png")).convert()
    img_abertura = pygame.transform.scale(img_abertura, (tela_largura, tela_altura))
    img_gameover = pygame.image.load(os.path.join("assets", "images", "gameover.png")).convert()
    img_gameover = pygame.transform.scale(img_gameover, (tela_largura, tela_altura))

    # Estrada
    img_road_orig = pygame.image.load(os.path.join("assets", "images", "road.png")).convert()
    road_width = min(img_road_orig.get_width(), int(tela_largura * 0.4))
    img_road = pygame.transform.smoothscale(img_road_orig, (road_width, img_road_orig.get_height()))
    H_tile = img_road.get_height()
    road_x = (tela_largura - road_width) // 2
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

    # Gerenciador de Playlist
    playlist_manager = PlaylistManager()
    
    # Debug: verifica se a playlist foi carregada
    print(f"🎵 Playlist inicializada com {len(playlist_manager.musicas)} músicas")
    if playlist_manager.musicas:
        print(f"🎵 Músicas disponíveis: {[os.path.basename(m) for m in playlist_manager.musicas]}")

    while True:
        agora = pygame.time.get_ticks() / 1000.0
        dt = agora - ultimo_t
        ultimo_t = agora
        dt = min(dt, 0.05)  # evita "teleporte" em quedas de FPS

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if estado == MENU and e.type == pygame.KEYDOWN and e.key == pygame.K_SPACE:
                estado = JOGANDO
                # Para música de abertura e inicia playlist
                pygame.mixer.music.stop()
                print("🎮 Iniciando jogo...")
                
                carro = CarroJogador(img_carro_jogador, inner_x, inner_w, lane_w)  # <<< adiciona lane_w
                obstaculos.clear()
                spawn_timer = 0.0
                spawn_interval = 0.7
                vel_obst = OBST_VEL_INICIAL
                pontuacao = 0
                dificuldade = 1
                road_y1, road_y2 = 0, -H_tile
                road_speed = 200.0
            if estado == GAME_OVER and e.type == pygame.KEYDOWN and e.key == pygame.K_r:
                estado = MENU
                # Para playlist e volta para música do menu
                playlist_manager.parar_com_fade()
                if os.path.exists(trilha_abertura):
                    pygame.mixer.music.load(trilha_abertura)
                    pygame.mixer.music.play(-1)
            
            # Controles da playlist durante o jogo
            if estado == JOGANDO and e.type == pygame.KEYDOWN:
                if e.key == pygame.K_n:  # Próxima música
                    playlist_manager.tocar_proxima()
                elif e.key == pygame.K_r:  # Música aleatória
                    playlist_manager.tocar_aleatoria()
                elif e.key == pygame.K_p:  # Pausar/Despausar
                    if pygame.mixer.music.get_busy():
                        playlist_manager.pausar()
                    else:
                        playlist_manager.despausar()
                elif e.key == pygame.K_m:  # Mudo/Desmudo
                    if playlist_manager.volume > 0:
                        playlist_manager.definir_volume(0.0)
                    else:
                        playlist_manager.definir_volume(PLAYLIST_VOLUME)

        if estado == MENU:
            # Toca música de abertura apenas se não estiver tocando
            if not pygame.mixer.music.get_busy() and os.path.exists(trilha_abertura):
                pygame.mixer.music.load(trilha_abertura)
                pygame.mixer.music.play(-1)
                print("🎵 Tocando música de abertura")
            desenhar_tela_abertura(tela, img_abertura)

        elif estado == JOGANDO:
            # Garante que a playlist esteja tocando
            if not playlist_manager.musica_atual:
                print("🚀 Iniciando playlist do jogo...")
                playlist_manager.tocar_aleatoria()
            
            # Verifica se a música atual terminou e toca a próxima
            if playlist_manager.musica_atual and not pygame.mixer.music.get_busy():
                print("🔄 Música terminou, tocando próxima...")
                playlist_manager.tocar_proxima()

            # LIMPAR A TELA DO FRAME ANTERIOR
            tela.fill((50, 150, 50))

            # Estrada infinita (duas cópias)
            road_y1 += road_speed * dt
            road_y2 += road_speed * dt
            if road_y1 >= tela_altura: road_y1 = road_y2 - H_tile
            if road_y2 >= tela_altura: road_y2 = road_y1 - H_tile
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
                obstaculos.append(Obstaculo(vel_obst, lane_centers, lane_w))  # <<< passa lane_w
                spawn_timer = 0.0
                spawn_interval = max(0.35, spawn_interval - 0.02)  # mais agressivo

            # Obstáculos + colisão
            hit = False
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

                if COLLISION_MODE == "mask":
                    if collide_mask(carro, obst):
                        hit = True
                        break
                else:  # "shrink"
                    if collide_shrink(carro.hit_rect, obst.hit_rect):
                        hit = True
                        break

            if hit:
                # Para playlist quando perde
                playlist_manager.parar_com_fade()
                estado = GAME_OVER

            # HUD
            fonte = pygame.font.SysFont('Arial', 28)
            tela.blit(fonte.render(f'Pontuação: {pontuacao}', True, (255,255,255)), (10, 10))
            
            # Mostra aviso de carro da polícia se houver algum
            for obst in obstaculos:
                if obst.nome_imagem == "police.png":
                    fonte_police = pygame.font.SysFont('Arial', 24, True)
                    aviso = fonte_police.render('🚨 CARRO DA POLÍCIA! 🚨', True, (255, 0, 0))
                    tela.blit(aviso, (tela_largura - aviso.get_width() - 10, 10))
                    break
            
            # Atualiza playlist
            playlist_manager.atualizar(dt)
            
            # Mostra informações da playlist no HUD
            if playlist_manager.musica_atual:
                nome_musica = os.path.basename(playlist_manager.musica_atual)
                # Remove extensão do arquivo
                nome_musica = os.path.splitext(nome_musica)[0]
                fonte_musica = pygame.font.SysFont('Arial', 16)
                texto_musica = fonte_musica.render(f'🎵 {nome_musica}', True, (200, 200, 200))
                tela.blit(texto_musica, (10, tela_altura - 30))
                
                # Controles da playlist
                controles = fonte_musica.render('N: Próxima | R: Aleatória | P: Pausar | M: Mudo', True, (150, 150, 150))
                tela.blit(controles, (10, tela_altura - 50))

        elif estado == GAME_OVER:
            desenhar_tela_gameover(tela, pontuacao, img_gameover)

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == '__main__':
    main()
