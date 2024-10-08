from abc import ABC, abstractmethod, abstractproperty


class ControleRemoto(ABC):
    @abstractmethod
    def ligar(self):
        pass

    @abstractmethod
    def desligar(self):
        pass

    @property
    @abstractproperty
    def marca(self):
        pass


class ControleTV(ControleRemoto):
    def ligar(self):
        print("Ligando a TV...")
        print("Ligada!")

    def desligar(self):
        print("Desligando a TV...")
        print("Desligada!")

    @property
    def marca(self):
        return "Philco"


class ControleArCondicionado(ControleRemoto):
    def ligar(self):
        print("Ligando o Ar Condicionado...")
        print("Ligado!")

    def desligar(self):
        print("Desligando o Ar Condicionado...")
        print("Desligado!")

    @property
    def marca(self):
        return "LG"


controle = ControleTV()
controle.ligar()
controle.desligar()
print(controle.marca)


controle = ControleArCondicionado()
controle.ligar()
controle.desligar()
print(controle.marca)



class ControleGeladeira(ControleRemoto):
    def __init__(self):
        self.super = True
        self.ligar()

    def ligar(self):
        print("Ligando a Geladeira...")
        if(self.super):
            print("Ligando a Super Gelo...")
        print("Geladeira On!")

    def desligar(self):
        print("Desligando o Geladeira...")
        print("Geladeira Off!")

    def superGelo(self):
        if(self.super):
            print("Desligando Super Gelo...")    
        else:
            print("Ligando Super Gelo...")
        self.super = not self.super
        print("Desligado!")

    @property
    def marca(self):
        return "Gelato"


crGeladeira = ControleGeladeira()
crGeladeira.superGelo()
crGeladeira.superGelo()
crGeladeira.superGelo()
