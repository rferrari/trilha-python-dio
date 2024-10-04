import time

class Veiculo:
    def __init__(self, cor, placa, numero_rodas):
        self.cor = cor
        self.placa = placa
        self.numero_rodas = numero_rodas

    def ligar_motor(self):
        print(self.placa + ": Ligando o motor")

    def __str__(self):
        return f"{self.__class__.__name__}: {', '.join([f'{chave}={valor}' for chave, valor in self.__dict__.items()])}"


class Motocicleta(Veiculo):
    pass


class Carro(Veiculo):
    pass


class Caminhao(Veiculo):
    def __init__(self, cor, placa, numero_rodas, carregado):
        super().__init__(cor, placa, numero_rodas)
        self.peso = 0
        self.carregado = False

    def esta_carregado(self):
        return self.carregado
    
    def carrega(self, peso):
        self.peso += peso
        time.sleep(0.35)
        print("||" * (100 - (100 - self.peso // 10)))
        return self.carregado
    
    def peso_carga(self):
        return self.peso


moto = Motocicleta("preta", "moto-1234", 2)
carro = Carro("branco", "carro-0098", 4)
caminhao = Caminhao("roxo", "truck-8712", 8, True)

print(moto)
print(carro)
print(caminhao)

print("Caminhao esta carregado? " + str(caminhao.esta_carregado()))
while (not caminhao.carregado):
    if(caminhao.peso_carga() == 100):
        caminhao.carregado = True
    if(caminhao.carregado):
        print("Sim estou carregado")
    else:
        caminhao.carrega(10)
    print(caminhao.peso_carga())

moto.ligar_motor()
carro.ligar_motor()
caminhao.ligar_motor()
