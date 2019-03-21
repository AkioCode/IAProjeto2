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
		
	#jogar no arquivo, de modo organizado, os samples gerados 
	
	
	#TESTE
	#print(samples)
