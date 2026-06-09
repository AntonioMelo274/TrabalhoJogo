import pygame
import random
import os
import sys
from recursos.funcoes import inicializarBancoDeDados, limpar_tela, escreverDados, maior_pontuador
from recursos.trabalho import desenhar_pausa, tela_boas_vindas, desenhar_texto_centralizado

# Garante que caminhos relativos partem sempre da pasta do main.py
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(BASE_DIR)

limpar_tela()
inicializarBancoDeDados()
nome_maior, maior_pontos, dataJogada = maior_pontuador()
pygame.init()

# ── Ponto 8: Tela 1000 x 700 ─────────────────────────────────────────────────
LARGURA, ALTURA = 1000, 700

while True:
    nome = input("Nickname: ")
    if len(nome) > 0:
        break
    else:
        print("Nome Inválido!")

pygame.display.set_caption("Iron Man - Pensamento Computacional")
icone = pygame.image.load("assets/icone.png")
pygame.display.set_icon(icone)
relogio = pygame.time.Clock()
tela = pygame.display.set_mode((LARGURA, ALTURA))

# Cores
branco     = (255, 255, 255)
preto      = (0,   0,   0)
amarelo    = (255, 215, 0)
cinza_semi = (50,  50,  50, 180)

# ── Assets ────────────────────────────────────────────────────────────────────
fundo      = pygame.image.load("assets/background.jpg")
fundoDead  = pygame.image.load("assets/backgroundDead.jpg")
fundoStart = pygame.image.load("assets/backgroundStart.jpg")

# Escala o fundo para preencher a tela
fundo      = pygame.transform.scale(fundo,      (LARGURA, ALTURA))
fundoDead  = pygame.transform.scale(fundoDead,  (LARGURA, ALTURA))
fundoStart = pygame.transform.scale(fundoStart, (LARGURA, ALTURA))

iron   = pygame.image.load("assets/IronMan.png")
iron   = pygame.transform.scale(iron,   (116, 51))
missel = pygame.image.load("assets/missile.png")
missel = pygame.transform.scale(missel, (125, 25))

missileSound  = pygame.mixer.Sound("assets/missile.wav")
explosaoSound = pygame.mixer.Sound("assets/explosao.wav")
pygame.mixer.music.load("assets/ironsound.mp3")

fonteMenu     = pygame.font.SysFont("comicsans", 20)
fonteGrande   = pygame.font.SysFont("comicsans", 36, bold=True)
fontePequena  = pygame.font.SysFont("comicsans", 16)

# ── Ponto 9: Tela de boas-vindas ──────────────────────────────────────────────
tela_boas_vindas(tela, relogio, nome, fundoStart)


# ─────────────────────────────────────────────────────────────────────────────
def jogar():
    # Variáveis de fundo rolante
    fundoMov1 = 0
    fundoMov2 = LARGURA

    # Personagem – movimento SOMENTE no eixo Y (Ponto 13)
    posicaoXPersona      = 50
    posicaoYPersona      = ALTURA // 2
    movimentoYPersona    = 0
    velocidadeMovPersona = 6

    # Míssel
    posicaoXMissel   = LARGURA
    posicaoYMissel   = random.randint(0, ALTURA - 60)
    velocidadeMissel = 4

    pontos      = 0
    dificuldade = 20

    # ── Ponto 11: controle de pausa ──────────────────────────────────────────
    pausado = False

    # ── Objeto decorativo (Ponto 14): nuvens randômicas ──────────────────────
    nuvens = [
        {"x": random.randint(0, LARGURA), "y": random.randint(20, ALTURA - 80),
         "vel": random.uniform(0.5, 2.0), "raio": random.randint(18, 40)}
        for _ in range(6)
    ]

    # ── Sol pulsante (Ponto 16) ───────────────────────────────────────────────
    sol_raio_base = 45
    sol_raio      = sol_raio_base
    sol_pulsando  = 1          # +1 crescendo, -1 diminuindo
    SOL_MIN, SOL_MAX = 35, 60

    pygame.mixer.Sound.play(missileSound)
    pygame.mixer.music.play(-1)

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                quit()

            # Ponto 20: ESC fecha o jogo
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                quit()

            # Ponto 11: Space pausa/despausa
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_SPACE:
                pausado = not pausado

            # Movimento SÓ em Y
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_UP:
                movimentoYPersona = -velocidadeMovPersona
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_DOWN:
                movimentoYPersona = velocidadeMovPersona
            elif evento.type == pygame.KEYUP and (
                    evento.key == pygame.K_UP or evento.key == pygame.K_DOWN):
                movimentoYPersona = 0

        # ── Lógica só roda quando não pausado ────────────────────────────────
        if not pausado:
            # Mover personagem (eixo Y apenas)
            posicaoYPersona += movimentoYPersona
            posicaoYPersona  = max(0, min(posicaoYPersona, ALTURA - 51))

            # Mover míssel
            posicaoXMissel -= velocidadeMissel
            if posicaoXMissel < -125:
                pygame.mixer.Sound.play(missileSound)
                posicaoXMissel   = LARGURA
                posicaoYMissel   = random.randint(0, ALTURA - 60)
                pontos          += 1
                velocidadeMissel += 0.5

            # Fundo rolante
            fundoMov1 -= 2
            fundoMov2 -= 2
            if fundoMov1 <= -LARGURA:
                fundoMov1 = LARGURA
            if fundoMov2 <= -LARGURA:
                fundoMov2 = LARGURA

            # Sol pulsante
            sol_raio += sol_pulsando * 0.15
            if sol_raio >= SOL_MAX:
                sol_pulsando = -1
            elif sol_raio <= SOL_MIN:
                sol_pulsando = 1

            # Nuvens decorativas
            for nuvem in nuvens:
                nuvem["x"] -= nuvem["vel"]
                if nuvem["x"] < -60:
                    nuvem["x"]   = LARGURA + 30
                    nuvem["y"]   = random.randint(20, ALTURA - 80)
                    nuvem["vel"] = random.uniform(0.5, 2.0)

        # ── Desenho ───────────────────────────────────────────────────────────
        tela.fill(branco)
        tela.blit(fundo, (fundoMov1, 0))
        tela.blit(fundo, (fundoMov2, 0))

        # Sol pulsante no canto superior direito (Ponto 16)
        pygame.draw.circle(tela, (255, 230, 0),
                           (LARGURA - 70, 70), int(sol_raio))
        pygame.draw.circle(tela, (255, 200, 0),
                           (LARGURA - 70, 70), int(sol_raio * 0.65))

        # Nuvens decorativas – círculos brancos suaves (Ponto 14)
        for nuvem in nuvens:
            cor_nuvem = (220, 220, 255, 160)
            surf_n = pygame.Surface((nuvem["raio"] * 4, nuvem["raio"] * 2), pygame.SRCALPHA)
            pygame.draw.ellipse(surf_n, (210, 210, 240, 120),
                                (0, 0, nuvem["raio"] * 4, nuvem["raio"] * 2))
            tela.blit(surf_n, (nuvem["x"] - nuvem["raio"] * 2,
                                nuvem["y"] - nuvem["raio"]))

        # Personagem e míssel
        tela.blit(iron,   (posicaoXPersona, posicaoYPersona))
        tela.blit(missel, (posicaoXMissel,  posicaoYMissel))

        # HUD – pontuação
        texto_pontos = fonteGrande.render(f"Pontos: {int(pontos)}", True, amarelo)
        tela.blit(texto_pontos, (10, 10))

        # Ponto 12: mensagem de pausa discreta
        hint = fontePequena.render("Press Space to Pause Game", True, (200, 200, 200))
        tela.blit(hint, (LARGURA - hint.get_width() - 10, ALTURA - 28))

        # Ponto 11: overlay de pausa
        if pausado:
            desenhar_pausa(tela)

        # Colisão
        pixelsPersonaX = list(range(posicaoXPersona, posicaoXPersona + 116))
        pixelsPersonaY = list(range(posicaoYPersona, posicaoYPersona + 51))
        pixelsMisselX  = list(range(int(posicaoXMissel), int(posicaoXMissel) + 125))
        pixelsMisselY  = list(range(posicaoYMissel, posicaoYMissel + 25))

        if not pausado:
            if len(set(pixelsMisselY) & set(pixelsPersonaY)) > dificuldade:
                if len(set(pixelsMisselX) & set(pixelsPersonaX)) > dificuldade:
                    escreverDados(nome, int(pontos))
                    dead()

        pygame.display.update()
        relogio.tick(60)


# ─────────────────────────────────────────────────────────────────────────────
def dead():
    pygame.mixer.music.stop()
    pygame.mixer.Sound.play(explosaoSound)

    nome_m, pts_m, data_m = maior_pontuador()

    btn_larg, btn_alt = 200, 50
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                quit()
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                quit()
            elif evento.type == pygame.MOUSEBUTTONUP:
                if startButton.collidepoint(evento.pos):
                    jogar()
                if quitButton.collidepoint(evento.pos):
                    quit()

        tela.fill(branco)
        tela.blit(fundoDead, (0, 0))

        # Título
        desenhar_texto_centralizado(tela, "GAME OVER", fonteGrande, (220, 50, 50), 60)

        # Ponto 18: Melhor pontuador na tela de morte
        if nome_m:
            desenhar_texto_centralizado(
                tela,
                f"🏆  Melhor: {nome_m}  |  {pts_m} pts  |  {data_m}",
                fonteMenu, amarelo, 130
            )
        else:
            desenhar_texto_centralizado(tela, "Sem registros ainda.", fonteMenu, amarelo, 130)

        # Botões
        startButton = pygame.draw.rect(tela, branco,
                                       (LARGURA // 2 - 220, 210, btn_larg, btn_alt),
                                       border_radius=12)
        tela.blit(fonteMenu.render("Jogar Novamente", True, preto),
                  (LARGURA // 2 - 210, 223))

        quitButton = pygame.draw.rect(tela, branco,
                                      (LARGURA // 2 + 20, 210, btn_larg, btn_alt),
                                      border_radius=12)
        tela.blit(fonteMenu.render("Sair do Jogo", True, preto),
                  (LARGURA // 2 + 35, 223))

        pygame.display.update()
        relogio.tick(60)


# ─────────────────────────────────────────────────────────────────────────────
def start():
    btn_larg, btn_alt = 200, 50
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                quit()
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                quit()
            elif evento.type == pygame.MOUSEBUTTONUP:
                if startButton.collidepoint(evento.pos):
                    jogar()
                if quitButton.collidepoint(evento.pos):
                    quit()

        tela.fill(branco)
        tela.blit(fundoStart, (0, 0))

        startButton = pygame.draw.rect(tela, branco,
                                       (10, 10, btn_larg, btn_alt), border_radius=12)
        tela.blit(fonteMenu.render("Iniciar Game", True, preto), (30, 22))

        quitButton = pygame.draw.rect(tela, branco,
                                      (10, 70, btn_larg, btn_alt), border_radius=12)
        tela.blit(fonteMenu.render("Sair do Game", True, preto), (30, 82))

        texto_best = fonteMenu.render(
            f"The Best - {nome_maior} - {maior_pontos} - {dataJogada}", True, branco
        )
        tela.blit(texto_best, (LARGURA - texto_best.get_width() - 10, 10))

        pygame.display.update()
        relogio.tick(60)


start()
