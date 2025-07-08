# Cores
PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)
AMARELO = (255, 255, 0)
AZUL = (100, 255, 255)
VERMELHO = (255, 100, 100)

def render_init(fonte_ref, tela_ref, jogo):
    global fonte, tela, pygame
    fonte = fonte_ref
    tela = tela_ref
    pygame = jogo

def desenhar_matriz(matriz2D, origem, cor, nome_matriz):
    global fonte, tela, pygame
    
    altura_texto1 = desenhar_linha1(matriz2D, origem, cor)
    altura_texto2 = desenhar_linha2(matriz2D, origem, cor, altura_texto1)

    largura_interna_matriz = 115 # Largura de um colchete a outro
    altura_total = altura_texto1 + altura_texto2

    largura_nome = desenhar_nome(origem, cor, nome_matriz, altura_texto1, largura_interna_matriz, altura_total)

    desenhar_colchete_esquerda(origem, cor, altura_total)
    
    desenhar_colchete_direita(origem, cor, largura_interna_matriz, altura_total)

    return adicionar_coordenadas(origem, (largura_interna_matriz + 8 + 10 + largura_nome, altura_total)) # 8 e 10 hardcoded

def desenhar_colchete_direita(origem, cor, max_width, full_height):
    inicio = adicionar_coordenadas(origem, (max_width + 5, 0))
    fim = adicionar_coordenadas(origem, (max_width + 5, full_height))
    pygame.draw.line(tela, cor, inicio, fim, 3)

def desenhar_colchete_esquerda(origem, cor, full_height):
    inicio = adicionar_coordenadas(origem, (3,0))
    fim = adicionar_coordenadas(origem, (3, full_height))
    pygame.draw.line(tela, cor, inicio, fim , 3)

def desenhar_nome(origem, cor, nome_matriz, text_height, max_width, full_height):
    nome_surface = fonte.render(nome_matriz, True, cor)
    nome_coord = (max_width + 10, full_height/2 - text_height/2)
    tela.blit(nome_surface,  adicionar_coordenadas(origem, nome_coord))
    largura_nome = nome_surface.get_size()[0]
    return largura_nome

def desenhar_linha2(matriz2D, origem, cor, text_height):
    linha2 = fonte.render(f"{matriz2D[1][0]:.3f}, {matriz2D[1][1]:.3f}", True, cor)
    largura_texto2, altura_texto2 = linha2.get_size()
    tela.blit(linha2,  adicionar_coordenadas(origem, (5,text_height)))
    return altura_texto2

def desenhar_linha1(matriz2D, origem, cor):
    coord_inicio = adicionar_coordenadas(origem, (5, 5))
    linha1 = fonte.render(f"{matriz2D[0][0]:.3f}, {matriz2D[0][1]:.3f}", True, cor)
    largura_texto1, largura_texto2 = linha1.get_size()
    tela.blit(linha1, coord_inicio)
    return largura_texto2

def adicionar_coordenadas(coord1, coord2):
    return (coord1[0] + coord2[0], coord1[1] + coord2[1])

### Renders de feixes

def desenhar_raio_refletido(ponto_intersecao, v_refletido):
    fim_refletido = (ponto_intersecao[0] + v_refletido[0]*1000, 
                        ponto_intersecao[1] + v_refletido[1]*1000)
    pygame.draw.line(tela, AZUL, ponto_intersecao, fim_refletido, 2)

def desenhar_reta_normal(ponto_intersecao, normal):
    normal_end = (ponto_intersecao[0] + normal[0]*50, 
                     ponto_intersecao[1] + normal[1]*50)
    pygame.draw.line(tela, VERMELHO, ponto_intersecao, normal_end, 1)

def desenhar_raio_infinito(origem, direcao):
    pygame.draw.line(tela, AMARELO, origem, (origem[0] + direcao[0]*1000, origem[1] + direcao[1]*1000), 3)