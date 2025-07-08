import pygame
import math
import sys
import render_lib

# Inicialização
pygame.init()
largura, altura = 800, 600
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

# Parâmetros da parábola (y = a(x-h)² + k)
a = 1/300
h, k = 550, 250
foco = (h, k + 1/(4*a))

# Fonte de luz
origem = (h, altura - 50)
angulo = 0

# ÁLGEBRA LINEAR
class Matriz2D:
    def __init__(self, a, b, c, d):
        self.m = [[a, b], [c, d]]  # Matriz 2x2
    
    def aplicar(self, vetor):
        """Multiplica matriz por vetor: M*v"""
        x = self.m[0][0] * vetor[0] + self.m[0][1] * vetor[1]
        y = self.m[1][0] * vetor[0] + self.m[1][1] * vetor[1]
        return (x, y)

def matriz_rotacao(theta_graus):
    """Matriz de rotação 2D (sentido anti-horário)"""
    theta = math.radians(theta_graus)
    cos_t = math.cos(theta)
    sin_t = math.sin(theta)
    return Matriz2D(cos_t, -sin_t, sin_t, cos_t)

def matriz_reflexao(normal):
    """Matriz de reflexão sobre a normal unitária n"""
    nx, ny = normal
    return Matriz2D(
        1 - 2*nx*nx, -2*nx*ny,
        -2*nx*ny,    1 - 2*ny*ny
    )

# ÁLGEBRA LINEAR

def desenhar_parabola():
    pontos = []
    for x in range(400, 700):
        y = int(a * (x - h)**2 + k)
        pontos.append((x, y))
    pygame.draw.lines(tela, BRANCO, False, pontos, 2)
    pygame.draw.circle(tela, VERMELHO, (int(foco[0]), int(foco[1])), 8)

def calcular_normal(x_parabola):
    """Vetor normal unitário à parábola no ponto x"""
    derivada = 2 * a * (x_parabola - h)
    normal_nao_unitario = (-derivada, 1)
    comprimento = math.sqrt(normal_nao_unitario[0]**2 + normal_nao_unitario[1]**2)
    return (normal_nao_unitario[0]/comprimento, normal_nao_unitario[1]/comprimento)

def intersecao_raio_parabola(origem, direcao):
    """Calcula interseção raio-parábola usando álgebra"""
    x0, y0 = origem
    dx, dy = direcao
    A = a * dx**2
    B = 2 * a * dx * (x0 - h) - dy
    C = a * (x0 - h)**2 + k - y0
    discriminante = B**2 - 4*A*C
    
    if discriminante < 0: return None
    
    t1 = (-B + math.sqrt(discriminante)) / (2*A)
    t2 = (-B - math.sqrt(discriminante)) / (2*A)
    t_valido = [t for t in (t1, t2) if t > 0]
    t = min(t_valido) if t_valido else None
    
    if t is None: return None
    
    x, y = x0 + t*dx, y0 + t*dy
    return (x, y) if 400 <= x <= 700 else None

# Loop principal
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
