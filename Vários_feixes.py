import pygame
import math
import sys
import render_lib

pygame.init()
largura, altura = 1000, 600
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Reflexão em Parábola - Álgebra Linear Aplicada")
relogio = pygame.time.Clock()
fonte = pygame.font.SysFont("arial", 18)
# Inicializa referencias globais
render_lib.render_init(fonte, tela, pygame)

# Cores
PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)
AMARELO = (255, 255, 0)
AZUL = (0, 200, 255)
LARANJA = (255, 150, 0)
VERMELHO = (255, 80, 80)
CINZA = (200, 200, 200)

# Parábola
a = 1 / 300
h, k = 550, 250
foco = (h, k + 1 / (4 * a))
fora_do_foco = (h, altura - 50)

# MATRIZES LINEARES
def matriz_reflexao(normal):
    nx, ny = normal
    return [[1 - 2*nx*nx, -2*nx*ny],
            [-2*nx*ny, 1 - 2*ny*ny]]

def matriz_rotacao(angulo_graus):
    t = math.radians(angulo_graus)
    return [[math.cos(t), -math.sin(t)],
            [math.sin(t), math.cos(t)]]

def aplicar_matriz(m, v):
    return (
        m[0][0] * v[0] + m[0][1] * v[1],
        m[1][0] * v[0] + m[1][1] * v[1]
    )

# GEOMETRIA
def desenhar_parabola():
    pontos = []
    for x in range(400, 700):
        y = int(a * (x - h) ** 2 + k)
        pontos.append((x, y))
    pygame.draw.lines(tela, BRANCO, False, pontos, 2)
    pygame.draw.circle(tela, BRANCO, (int(h), int(k)), 5, 1)
    pygame.draw.circle(tela, BRANCO, (int(foco[0]), int(foco[1])), 6)
    pygame.draw.circle(tela, BRANCO, (int(fora_do_foco[0]), int(fora_do_foco[1])), 6)

def calcular_normal(x_parabola):
    derivada = 2 * a * (x_parabola - h)
    normal_nao_unitario = (-derivada, 1)
    comprimento = math.hypot(*normal_nao_unitario)
    if comprimento == 0:
        return (0, 1)
    return (normal_nao_unitario[0]/comprimento, normal_nao_unitario[1]/comprimento)

def intersecao_raio_parabola(origem, direcao):
    x0, y0 = origem
    dx, dy = direcao

    if abs(dx) < 1e-6:
        return None

    A = a * dx**2
    B = 2 * a * dx * (x0 - h) - dy
    C = a * (x0 - h)**2 + k - y0
    D = B**2 - 4 * A * C

    if abs(A) < 1e-8 or D < 0:
        return None

    t1 = (-B + math.sqrt(D)) / (2 * A)
    t2 = (-B - math.sqrt(D)) / (2 * A)
    t_valido = [t for t in (t1, t2) if t > 0]
    t = min(t_valido) if t_valido else None
    if t is None:
        return None

    x = x0 + t * dx
    y = y0 + t * dy
    return (x, y) if 400 <= x <= 700 else None

def desenhar_feixes(origem, cor_raio, cor_reflexao, angulo_global):
    tamanho_matriz_desenhada = (0,100)
    counter = 0
    for ang in range(-50, 51, 10):
        counter += 1
        base = (math.cos(math.radians(ang)), math.sin(math.radians(ang)))
        M_rot = matriz_rotacao(angulo_global)
        # Desenha matriz de rotação
        tamanho_matriz_desenhada = render_lib.desenhar_matriz(M_rot, (0,tamanho_matriz_desenhada[1]), BRANCO, f"Matriz Rotação Raio {counter}")
        direcao = aplicar_matriz(M_rot, base)
        ponto = intersecao_raio_parabola(origem, direcao)
        if ponto:
            pygame.draw.line(tela, cor_raio, origem, ponto, 2)
            normal = calcular_normal(ponto[0])
            M_refl = matriz_reflexao(normal)
            tamanho_matriz_desenhada = render_lib.desenhar_matriz(M_refl, (0,tamanho_matriz_desenhada[1]), AMARELO, f"Matriz Reflexão Raio {counter}")
            refletido = aplicar_matriz(M_refl, direcao)
            fim = (ponto[0] + refletido[0] * 1000, ponto[1] + refletido[1] * 1000)
            pygame.draw.line(tela, cor_reflexao, ponto, fim, 1)

def desenhar_legendas():
    textos = [
        ("Fonte no FOCO → Feixes refletidos saem paralelos (Farol Ideal)", AMARELO),
       
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
    desenhar_feixes(foco, AMARELO, AZUL, angulo_global)

   

    pygame.display.flip()
    relogio.tick(60)

pygame.quit()
sys.exit()

