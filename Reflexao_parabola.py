import pygame
import sys
import render_lib
from render_lib import PRETO, BRANCO, AMARELO, VERMELHO, AZUL
from algebra_linear import calcular_pontos_parabola, foco, h, k, calcular_feixe
from math import ceil, floor

pygame.init()
largura, altura = 1000, 600
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Reflexão em Parábola - Álgebra Linear")
relogio = pygame.time.Clock()
fonte = pygame.font.SysFont("arial", 18)
# Inicializa referencias globais
render_lib.render_init(fonte, tela, pygame)
origem = (h, altura - 50)

def desenhar_feixes(angulo_global, quantidade_feixes):
    tamanho_matriz_desenhada = (0,100)
    numero_raio = 0
    start = ceil(-(quantidade_feixes/2)) * 10
    end =  (floor((quantidade_feixes/2)) *10) + 1
    
    for ang in range(start, end, 10):
        numero_raio += 1
        (M_rot, direcao,  ponto_intersecao, normal, M_refl, v_refletido) = calcular_feixe(ang+ angulo_global, origem)
        if numero_raio == 1:
            tamanho_matriz_desenhada = render_lib.desenhar_matriz(M_rot.m,(0, tamanho_matriz_desenhada[1]), BRANCO, f"Matriz Rotação Raio {numero_raio} {angulo_global + ang} graus")
            print()
        else:
            tamanho_matriz_desenhada = render_lib.desenhar_matriz(M_rot.m, (0,tamanho_matriz_desenhada[1]), BRANCO, f"Matriz Rotação Raio {numero_raio}")
        if ponto_intersecao:
            # Desenha Raio
            pygame.draw.line(tela, AMARELO, origem, ponto_intersecao, 2)

            # Desenha raio refletido
            render_lib.desenhar_raio_refletido(ponto_intersecao, v_refletido)

            # Desenha matriz de rotação e reflexão
            if numero_raio == 1:
                tamanho_matriz_desenhada = render_lib.desenhar_matriz(M_refl.m, (0, tamanho_matriz_desenhada[1]), AMARELO, f"Matriz Reflexão Raio ({direcao[0]:.3f}, {direcao[1]:.3f}) -> ({v_refletido[0]:.3f}, {v_refletido[1]:.3f})")
            else:
                tamanho_matriz_desenhada = render_lib.desenhar_matriz(M_refl.m, (0,tamanho_matriz_desenhada[1]), AMARELO, f"Matriz Reflexão Raio {numero_raio}")
            
            # Desenha reta normal
            if quantidade_feixes == 1:
                render_lib.desenhar_reta_normal(ponto_intersecao, normal)

        else:
            # Desenha raio ao infinito
            render_lib.desenhar_raio_infinito(origem, direcao)

# LOOP PRINCIPAL
angulo_global = 0
# Menus
rodando = True
menu = True
simulando = False
configurando = False

selecao = 0
opcoes = [ "Unico Feixe", "Varios Feixes", "Configurar Origem"]
quantidade_opcoes = len(opcoes)

while rodando:
    while menu:
        tela.fill(PRETO)    
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                menu = False
                rodando = False
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_UP:
                    selecao = (selecao - 1) % quantidade_opcoes
                elif evento.key == pygame.K_DOWN:
                    selecao = (selecao + 1) % quantidade_opcoes
                elif evento.key == pygame.K_RETURN:
                    menu = False
                    simulando = True
                elif evento.key == pygame.K_ESCAPE:
                    menu = False
                    rodando = False

        for i, txt in enumerate(opcoes):
            cor = VERMELHO if selecao == i else BRANCO
            texto = fonte.render(txt, True, cor)
            tela.blit(texto, (20, 20 + i * 25))

        pygame.display.flip()
        relogio.tick(60)
    # Entra em configuração de origem
    if selecao == 2:
        configurando = True
    while configurando:
        tela.fill(PRETO)
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                simulando = False
                rodando = False

        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT]: origem = (origem[0] - 1, origem[1])
        if teclas[pygame.K_RIGHT]: origem = (origem[0] + 1, origem[1])
        if teclas[pygame.K_UP]: origem = (origem[0], origem[1] - 1)
        if teclas[pygame.K_DOWN]: origem = (origem[0], origem[1] + 1)
        if teclas[pygame.K_1]: origem = (h, altura - 50)
        if teclas[pygame.K_2]: origem = foco
        if teclas[pygame.K_ESCAPE]:
            configurando = False
            simulando = False
            menu = True
        
        pontos = calcular_pontos_parabola()
        render_lib.desenhar_parabola(pontos, h, k, foco, origem)
        render_lib.desenhar_legendas(selecao)
        pygame.display.flip()
        relogio.tick(60)

    while simulando:
        tela.fill(PRETO)
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                simulando = False
                rodando = False

        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT]: angulo_global -= 1
        if teclas[pygame.K_RIGHT]: angulo_global += 1
        if teclas[pygame.K_ESCAPE]:
            simulando = False
            menu = True
            angulo_global = 0
        
        pontos = calcular_pontos_parabola()
        render_lib.desenhar_parabola(pontos, h, k, foco, origem)
        render_lib.desenhar_legendas(selecao)
        
        quantidade_feixes = 0
        if (selecao == 0):
            quantidade_feixes = 1
        if (selecao == 1):
            quantidade_feixes = 11

        desenhar_feixes(angulo_global, quantidade_feixes)
        
        pygame.display.flip()
        relogio.tick(60)

pygame.quit()
sys.exit()

