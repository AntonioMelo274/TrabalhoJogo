# 🚀 Space Defender

## Desenvolvedores

| Nome Completo | RA (Registro Acadêmico) |
|---------------|------------------------|
| *(Seu nome completo aqui)* | *(Seu RA aqui)* |
| *(Nome do colega — se dupla)* | *(RA do colega)* |

---

## 📖 História do Jogo

Em um futuro distante, a galáxia está sendo invadida por um enxame de asteroides mortais.
Você é o último piloto de defesa da humanidade — sua missão é manter sua nave espacial em
rota e desviar de todos os obstáculos pelo maior tempo possível.
Quanto mais você aguentar, maior será sua pontuação no Hall da Fama.
O universo conta com você, piloto!

---

## 🎮 Como Jogar

- **Setas ↑ / ↓** — mover a nave para cima ou para baixo
- **Espaço** — pausar / retomar o jogo
- **ESC** — fechar o jogo
- Cada asteroide desviado vale **1 ponto**
- A dificuldade aumenta progressivamente

---

## 🛠️ Tecnologias Utilizadas

| Tecnologia | Versão / Descrição |
|---|---|
| Python | 3.12 |
| Pygame | Renderização gráfica, sons e controle de eventos |
| pyttsx3 | Text-to-Speech (voz de boas-vindas e game over) |
| cx_Freeze | Geração do executável `.exe` |
| JSON | Persistência de pontuações (`base.atitus`) |

---

## 📁 Estrutura do Projeto

```
IronManV2/
├── bases/          ← Todos os assets (imagens, sons, ícones)
├── recursos/
│   ├── funcoes.py  ← Funções de banco de dados e log
│   └── trabalho.py ← Funções auxiliares (TTS, telas, desenhos)
├── main.py         ← Arquivo principal do jogo
├── setup.py        ← Configuração do executável
├── base.atitus     ← Banco de dados de pontuações (JSON)
├── log.dat         ← Log de partidas
└── readme.md       ← Este arquivo
```

---

## ▶️ Como Executar

```bash
python main.py
```

## 📦 Gerar Executável

```bash
python setup.py build
```

O executável será gerado na pasta `build/`.
