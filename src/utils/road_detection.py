# -*- coding: utf-8 -*-
"""
Utilitários para detecção de asfalto e limites da estrada
"""

import pygame
import numpy as np


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

    r, g, b = arr[..., 0], arr[..., 1], arr[..., 2]
    mx = np.max(arr, axis=2)
    mn = np.min(arr, axis=2)
    diff = mx - mn

    S = np.where(mx == 0, 0, diff / (mx + 1e-6))
    V = mx

    y0, y1 = int(H * 0.30), int(H * 0.70)
    S_line = S[:, y0:y1].mean(axis=1)
    V_line = V[:, y0:y1].mean(axis=1)

    # thresholds (ajustáveis)
    asphalt_mask = (S_line < 0.40) & (V_line < 0.65)

    # fechamento simples
    k = 5
    pad = np.pad(asphalt_mask, (k // 2,), constant_values=False)
    for _ in range(2):
        dil = np.convolve(pad.astype(np.uint8), np.ones(k, dtype=np.uint8), mode='same') > 0
        ero = np.convolve(dil.astype(np.uint8), np.ones(k, dtype=np.uint8), mode='same') == k
        pad = ero
    asphalt_mask = pad[k // 2: -k // 2]

    # maior bloco contínuo
    best_len, best_l, cur_l = 0, 0, None
    for i, v in enumerate(asphalt_mask):
        if v and cur_l is None:
            cur_l = i
        elif (not v or i == len(asphalt_mask) - 1) and cur_l is not None:
            rgt = i if not v else i + 1
            if rgt - cur_l > best_len:
                best_len, best_l = rgt - cur_l, cur_l
            cur_l = None

    if best_len <= 0:
        l_small = int(W * 0.15)
        r_small = int(W * 0.85)
    else:
        l_small = best_l
        r_small = best_l + best_len

    if scale < 1.0:
        l_src = int(l_small / scale)
        r_src = int(r_small / scale)
    else:
        l_src, r_src = l_small, r_small

    inner_w_sprite = max(1, r_src - l_src)
    inner_x_screen = road_x + l_src
    return inner_x_screen, inner_w_sprite 