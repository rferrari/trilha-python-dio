class Pessoa:
    def __init__(self, nome, idade):
        self.nome = nome
        self.idade = idade
        print("Pessoa nasceu, seu nome sera:" + self.nome)

    @classmethod
    def criar_de_data_nascimento(cls, ano, mes, dia, nome):
        idade = 2022 - ano
        return cls(nome, idade)

    @staticmethod
    def e_maior_idade(idade):
        #print(self.nome)
        return idade >= 21


p = Pessoa.criar_de_data_nascimento(1994, 3, 21, "Guilherme")
print(p.nome, p.idade)

print(Pessoa.e_maior_idade(p.idade))
print(Pessoa.e_maior_idade(p.idade-5))



p2 = Pessoa("Nome",21).criar_de_data_nascimento(1994, 3, 21, "Guilherme")
print(p2.nome)
print(Pessoa.e_maior_idade(p2.idade))
