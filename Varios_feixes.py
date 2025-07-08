import pygame
import sys
import render_lib
from render_lib import PRETO, BRANCO, AMARELO, VERMELHO, AZUL
from algebra_linear import calcular_pontos_parabola, intersecao_raio_parabola,matriz_rotacao,foco, calcular_normal, matriz_reflexao, mudar_largura_altura, h,k, calcular_feixe

pygame.init()
largura, altura = 1000, 600
mudar_largura_altura(largura,altura)
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Reflexão em Parábola - Álgebra Linear Aplicada")
relogio = pygame.time.Clock()
fonte = pygame.font.SysFont("arial", 18)
# Inicializa referencias globais
render_lib.render_init(fonte, tela, pygame)

origem = (h, altura - 50)

def desenhar_parabola():
    pontos = calcular_pontos_parabola()
    pygame.draw.lines(tela, BRANCO, False, pontos, 2)
    pygame.draw.circle(tela, BRANCO, (int(h), int(k)), 5, 1)
    pygame.draw.circle(tela, AMARELO, (int(foco[0]), int(foco[1])), 6)
    pygame.draw.circle(tela, VERMELHO, (int(origem[0]), int(origem[1])), 6)

def desenhar_feixes(cor_raio, angulo_global):
    tamanho_matriz_desenhada = (0,100)
    numero_raio = 0
    for ang in range(-50, 51, 10):
        numero_raio += 1
        (M_rot, direcao,  ponto_intersecao, normal, M_refl, v_refletido) = calcular_feixe(ang+ angulo_global, foco)
        
        if ponto_intersecao:
            # Desenha Raio
            pygame.draw.line(tela, cor_raio, origem, ponto_intersecao, 2)

            # Desenha raio refletido
            render_lib.desenhar_raio_refletido(ponto_intersecao, v_refletido)

            # Desenha matriz de rotação e reflexão
            tamanho_matriz_desenhada = render_lib.desenhar_matriz(M_rot.m, (0,tamanho_matriz_desenhada[1]), BRANCO, f"Matriz Rotação Raio {numero_raio}")
            tamanho_matriz_desenhada = render_lib.desenhar_matriz(M_refl.m, (0,tamanho_matriz_desenhada[1]), AMARELO, f"Matriz Reflexão Raio {numero_raio}")
        else:
            # Desenha raio ao infinito
            render_lib.desenhar_raio_infinito(foco, direcao)

def desenhar_legendas():
    textos = [
        ("Fonte no FOCO -> Feixes refletidos saem paralelos (Farol Ideal)", AMARELO),
       
        ("RAIO incidente", BRANCO),
        ("RAIO refletido", AZUL),
    ]
    for i, (txt, cor) in enumerate(textos):
        texto = fonte.render(txt, True, cor)
        tela.blit(texto, (20, 20 + i * 25))

# LOOP PRINCIPAL
angulo_global = 0
rodando = True
while rodando:
    tela.fill(PRETO)
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_LEFT]: angulo_global -= 1
    if teclas[pygame.K_RIGHT]: angulo_global += 1
    
    desenhar_parabola()
    desenhar_legendas()

    # Fonte no foco (ideal)
    origem = foco
    desenhar_feixes(AMARELO, angulo_global)
    
    pygame.display.flip()
    relogio.tick(60)

pygame.quit()
sys.exit()

