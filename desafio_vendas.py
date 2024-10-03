def analise_vendas(vendas):
    # TODO: Calcule o total de vendas e realize a média mensal:
    total_vendas = sum(vendas)
    media_vendas = total_vendas / len(vendas)
    return f"{total_vendas}, {media_vendas:.2f}"

def obter_entrada_vendas():
    # Solicita a entrada do usuário em uma única linha
    entrada = input()

    # TODO: Converta a entrada em uma lista de inteiros:
    #entrada_vendas = entrada.split(',')
    #entrada_vendas = map(int, entrada_vendas)
    #vendas = list(entrada_vendas)
    vendas = list(map(int, entrada.split(',')))
    
    return vendas

vendas = obter_entrada_vendas()
print(analise_vendas(vendas))

# 120, 150, 170, 130, 200, 250, 180, 220, 210, 160, 140, 190
#2120, 176.67
# 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120
#780, 65.00
# 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60
#390, 32.50
