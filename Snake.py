import random
import tkinter
from tkinter import messagebox

ALTURA_JANELA = LARGURA_JANELA = 500
VELOCIDADE_COBRA = 250 # Pixels por segundo
TAMANHO_QUADRADO = 50 # Pixels
TEMPO = int(1000*TAMANHO_QUADRADO/VELOCIDADE_COBRA) # Tempo em milissegundos
COR_COBRA = "#00FF00" # Verde
COR_COMIDA = "#FF0000" # Vermelho
COR_FUNDO = "#000000" # Preto
PONTUACAO_MAXIMA = ((ALTURA_JANELA / TAMANHO_QUADRADO)**2) - 2
valor_pontuacao = 0
direcao = 'b'
tecla_pressionada = direcao

def inicializar_modo_grafico():
    global valor_pontuacao
    global COR_FUNDO
    global ALTURA_JANELA
    global LARGURA_JANELA
    
    window = tkinter.Tk()
    window.title("Cobrinha")
    window.resizable(False, False)

    placar = tkinter.Label(window, text="Pontuação: {}".format(valor_pontuacao), font=('consolas', 40))
    placar.pack()
    
    mapa = tkinter.Canvas(window, bg = COR_FUNDO, height = ALTURA_JANELA, width = LARGURA_JANELA)
    mapa.pack()

    window.update()

    largura_janela = window.winfo_width()
    altura_janela = window.winfo_height()
    largura_tela = window.winfo_screenwidth()
    altura_tela = window.winfo_screenheight()

    x = int((largura_tela/2) - (largura_janela/2))
    y = int((altura_tela/2) - (altura_janela/2))

    window.geometry(f"{largura_janela}x{altura_janela}+{x}+{y}")

    window.bind('<Left>', lambda event: proxima_direcao('e'))
    window.bind('<Right>', lambda event: proxima_direcao('d'))
    window.bind('<Up>', lambda event: proxima_direcao('c'))
    window.bind('<Down>', lambda event: proxima_direcao('b'))
    window.bind('a', lambda event: proxima_direcao('e'))
    window.bind('d', lambda event: proxima_direcao('d'))
    window.bind('w', lambda event: proxima_direcao('c'))
    window.bind('s', lambda event: proxima_direcao('b'))
    window.bind('A', lambda event: proxima_direcao('e'))
    window.bind('D', lambda event: proxima_direcao('d'))
    window.bind('W', lambda event: proxima_direcao('c'))
    window.bind('S', lambda event: proxima_direcao('b'))

    return window, mapa, placar

def loop_cobrinha(cobra, comida):
    global valor_pontuacao # Pontuação no placar
    global direcao
    global TEMPO

    direcao = mudar_direcao(direcao) # Atualiza a direção
    cobra = atualiza_posicao_cobra(cobra) # Atualiza as coordenadas da cobra
    
    comeu = cobra_comeu_comida(cobra, comida) # Verifica se a cobra comeu a comida
    if not comeu:
        cobra = remove_cauda(cobra)
    else:
        valor_pontuacao = aumenta_pontuacao(valor_pontuacao) # Acrescenta a pontuação e muda o placar
        remove_comida_da_tela()
        if valor_pontuacao < PONTUACAO_MAXIMA:
            comida = nova_comida(cobra, comida)
            comida = desenha_comida(comida)

    if valor_pontuacao >= PONTUACAO_MAXIMA: # Caso tenha alcançado a pontuação máxima
        ganhou()
        escolha = jogar_novamente()
        return escolha
    
    colidiu = checa_colisoes(cobra) # Verifica se a cobra colidiu com ela mesma ou com as paredes
    if colidiu:
        perdeu()
        escolha = jogar_novamente()
        return escolha
    else:
        window.after(TEMPO, loop_cobrinha, cobra, comida)    
    
def desenha_comida(comida):
    global TAMANHO_QUADRADO
    global COR_COMIDA

    x, y = comida['coordenadas']
    circulo = mapa.create_oval(x,y,x+TAMANHO_QUADRADO,y+TAMANHO_QUADRADO,fill=COR_COMIDA,tag="comida")
    comida['desenhos'] = circulo
    return comida

def desenha_cobra(cobra):
    global TAMANHO_QUADRADO
    global COR_COBRA

    for x, y in cobra['coordenadas']:
        quadrado = mapa.create_rectangle(x, y, x + TAMANHO_QUADRADO, y + TAMANHO_QUADRADO, fill=COR_COBRA, tag="cobrinha")
        cobra['desenhos'].append(quadrado)

    return cobra

def atualiza_posicao_cobra(cobra):
    global TAMANHO_QUADRADO

    x, y = cabeca_da_cobra(cobra)
    x, y = nova_posicao_cabeca(x, y)
    cobra = desenha_cabeca_cobra(cobra, x, y)

    return cobra

def cabeca_da_cobra(cobra):
    x, y = cobra['coordenadas'][0]
    return x, y

def nova_posicao_cabeca(x, y):
    if direcao == 'c':
        y -= TAMANHO_QUADRADO
    elif direcao == 'b':
        y += TAMANHO_QUADRADO
    elif direcao == 'e':
        x -= TAMANHO_QUADRADO
    elif direcao == 'd':
        x += TAMANHO_QUADRADO
    
    return x, y

def desenha_cabeca_cobra(cobra, x, y):
    global TAMANHO_QUADRADO
    global COR_COBRA

    cobra['coordenadas'].insert(0, (x, y))
    quadrado = mapa.create_rectangle(x, y, x + TAMANHO_QUADRADO, y + TAMANHO_QUADRADO, fill=COR_COBRA)
    cobra['desenhos'].insert(0, quadrado)

    return cobra

def cobra_comeu_comida(cobra, comida):
    x_cobra, y_cobra = cabeca_da_cobra(cobra)
    x_comida, y_comida = comida['coordenadas']
    return (x_cobra == x_comida) and (y_cobra == y_comida)

def remove_cauda(cobra):
    del cobra['coordenadas'][-1]
    mapa.delete(cobra['desenhos'][-1])
    del cobra['desenhos'][-1]

    return cobra

def aumenta_pontuacao(valor_pontuacao):
    valor_pontuacao += 1
    placar.config(text="Pontuação: {}".format(valor_pontuacao))

    return valor_pontuacao

def remove_comida_da_tela():
    mapa.delete("comida")

def nova_comida(cobra, comida):
    global LARGURA_JANELA
    global ALTURA_JANELA
    global TAMANHO_QUADRADO

    while True:
        x = random.randint(0, (LARGURA_JANELA / TAMANHO_QUADRADO)-1) * TAMANHO_QUADRADO
        y = random.randint(0, (ALTURA_JANELA / TAMANHO_QUADRADO)-1) * TAMANHO_QUADRADO

        if not (tuple([x, y]) in cobra['coordenadas']):
            comida['coordenadas'] = [x, y]
            break

    return comida

def checa_colisoes(cobra):
    global LARGURA_JANELA
    global ALTURA_JANELA
    x, y = cabeca_da_cobra(cobra)
    colidiu = (x < 0) or (x >= LARGURA_JANELA) or (y < 0) or (y >= ALTURA_JANELA) or (tuple([x, y]) in cobra['coordenadas'][1:])

    return colidiu

def mudar_direcao(direcao):
    global tecla_pressionada
    nova_direcao = tecla_pressionada

    if direcao_permitida(direcao, nova_direcao):
        return nova_direcao
    else:
        return direcao

def direcao_permitida(d, nd):
    # d = direcao
    # nd = nova direcao
    if d == '':
        return False
    return ((nd == 'c') and (d != 'b')) or ((nd == 'b') and (d != 'c')) or ((nd == 'e') and (d != 'd')) or ((nd == 'd') and (d != 'e'))

def ganhou():
    mapa.delete(tkinter.ALL)
    mapa.create_text(mapa.winfo_width()/2, mapa.winfo_height()/8,
                       font=('consolas',40), text="Você ganhou!", fill="green", tag="game_over")

def perdeu():
    mapa.delete(tkinter.ALL)
    mapa.create_text(mapa.winfo_width()/2, mapa.winfo_height()/8,
                       font=('consolas',40), text="GAME OVER", fill="red", tag="game_over")

def proxima_direcao(tecla):
    global tecla_pressionada
    tecla_pressionada = tecla

def jogar_novamente():
    res = messagebox.askquestion('Jogar novamente?', 'Deseja jogar novamente?')
    
    if res == 'yes':
        escolha = True
        mapa.delete(tkinter.ALL)
        novo_jogo()
    else:
        escolha = False
        window.destroy()
    
    return escolha

def novo_jogo():
    global valor_pontuacao
    global direcao
    global tecla_pressionada

    valor_pontuacao = 0
    direcao = 'b'
    tecla_pressionada = direcao

    placar.config(text="Pontuação: {}".format(valor_pontuacao))

    cobra = cobra_inicial()
    comida = comida_inicial()
    comida = desenha_comida(comida)
    cobra = desenha_cobra(cobra)
    game = loop_cobrinha(cobra, comida)

    return game

def cobra_inicial():
    cobra = {'coordenadas': [(0, TAMANHO_QUADRADO), (0,0)], 'desenhos': []}
    
    return cobra

def comida_inicial():
    comida = {'coordenadas': [2*TAMANHO_QUADRADO, 3*TAMANHO_QUADRADO], 'desenhos': []}
    
    return comida

if __name__ == "__main__":
    window, mapa, placar = inicializar_modo_grafico()
    jogo = novo_jogo()
    window.mainloop()
