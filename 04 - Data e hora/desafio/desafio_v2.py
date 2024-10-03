import textwrap
from abc import ABC, abstractclassmethod, abstractproperty
from datetime import datetime, timezone, timedelta
import time
import pytz



class ContasIterador:
    def __init__(self, contas):
        self.contas = contas
        self._index = 0

    def __iter__(self):
        return self

    def __next__(self):
        try:
            conta = self.contas[self._index]
            return f"""\
            Agência:\t{conta.agencia}
            Número:\t\t{conta.numero}
            Titular:\t{conta.cliente.nome}
            Saldo:\t\tR$ {conta.saldo:.2f}
        """
        except IndexError:
            raise StopIteration
        finally:
            self._index += 1


class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []
        self.indice_conta = 0

    def realizar_transacao(self, conta, transacao):
        if len(conta.historico.transacoes_do_dia()) >= 10:
            print("\n@@@ Você excedeu o número de transações permitidas para hoje! @@@")
            return

        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)


class PessoaFisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf


class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)

    @property
    def saldo(self):
        return self._saldo

    @property
    def numero(self):
        return self._numero

    @property
    def agencia(self):
        return self._agencia

    @property
    def cliente(self):
        return self._cliente

    @property
    def historico(self):
        return self._historico

    def sacar(self, valor):
        saldo = self.saldo
        excedeu_saldo = valor > saldo

        if excedeu_saldo:
            print("\n@@@ Operação falhou! Você não tem saldo suficiente. @@@")

        elif valor > 0:
            self._saldo -= valor
            print("\n=== Saque realizado com sucesso! ===")
            return True

        else:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")

        return False

    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print("\n=== Depósito realizado com sucesso! ===")
        else:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
            return False

        return True


class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self._limite = limite
        self._limite_saques = limite_saques

    @classmethod
    def nova_conta(cls, cliente, numero, limite, limite_saques):
        return cls(numero, cliente, limite, limite_saques)

    def sacar(self, valor):
        numero_saques = len(
            [
                transacao
                for transacao in self.historico.transacoes
                if transacao["tipo"] == Saque.__name__
            ]
        )

        excedeu_limite = valor > self._limite
        excedeu_saques = numero_saques >= self._limite_saques

        if excedeu_limite:
            print("\n@@@ Operação falhou! O valor do saque excede o limite. @@@")

        elif excedeu_saques:
            print("\n@@@ Operação falhou! Número máximo de saques excedido. @@@")

        else:
            return super().sacar(valor)

        return False

    def __str__(self):
        return f"""\
            Agência:\t{self.agencia}
            C/C:\t\t{self.numero}
            Titular:\t{self.cliente.nome}
        """


class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.utcnow().strftime("%d/%m/%Y %H:%M:%S"),
            }
        )

    def gerar_relatorio(self, tipo_transacao=None):
        for transacao in self._transacoes:
            if (
                tipo_transacao is None
                or transacao["tipo"].lower() == tipo_transacao.lower()
            ):
                yield transacao

    def transacoes_do_dia(self):
        data_atual = datetime.utcnow().date()
        transacoes = []
        for transacao in self._transacoes:
            data_transacao = datetime.strptime(
                transacao["data"], "%d/%m/%Y %H:%M:%S"
            ).date()
            if data_atual == data_transacao:
                transacoes.append(transacao)
        return transacoes


class Transacao(ABC):
    @property
    @abstractproperty
    def valor(self):
        pass

    @abstractclassmethod
    def registrar(self, conta):
        pass


class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)


class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)


def log_transacao(func):
    def envelope(*args, **kwargs):
        resultado = func(*args, **kwargs)
        print(f"{datetime.now()}: {func.__name__.upper()}")
        return resultado

    return envelope


def menu():

    hora_atual = datetime.now().hour
    if hora_atual < 12:
        mensagem = "Bom dia!"
    elif hora_atual < 18:
        mensagem = "Boa tarde!"
    else:
        mensagem = "Boa noite!"

    menu = f"""\n
    {mensagem} Como posso ajudar?\n
    ================ MENU ================
    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [nc]\tNova conta
    [lc]\tListar contas
    [nu]\tNovo usuário
    [demo]\tCriar Templates Demonstracao
    [itc]\tImprimir Todos Clientes
    [q]\tSair
    => """
    return input(textwrap.dedent(menu))


def filtrar_cliente(cpf, clientes):
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None


def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print("\n@@@ Cliente não possui conta! @@@")
        return

    # FIXME: não permite cliente escolher a conta
    return cliente.contas[0]


@log_transacao
def depositar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return

    valor = float(input("Informe o valor do depósito: "))
    transacao = Deposito(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    cliente.realizar_transacao(conta, transacao)


@log_transacao
def sacar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return

    valor = float(input("Informe o valor do saque: "))
    transacao = Saque(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    cliente.realizar_transacao(conta, transacao)


@log_transacao
def exibir_extrato(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    print("\n================ EXTRATO ================")
    extrato = ""
    tem_transacao = False
    for transacao in conta.historico.gerar_relatorio():
        tem_transacao = True
        extrato += f"\n{transacao['data']}\t{transacao['tipo']}:\tR$ {transacao['valor']:.2f}"

    if not tem_transacao:
        extrato = "Não foram realizadas movimentações"

    print(extrato)
    print(f"\nSaldo:\t\tR$ {conta.saldo:.2f}")
    print("==========================================")


@log_transacao
def criar_cliente(clientes):
    cpf = input("Informe o CPF (somente número): ")
    cliente = filtrar_cliente(cpf, clientes)

    if cliente:
        print("\n@@@ Já existe cliente com esse CPF! @@@")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input(
        "Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): "
    )

    cliente = PessoaFisica(
        nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco
    )

    clientes.append(cliente)

    now = datetime.now().strftime("%d/%m/%y %H:%M")
    print(f"\n=== Cliente criado com sucesso @ {now}! ===")


def criar_templates(contas, clientes):
    start_time = datetime.now(timezone.utc)
    print(f"\n=== Iniciando Rotina Criacao Clientes Demonstracao ===")
    for i in range(10):
        cpf = (str(i) * 9) + "00"

        if filtrar_cliente(cpf, clientes):
            print("\n@@@ Já existe cliente com esse CPF! @@@")
        else:
            nome = "Cliente 0"+str(i+1)
            print("Cadastrado cliente: " + nome)

            hora_atual = datetime.now()
            data_nascimento = hora_atual.replace(year=hora_atual.year-10-i, month=hora_atual.month, day=hora_atual.day) - timedelta(days=i)
            # print(data_nascimento.strftime("%d-%m-%Y"))

            endereco = "Endereço Cliente " + str(i+1)

            cliente = PessoaFisica(
                nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco
            )

            clientes.append(cliente)

            numero_conta = len(contas) + 1
            conta = ContaCorrente.nova_conta(
                cliente=cliente, numero=numero_conta, limite=500, limite_saques=50
            )
            contas.append(conta)
            cliente.contas.append(conta)

            print("Cliente Cadastrado Com sucesso!")
            print(f"Nome: {cliente.nome}, CPF: {cliente.cpf}, Nasc.: {cliente.data_nascimento}, End.: {cliente.endereco}")
            print(f"  Número da Conta: {conta.numero}")
            time.sleep(1+(i/10))
    
    # Captura o horário de fim em UTC
    end_time = datetime.now(timezone.utc)

    # Calcula a diferença em segundos
    elapsed_time = (end_time - start_time).total_seconds()
    print(f"Clientes Cadastrados em {elapsed_time:.2f} segundos")


def imprimir_todos_clientes(contas, clientes):
    start_time = datetime.now(timezone.utc)

    for cliente in clientes:
        print(f"Nome: {cliente.nome}, CPF: {cliente.cpf}, Nasc.: {cliente.data_nascimento}, End.: {cliente.endereco}")
        for conta in cliente.contas:
            print(f"  Número da Conta: {conta.numero}")
            time.sleep(1)
    
    # Captura o horário de fim em UTC
    end_time = datetime.now(timezone.utc)

    # Calcula a diferença em segundos
    elapsed_time = (end_time - start_time).total_seconds()
    print(f"Lista de Clientes Impressa em {elapsed_time:.2f} segundos")



@log_transacao
def criar_conta(numero_conta, clientes, contas):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado, fluxo de criação de conta encerrado! @@@")
        return

    conta = ContaCorrente.nova_conta(
        cliente=cliente, numero=numero_conta, limite=500, limite_saques=50
    )
    contas.append(conta)
    cliente.contas.append(conta)

    print("\n=== Conta criada com sucesso! ===")


def listar_contas(contas):
    for conta in ContasIterador(contas):
        print("=" * 100)
        print(textwrap.dedent(str(conta)))


def main():
    clientes = []
    contas = []

    # Definindo os fusos horários
    fuso_suica = pytz.timezone('Europe/Zurich')
    fuso_tokyo = pytz.timezone('Asia/Tokyo')
    fuso_los_angeles = pytz.timezone('America/Los_Angeles')

    # Convertendo a hora atual para os fusos horários definidos
    hora_atual = datetime.now()
    hora_suica = hora_atual.astimezone(fuso_suica)
    hora_tokyo = hora_atual.astimezone(fuso_tokyo)
    hora_los_angeles = hora_atual.astimezone(fuso_los_angeles)

    # Exibindo as horas
    print()
    print(f"Hora local: {hora_atual.strftime('%m-%d %H:%M')}")
    print(f"Horário na Suíça: {hora_suica.strftime('%m-%d %H:%M')}")
    print(f"Horário em Tóquio: {hora_tokyo.strftime('%m-%d %H:%M')}")
    print(f"Horário em Los Angeles: {hora_los_angeles.strftime('%m-%d %H:%M')}")

    while True:
        opcao = menu()

        if opcao == "d":
            depositar(clientes)

        elif opcao == "s":
            sacar(clientes)

        elif opcao == "e":
            exibir_extrato(clientes)

        elif opcao == "nu":
            criar_cliente(clientes)

        elif opcao == "nc":
            numero_conta = len(contas) + 1
            criar_conta(numero_conta, clientes, contas)

        elif opcao == "lc":
            listar_contas(contas)

        elif opcao == "q":
            break

        elif opcao == "demo":
            criar_templates(contas, clientes)

        elif opcao == "itc":
            imprimir_todos_clientes(contas, clientes)

        else:
            print(
                "\n@@@ Operação inválida, por favor selecione novamente a operação desejada. @@@"
            )


main()
