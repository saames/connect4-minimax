import math
import copy
import random

LINHAS = 6
COLUNAS = 7

VAZIO = 0
JOGADOR = 1
IA = 2

# FUNÇÕES
def criar_tabuleiro():
    return [[VAZIO for _ in range(COLUNAS)] for _ in range(LINHAS)]

def imprimir_tabuleiro(tabuleiro):
    print("\n 0 1 2 3 4 5 6")
    print("---------------")
    for linha in tabuleiro:
        print("|" + "|".join([str(p) if p != VAZIO else " " for p in linha]) + "|")
    print("---------------")

def movimento_valido(tabuleiro, coluna):
    return tabuleiro[0][coluna] == VAZIO

def obter_linha_valida(tabuleiro, coluna):
    for r in range(LINHAS - 1, -1, -1):
        if tabuleiro[r][coluna] == VAZIO:
            return r
    return -1

def jogar_peca(tabuleiro, linha, coluna, peca):
    tabuleiro[linha][coluna] = peca

def verificar_vitoria(tabuleiro, peca):
    # Horizontais
    for c in range(COLUNAS - 3):
        for r in range(LINHAS):
            if tabuleiro[r][c] == peca and tabuleiro[r][c+1] == peca and tabuleiro[r][c+2] == peca and tabuleiro[r][c+3] == peca:
                return True
    # Verticais
    for c in range(COLUNAS):
        for r in range(LINHAS - 3):
            if tabuleiro[r][c] == peca and tabuleiro[r+1][c] == peca and tabuleiro[r+2][c] == peca and tabuleiro[r+3][c] == peca:
                return True
    # Diagonais Positivas
    for c in range(COLUNAS - 3):
        for r in range(LINHAS - 3):
            if tabuleiro[r][c] == peca and tabuleiro[r+1][c+1] == peca and tabuleiro[r+2][c+2] == peca and tabuleiro[r+3][c+3] == peca:
                return True
    # Diagonais Negativas
    for c in range(COLUNAS - 3):
        for r in range(3, LINHAS):
            if tabuleiro[r][c] == peca and tabuleiro[r-1][c+1] == peca and tabuleiro[r-2][c+2] == peca and tabuleiro[r-3][c+3] == peca:
                return True
    return False

def obter_colunas_validas(tabuleiro):
    return [col for col in range(COLUNAS) if movimento_valido(tabuleiro, col)]

def tabuleiro_esta_vazio(tabuleiro):
    # Otimização: se a base está vazia, tudo está vazio
    for c in range(COLUNAS):
        if tabuleiro[LINHAS - 1][c] != VAZIO:
            return False
    return True

# HEURÍSTICA
TABELA_PESOS = [
    [3, 4, 5,  7,  5, 4, 3],
    [4, 6, 8, 10,  8, 6, 4],
    [5, 8, 11, 13, 11, 8, 5],
    [5, 8, 11, 13, 11, 8, 5],
    [4, 6, 8, 10,  8, 6, 4],
    [3, 4, 5,  7,  5, 4, 3]
]

def pontuacao_posicao(tabuleiro, peca_ia):
    pontuacao = 0
    peca_jogador = JOGADOR if peca_ia == IA else IA

    for linha in range(LINHAS):
        for coluna in range(COLUNAS):
            if tabuleiro[linha][coluna] == peca_ia:
                # Soma pontos se a peça for da IA
                pontuacao += TABELA_PESOS[linha][coluna]
            elif tabuleiro[linha][coluna] == peca_jogador:
                # Subtrai pontos se a peça for do Jogador
                pontuacao -= TABELA_PESOS[linha][coluna]

    return pontuacao

# MINIMAX
def eh_no_terminal(tabuleiro):
    return verificar_vitoria(tabuleiro, JOGADOR) or verificar_vitoria(tabuleiro, IA) or len(obter_colunas_validas(tabuleiro)) == 0

def minimax(tabuleiro, profundidade, maximizando):
    colunas_validas = obter_colunas_validas(tabuleiro)
    
    terminal = eh_no_terminal(tabuleiro)
    if terminal:
        if verificar_vitoria(tabuleiro, IA):
            return (None, 1000000)
        elif verificar_vitoria(tabuleiro, JOGADOR):
            return (None, -1000000)
        else:
            return (None, 0)
            
    if profundidade == 0:
        return (None, pontuacao_posicao(tabuleiro, IA))

    if maximizando:
        valor_max = -math.inf
        melhor_coluna = colunas_validas[0]
        for col in colunas_validas:
            linha = obter_linha_valida(tabuleiro, col)
            tabuleiro_copia = copy.deepcopy(tabuleiro)
            jogar_peca(tabuleiro_copia, linha, col, IA)
            
            novo_valor = minimax(tabuleiro_copia, profundidade - 1, False)[1]
            if novo_valor > valor_max:
                valor_max = novo_valor
                melhor_coluna = col
        return melhor_coluna, valor_max

    else: # Minimizando
        valor_min = math.inf
        melhor_coluna = colunas_validas[0]
        for col in colunas_validas:
            linha = obter_linha_valida(tabuleiro, col)
            tabuleiro_copia = copy.deepcopy(tabuleiro)
            jogar_peca(tabuleiro_copia, linha, col, JOGADOR)
            
            novo_valor = minimax(tabuleiro_copia, profundidade - 1, True)[1]
            if novo_valor < valor_min:
                valor_min = novo_valor
                melhor_coluna = col
        return melhor_coluna, valor_min


# CONNECT 4
def iniciar_jogo():
    tabuleiro = criar_tabuleiro()
    fim_de_jogo = False
    turno = random.choice([0,1]) # 0 Jogador, 1 IA

    imprimir_tabuleiro(tabuleiro)

    while not fim_de_jogo:
        if turno == 0:
            try:
                col = int(input("Sua vez (escolha uma coluna de 0 a 6): "))
            except ValueError:
                print("Por favor, digite um número válido.")
                continue
                
            if 0 <= col <= 6 and movimento_valido(tabuleiro, col):
                linha = obter_linha_valida(tabuleiro, col)
                jogar_peca(tabuleiro, linha, col, JOGADOR)
                
                if verificar_vitoria(tabuleiro, JOGADOR):
                    imprimir_tabuleiro(tabuleiro)
                    print("\nVocê venceu!")
                    fim_de_jogo = True
                
                turno += 1
                turno = turno % 2
                imprimir_tabuleiro(tabuleiro)
            else:
                print("Movimento inválido. Tente novamente.")
                
        else:
            print("\nTurno da IA pensando...")
            # Se o tabuleiro estiver vazio, começa no meio
            if tabuleiro_esta_vazio(tabuleiro):
                coluna = COLUNAS // 2
            else:
                coluna, pontuacao = minimax(tabuleiro, 4, True) # Profundidade 4 
            
            if movimento_valido(tabuleiro, coluna):
                linha = obter_linha_valida(tabuleiro, coluna)
                jogar_peca(tabuleiro, linha, coluna, IA)
                
                if verificar_vitoria(tabuleiro, IA):
                    imprimir_tabuleiro(tabuleiro)
                    print("\nA IA venceu!")
                    fim_de_jogo = True
                    
                turno += 1
                turno = turno % 2
                imprimir_tabuleiro(tabuleiro)

if __name__ == "__main__":
    iniciar_jogo()