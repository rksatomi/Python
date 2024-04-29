# Implementação de Sistema Bancário utilizando POO em Python

#importação de bibliotecas ABC e e data/time
from abc import ABC, abstractclassmethod
from datetime import datetime

#classe Conta
class Conta:
    def __init__(self,nro_conta,cliente):
        #declaração de atributos privados
        self.__saldo=0
        self.__nro_conta=nro_conta
        self.__agencia="0001"
        self._cliente=cliente
        self.__historico=Historico()
    
    @classmethod
    def novaConta(cls, cliente, nro_conta):
        return cls(nro_conta,cliente)

    # acesso aos atributos privados
    @property
    def saldo(self):
        return self._saldo
    # acesso aos atributos privados
    @property
    def nro_conta(self):
        return self._nro_conta
    # acesso aos atributos privados
    @property
    def agencia(self):
        return self._agencia
    # acesso aos atributos privados
    @property
    def cliente(self):
        return self._cliente
    # acesso aos atributos privados
    @property
    def historico(self):
        return self._historico
    
    def sacar(self, valor):
        saldo=self.saldo
        
        if saldo<valor: #condiçao de verificação de saldo suficiente
            print("\nErro de Operação! Você não tem saldo suficiente.\n")
            print("\nSaldo: R$ {saldo:.2f} \n")
        elif saldo>0: #condição aceite
            print("\nErro de Operação! O valor do saque excede o limite DE R$ 500 ao dia.\n")
            return True
        else:
            print("\nErro de Operação! O valor informado é inválido.\n")

        return False

    #função de deposito
    def depositar (self,valor):
        if valor > 0: #condiçao de depósito maior que 0
            self._saldo += valor #adiciona valor de depósito ao saldo, desde de que seja aceita a condição anterior
            print("Valor depositado R$ %.2f com sucesso!" % valor + "\n")
        else:
            print("Erro de Operação! O valor informado é inválido.") #resultado da condiçao de depósito inferior a  0
            return False
        return True

   
    
    
#classe contaCorrente, herança da classe Conta
class ContaCorrente(Conta):
    def __init__(self,nro_conta, cliente, limite=500, limite_saques=3):
        super().__init__(nro_conta,cliente)
        self._limite=limite
        self._limite_saques=limite_saques
    
    def sacar(self, valor):
        nro_saques=len(
            [transacao for transacao in self.historico.trasacoes if transacao["tipo"]==Saque.__name__]
        )
        
        
        if self._limite>valor: #condiçao de verificação de saldo suficiente
            print("\nErro de Operação! O valor do saque excede o limite DE R$ 500 ao dia.\n")
        elif nro_saques>=self.limite_saques: #condição aceite
            print("\nErro de Operação! O valor do saque excede o número máximo de saques\n")
            return True
        else:
           return super().sacar(valor)

        return False    
    
    def __str__(self):
        return f""""\
            Agência:\t{self.agencia}
            C/C:\t{self.nro_conta}
            Titular:\t{self.cliente.nome}
        """        
         
         

#classe historico
class Historico:
    def __init__(self):
        self._trasacoes=[]
        
    @property
    def transacoes(self):
        return self.transacoes
    
    def adicionar_transacoes(self, transacao):
        self._trasacoes.append(
            {
                "tipo":Transacao.__class__.__name__,
                "valor":Transacao.valor,
                "data":datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
            }
        )    

#classe cliente
class Cliente:
    def __init__(self,endereco):
        self.endereco=endereco
        self.contas=[]
    
    def exec_trasancao(self, conta,transacao):
        transacao.registrar(conta)    
        
    def add_conta(self,conta):
        self.contas.append(conta)
        
# classe Pessoa Fisica        
class PessoaFisica(Cliente):
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
    def registrar(self,):
        pass       

#classe Saque
class Saque(Transacao):
    def __init__(self,valor):
        self._valor=valor
        # acesso aos atributos privados

    @property
    def valor(self):
        return self._valor
    
    def registrar(self,conta):
        suces_transacao=conta.sacar(self.valor)
        if suces_transacao:
            conta.historico.adicionar_transacoes(self)

#classe Deposito
class Deposito(Transacao):
    def __init__(self,valor):
        
        @property
        def valor(self):
            return self._valor
        
        def registrar(self, conta):
            suces_transacao=conta.depositar(self.valor)
            if suces_transacao:
                conta.historico.adicionar_transacao(self)
            
            
            