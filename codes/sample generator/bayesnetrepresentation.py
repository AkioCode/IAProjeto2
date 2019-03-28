#####################################################
# Chest Clinic Bayes net representatin  library     # 
#####################################################

#Ordem seguida pelo prior: Visitou Asia(Sim,Nao); Fuma(Sim,Nao); Tuberculose(Sim,Nao); Cancer Pulmao(Sim,Nao); Bronquite(Sim,Nao); Tuberculose ou Cancer(VERDADE, FALSO); RaioX(Normal,Abnormal); Dispneia(Sim,Nao); -> Nó(1,0)

#Definindo quais dos nós será a classe para o aprendizado
classe = 7

#Relacao de dependência entre os nós (ordem de prioridade):
d = []
d.append([])  	# 0:Visit Asia
d.append([])  	# 1:Fuma
d.append([0]) 	# 2:Turbeculos <- Visit Asia 
d.append([1]) 	# 3:Cancer Pulmao <- Fuma
d.append([1]) 	# 4:Bronquite <- Fuma
d.append([2, 3])# 5:Turbe. ou Cancer. <- Turbe., Cancer.
d.append([5]) 	# 6:RaioX <- 5
d.append([5, 4])# 7:Dispinea <- Tuber. ou Cancer. , Bronquite

#probabilidades positivas para os 8 nós (inteiro de 1 a 100)
#A probabilidade será recursiva para dentro da tupla de acordo com a quantidade de dependências sendo primeiro valor a negacao da condicao
# ex: uma dependência, p[k] = ((-, +)), k dependendo de j então quando j for - pega-se p[k][0], e vice versa.
# para duas dependências p[k] = ((--, -+), (+-, ++))


# Probabilidades
p = [0,1,2,3,4,5,6,7] # inicializando 8 nós
p[0] = 1
p[1] = 50
p[2] = (1, 5) 
p[3] = (1, 10)
p[4] = (30, 60)
p[5] = ((0, 100), (100, 100))
p[6] = (95, 2)
p[7] = ((10, 80), (70, 90))

def getDepencies():
	return d

def getProbabilities():
	return p

def getClass():
	return classe
