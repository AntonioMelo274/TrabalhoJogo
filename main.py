import pygame
import random
import os
import sys
from recursos.funcoes import inicializarBancoDeDados, limpar_tela, escreverDados, maior_pontuador
from recursos.trabalho import (
    desenhar_pausa,
    tela_boas_vindas,
    desenhar_texto_centralizado,
    falar_texto,
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(BASE_DIR)

limpar_tela()
inicializarBancoDeDados()
nome_maior, maior_pontos, dataJogada = maior_pontuador()
pygame.init()

LARGURA, ALTURA = 1000, 700

while True:
    nome = input("Nickname do Piloto: ")
    if len(nome) > 0:
        break
    else:
        print("Nome inválido! Tente novamente.")

pygame.display.set_caption("Space Defender - Pensamento Computacional")
icone = pygame.image.load("bases/icone.png")
pygame.display.set_icon(icone)
relogio = pygame.time.Clock()
tela = pygame.display.set_mode((LARGURA, ALTURA))

branco   = (255, 255, 255)
preto    = (  0,   0,   0)
amarelo  = (255, 215,   0)
vermelho = (220,  50,  50)

fundo      = pygame.image.load("bases/background.jpg")
fundoDead  = pygame.image.load("bases/backgroundDead.jpg")
fundoStart = pygame.image.load("bases/backgroundStart.jpg")

fundo      = pygame.transform.scale(fundo,      (LARGURA, ALTURA))
fundoDead  = pygame.transform.scale(fundoDead,  (LARGURA, ALTURA))
fundoStart = pygame.transform.scale(fundoStart, (LARGURA, ALTURA))

nave      = pygame.image.load("bases/IronMan.png")
nave      = pygame.transform.scale(nave, (116, 51))
asteroide = pygame.image.load("bases/missile.png")
asteroide = pygame.transform.scale(asteroide, (125, 25))

missileSound  = pygame.mixer.Sound("bases/missile.wav")
explosaoSound = pygame.mixer.Sound("bases/explosao.wav")
pygame.mixer.music.load("bases/ironsound.mp3")

fonteMenu    = pygame.font.SysFont("comicsans", 20)
fonteGrande  = pygame.font.SysFont("comicsans", 36, bold=True)
fontePequena = pygame.font.SysFont("comicsans", 16)

tela_boas_vindas(tela, relogio, nome, fundoStart)


def jogar():
    fundoMov1 = 0
    fundoMov2 = LARGURA

    posicaoXNave   = 50
    posicaoYNave   = ALTURA // 2
    movimentoYNave = 0
    velocidadeNave = 6

    posicaoXAst   = LARGURA
    posicaoYAst   = random.randint(0, ALTURA - 60)
    velocidadeAst = 4

    pontos      = 0
    dificuldade = 20
    pausado     = False

    estrelas = [
        {
            "x": random.randint(0, LARGURA),
            "y": random.randint(10, ALTURA - 10),
            "vel": random.uniform(0.3, 1.5),
            "raio": random.randint(2, 5),
            "brilho": random.randint(150, 255),
            "delta_brilho": random.choice([-2, 2]),
        }
        for _ in range(25)
    ]

    sol_raio     = 45
    sol_pulsando = 1
    SOL_MIN, SOL_MAX = 35, 60

    pygame.mixer.Sound.play(missileSound)
    pygame.mixer.music.play(-1)

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_SPACE:
                pausado = not pausado
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_UP:
                movimentoYNave = -velocidadeNave
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_DOWN:
                movimentoYNave = velocidadeNave
            elif evento.type == pygame.KEYUP and evento.key in (pygame.K_UP, pygame.K_DOWN):
                movimentoYNave = 0

        if not pausado:
            posicaoYNave += movimentoYNave
            posicaoYNave  = max(0, min(posicaoYNave, ALTURA - 51))

            posicaoXAst -= velocidadeAst
            if posicaoXAst < -125:
                pygame.mixer.Sound.play(missileSound)
                posicaoXAst   = LARGURA
                posicaoYAst   = random.randint(0, ALTURA - 60)
                pontos       += 1
                velocidadeAst += 0.5

            fundoMov1 -= 2
            fundoMov2 -= 2
            if fundoMov1 <= -LARGURA:
                fundoMov1 = LARGURA
            if fundoMov2 <= -LARGURA:
                fundoMov2 = LARGURA

            sol_raio += sol_pulsando * 0.15
            if sol_raio >= SOL_MAX:
                sol_pulsando = -1
            elif sol_raio <= SOL_MIN:
                sol_pulsando = 1

            for e in estrelas:
                e["x"] -= e["vel"]
                if e["x"] < -10:
                    e["x"]   = LARGURA + 5
                    e["y"]   = random.randint(10, ALTURA - 10)
                    e["vel"] = random.uniform(0.3, 1.5)
                e["brilho"] += e["delta_brilho"]
                if e["brilho"] >= 255 or e["brilho"] <= 80:
                    e["delta_brilho"] = -e["delta_brilho"]

        tela.fill(preto)
        tela.blit(fundo, (fundoMov1, 0))
        tela.blit(fundo, (fundoMov2, 0))

        pygame.draw.circle(tela, (255, 230, 0), (LARGURA - 70, 70), int(sol_raio))
        pygame.draw.circle(tela, (255, 200, 0), (LARGURA - 70, 70), int(sol_raio * 0.65))

        for e in estrelas:
            b = max(0, min(255, int(e["brilho"])))
            pygame.draw.circle(tela, (b, b, b), (int(e["x"]), int(e["y"])), e["raio"])

        tela.blit(nave,      (posicaoXNave, posicaoYNave))
        tela.blit(asteroide, (posicaoXAst,  posicaoYAst))

        texto_pontos = fonteGrande.render(f"Pontos: {int(pontos)}", True, amarelo)
        tela.blit(texto_pontos, (10, 10))

        hint = fontePequena.render("Press Space to Pause Game", True, (180, 180, 180))
        tela.blit(hint, (LARGURA - hint.get_width() - 10, ALTURA - 28))

        if pausado:
            desenhar_pausa(tela)

        pixelsNaveX = set(range(posicaoXNave, posicaoXNave + 116))
        pixelsNaveY = set(range(posicaoYNave, posicaoYNave + 51))
        pixelsAstX  = set(range(int(posicaoXAst), int(posicaoXAst) + 125))
        pixelsAstY  = set(range(posicaoYAst, posicaoYAst + 25))

        if not pausado:
            if len(pixelsAstY & pixelsNaveY) > dificuldade:
                if len(pixelsAstX & pixelsNaveX) > dificuldade:
                    escreverDados(nome, int(pontos))
                    dead()

        pygame.display.update()
        relogio.tick(60)


def dead():
    pygame.mixer.music.stop()
    pygame.mixer.Sound.play(explosaoSound)

    nome_m, pts_m, data_m = maior_pontuador()
    falar_texto("Game Over! Missão fracassada, piloto.")

    btn_larg, btn_alt = 210, 52

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.MOUSEBUTTONUP:
                if startButton.collidepoint(evento.pos):
                    jogar()
                if quitButton.collidepoint(evento.pos):
                    pygame.quit()
                    sys.exit()

        tela.fill(preto)
        tela.blit(fundoDead, (0, 0))

        ov = pygame.Surface((LARGURA, ALTURA), pygame.SRCALPHA)
        ov.fill((0, 0, 0, 120))
        tela.blit(ov, (0, 0))

        desenhar_texto_centralizado(tela, "GAME OVER", fonteGrande, vermelho, 60)

        if nome_m and pts_m >= 0:
            desenhar_texto_centralizado(
                tela,
                f"🏆  Melhor Piloto: {nome_m}  |  {pts_m} pts  |  {data_m}",
                fonteMenu, amarelo, 130,
            )
        else:
            desenhar_texto_centralizado(
                tela, "Nenhum registro encontrado.", fonteMenu, amarelo, 130
            )

        startButton = pygame.draw.rect(
            tela, branco,
            pygame.Rect(LARGURA // 2 - 230, 210, btn_larg, btn_alt),
            border_radius=12,
        )
        tela.blit(
            fonteMenu.render("Jogar Novamente", True, preto),
            (LARGURA // 2 - 218, 224),
        )

        quitButton = pygame.draw.rect(
            tela, branco,
            pygame.Rect(LARGURA // 2 + 20, 210, btn_larg, btn_alt),
            border_radius=12,
        )
        tela.blit(
            fonteMenu.render("Sair do Jogo", True, preto),
            (LARGURA // 2 + 40, 224),
        )

        pygame.display.update()
        relogio.tick(60)


def start():
    btn_larg, btn_alt = 200, 50
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.MOUSEBUTTONUP:
                if startButton.collidepoint(evento.pos):
                    jogar()
                if quitButton.collidepoint(evento.pos):
                    pygame.quit()
                    sys.exit()

        tela.fill(preto)
        tela.blit(fundoStart, (0, 0))

        startButton = pygame.draw.rect(
            tela, branco, (10, 10, btn_larg, btn_alt), border_radius=12
        )
        tela.blit(fonteMenu.render("Iniciar Game", True, preto), (30, 22))

        quitButton = pygame.draw.rect(
            tela, branco, (10, 70, btn_larg, btn_alt), border_radius=12
        )
        tela.blit(fonteMenu.render("Sair do Game", True, preto), (30, 82))

        texto_best = fonteMenu.render(
            f"The Best - {nome_maior} - {maior_pontos} - {dataJogada}",
            True, branco,
        )
        tela.blit(texto_best, (LARGURA - texto_best.get_width() - 10, 10))

        pygame.display.update()
        relogio.tick(60)


start()
