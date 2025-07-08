import pygame
import math
import sys
import render_lib
from algebra_linear import calcular_pontos_parabola, origem,intersecao_raio_parabola,matriz_rotacao,foco, calcular_normal, matriz_reflexao, mudar_largura_altura

# Inicialização
pygame.init()
largura, altura = 800, 600
mudar_largura_altura(largura,altura)
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Reflexão em Parábola com Álgebra Linear")
relogio = pygame.time.Clock()
fonte = pygame.font.SysFont("arial", 18)
# Inicializa referencias globais
render_lib.render_init(fonte, tela, pygame)

# Cores
PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)
AMARELO = (255, 255, 0)
AZUL = (100, 255, 255)
VERMELHO = (255, 100, 100)


def desenhar_parabola():
    pontos = calcular_pontos_parabola()
    pygame.draw.lines(tela, BRANCO, False, pontos, 2)
    pygame.draw.circle(tela, VERMELHO, (int(foco[0]), int(foco[1])), 8)

# Loop principal
angulo = 0
rodando = True
while rodando:
    tela.fill(PRETO)
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

    # Controles
    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_LEFT]: angulo -= 1
    if teclas[pygame.K_RIGHT]: angulo += 1

    # Desenhar parábola e foco
    desenhar_parabola()
    pygame.draw.circle(tela, AMARELO, origem, 10)

    ### --- TRANSFORMAÇÕES --- ###
    # 1. Matriz de rotação para o raio incidente
    M_rot = matriz_rotacao(angulo)
    tamanho_matriz_desenhada = render_lib.desenhar_matriz(M_rot.m,(0,0), BRANCO, "Matriz Rotacao")
    direcao = M_rot.aplicar((1, 0))  # Rotaciona vetor (1,0) pelo ângulo
    
    # 2. Encontrar ponto de interseção
    ponto_intersecao = intersecao_raio_parabola(origem, direcao)
    
    if ponto_intersecao:
        pygame.draw.line(tela, AMARELO, origem, ponto_intersecao, 3)
        
        # 3. Calcular normal e matriz de reflexão
        normal = calcular_normal(ponto_intersecao[0])
        M_refl = matriz_reflexao(normal)
        render_lib.desenhar_matriz(M_refl.m, (0, tamanho_matriz_desenhada[1] + 10), AMARELO, "Matriz Reflexao")
        
        # 4. Aplicar reflexão ao vetor direção
        v_refletido = M_refl.aplicar(direcao)
        
        # Desenhar raio refletido
        fim_refletido = (ponto_intersecao[0] + v_refletido[0]*300, 
                        ponto_intersecao[1] + v_refletido[1]*300)
        pygame.draw.line(tela, AZUL, ponto_intersecao, fim_refletido, 2)
        
        # Desenhar normal (para visualização)
        normal_end = (ponto_intersecao[0] + normal[0]*50, 
                     ponto_intersecao[1] + normal[1]*50)
        pygame.draw.line(tela, VERMELHO, ponto_intersecao, normal_end, 1)

    pygame.display.flip()
    relogio.tick(60)

pygame.quit() 
sys.exit()
