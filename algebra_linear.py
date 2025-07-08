import math

largura, altura = 800, 600

# Parâmetros da parábola (y = a(x-h)² + k)
a = 1 / 300
h, k = 550, 250
foco = (h, k + 1 / (4 * a))
origem = (h, altura - 50)

def mudar_largura_altura(nova_largura, nova_altura):
    global largura, altura
    largura = nova_largura
    altura = nova_altura

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

def calcular_pontos_parabola():
    pontos = []
    for x in range(400, 700):
        y = int(a * (x - h)**2 + k)
        pontos.append((x, y))
    return pontos

def calcular_normal(x_parabola):
    """Vetor normal unitário à parábola no ponto x"""
    derivada = 2 * a * (x_parabola - h)
    normal_nao_unitario = (-derivada, 1)
    comprimento = math.sqrt(normal_nao_unitario[0]**2 + normal_nao_unitario[1]**2)
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