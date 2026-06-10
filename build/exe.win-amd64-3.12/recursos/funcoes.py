import os, time
import json
from datetime import datetime

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def _caminho(arquivo):
    return os.path.join(_ROOT, arquivo)

def limpar_tela():
    os.system("cls")

def aguarde(segundos):
    time.sleep(segundos)

def inicializarBancoDeDados():
    caminho = _caminho("base.atitus")
    if not os.path.exists(caminho):
        print("Banco de Dados Inexistente. Criando...")
        open(caminho, "w").close()

def escreverDados(nome, pontos):
    caminho = _caminho("base.atitus")
    try:
        with open(caminho, "r") as banco:
            dados = banco.read()
    except Exception:
        dados = ""

    dadosDict = json.loads(dados) if dados else {}

    data_br = datetime.now().strftime("%d/%m/%Y")
    hora_br = datetime.now().strftime("%H:%M:%S")

    if nome not in dadosDict or pontos > dadosDict[nome][0]:
        dadosDict[nome] = [pontos, data_br, hora_br]

    with open(caminho, "w") as banco:
        banco.write(json.dumps(dadosDict))

    with open(_caminho("log.dat"), "a") as log:
        log.write(f"{nome},{pontos},{data_br},{hora_br}\n")

def maior_pontuador():
    caminho = _caminho("base.atitus")
    try:
        with open(caminho, "r") as banco:
            dados = banco.read()
    except Exception:
        dados = ""

    dadosDict = json.loads(dados) if dados else {}

    nome_maior   = None
    dataJogada   = None
    maior_pontos = -1

    for nome, info in dadosDict.items():
        pontos = info[0]
        if pontos > maior_pontos:
            maior_pontos = pontos
            nome_maior   = nome
            dataJogada   = info[1] if len(info) > 1 else "-"

    return nome_maior, maior_pontos, dataJogada
