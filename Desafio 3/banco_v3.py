# Implementação de Sistema Bancário utilizando POO em Python
#importação de bibliotecas ABC e e data/time
from abc import ABC, abstractclassmethod
from datetime import datetime
import textwrap
import os 


#implementação de interador
class ContasInterador:
    def __init__(self,contas):
        self.contas=contas
        self._index=0
        
    def __inter__(self):
        return self
    
    def __next__(self):
        try:
            conta=self.contas[self._index]
            return f"""\
                Agência:\t{conta.agencia}
                Número:\t{conta.nro_conta}
                Titular:\t{conta.cliente.nome}
                Saldo:\tR${conta.saldo:.2f}
                """
        except IndexError:
            raise StopIteration
        finally:
            self._index+=1    
        

#classe Conta
class Conta:
    #inicializador da classe
    def __init__(self,nro_conta,cliente,data):
        #declaração de atributos    
        self._saldo=0
        self._nro_conta=nro_conta
        self._agencia="0001"
        self._cliente=cliente
        self._historico=Historico()
        self.data=data
    
    @classmethod
    def novaConta(cls, cliente, nro_conta,data):
        return cls(nro_conta,cliente,data)
    
    # acesso aos atributos privados
    @property #decorador, podendo usar o método como atributo
    def saldo(self):
        return self._saldo
    
    # acesso aos atributos privados
    @property #decorador, podendo usar o método como atributo
    def nro_conta(self):
        return self._nro_conta
   
    # acesso aos atributos privados
    @property #decorador, podendo usar o método como atributo
    def agencia(self):
        return self._agencia
   
    # acesso aos atributos privados
    @property #decorador, podendo usar o método como atributo
    def cliente(self):
        return self._cliente
  
    # acesso aos atributos privados
    @property #decorador, podendo usar o método como atributo
    def historico(self):
        return self._historico
   
    #método sacar
    def sacar(self, valor):
        saldo=self.saldo
        
        if valor>saldo: #condiçao de verificação de saldo suficiente
            print("\nErro de Operação! Você não tem saldo suficiente.\n")
            print("\nSaldo: R$ {saldo:.2f} \n")
        elif saldo>0: #condição aceite
            self._saldo -= valor #subtrai valor de saque ao saldo
            print("\nSaque realizado com sucesso!!!")
            return True
        else:
            print("\nErro de Operação! O valor informado é inválido.\n")

        return False
  
    #Método de deposito
    def depositar(self, valor):
        if valor > 0: #condiçao de depósito maior que 0
            self._saldo += valor #adiciona valor de depósito ao saldo, desde de que seja aceita a condição anterior
            print("Valor depositado R$ %.2f com sucesso!" % valor + "\n")
        else:
            print("Erro de Operação! O valor informado é inválido.") #resultado da condiçao de depósito inferior a  0
            return False
        return True
    
#classe contaCorrente, herança da classe Conta
class ContaCorrente(Conta):
    #inicializador da classe
    def __init__(self,nro_conta, cliente, data, limite=500, limite_saques=3):
        super().__init__(nro_conta,cliente,data)
        self._limite=limite
        self._limite_saques=limite_saques
    #método sacar - classe conta corrente
    def sacar(self, valor):
        #verificar quantidade de saques realizados (Limite de 3 saques definido pelo problema)
        nro_saques=len(
            [transacao for transacao in self.historico.transacoes if transacao["tipo"]==Saque.__name__]
        )        
        if valor>self._limite: #condiçao de verificação de saldo suficiente
            print("\nErro de Operação! O valor do saque excede o limite DE R$ 500 ao dia.\n")
        elif nro_saques>=self._limite_saques: #condição aceite
            print("\nErro de Operação! O valor do saque excede o número máximo de saques\n")
            return True
        else:
           return super().sacar(valor)

        return False    
    #método str para exibir os dados do cadastro de conta bancaria 
    def __str__(self):
        return f"""
            Data:\t{self.data}
            Agência:\t{self.agencia}
            C/C:\t{self.nro_conta}
            Titular:\t{self.cliente.nome}
        """           
              
#classe historico
class Historico:
    def __init__(self):
        self._transacoes=[]
        
    @property
    def transacoes(self):
        return self._transacoes
    
    def adicionar_transacoes(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor":transacao.valor,
                "data":datetime.now().strftime("%m/%d/%Y - %H:%M:%S")
            }
        )
        
    def gerar_relatorio(self, tipo_transacao):
        for transacao in self._transacoes:
            if tipo_transacao is None or transacao['tipo'].lower()==tipo_transacao.lower():
                yield transacao
         
    #método para filtrar transações realizadas no dia
    def transacoes_dia(self):
        transacoes_do_dia=[]            
        for transacao in self._transacoes:
            data_transacao=transacao["data"].split()                            
            data_atual=datetime.today().strftime("%m/%d/%Y")
            if data_atual==data_transacao[0]:
                transacoes_do_dia.append(transacao)
        return transacoes_do_dia
        
    
#classe cliente
class Cliente:
    #inicializador da classe
    def __init__(self,endereco):
        self.endereco=endereco
        self.contas=[]
    #método executar transação - classe cliente 
    def exec_transacao(self, conta, transacao):
        if len(conta.historico.transacoes_dia()) >= 9:
            print("Limite de transações do dia excedida")
            return
        transacao.registrar(conta)
    #método adicionar conta - classe cliente    
    def add_conta(self,conta):
        self.contas.append(conta)
                
          
# classe Pessoa Fisica        
class PessoaFisica(Cliente):
    #inicializador da classe
    def __init__(self,cpf,nome,dataNascimento,endereco):
        super().__init__(endereco)    
        self.cpf=cpf
        self.nome=nome 
        self.dataNascimento=dataNascimento

#interface transacao
class Transacao(ABC):
    @property
    @abstractclassmethod
    def valor(self):
        pass
    
    @abstractclassmethod
    def registrar(self,conta):
        pass       

#classe Saque
class Saque(Transacao):
    def __init__(self,valor):
        self._valor=valor
        # acesso aos atributos privados

    @property #decorador, podendo usar o método como atributo
    def valor(self):
        return self._valor

    #método registrar transação da classe Saque
    def registrar(self,conta):
        #verificação de requisitos para realização de saque (valor > saldo e 0 / ser cliente cadastrado)
        suces_transacao=conta.sacar(self.valor)
        if suces_transacao:
            conta.historico.adicionar_transacoes(self)

#classe Deposito
class Deposito(Transacao):
    #inicializador da classe
    def __init__(self, valor):
        self._valor = valor

    @property #decorador, podendo usar o método como atributo
    def valor(self):
        return self._valor
    #método registrar transação da classe Depósito
    def registrar(self, conta):
        #verificação de requisitos para realização de depósito (valor > 0 e ser cliente cadastrado)
        sucesso_transacao = conta.depositar(self.valor)
        if sucesso_transacao:
            conta.historico.adicionar_transacoes(self)
                          
# função de decorador (irá indicar as funções executadas como um log de eventos)                          
def log_trasacao(func):
    def envelope(*args, **kwargs):  #indicação de argumentos variaveis sem necessidade de reajustar de acordo com o problema
        resultado=func(*args, **kwargs) #definição de retorno, neste probema só necessitamos do print
        print(f"{datetime.now()}: {func.__name__.upper()}")
        return resultado
    return envelope       

                            
                          
#Definição da tela de MENU Exibida
def menu():
    menu = """
    *************************************
    *   Seja Bem vindo ao Nosso Banco   *
    *                                   *
    *    Informe a opção desejada       *
    *                                   *
    *    [d]  Depositar                 *
    *    [s]  Sacar                     *
    *    [e]  Extrato                   *
    *    [nc] Nova conta                *
    *    [nu] Novo usuário              *
    *    [lc] Listar contas             *
    *    [q]  Sair                      *
    *                                   *
    *                                   *
    *************************************
    =>"""
    #Coleta da opção desejada, com elimitação de espaços 
    return input(textwrap.dedent(menu))

#Definição da tela de MENU EXtrato
def menu_extrato():
    menu_extrato = """
    *************************************
    *   Seja Bem vindo ao Nosso Banco   *
    *                                   *
    *    Informe a opção Extrato        *
    *                                   *
    *    [d]  Depositos                 *
    *    [s]  Sacar                     *
    *    [e]  Todos                     *
    *                                   *
    *                                   *
    *************************************
    =>"""
    #Coleta da opção desejada, com elimitação de espaços 
    return input(textwrap.dedent(menu_extrato))


#função para filtrar clientes cadastrados           
def filtrar_cliente(clientes):
    cpf = input("\nInforme o CPF do cliente:")    
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf==cpf]
    return clientes_filtrados[0] if clientes_filtrados else None

#função para verificar de o cliente possui conta bancária
def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print("Cliente não possui conta!")
        return
    return cliente.contas[0]

#função para depósito
#inserir função de formato de CPF como no desafio do telefone
@log_trasacao # indicação de decorador (log de eventos)
def depositar(clientes):
    os.system("cls")
    print("Função Depósito")
    #cpf = input("Informe o CPF do cliente:")
    cliente=filtrar_cliente(clientes)
    if not cliente:
        print("Cliente não encontrado")
        return
    valor=float(input("Informe o valor do depósito R$:"))
    #verificação dos requisitos para depósito
    transacao=Deposito(valor)
    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    cliente.exec_transacao(conta, transacao)
   
#função sacar
@log_trasacao # indicação de decorador (log de eventos)
def sacar(clientes):
    os.system("cls")
    print("Função Saque")
    #cpf = input("Informe o CPF do cliente:")
    cliente=filtrar_cliente(clientes)
    if not cliente:
        print("Cliente não encontrado")
        return
    valor=float(input("Informe o valor do Saque  R$:"))
    transacao=Saque(valor)
    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    cliente.exec_transacao(conta, transacao)

    
#função exibir extrato    
@log_trasacao # indicação de decorador (log de eventos)
def exibir_extrato(clientes):
    #cpf = input("Informe o CPF do cliente:")
    cliente=filtrar_cliente(clientes)
    if not cliente:
        print("Cliente não encontrado")
        return
    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    os.system("cls")
      
    #definição do menu de extrato
    opcao=menu_extrato()
    if opcao =="d":
        tipo_extrato="deposito"
    elif opcao=="s":
        tipo_extrato="saque"
    else:
        tipo_extrato=None
        
    print(tipo_extrato)
    
    print("\nFunção escolhida : EXTRATO \n")
    print("\n**************** EXTRATO ****************")
    extrato=""
    tem_transacao = False
    for transacao in conta.historico.gerar_relatorio(tipo_extrato):
        tem_transacao   = True
        extrato += f"\n{transacao['tipo']}:\n\tR$ {transacao['valor']:.2f}"   
    if not tem_transacao and  tipo_extrato == "deposito":
        extrato="Não foram realizadas movimentações de Depósito"
    elif not tem_transacao and  tipo_extrato == "Saque":
        extrato="Não foram realizadas movimentações de Saque"
    else:
        extrato="Não foram realizadas movimentações de Saques e Depósitos"

    print(extrato)        
    print("\nSaldo:\tR$%.2f"%conta.saldo)
    print("*******************************************")  
    print(datetime.now().strftime("%m/%d/%Y, %H:%M:%S"))
    

#função de criação de conta bancária (obs Necessário cadastro do cliente antes desse processo)    
@log_trasacao
def criar_conta(nro_conta, clientes, contas):
    os.system("cls")
    #verificação de cliente, caso já esteja cadastrado
    print("Cadastro de Conta Bancaria")
    cliente=filtrar_cliente(clientes)
    if not cliente:
        print("\nCliente encontrado, não é possível criar uma conta bancário sem cadastrar o cliente primeiro!")
        return
    data=datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
    conta = ContaCorrente.novaConta(cliente=cliente,nro_conta=nro_conta,data=data)
    contas.append(conta)
    cliente.contas.append(conta)
    print(conta)
    print("\nConta Bancária criada com sucesso!!!")

#função de listar contas    
def listar_contas(contas):
    os.system("cls")
    print("Função de Lista de Contas Bancaria")
    for conta in ContasInterador(contas):
        print("=" * 100)
        print(textwrap.dedent(str(conta)))
        
#função de criação de clientes
@log_trasacao
def criar_clientes(clientes):
    #verificação de cliente, caso já esteja cadastrado
    cliente=filtrar_cliente(clientes)
    if cliente:
        print("\nCliente encontrado")
        return
    os.system("cls")
    print("Cadastro de Clientes")
    #Informe de dados cadastrais
    cpf = input("\nInforme o CPF do cliente:")
    nome=input("\nInforme o nome do cliente:  ")
    data_nascimento=input("\nInforme a data de nascimento: dd-mm-aaaa:  ")
    endereco=input("\nInforme o endereço (logadouro, nro - bairro - cidade/sigla estado):  ")
    cliente = PessoaFisica(nome=nome, dataNascimento=data_nascimento, cpf=cpf,endereco=endereco)
    clientes.append(cliente)
    print("\nCliente criado com sucesso !!!!!")

#definição do menu na tela
def main():
    clientes=[]
    contas=[]
 
    while True: #Exibição contínua, após execução da opção escolhida. 
        opcao=menu()
        if opcao =="d":
            depositar(clientes)
        elif opcao=="s":
            sacar(clientes)
        elif opcao =="e":
            exibir_extrato(clientes)
        elif opcao =="nu":
            criar_clientes(clientes)
        elif opcao=="nc":
            nro_conta=len(contas)+1
            criar_conta(nro_conta,clientes,contas)
        elif opcao=="lc":
            listar_contas(contas)
        elif opcao=="q":
            os.system("cls")
            break
        else:
            print("\nErro de Operação, por favor selecione operação desejada.\n")   

#Chamada de execução    
main()



