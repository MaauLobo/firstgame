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

# Carros (tamanho renderizado)
CARRO_LARGURA = 50
CARRO_ALTURA  = 90
CARRO_VEL     = 380  # px/s

# Obstáculos
OBST_LARGURA      = 50
OBST_ALTURA       = 90
OBST_VEL_INICIAL  = 280  # px/s

LANE_COUNT = 3

# Colisão
COLLISION_MODE      = "mask"   # "shrink" ou "mask"
HITBOX_SHRINK_W     = 0.15     # 15% na largura (modo shrink)
HITBOX_SHRINK_H     = 0.18     # 18% na altura  (modo shrink)
ALPHA_THRESHOLD     = 50       # opacidade mínima p/ máscara
SHOW_HITBOX_DEBUG   = False

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
                img = pygame.transform.smoothscale(img, (OBST_LARGURA, OBST_ALTURA)).convert_alpha()
                cls.inimigos_imgs.append(img)

    def __init__(self, vel_px_s: float, lane_centers: list[int]):
        if not Obstaculo.inimigos_imgs:
            Obstaculo.carregar_imgs()

        self.largura = OBST_LARGURA
        self.altura  = OBST_ALTURA
        self.vel     = vel_px_s
        self.img     = random.choice(Obstaculo.inimigos_imgs)
        self.mask    = pygame.mask.from_surface(self.img, ALPHA_THRESHOLD)

        center = random.choice(lane_centers)
        self.x = center - self.largura // 2
        self.y = -self.altura

    def mover(self, dt):
        self.y += self.vel * dt

    def desenhar(self, tela):
        tela.blit(self.img, (int(self.x), int(self.y)))
        if SHOW_HITBOX_DEBUG:
            pygame.draw.rect(tela, (255,0,0), self.hit_rect, 2)
            if COLLISION_MODE == "mask":
                msurf = self.mask.to_surface(setcolor=(255,0,0,80), unsetcolor=(0,0,0,0))
                msurf.set_colorkey((0,0,0))
                tela.blit(msurf, (int(self.x), int(self.y)))

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
    def __init__(self, img, inner_x: int, inner_w: int):
        self.inner_x = inner_x
        self.inner_w = inner_w
        self.x = inner_x + inner_w // 2 - CARRO_LARGURA // 2
        self.y = tela_altura - CARRO_ALTURA - 20
        self.largura = CARRO_LARGURA
        self.altura  = CARRO_ALTURA
        self.vel     = CARRO_VEL
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
    road_accel = 2.0

    # Detecta asfalto e define faixas
    inner_x, inner_w = detect_asphalt_bounds(img_road, road_x)
    lane_w = inner_w // LANE_COUNT
    lane_centers = [inner_x + lane_w//2 + i*lane_w for i in range(LANE_COUNT)]

    carro = CarroJogador(img_carro_jogador, inner_x, inner_w)

    obstaculos = []
    spawn_timer = 0.0
    spawn_interval = 0.7
    vel_obst = OBST_VEL_INICIAL
    pontuacao = 0
    dificuldade = 1

    ultimo_t = pygame.time.get_ticks() / 1000.0

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
                carro = CarroJogador(img_carro_jogador, inner_x, inner_w)
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
                if os.path.exists(trilha_abertura):
                    pygame.mixer.music.load(trilha_abertura)
                    pygame.mixer.music.play(-1)

        if estado == MENU:
            if not pygame.mixer.music.get_busy() and os.path.exists(trilha_abertura):
                pygame.mixer.music.load(trilha_abertura); pygame.mixer.music.play(-1)
            desenhar_tela_abertura(tela, img_abertura)

        elif estado == JOGANDO:
            # para trilha do menu
            if pygame.mixer.music.get_busy():
                pygame.mixer.music.stop()

            # LIMPAR A TELA DO FRAME ANTERIOR
            tela.fill((50, 150, 50))  # ou (0,0,0) se preferir

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
                obstaculos.append(Obstaculo(vel_obst, lane_centers))
                spawn_timer = 0.0
                spawn_interval = max(0.35, spawn_interval - 0.01)

            # Obstáculos + colisão
            hit = False
            for obst in obstaculos[:]:
                obst.mover(dt)
                obst.desenhar(tela)

                if obst.fora_da_tela():
                    obstaculos.remove(obst)
                    pontuacao += 1
                    if pontuacao % 10 == 0:
                        dificuldade += 1
                        vel_obst += 20
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
                estado = GAME_OVER

            # HUD
            fonte = pygame.font.SysFont('Arial', 28)
            tela.blit(fonte.render(f'Pontuação: {pontuacao}', True, (255,255,255)), (10, 10))

        elif estado == GAME_OVER:
            desenhar_tela_gameover(tela, pontuacao, img_gameover)

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == '__main__':
    main()
