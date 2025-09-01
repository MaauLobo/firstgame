# -*- coding: utf-8 -*-
"""
Interface do usuário e HUD do jogo
"""

import pygame
import os
from ..config import TELA_LARGURA, TELA_ALTURA, POWERUP_TIPOS, POWERUP_SPAWN_CHANCE


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


def desenhar_tela_powerup_help(tela):
    """Desenha a tela de ajuda dos power-ups"""
    # Fundo semi-transparente
    overlay = pygame.Surface((TELA_LARGURA, TELA_ALTURA), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))  # Fundo preto semi-transparente
    tela.blit(overlay, (0, 0))
    
    # Verifica se há espaço suficiente na tela
    altura_disponivel = TELA_ALTURA - 100  # Reserva espaço para título e instruções
    altura_necessaria = 150 + len(POWERUP_TIPOS) * 70 + 200  # Lista + dicas + estatísticas
    
    if altura_necessaria > altura_disponivel:
        # Se não há espaço suficiente, reduz ainda mais o espaçamento
        espacamento = 60
    else:
        espacamento = 70
    
    # Título
    fonte_titulo = pygame.font.SysFont('Arial', 48, True)
    titulo = fonte_titulo.render('🎁 POWER-UPS DISPONÍVEIS', True, (255, 255, 255))
    tela.blit(titulo, (TELA_LARGURA//2 - titulo.get_width()//2, 50))
    
    # Subtítulo
    fonte_subtitulo = pygame.font.SysFont('Arial', 24)
    subtitulo = fonte_subtitulo.render('Colete power-ups na estrada para obter vantagens especiais!', True, (200, 200, 200))
    tela.blit(subtitulo, (TELA_LARGURA//2 - subtitulo.get_width()//2, 100))
    
    # Lista de power-ups (espaçamento dinâmico baseado no tamanho da tela)
    y_inicial = 150
    
    for i, (tipo, config) in enumerate(POWERUP_TIPOS.items()):
        y_pos = y_inicial + i * espacamento
        
        # Ícone do power-up (círculo colorido com símbolo)
        raio = 25
        centro_x = 150
        centro_y = y_pos + 15
        
        # Círculo externo (borda branca)
        pygame.draw.circle(tela, (255, 255, 255), (centro_x, centro_y), raio + 2)
        # Círculo interno (cor do power-up)
        pygame.draw.circle(tela, config['cor'], (centro_x, centro_y), raio)
        # Círculo interno mais claro (brilho)
        cor_brilho = tuple(min(255, c + 50) for c in config['cor'])
        pygame.draw.circle(tela, cor_brilho, (centro_x, centro_y), raio - 5)
        
        # Adiciona símbolo específico para cada power-up
        cor_simbolo = (255, 255, 255)
        tamanho_simbolo = 10  # Reduzido de 12 para 10 para melhor proporção
        
        if tipo == 'shield':
            # Escudo - triângulo
            pontos = [
                (centro_x, centro_y - tamanho_simbolo),
                (centro_x - tamanho_simbolo, centro_y + tamanho_simbolo),
                (centro_x + tamanho_simbolo, centro_y + tamanho_simbolo)
            ]
            pygame.draw.polygon(tela, cor_simbolo, pontos)
        elif tipo == 'speed_boost':
            # Turbo - seta para cima
            pontos = [
                (centro_x, centro_y - tamanho_simbolo),
                (centro_x - tamanho_simbolo//2, centro_y),
                (centro_x + tamanho_simbolo//2, centro_y)
            ]
            pygame.draw.polygon(tela, cor_simbolo, pontos)
        elif tipo == 'slow_motion':
            # Câmera lenta - relógio
            pygame.draw.circle(tela, cor_simbolo, (centro_x, centro_y), tamanho_simbolo//2, 2)
            pygame.draw.line(tela, cor_simbolo, (centro_x, centro_y), (centro_x, centro_y - tamanho_simbolo//3), 2)
            pygame.draw.line(tela, cor_simbolo, (centro_x, centro_y), (centro_x + tamanho_simbolo//4, centro_y), 2)
        elif tipo == 'magnet':
            # Ímã - formato de U
            pygame.draw.rect(tela, cor_simbolo, (centro_x - tamanho_simbolo//2, centro_y - tamanho_simbolo//2, tamanho_simbolo, tamanho_simbolo//2))
            pygame.draw.rect(tela, cor_simbolo, (centro_x - tamanho_simbolo//3, centro_y, tamanho_simbolo*2//3, tamanho_simbolo//2))
        elif tipo == 'double_points':
            # Pontos duplos - dois círculos
            pygame.draw.circle(tela, cor_simbolo, (centro_x - tamanho_simbolo//3, centro_y), tamanho_simbolo//3)
            pygame.draw.circle(tela, cor_simbolo, (centro_x + tamanho_simbolo//3, centro_y), tamanho_simbolo//3)
        
        # Nome do power-up
        fonte_nome = pygame.font.SysFont('Arial', 20, True)
        nome = fonte_nome.render(config['nome'], True, config['cor'])
        tela.blit(nome, (200, y_pos))
        
        # Descrição
        fonte_desc = pygame.font.SysFont('Arial', 16)
        desc = fonte_desc.render(config['descricao'], True, (255, 255, 255))
        tela.blit(desc, (200, y_pos + 25))
        
        # Duração
        fonte_duracao = pygame.font.SysFont('Arial', 14)
        duracao = fonte_duracao.render(f'Duração: {config["duracao"]}s', True, (180, 180, 180))
        tela.blit(duracao, (200, y_pos + 45))
    
    # Estatísticas dos power-ups (ajustado para não cortar)
    fonte_stats = pygame.font.SysFont('Arial', 18, True)
    stats_titulo = fonte_stats.render('📊 ESTATÍSTICAS:', True, (0, 255, 255))
    tela.blit(stats_titulo, (TELA_LARGURA - 300, y_inicial + len(POWERUP_TIPOS) * espacamento + 20))
    
    fonte_stat = pygame.font.SysFont('Arial', 16)
    stats = [
        f"• Chance de spawn: {POWERUP_SPAWN_CHANCE * 100:.1f}%",
        f"• Intervalo de spawn: 2.0s",
        f"• Total de tipos: {len(POWERUP_TIPOS)}",
        f"• Duração média: {sum(config['duracao'] for config in POWERUP_TIPOS.values()) / len(POWERUP_TIPOS):.1f}s"
    ]
    
    for i, stat in enumerate(stats):
        stat_texto = fonte_stat.render(stat, True, (220, 220, 220))
        tela.blit(stat_texto, (TELA_LARGURA - 300, y_inicial + len(POWERUP_TIPOS) * espacamento + 45 + i * 22))
    
    # Dicas gerais (ajustado para não cortar)
    fonte_dicas = pygame.font.SysFont('Arial', 18, True)
    dicas_titulo = fonte_dicas.render('💡 DICAS:', True, (255, 255, 0))
    tela.blit(dicas_titulo, (TELA_LARGURA//2 - dicas_titulo.get_width()//2, y_inicial + len(POWERUP_TIPOS) * espacamento + 20))
    
    fonte_dica = pygame.font.SysFont('Arial', 16)
    dicas = [
        "• Múltiplos power-ups podem estar ativos simultaneamente",
        "• O Ímã atrai power-ups próximos automaticamente",
        "• O Escudo te protege de TODAS as colisões",
        "• Pontos Duplos multiplicam sua pontuação",
        "• Turbo e Câmera Lenta afetam a velocidade do jogo"
    ]
    
    for i, dica in enumerate(dicas):
        dica_texto = fonte_dica.render(dica, True, (220, 220, 220))
        tela.blit(dica_texto, (TELA_LARGURA//2 - dica_texto.get_width()//2, y_inicial + len(POWERUP_TIPOS) * espacamento + 45 + i * 22))
    
    # Instruções para voltar (ajustado para não cortar)
    fonte_instrucoes = pygame.font.SysFont('Arial', 20, True)
    instrucoes = fonte_instrucoes.render('Pressione H para voltar ao jogo', True, (255, 255, 255))
    tela.blit(instrucoes, (TELA_LARGURA//2 - instrucoes.get_width()//2, TELA_ALTURA - 40))
    
    # Controles adicionais
    fonte_controles = pygame.font.SysFont('Arial', 16)
    controles = fonte_controles.render('ESC: Pausar | H: Ajuda Power-ups | R: Reiniciar', True, (150, 150, 150))
    tela.blit(controles, (TELA_LARGURA//2 - controles.get_width()//2, TELA_ALTURA - 20))


def desenhar_tela_abertura(tela, img_abertura):
    """Desenha a tela de abertura"""
    tela.blit(img_abertura, (0, 0))
    
    # Adiciona instrução sobre power-ups (apenas tecla H, posicionada mais acima)
    fonte_instrucoes = pygame.font.SysFont('Arial', 20)
    instrucoes_ajuda = fonte_instrucoes.render('Pressione H para ver os power-ups', True, (200, 200, 200))
    
    # Posiciona a instrução mais acima na tela
    tela.blit(instrucoes_ajuda, (TELA_LARGURA//2 - instrucoes_ajuda.get_width()//2, TELA_ALTURA - 120))


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


def desenhar_powerups_ativos(tela, powerup_manager):
    """Desenha os power-ups ativos no canto superior direito"""
    if not powerup_manager.powerups_ativos:
        return
    
    # Posição inicial no canto superior direito
    x_inicial = TELA_LARGURA - 200
    y_inicial = 10
    espacamento = 25
    
    fonte_nome = pygame.font.SysFont('Arial', 16, True)
    fonte_tempo = pygame.font.SysFont('Arial', 14)
    
    for i, (tipo, dados) in enumerate(powerup_manager.powerups_ativos.items()):
        config = POWERUP_TIPOS[tipo]
        tempo_restante = dados['tempo_restante']
        
        y_pos = y_inicial + i * espacamento
        
        # Nome do power-up com cor específica
        nome_texto = fonte_nome.render(config['nome'], True, config['cor'])
        tela.blit(nome_texto, (x_inicial, y_pos))
        
        # Tempo restante
        tempo_texto = fonte_tempo.render(f'{tempo_restante:.1f}s', True, (200, 200, 200))
        tela.blit(tempo_texto, (x_inicial + nome_texto.get_width() + 10, y_pos))


def desenhar_hud_jogo(tela, pontuacao, obstaculos, playlist_manager, record_manager, powerup_manager=None, game_state=None):
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
    
    # Power-ups ativos
    if powerup_manager:
        desenhar_powerups_ativos(tela, powerup_manager)
    
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
        
        # Comando para ajuda dos power-ups (movido para a direita)
        fonte_ajuda = pygame.font.SysFont('Arial', 14)
        ajuda_controle = fonte_ajuda.render('H: Ajuda Power-ups', True, (100, 100, 100))
        tela.blit(ajuda_controle, (TELA_LARGURA - ajuda_controle.get_width() - 10, TELA_ALTURA - 110)) 