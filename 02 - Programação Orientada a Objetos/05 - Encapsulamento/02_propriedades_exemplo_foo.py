class Foo:
    def __init__(self, x=None):
        self._x = x

    @property
    def x(self):
        return self._x or 0

    @x.setter
    def x(self, value):
        self._x += value

    @x.deleter
    def x(self):
        self._x = 0


foo = Foo(10)
print(foo.x)
del foo.x
print(foo.x)
foo.x = 10
print(foo.x)


class Cidadao:
    def __init__(self, n=None, s=None, nc=None):
        self._nome = n
        self._sobrenome = s
        self._nomecomleto = nc

    @property
    def n(self):
        return self._nome or ""
    
    @property
    def s(self):
        return self._sobrenome or ""
    
    @property
    def nc(self):
        return self._nomecomleto or (self._nome + " " + self._sobrenome)

    @n.setter
    def n(self, value):
        self._nome = value
        self._nomecomleto = value +" "+ self._nomecomleto.split(' ')[1]

    @s.setter
    def s(self, value):
        self._sobrenome = value
        self._nomecomleto = self._nomecomleto.split(' ')[0] + " " + self._sobrenome

    @nc.setter
    def nc(self, value):
        self._nomecomleto = value
        if not self._nomecomleto: 
            self._nome = self._nome
            self._sobrenome = self._sobrenome
        else:
            self._nome = self._nomecomleto.split(' ')[0] if ' ' in self._nomecomleto else self._nomecomleto     
            self._sobrenome = self._nomecomleto.split(' ')[1] if ' ' in self._nomecomleto else ''

    @n.deleter
    def n(self):
        self._nomecomleto = ""

    @s.deleter
    def s(self):
        self._sobrenome = ""

    @nc.deleter
    def nc(self):
        self._nomecomleto = ""


pessoa = Cidadao("Nome", "Sobrenome")
print(pessoa.n)
del pessoa.n
print(pessoa.s)
pessoa.s = "Silva"
print(pessoa.nc)
pessoa.n = "Adam"
pessoa.s = "Ferri"
print(pessoa.nc)

pessoa2 = Cidadao()
pessoa2.nc = "Cidadao Mundo"
print(pessoa2.n)
print(pessoa2.s)
pessoa2.s = "Woods"
print(pessoa2.nc)
pessoa2.n = "Adam"
print(pessoa2.nc)
