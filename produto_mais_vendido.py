def produto_mais_vendido(produtos):
    contagem = {}
    
    for produto in produtos:
        produto = produto.strip()
        if produto in contagem:
            contagem[produto] += 1
        else:
            contagem[produto] = 1
    
    max_produto = None
    max_count = 0
    
    for produto, count in contagem.items():
        # TODO: Encontre o produto com a maior contagem:
        if(count > max_count):
           max_produto = produto 
           max_count = count
        #print(produto, count)
        
    
    return max_produto

def obter_entrada_produtos():
    # Solicita a entrada do usuário em uma única linha
    entrada = input()
    # TODO: Converta a entrada em uma lista de strings, removendo espaços extras:
    produtos = list(map(str, entrada.split(',')))
    
    return produtos

produtos = obter_entrada_produtos()
print(produto_mais_vendido(produtos))

#Notebook, Mouse, Teclado, Mouse, Monitor, Mouse, Teclado
