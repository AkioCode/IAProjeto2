#####################################################
# Prior Sample Algorithm						 	# 
#####################################################

import numpy as np
import sys
import bayesnetrepresentation as bnr
from random import randint


def generateSample(d, p):
	# x é o próximo sample
	x = [-1 for _ in range(len(p))] #-1 é quando não foi colocado valor algum ainda, 1 é a afirmação, 0 negacao
	for i in range(len(x)):
		prob = p[i]
		for noD in d[i]:
			prob = prob[x[noD]]
		#prob positiva atualizada do no i dado as denpendencias d[i]
		randNum = randint(0, 100)
		if randNum <= prob:
			x[i] = 1
		else:
			x[i] = 0
	
	return x

def swapPosition(samples, index):
	##### Colocar código swap aqui para todos os items de samples
	return samples
	
def mostrarPorcentagens(samples):
	
	contAsia, contFuma, contTuber, contCan, contBronq, contOU, contRaio, contDisp = 0, 0, 0, 0, 0, 0, 0, 0
	
	for i in range(len(samples)):
		if samples[i][0] == 1:
			contAsia += 1
		if samples[i][1] == 1:
			contFuma += 1
		if samples[i][2] == 1:
			contTuber += 1
		if samples[i][3] == 1:
			contCan += 1
		if samples[i][4] == 1:
			contBronq += 1
		if samples[i][5] == 1:
			contOU += 1
		if samples[i][6] == 1:
			contRaio += 1
		if samples[i][7] == 1:
			contDisp += 1

    #esses prints eram so pra testes
	print("Visitou Asia --------->","%.0f" %((contAsia/len(samples))*100),"% das amostras")
	print("Fuma ----------------->","%.0f" %((contFuma/len(samples))*100),"% das amostras")
	print("Tuberculose ---------->","%.0f" %((contTuber/len(samples))*100),"% das amostras")
	print("Cancer Pulmao -------->","%.0f" %((contCan/len(samples))*100),"% das amostras")
	print("Bronquite ------------>","%.0f" %((contBronq/len(samples))*100),"% das amostras", 10)
	print("Tuberculose ou Cancer->","%.0f" %((contOU/len(samples))*100),"% das amostras", 10)
	print("RaioX ---------------->","%.0f" %((contRaio/len(samples))*100),"% das amostras")
	print("Dispneia ------------->","%.0f" %((contDisp/len(samples))*100),"% das amostras")

def salvarSamples(samples):
	arquivo = open('samplesTESTANDO.txt', 'w')
	for x in samples:
		linha = '';
		for val in x:
			linha += str(val) + ","
		linha = linha[:-1]
		linha += "\n"
		arquivo.write(linha)
	arquivo.close()

#### main program ####
### Chamada do tipo: python3 priorsample.py 1000
###												: onde 1000 é a quantidade de exemplos que será gerada
if __name__ == '__main__':
	numberOfSample = int(sys.argv[1])
	d = bnr.getDepencies()
	p = bnr.getProbabilities()
	classIndex = bnr.getClass()
	
	samples = []
	while(numberOfSample > 0):
		samples.append(generateSample(d, p))
		numberOfSample-=1
	
	if len(samples[0])-1 != classIndex:
		#troca ultima posicao de cada sample pela possicao q esta a classe (classIndex)
		samples = swapPosition(samples, classIndex)	
		
	#Mostrando porcentagem das caracteristicas geradas para comparar com os dados reais
	mostrarPorcentagens(samples)
	
	#jogar no arquivo, de modo organizado, os samples gerados 
	salvarSamples(samples)
