import pygame
import json
import os
import threading
from datetime import datetime

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def falar_texto(texto: str):
    def _falar():
        try:
            import pyttsx3
            engine = pyttsx3.init()
            engine.setProperty("rate", 160)
            engine.say(texto)
            engine.runAndWait()
        except Exception:
            pass

    t = threading.Thread(target=_falar, daemon=True)
    t.start()


def desenhar_texto_centralizado(tela, texto, fonte, cor, y):
    superficie = fonte.render(texto, True, cor)
    x = (tela.get_width() - superficie.get_width()) // 2
    tela.blit(superficie, (x, y))


def desenhar_caixa_texto(tela, fonte, cor_texto, cor_fundo, cor_borda, rect, texto):
    pygame.draw.rect(tela, cor_fundo, rect, border_radius=10)
    pygame.draw.rect(tela, cor_borda, rect, 2, border_radius=10)
    superficie = fonte.render(texto, True, cor_texto)
    tx = rect.x + (rect.width - superficie.get_width()) // 2
    ty = rect.y + (rect.height - superficie.get_height()) // 2
    tela.blit(superficie, (tx, ty))


def desenhar_pausa(tela):
    largura = tela.get_width()
    altura = tela.get_height()

    overlay = pygame.Surface((largura, altura), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 160))
    tela.blit(overlay, (0, 0))

    fonte_pause = pygame.font.SysFont("comicsans", 90, bold=True)
    superficie = fonte_pause.render("PAUSE", True, (255, 255, 0))
    x = (largura - superficie.get_width()) // 2
    y = (altura - superficie.get_height()) // 2
    tela.blit(superficie, (x, y))

    fonte_sub = pygame.font.SysFont("comicsans", 24)
    sub = fonte_sub.render("Pressione Space para continuar", True, (255, 255, 255))
    x2 = (largura - sub.get_width()) // 2
    tela.blit(sub, (x2, y + superficie.get_height() + 15))


def obter_melhor_pontuador(caminho_banco=None):
    if caminho_banco is None:
        caminho_banco = os.path.join(_ROOT, "base.atitus")
    try:
        with open(caminho_banco, "r") as f:
            dados = f.read()
        dadosDict = json.loads(dados) if dados else {}
    except Exception:
        dadosDict = {}

    nome_maior, maior_pontos, data_jogada = None, -1, None
    for nome, info in dadosDict.items():
        pontos = info[0]
        if pontos > maior_pontos:
            maior_pontos = pontos
            nome_maior = nome
            data_jogada = info[1] if len(info) > 1 else "-"

    return nome_maior, maior_pontos, data_jogada


def tela_boas_vindas(tela, relogio, nome_jogador, fundo_bv):
    largura = tela.get_width()
    altura = tela.get_height()

    fonte_titulo  = pygame.font.SysFont("comicsans", 46, bold=True)
    fonte_media   = pygame.font.SysFont("comicsans", 26)
    fonte_pequena = pygame.font.SysFont("comicsans", 20)

    amarelo  = (255, 215,   0)
    branco   = (255, 255, 255)
    verde    = ( 50, 210,  80)
    azul_esc = ( 10,  10,  50)

    btn_largura, btn_altura = 280, 62
    btn_x = (largura - btn_largura) // 2
    btn_y = altura - 120
    btn_rect = pygame.Rect(btn_x, btn_y, btn_largura, btn_altura)

    nome_maior, maior_pontos, data_jogada = obter_melhor_pontuador()
    hora_atual = datetime.now().strftime("%d/%m/%Y  %H:%M:%S")

    mecanica = [
        "Pilote sua nave e desvie dos asteroides!",
        "Use as setas CIMA / BAIXO para mover a nave.",
        "Cada asteroide desviado vale 1 ponto.",
        "A velocidade aumenta conforme você avança.",
        "Boa sorte, piloto!",
    ]

    falar_texto(f"Bem-vindo, {nome_jogador}! Prepare-se para defender o espaço!")

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
                    return

        if fundo_bv:
            tela.blit(pygame.transform.scale(fundo_bv, (largura, altura)), (0, 0))
        else:
            tela.fill(azul_esc)

        overlay = pygame.Surface((largura, altura), pygame.SRCALPHA)
        overlay.fill((0, 0, 20, 200))
        tela.blit(overlay, (0, 0))

        desenhar_texto_centralizado(tela, "🚀 Space Defender", fonte_titulo, amarelo, 38)
        desenhar_texto_centralizado(tela, f"Piloto: {nome_jogador}", fonte_media, branco, 112)

        pygame.draw.line(tela, amarelo, (80, 158), (largura - 80, 158), 2)

        desenhar_texto_centralizado(tela, "Como Jogar:", fonte_media, amarelo, 175)
        for i, linha in enumerate(mecanica):
            desenhar_texto_centralizado(tela, linha, fonte_pequena, branco, 215 + i * 32)

        pygame.draw.line(tela, amarelo, (80, 380), (largura - 80, 380), 2)

        desenhar_texto_centralizado(tela, "🏆 Hall da Fama", fonte_media, amarelo, 398)
        if nome_maior and maior_pontos >= 0:
            desenhar_texto_centralizado(
                tela,
                f"{nome_maior}   |   {maior_pontos} pontos   |   {data_jogada}",
                fonte_pequena, verde, 443,
            )
        else:
            desenhar_texto_centralizado(
                tela, "Nenhum registro ainda. Seja o primeiro!", fonte_pequena, verde, 443
            )

        desenhar_texto_centralizado(
            tela, f"Data da Partida: {hora_atual}", fonte_pequena, (180, 180, 180), 485
        )

        cor_btn = (50, 200, 70) if btn_hover else (30, 140, 50)
        desenhar_caixa_texto(
            tela, fonte_media, branco, cor_btn, amarelo, btn_rect, "▶  Iniciar Partida"
        )

        pygame.display.update()
        relogio.tick(60)
