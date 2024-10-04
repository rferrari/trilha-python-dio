class Cachorro:
    def __init__(self, nome, cor, acordado=True):
        print("\nInicializando a classe...")
        self.nome = nome
        self.cor = cor
        self.acordado = acordado
        print("Classe iniciada" + str(vars(self)))


    def __del__(self):
        print(f"Removendo a instância da classe: {self.nome}")
        print(f"{self.nome} say: auuuuuuuuuuuuuuu\n")

    def falar(self):
        if(self.acordado):
            print(self.nome + " say: Au Au")
        else:
            print(self.nome + ":  Zzzzzz  Zzzzzz  Zzzzzz")


def criar_cachorro():
    c = Cachorro("Zeus", "Branco e preto", False)
    return c
    # print(c.nome)


c = Cachorro("Chappie", "amarelo")
c.falar()
del c

c = Cachorro("Dog", "gray", False)
print(f"{c.nome}!!!")
c.falar() 

if(c.acordado == False):
    print(f"{c.nome} wake up!")
    c.acordado = True
c.falar() 

c.acordado = True
print(f"{c.nome}!!!")
c.falar()


z = criar_cachorro()
z.falar() 
if(z.acordado == False):
    print(f"{z.nome} wake up!")
    z.acordado = True
print(f"{z.nome}!!!")

z.falar()
c.falar()
