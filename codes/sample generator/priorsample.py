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
	
	#Conta o numero de vezes q cada variavel assume uma confirmação
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
    
    print("Visitou Asia->", contAsia ," de ", 10)
    print("Fuma->", contFuma ," de ", 10)
    print("Tuberculose->", contTuber ," de ", 10)
    print("Cancer Pulmao->", contCan ," de ", 10)
    print("Bronquite->", contBronq ," de ", 10)
    print("Tuberculose ou Cancer->", contOU ," de ", 10)
    print("RaioX->", contRaio ," de ", 10)
    print("Dispneia->", contDisp ," de ", 10)
    
    #escreve uma amostra por linha no arquivo
    arquivo = open('TESTE.txt', 'w')
     
    for i in range(len(samples)) :
        linha = str(samples[i]) + "\n"
        arquivo.write(linha)
   
    arquivo.close()
