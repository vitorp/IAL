import math

# Parâmetros da parábola (y = a(x-h)² + k)
a = 1 / 300
h, k = 550, 250
foco = (h, k + 1 / (4 * a))

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

def calcular_feixe(angulo, origem):
    ### TRANSFORMAÇÕES
    # 1. Matriz de rotação para o raio incidente
    M_rot = matriz_rotacao(angulo)
    direcao = M_rot.aplicar((1,0))  # Rotaciona vetor (1,0) pelo ângulo
    
    # 2. Encontrar ponto de interseção
    ponto_intersecao = intersecao_raio_parabola(origem, direcao)

    if ponto_intersecao:
        # 3. Calcular normal e matriz de reflexão
        normal = calcular_normal(ponto_intersecao[0])
        M_refl = matriz_reflexao(normal)
        
        # 4. Aplicar reflexão ao vetor direção
        v_refletido = M_refl.aplicar(direcao)

        return (M_rot, direcao, ponto_intersecao, normal, M_refl, v_refletido)
    else:
        return(M_rot, direcao, ponto_intersecao, None, None, None)

def calcular_normal(x_parabola):
    """Vetor normal unitário à parábola no ponto x"""
    derivada = 2 * a * (x_parabola - h)
    normal_nao_unitario = (-derivada, 1)
    comprimento = math.sqrt(normal_nao_unitario[0]**2 + normal_nao_unitario[1]**2)
    return (normal_nao_unitario[0]/comprimento, normal_nao_unitario[1]/comprimento)

def intersecao_raio_parabola(origem, direcao):
    x0, y0 = origem
    dx, dy = direcao

    A = a * dx**2
    B = 2 * a * dx * (x0 - h) - dy
    C = a * (x0 - h)**2 + k - y0
    D = B**2 - 4 * A * C

    t1 = (-B + math.sqrt(D)) / (2 * A)
    t2 = (-B - math.sqrt(D)) / (2 * A)
    t_valido = [t for t in (t1, t2) if t > 0]
    t = min(t_valido) if t_valido else None
    if t is None:
        return (h, k)

    x = x0 + t * dx
    y = y0 + t * dy
    return (x, y) if 400 <= x <= 700 else None