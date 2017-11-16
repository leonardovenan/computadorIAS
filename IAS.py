# -*- coding: utf-8 -*-
"""
Created on Mon Set 24 15:51:37 2017

@author: Leonardo Venancio
"""

def sm_para_dec(num):
    #primeiro verificando se tal numeor eh binario ou nao	
    num = str(num)    
    for x in num:
        if x != '0' and x != '1':
            print("Nao eh um numero binario!")
            return None
            break
    if len(num)!= 40:
        print("Tamanho de bits invalido para Sinal-Magnitude!")
        return None
    else:
        n=0
        res = 0
        signal = int(num[0])
        num = num[1:]
        for x in num[::-1]:
            res += int(x)*2**n
            n += 1
        if signal == 0:
            return str(res)
        else:
            return str(-res)

def ad_para_dec(num):
   #primeiro verificando se tal numeor eh binario ou nao    
    num = str(num)    
    for x in num:
        if x != '0' and x != '1':
            print("Nao eh um numero binario!")
            return None
            break
    if len(num)!= 12:
        print("Tamanho de bits invalido para endereco!")
        return None
    else:
        n=0
        res = 0
        num = num[1:]
        for x in num[::-1]:
            res += int(x)*2**n
            n += 1
        return res        

def dec_para_ad(num):
    #Recebe um decimal e retorna uma string no formato sinal-magnitude
    num = int(num)
    remainder = []
    while num > 0:
        remainder.append(num%2)
        num = num//2
    res = ''
    for x in reversed(remainder):
        res += str(x)        
    return '0'*(12-len(res))+res

def dec_para_sm(num):
    #Recebe um decimal e retorna uma string no formato sinal-magnitude
    num = int(num)
    remainder = []
    while num > 0:
        remainder.append(num%2)
        num = num//2
    res = ''
    for x in reversed(remainder):
        res += str(x)        
    return '0'*(40-len(res))+res

class MBR():
    def __init__(self):
        self.dado = None
        
    def getDado(self):
        return self.dado
        
    def setDado(self, novoDado):
        self.dado = novoDado

class IR():
    def __init__(self):
        self.dado = None

    def getDado(self):
        return self.dado

    def setDado(self, dado):
        self.dado = dado
        
class PC():
    def __init__(self, MEM):
        self.MEM = MEM
        self.endereco = '000000000000'

    def getEndereco(self):
        return self.endereco

    def setEndereco(self, endereco):
        self.endereco = endereco

    def proximo(self):
        self.endereco = dec_para_ad(ad_para_dec(self.endereco)+1)

class MEM():
    def __init__(self):
        self.palavras = []
        self.setPalavras()

    def setPalavras(self):
        with open('MEM.txt', 'r') as palavras:
            self.palavras = [x[:40] for x in palavras.read().splitlines()]

    def leitura(self, endereco):
        return self.palavras[ad_para_dec(endereco)]

    def escrita(self, endereco, dado):
        self.palavras[ad_para_dec(endereco)] = dado

class MAR():

    def __init__(self, pc, MEM, mbr):
        self.MEM = MEM
        self.pc = pc
        self.mbr = mbr
        self.endereco = pc.getEndereco()

    def setMbr(self):
        mbr.setDado(MEM.leitura(self.endereco))

    def atualizar(self):
        self.endereco = pc.getEndereco()
        
    def setEndereco(self, endereco):
        self.endereco = endereco

    def getEndereco(self):
        return self.endereco

class MQ():
    def __init__ (self):
        self.dado = '0'*39 + '1'

    def setDado(self, dado):
        self.dado = dado
        
    def getDado(self):
        return self.dado

    def multiplicar(self, dado):
        self.dado = dec_para_sm(int(sm_para_dec(dado))*int(sm_para_dec(self.dado)))

    def quociente(self, dado):
        self.dado = dec_para_sm(int(sm_para_dec(self.dado))//int(sm_para_dec(dado)))

class AC():
    def __init__ (self):
        self.dado = '0'*40

    def setDado(self, dado):
        self.dado = dado

    def getDado(self):
        return self.dado

    def adicionar(self, dado):
        self.dado = dec_para_sm(int(sm_para_dec(dado))+int(sm_para_dec(self.dado)))

    def subtrair(self, dado):
        self.dado = dec_para_sm(int(sm_para_dec(dado))-int(sm_para_dec(self.dado)))

    def resto(self, dado):
        self.dado = dec_para_sm(int(sm_para_dec(self.dado))%int(sm_para_dec(dado)))
        
class IBR():
    def __init__(self):
        self.dado = None

    def setDado(self, dado):
        self.dado = dado

    def getDado(self):
        return self.dado

class CPU():
    def __init__ (self, MEM, pc, mbr, mar, ibr, ir, mq, ac):
        self.MEM = MEM
        self.pc = pc
        self.mbr = mbr
        self.mar = mar
        self.ibr = ibr
        self.ir = ir
        self.mq = mq
        self.ac = ac
        self.stop = False

    def pararfunc(self):
        while not self.stop:            
            if self.ibr.getDado() == None:                
                self.mar.atualizar()
                self.mar.setMbr()
                self.ibr.setDado(self.mbr.getDado()[20:])
                self.ir.setDado(self.mbr.getDado()[0:8])
                self.mar.setEndereco(self.mbr.getDado()[8:20])
                self.pc.proximo()
                self.executar()
            else:
                self.ir.setDado(self.ibr.getDado()[:8])
                self.mar.setEndereco(self.ibr.getDado()[8:])
                self.ibr.setDado(None)
                self.executar()            
    #opcodes
    def executar(self):
        atual = self.ir.getDado()
        #Carregar MQ - Transferencia de conteúdo de MQ para AC        
        if atual == '00001010': 
            self.ac.setDado(self.mq.getDado())
        #Carregar M(X) - Armazenamento M(X) em AC    
        elif atual == '00000001': 
            self.ac.setDado(self.MEM.leitura(self.mar.getEndereco()))
        #Carregar MQ,M(X) - Transferencia de conteúdo do local de memória X para MQ    
        elif atual == '00001001': 
            self.mq.setDado(self.MEM.leitura(self.mar.getEndereco()))
        #Separar M(X) - Armazenamento de conteúdo de AC no endereço X da memória     
        elif atual == '00100001': 
            self.MEM.escrita(self.mar.getEndereco(), self.ac.getDado())  
        #Carregar - M(X) - Armazenamento de -M(X) em AC    
        elif atual == '00000010': 
            dado = self.MEM.leitura(self.mar.getEndereco())            
            if dado.startswith('0'):
                dado = dado.replace('0','1',1)
            else:
                dado = dado.replace('1','0',1)            
            self.ac.setDado(dado)
        #Carregar -|M(X)| - Armazenamento -|M(X)| em AC    
        elif atual == '00000100': 
            dado = self.MEM.leitura(self.mar.getEndereco())            
            if dado.startswith('0'):
                dado = dado.replace('0','1',1)
            self.ac.setDado(dado)
        #JUMP M(X,0:19) - Saltar para a instrução da esquerda da palavra em M(X)    
        elif atual == '00001101': 
            self.ibr.setDado(None)            
            self.pc.setEndereco(self.mar.getEndereco())
        #JUMP M(X,20:39) - Saltar para a instrução da direita da palavra em M(X)    
        elif atual == '00001110': 
            palavra = self.MEM.leitura(self.mar.getEndereco())
            self.ibr.setDado(palavra[20:])
            self.pc.setEndereco(dec_para_ad(int(ad_para_dec(self.mar.getEndereco()) + 1)))
        #Carregar |M(X)| - Armazenamento o valor absoluto de M(X) em AC     
        elif atual == '00000011': 
            dado = self.MEM.leitura(self.mar.getEndereco())            
            if dado.startswith('1'):
                dado = dado.replace('1','0',1)
            self.ac.setDado(dado)
        #JUMP+M(X,20:39) - Se AC >= 0: Saltar para a instrução da direita da palavra em M(X)    
        elif atual == '0001000': 
            dado_ac = self.ac.getDado()
            if dado_ac.startswith('0'):
                palavra = self.MEM.leitura(self.mar.getEndereco())
                self.ibr.setDado(palavra[20:])
                self.pc.setEndereco(dec_para_ad(int(ad_para_dec(self.mar.getEndereco()) + 1)))       
        #ADD M(X) - Somar o valor em M(X) com o valor em AC e armazena em AC        
        elif atual == '00000101': 
            self.ac.adicionar(self.MEM.leitura(self.mar.getEndereco()))
        #ADD |M(X)| - Somar o valor absoluto de M(X) com o valor em AC e armazena em AC        
        elif atual == '00000111': 
            dado = self.MEM.leitura(self.mar.getEndereco())
            if dado.startswith('1'):
                dado = dado.replace('1','0',1)
            self.ac.adicionar(dado)
        #JUMP+M(X,0:19) - Se AC >= 0: Saltar para a instrução da esquerda da palavra em M(X)    
        elif atual == '00001111': 
            dado_ac = self.ac.getDado()
            if dado_ac.startswith('0'):
                self.ibr.setDado(None)            
                self.pc.setEndereco(self.mar.getEndereco())
        #SUB M(X) - Subtrai o valor em M(X) do valor presente em AC e armazena em Ac        
        elif atual == '00000110': 
            self.ac.subtrair(self.MEM.leitura(self.mar.getEndereco()))        
        #SUB |M(X)| - Subtrai o valor absoluto de M(X) do valor em AC e armazena em AC    
        elif atual == '00001000': 
            dado = self.MEM.leitura(self.mar.getEndereco())
            if dado.startswith('1'):
                dado = dado.replace('1','0',1)
            self.ac.subtrair(dado)
        #MUL M(X) - Multiplica o valor em M(X) pelo valor em MQ e armazena em AC e em MQ    
        elif atual == '00001011': 
            self.mq.multiplicar(self.MEM.leitura(self.mar.getEndereco()))
            self.ac.setDado(self.mq.getDado())
        #DIV M(X) Divide o valor em AC pelo valor de M(X). Armazena o quociente em MQ e o resto em AC    
        elif atual == '00001100': 
            self.mq.setDado(self.ac.getDado())
            self.mq.quociente(self.MEM.leitura(self.mar.getEndereco()))
            self.ac.resto(self.MEM.leitura(self.mar.getEndereco()))
        #LSH (Left Shift) - Desloca os bits do AC para a esquerda. Equivale a multiplicar AC por 2    
        elif atual == '00010100': 
            dado_ac = self.ac.getDado()
            if dado_ac.startswith('1'):
                meta = dado_ac[2:] + '0'
                novo_dado = '1' + meta
                self.ac.setDado(novo_dado)
            else:
                meta = dado_ac[2:] + '0'
                novo_dado = '0' + meta
                self.ac.setDado(novo_dado)
        #RSH (Right Shift) - Desloca os bits do AC para a direita. Equivale a dividir AC por 2        
        elif atual == '00010101': 
            dado_ac = self.ac.getDado()
            if dado_ac.startswith('1'):
                meta = dado_ac[1:len(dado_ac)]
                novo_dado = '10' + meta
                self.ac.setDado(novo_dado)
            else:
                meta = dado_ac[1:len(dado_ac)]
                novo_dado = '00' + meta
                self.ac.setDado(novo_dado)
        #STOP M(X,8:19) - Move os 12 bits à direita de AC para o campo endereço da instrução da esquerda da palavra em M(X)        
        elif atual == '00010010': 
            palavra = self.MEM.leitura(self.mar.getEndereco())
            novo_end = self.ac.getDado()[:27:-1]
            nova_palavra = palavra[:8] + novo_end + palavra[20:]
            self.MEM.escrita(self.mar.getEndereco(), nova_palavra)
        #STOP M(X, 28:39) - Move os 12 bits à direita de AC para o campo endereço da instrução da direita da palavra em M(X)                
        elif atual == '00010011': 
            palavra = self.MEM.leitura(self.mar.getEndereco())
            novo_end = self.ac.getDado()[:27:-1]
            nova_palavra = palavra[:28] + novo_end
            self.MEM.escrita(self.mar.getEndereco(), nova_palavra)            
        #Condição de parada     
        elif atual == '00000000': 
            self.stop = True

mbr = MBR()
MEM = MEM()
pc = PC(MEM)
mar = MAR(pc, MEM, mbr)
ac = AC()
mq = MQ()
ibr = IBR()
ir = IR()
cpu = CPU(MEM, pc, mbr, mar, ibr, ir, mq, ac)
cpu.pararfunc()
