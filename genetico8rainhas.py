from random import shuffle
import random
import sys
import operator
import time

class Cromossomo:

	def __init__(self, tam):
		self._data = list(range(tam))
		self._taxaMutacao = random.random()
		shuffle(self._data)

	def getGene(self, idx):
		return self._data[idx]

	def setData(self, data):
		self._data = data

	def setTaxaMutacao(self, taxaMutacao):
		self._taxaMutacao = taxaMutacao

	def setGene(self, idx, valor):
		self._data[idx] = valor

	def getData(self):
		return self._data

	def __getitem__(self, idx):
		return self._data[idx]

	def size(self):
		return len(self._data)

	def __repr__(self):
		return str(self._data)

	def _boundsOK(self, i, j):
		if (i < self.size() and i >= 0 and j < self.size() and j >= 0):
			return True
		return False


	# numero de colisoes
	def getAvaliacao(self):
		colisoes = 0

		for i in range(self.size()):
			# diagonal principal superior
			for l in range(self.size()):
				# Diag Sup or Diag Inf or Diga Inv Sup or Diag Inv Inf
				if ( ( self._boundsOK( i - (l + 1), self._data[i] + (l + 1) ) and self._data[i - (l + 1)] == self._data[i] + (l + 1) ) or
				( self._boundsOK( i + (l + 1), self._data[i] - (l + 1) ) and self._data[i + (l + 1)] == self._data[i] - (l + 1) ) or
				( self._boundsOK( i - (l + 1), self._data[i] - (l + 1) ) and self._data[i - (l + 1)] == self._data[i] - (l + 1) ) or
				( self._boundsOK( i + (l + 1), self._data[i] + (l + 1) ) and self._data[i + (l + 1)] == self._data[i] + (l + 1) ) ):
					colisoes+= 1
		return colisoes

	def cruzamento(self, outro):
		# olhar funcao de cruzamento do PCV-PQ

		pontoFlutuante = random.randint(1, self.size() - 1)

		f1 = self._data[0:pontoFlutuante]
		f2 = outro[0:pontoFlutuante]

		verif1 = [0] * self.size()
		verif2 = [0] * self.size()

		for i in range(pontoFlutuante):
			verif1[f1[i]] = 1
			verif2[f2[i]] = 1

		for i in range(self.size()):
			# if outro[i] not in f1:
			# 	f1.append(outro[i])
			# if self._data[i] not in f2:
			# 	f2.append(self._data[i])
			if verif1[outro[i]] == 0:
				f1.append(outro[i])
			if verif2[self._data[i]] == 0:
				f2.append(self._data[i])

		x = Cromossomo(self.size())
		x.setData(f1)
		x.setTaxaMutacao(random.random())

		y = Cromossomo(self.size())
		y.setData(f2)
		y.setTaxaMutacao(random.random())

		return [x, y]

	def mutacao(self, taxaMutacao):
		if taxaMutacao <= self._taxaMutacao:
			idx1 = random.randint(0, self.size() - 1)
			idx2 = random.randint(0, self.size() - 1)

			aux = self._data[idx1]
			self._data[idx1] = self._data[idx2]
			self._data[idx2] = aux

class Genetico:

	# popSize - tamanho da populacao
	# txMutacao - taxa de mutacao (0 a 1)
	# porcentCruzamento - procentagem da populacao para fazer cruzamento (0 a 100)
	# geracoes - numero de geracoes

	def __init__(self, popSize, txMutacao, porcentCruzamento, geracoes, tamanhoTabuleiro):
		#parametros
		self._populacao = []
		self._popSize = popSize
		self._txMutacao = txMutacao
		self._geracoes = 0
		self._cruzamentos = int ( (porcentCruzamento/100.0) * self._popSize ) // 2
		self._tamanhoTabuleiro = tamanhoTabuleiro

	def run(self):

		self.gerarPopulacaoInicial()
		self._populacao.sort(key=operator.methodcaller("getAvaliacao"), reverse=False)

		while self._geracoes < geracoes :
			#print "POP da iteracao: ", self._geracoes
			#print self.printPop()
			self._geracoes+= 1
			# print (self.aptdMedia())
			# print 'geracao ', self._geracoes
			for i in range(self._cruzamentos/2):

				# indA = self.roleta()
				# indB = self.roleta()
				indA = self._populacao[i]
				indB = self._populacao[i + 1]

				#Reproducao
				filhos = indA.cruzamento(indB)
				filhos[0].mutacao(self._txMutacao)
				filhos[1].mutacao(self._txMutacao)

				self._populacao.append(filhos[0])
				self._populacao.append(filhos[1])

			self.selecao()
			if self._populacao[0].getAvaliacao() == 0:
				break
			#print "aqui2"

		#return self.getSolucaoDeElite()
		#print self.printPop()
		return self._populacao[0]

	def getPopulacao(self):
		return self._populacao

	def gerarPopulacaoInicial(self):
		for i in range(0, self._popSize + 1):
			self._populacao.append(Cromossomo(self._tamanhoTabuleiro))

	def roleta(self):
		# x = soteira num 0 - soma
		# subtrai dos x os valores dos individuos ate que x assuma um valor <=0, there is the guy
		soma = 0.0
		for i in range(len(self._populacao)):
			if self._populacao[i].getAvaliacao() > 0:
				soma+= 1.0/self._populacao[i].getAvaliacao()
			else:
				soma+= 1;
		x = random.random() * soma

		i = 0
		while x >= 0 and i < len(self._populacao):
			if self._populacao[i].getAvaliacao() > 0:
				x-= 1.0/self._populacao[i].getAvaliacao()
			else:
				x-= 1.0
			i+= 1
		return self._populacao[i - 1]


	def elite(self):
		#print "Pop anterior: "
		#print self.printPop()
		self._populacao.sort(key=operator.methodcaller("getAvaliacao"), reverse=False)
		self._populacao = self._populacao[0:self._popSize + 1]
		#print "Pop pos:"
		#print self.printPop()
		return self._populacao

	def getSolucaoDeElite(self):
		bestSol = sys.maxint
		for i in range(len(self._populacao)):
			# print self._populacao[i] , " --  ", self._populacao[i].getAvaliacao()
			if self._populacao[i].getAvaliacao() < bestSol:
				bestSol = self._populacao[i]

		return bestSol


	def selecao(self):
		opt = 1
		if opt == 0:
			newPop = []
			while len(newPop) != self._popSize:
				newPop.append(self.roleta())
			self._populacao = newPop
		else:
			return self.elite()

	def printPop(self):
		string = ''
		for i in range(0, len(self._populacao)):
			string+= str(i) + '-' + str(self._populacao[i]) + ' - ' + str(self._populacao[i].getAvaliacao()) + '\n'
		return string

	def aptdMedia(self):
		md = 0;
		for i in range(0, len(self._populacao)):
			md+= self._populacao[i].getAvaliacao()
		#print "soma:", md
		#print "len:", len(self._populacao)
		md/=(len(self._populacao) * 1.0)
		#print "media: ", md
		return md

# popSize - tamanho da populacao
# txMutacao - taxa de mutacao (0 a 1)
# porcentCruzamento - procentagem da populacao para fazer cruzamento (0 a 100)
# geracoes - numero de geracoes

# pyhton genetico8rainhas.py 200 0.5 50 500
# print sys.argv
popSize = int(sys.argv[1])
txMutacao = float(sys.argv[2])
porcentCruzamento = int(sys.argv[3])
geracoes = int(sys.argv[4])
tamanhoTabuleiro = 8

#popSize = 200
#txMutacao = 0.5
#porcentCruzamento = 50
#geracoes = 500
#tamanhoTabuleiro = 8
melhor_tempo = sys.float_info.max
pior_tempo = sys.float_info.min
tempo_medio = 0.0
num_sol_val = 0
mediaAptdMedia = 0.0
RODADAS = 10
melhorApt = sys.float_info.max

for i in range(0, RODADAS):
	#start_time = time.time()
	g = Genetico(popSize, txMutacao, porcentCruzamento, geracoes, tamanhoTabuleiro)
	sol = g.run()
	#print g.aptdMedia()
	mediaAptdMedia+= g.aptdMedia()
	#time_atual = (time.time() - start_time)
	#tempo_medio+= time_atual
	#if time_atual < melhor_tempo:
	#	melhor_tempo = time_atual
	#if time_atual > pior_tempo:
	#	pior_tempo = time_atual
	#if sol.getAvaliacao() == 0:
	#	num_sol_val+= 1
	#if g.aptdMedia() < melhorApt:
	#	melhorApt = g.aptdMedia()


#tempo_medio/=RODADAS
mediaAptdMedia/=RODADAS
#print("%.3f, %.3f, %.3f, %.3f, %.3f, %i" %(melhor_tempo, pior_tempo, tempo_medio, mediaAptdMedia, melhorApt, num_sol_val))
print ("%.3f" % mediaAptdMedia)
#print melhor_tempo, ", ", pior_tempo, ", ", tempo_medio, ", ", num_sol_val
#print ("%.3f" % total_time)

#print("%s" % (time.time() - start_time))

#print sol, sol.getAvaliacao()
