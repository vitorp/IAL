import pygame
import sys
import render_lib
from render_lib import PRETO, BRANCO, AMARELO, VERMELHO, AZUL
from algebra_linear import calcular_pontos_parabola,foco,h, mudar_largura_altura, calcular_feixe

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

# origem
origem = (h, altura - 50)

def desenhar_parabola():
    pontos = calcular_pontos_parabola()
    pygame.draw.lines(tela, BRANCO, False, pontos, 2)
    pygame.draw.circle(tela, VERMELHO, (int(foco[0]), int(foco[1])), 8)

def desenhar_legendas():
    textos = [
        ("Fonte Amarela, Foco Vermelho", VERMELHO),
       
        ("RAIO incidente", AMARELO),
        ("RAIO refletido", AZUL),
    ]
    for i, (txt, cor) in enumerate(textos):
        texto = fonte.render(txt, True, cor)
        tela.blit(texto, (20, 20 + i * 25))

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
    desenhar_legendas()

    (M_rot, direcao,  ponto_intersecao, normal, M_refl, v_refletido) = calcular_feixe(angulo, origem)
    tamanho_matriz_desenhada = render_lib.desenhar_matriz(M_rot.m,(0, 100), BRANCO, f"Matriz Rotação {angulo} graus")
        
    if ponto_intersecao:
        # Desenha raio
        pygame.draw.line(tela, AMARELO, origem, ponto_intersecao, 3)
        
        # Desenha matriz de reflexão
        render_lib.desenhar_matriz(M_refl.m, (0, tamanho_matriz_desenhada[1] + 10), AMARELO, f"Matriz Reflexão Raio ({direcao[0]:.3f}, {direcao[1]:.3f}) -> ({v_refletido[0]:.3f}, {v_refletido[1]:.3f})")
        
        # Desenha raio refletido
        render_lib.desenhar_raio_refletido(ponto_intersecao, v_refletido)
        
        # Desenha normal (para visualização)
        render_lib.desenhar_reta_normal(ponto_intersecao, normal)
    else:
        # Desenha raio ao infinito
        render_lib.desenhar_raio_infinito(origem, direcao)

    pygame.display.flip()
    relogio.tick(60)

pygame.quit() 
sys.exit()
