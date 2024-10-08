class Pessoa:
    def __init__(self, nome, sobrenome, nomecompleto = "", ano_nascimento = -1):
        self._nome = nome
        self._sobrenome = sobrenome
#        self._nomecomleto = nomecomleto if nomecomleto != "" else nomecomleto = (self._nome + " " + self._sobrenome)
        self._nomecomleto = nomecompleto if nomecompleto != "" else self._nome + " " + self._sobrenome 
        self._ano_nascimento = ano_nascimento

    def nomecompleto(self):
        return self._nomecomleto

    @property
    def idade(self):
        _ano_atual = 2022
        return _ano_atual - self._ano_nascimento


pessoa = Pessoa("Guilherme","Ramos", "", 1994)
print(pessoa.nomecompleto())

# print(f"Nome: {pessoa.nome} \tIdade: {pessoa.idade}")
