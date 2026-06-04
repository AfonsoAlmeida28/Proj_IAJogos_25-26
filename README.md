# 🏎️ RACING NEAT AI - INTELIGENCIA ARTIFICIAL EM JOGOS (25/26)

Este repositorio contem o projeto pratico para a disciplina de Inteligencia Artificial em Jogos. O objetivo central consiste em aplicar Redes Neuronais e Algoritmos Geneticos - especificamente o algoritmo NEAT (NeuroEvolution of Augmenting Topologies) - para treinar agentes autonomos capazes de conduzir num circuito fechado otimizando a sua propria trajetoria ao longo de geracoes.

## Abordagens e arquitetura

O projeto explora e compara duas metodologias distintas de percecao e recompensa para os agentes:

### 1. Cenario de Sensores (Radares / Raycasting)
* **Inputs:** 5 sensores de distancia baseados em raycasting (angulos de -60 a +60 graus). As distancias medidas ate aos limites da pista sao normalizadas no intervalo [0, 1] dividindo pelo alcance maximo do radar.
* **Outputs:** Dois neuronios de saida que controlam a aceleracao (throttle) e a direcao (steering). Foi aplicada uma "zona morta" (deadzone < 0.2) na direcao para evitar trepidacao excessiva e comportamentos erraticos nas retas.
* **Funcao de Fitness:** Focada na exploracao continua. Os agentes sao recompensados com base na distancia total percorrida e na velocidade media mantida sem colidir.

### 2. Cenario de Navegacao (Waypoints)
* **Inputs:** A distancia euclidiana normalizada e o angulo relativo entre a orientacao do carro e o proximo alvo invisivel (waypoint). O angulo e convertido num formato normalizado entre [-1, 1].
* **Outputs:** Identicos a abordagem de sensores.
* **Funcao de Fitness:** Baseada em recompensas explicitas. Os agentes recebem bonus de pontuacao (+200) sempre que cruzam com sucesso a sua bounding box do waypoint atual, guiando rigidamente o trajeto evolutivo.

## Estrutura do projeto

Para garantir a facil leitura e manutencao do codigo, o repositorio encontra-se organizado da seguinte forma:

```
Proj_IAJogos_25-26/
│
├── configs/                 #Ficheiros de configuração da biblioteca NEAT
│   ├── config-radares.txt   # Hiperparâmetros para o treino por sensores
│   └── config-waypoints.txt # Hiperparâmetros para o treino por navegação
│
├── models/                  # Modelos treinados e histórico (Pickle)
├── svgs/                    # Grafos gerados (Topologia das Redes Neuronais Ocultas)
|
├── base_jogo.py             # Lógica principal do simulador, colisões e física
├── utils.py                 # Funções auxiliares matemáticas e de imagem
├── visualize.py             # Script para renderizar o interior das Redes Neuronais
├── 25_26_IIAJogosProjecto_04.pdf # Relatório com uma explicação exaustiva de todos os componentes do projeto
├── Radares.ipynb            # Notebook de Treino: Abordagem por Sensores
├── Waypoints.ipynb          # Notebook de Treino: Abordagem por Checkpoints
├── Visualizacao_e_Resultados.ipynb # Análise comparativa da evolução do Fitness
└── Duelo_Final.ipynb    # Duelo Interativo
```

## Como Executar


### 1. Pre-Requisitos
Certifique-se de que possui as bibliotecas necessarias instaladas. Recomenda-se o uso de um ambiente virtual. Comando de instalacao via terminal:
pip install neat-python pygame matplotlib graphviz numpy

(Nota: Para a geracao visual da topologia das redes, e necessario ter o software Graphviz instalado no sistema operativo e adicionado as variaveis de ambiente).

### 2. O Grande Duelo (Modo Discussao/Apresentacao)
O script definitivo que compila os melhores resultados deste projeto encontra-se no ficheiro "Notebook_Defesa.ipynb". 

Este notebook executa:
- O carregamento dos cerebros extraindo o verdadeiro Melhor Genoma Historico do ficheiro de estatisticas, resolvendo o problema inerente de overfitting ou colapso evolutivo da ultima geracao guardada nativamente pela biblioteca NEAT.
- A renderizacao de um Duelo visual onde o campeao de Radares compete em tempo real contra o campeao de Waypoints.
- Testes modulares de robustez: variaveis de configuracao no topo do ficheiro permitem mudar dinamicamente a linha de partida ou inverter o sentido do circuito, testando a capacidade de generalizacao espacial de ambas as redes fora da sua distribuicao original de treino.


## Observações e Desafios Superados

- Minimos Locais: Durante o treino por Waypoints, a populacao apresentou tendencia para estagnar em maximos locais de recompensa (colisao prematura em curvas apertadas). Isto foi resolvido atraves de um sistema de Curriculum Learning interativo, onde os alvos puderam ser ajustados em tempo real, sendo a configuracao vitoriosa guardada em "waypoints_finais.pkl".

- Fisica e Subviragem: Foi fundamental garantir que as velocidades de rotacao estipuladas durante o treino se mantivessem consistentes na inferencia, pois pequenas discrepancias fisicas causavam comportamentos de subviragem/sobreviragem imprevisiveis.

- Determinismo vs. Ruido: Durante o treino, injetou-se ruido aleatorio nas acoes de steering e throttle para criar modelos resilientes a imperfeicoes mecanicas.

---------------------------------------------------------
Projeto desenvolvido por: **Afonso Almeida** e **João Nunes**, fc59810 e fc59806, respetivamente.