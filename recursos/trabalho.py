import pygame
import json
import os
from datetime import datetime

# Pasta raiz do projeto (IronManV2/IronManV2/)
_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def desenhar_texto_centralizado(tela, texto, fonte, cor, y):
    """Renderiza texto horizontalmente centralizado na tela."""
    superficie = fonte.render(texto, True, cor)
    x = (tela.get_width() - superficie.get_width()) // 2
    tela.blit(superficie, (x, y))


def desenhar_caixa_texto(tela, fonte, cor_texto, cor_fundo, cor_borda, rect, texto):
    """Desenha uma caixa de texto estilizada com fundo e borda."""
    pygame.draw.rect(tela, cor_fundo, rect, border_radius=10)
    pygame.draw.rect(tela, cor_borda, rect, 2, border_radius=10)
    superficie = fonte.render(texto, True, cor_texto)
    tx = rect.x + (rect.width - superficie.get_width()) // 2
    ty = rect.y + (rect.height - superficie.get_height()) // 2
    tela.blit(superficie, (tx, ty))


def desenhar_pausa(tela):
    """Sobrepõe a tela com um overlay semitransparente e exibe 'PAUSE' no centro."""
    largura = tela.get_width()
    altura = tela.get_height()
    overlay = pygame.Surface((largura, altura), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 150))
    tela.blit(overlay, (0, 0))

    fonte_pause = pygame.font.SysFont("comicsans", 80, bold=True)
    superficie = fonte_pause.render("PAUSE", True, (255, 255, 0))
    x = (largura - superficie.get_width()) // 2
    y = (altura - superficie.get_height()) // 2
    tela.blit(superficie, (x, y))

    fonte_sub = pygame.font.SysFont("comicsans", 24)
    sub = fonte_sub.render("Pressione Space para continuar", True, (255, 255, 255))
    x2 = (largura - sub.get_width()) // 2
    tela.blit(sub, (x2, y + superficie.get_height() + 15))


def obter_melhor_pontuador(caminho_banco=None):
    """Lê o banco de dados e retorna (nome, pontos, data) do maior pontuador."""
    if caminho_banco is None:
        caminho_banco = os.path.join(_ROOT, "base.atitus")
    try:
        with open(caminho_banco, "r") as f:
            dados = f.read()
        if dados:
            dadosDict = json.loads(dados)
        else:
            dadosDict = {}
    except Exception:
        dadosDict = {}

    nome_maior = None
    maior_pontos = -1
    data_jogada = None

    for nome, info in dadosDict.items():
        pontos = info[0]
        if pontos > maior_pontos:
            maior_pontos = pontos
            nome_maior = nome
            data_jogada = info[1] if len(info) > 1 else "-"

    return nome_maior, maior_pontos, data_jogada


def tela_boas_vindas(tela, relogio, nome_jogador, fundo_bv):
    """
    Exibe a tela de boas-vindas com:
      - Nome do jogador
      - Explicação da mecânica
      - Melhor pontuador + data/hora
      - Botão único para iniciar a partida
    Retorna quando o jogador clica em 'Iniciar'.
    """
    largura = tela.get_width()
    altura = tela.get_height()

    fonte_titulo = pygame.font.SysFont("comicsans", 48, bold=True)
    fonte_media = pygame.font.SysFont("comicsans", 26)
    fonte_pequena = pygame.font.SysFont("comicsans", 20)

    amarelo = (255, 215, 0)
    branco = (255, 255, 255)
    preto = (0, 0, 0)
    azul_escuro = (10, 10, 60)
    verde = (50, 200, 50)

    btn_largura, btn_altura = 260, 60
    btn_x = (largura - btn_largura) // 2
    btn_y = altura - 130
    btn_rect = pygame.Rect(btn_x, btn_y, btn_largura, btn_altura)

    nome_maior, maior_pontos, data_jogada = obter_melhor_pontuador()
    hora_atual = datetime.now().strftime("%d/%m/%Y  %H:%M:%S")

    btn_hover = False

    mecanica = [
        "Desvie dos mísseis usando as setas do teclado!",
        "Cada míssil desviado vale 1 ponto.",
        "A velocidade aumenta conforme você avança.",
        "Boa sorte, piloto!",
    ]

    while True:
        mouse_pos = pygame.mouse.get_pos()
        btn_hover = btn_rect.collidepoint(mouse_pos)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                pygame.quit()
                raise SystemExit
            if evento.type == pygame.MOUSEBUTTONUP and evento.button == 1:
                if btn_rect.collidepoint(evento.pos):
                    return  # sai da tela de boas-vindas → inicia o jogo

        # ---- Fundo ----
        if fundo_bv:
            tela.blit(pygame.transform.scale(fundo_bv, (largura, altura)), (0, 0))
        else:
            tela.fill(azul_escuro)

        # Overlay semitransparente para legibilidade
        overlay = pygame.Surface((largura, altura), pygame.SRCALPHA)
        overlay.fill((0, 0, 20, 190))
        tela.blit(overlay, (0, 0))

        # ---- Título ----
        desenhar_texto_centralizado(tela, "Bem-vindo ao Iron Man Game!", fonte_titulo, amarelo, 40)

        # ---- Nome do jogador ----
        desenhar_texto_centralizado(tela, f"Jogador: {nome_jogador}", fonte_media, branco, 115)

        # ---- Separador ----
        pygame.draw.line(tela, amarelo, (80, 160), (largura - 80, 160), 2)

        # ---- Como jogar ----
        desenhar_texto_centralizado(tela, "Como Jogar:", fonte_media, amarelo, 180)
        for i, linha in enumerate(mecanica):
            desenhar_texto_centralizado(tela, linha, fonte_pequena, branco, 220 + i * 32)

        # ---- Separador ----
        pygame.draw.line(tela, amarelo, (80, 370), (largura - 80, 370), 2)

        # ---- Melhor pontuador ----
        desenhar_texto_centralizado(tela, "Hall da Fama", fonte_media, amarelo, 390)
        if nome_maior:
            desenhar_texto_centralizado(
                tela,
                f"{nome_maior}   |   {maior_pontos} pontos   |   {data_jogada}",
                fonte_pequena,
                verde,
                435,
            )
        else:
            desenhar_texto_centralizado(tela, "Nenhum registro ainda. Seja o primeiro!", fonte_pequena, verde, 435)

        # ---- Data/hora atual ----
        desenhar_texto_centralizado(tela, f"Agora: {hora_atual}", fonte_pequena, (180, 180, 180), 475)

        # ---- Botão Iniciar ----
        cor_btn = (50, 200, 50) if btn_hover else (30, 150, 30)
        desenhar_caixa_texto(tela, fonte_media, branco, cor_btn, amarelo, btn_rect, "▶  Iniciar Partida")

        pygame.display.update()
        relogio.tick(60)
