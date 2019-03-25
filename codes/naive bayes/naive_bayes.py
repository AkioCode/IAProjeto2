# -*- coding: utf-8 -*-
from collections import defaultdict
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score
import math
from math import pi
from math import e
import random
import csv
import re
import numpy as np

#Implementação de naive bayes from stratch utilizando modelo Gaussiano   
class GaussNB_Stratch:
    def __init__(self):
        pass

    def loadCsv(self, filename):
        """
        :param filename: string com nome do arquivo csv
        :return:
        Cada string convertido em float
        """
        lines = csv.reader(open(filename, "r"))
        dataset = list(lines)
        for i in range(len(dataset)):
            dataset[i] = [float(x) for x in dataset[i]]
        return dataset

    def splitDataset(self, dataset, splitRatio):
        """
        :param dataset: conjunto de amostras
        :param splitRatio: porcentagem de linhas que irão ser usadas parar treinar
        :return:
        Dados para treinamento de acordo com sliptRatio e usa o resto como teste (3)
        """
        trainSize = int(len(dataset) * splitRatio)
        trainSet = []
        copy = list(dataset)
        while len(trainSet) < trainSize:
            index = random.randrange(len(copy))
            trainSet.append(copy.pop(index))
        return [np.asarray(trainSet), np.asarray(copy)]

    def separateByClass(self, dataset):
        """
        :param dataset: Conjunto de amostras (training set)
        :return:
        Cada classe mapeada em uma lista e suas características (features)
        """
        targetMap = defaultdict(list)
        for i in range(len(dataset)):
            features = dataset[i]
            if (features[-1] not in targetMap):
                targetMap[features[-1]] = []
            # última coluna é a coluna classe
            targetMap[features[-1]].append(features[:-1])
        return dict(targetMap)

    def mean(self, numbers):
        """
        :param numbers: lista de números
        :return:
        A média entre os números
        """
        result = sum(numbers) / float(len(numbers))
        return result

    def stdev(self, numbers):
        """
        :param numbers: lista de números
        :return:
        O desvio padrão entre a lista de números
        """
        avg = self.mean(numbers)
        variance = sum([pow(x-avg, 2) for x in numbers])/float(len(numbers)-1)
        return math.sqrt(variance)

    def summarize(self, testSet):
        """
        :param testSet: Conjunto de amostras teste
        :return:
        Nova lista contendo a média e desvio padrão de cada feature
        """
        for feature in zip(*testSet):
            yield {
                'stdev': self.stdev(feature),
                'mean': self.mean(feature)
            }

    def piorProb(self, group, target, data):
        """
        :return:
        Probabilidade a priori de cada classe 
        """
        total = float(len(data))
        result = len(group[target]) / total
        return result

    def train(self, trainList):
        """
        :param trainList: Conjunto de amostras para treinamento
        :return:
        Para cada classe:
            1. piorProb: probabilidade da classe
            2. resumo (summary): lista de {'mean': 0.0, 'stdev': 0.0}
        """
        group = self.separateByClass(trainList)
        self.summaries = {}
        for target, features in group.items():
            self.summaries[target] = {
                'piorProb': self.piorProb(group, target, trainList),
                'summary': [i for i in self.summarize(features)],
            }
        return self.summaries

    def NPDF(self, x, mean, stdev):
        """
        :param x: variável
        :param mean: valor esperado ou média de M amostras (µ)
        :param stdev: desvio padrão (σ)
        :return: função de densidade de probabilidade normal (gauss)
        N(x; µ, σ) = (1 / 2πσ) * (e ^ (x–µ)^2/-2σ^2
        """
        variance = stdev ** 2
        exp_squared_diff = (x - mean) ** 2
        exp_power = -exp_squared_diff / (2 * variance)
        exponent = e ** exp_power
        denominator = ((2 * pi) ** .5) * stdev
        normal_prob = exponent / denominator
        return normal_prob

    def MPDF(self, jointProbabilities):
        """
        :param jointProbabilities: conjunto de probabilidades conjuntas para cada feature
        :return:
        função densidade de probabilidade marginal
        """
        return sum(jointProbabilities.values())

    def jointProbabilities(self, testRow):
        """
        :param testRow: instância do conjunto de amostras teste
        :return:
        Produto de todas as NPDF e probabilidades a priori de cada feature
        """
        jointProbs = {}
        for target, features in self.summaries.items():
            totalFeatures = len(features['summary'])
            likelihood = 1
            for index in range(totalFeatures):
                feature = testRow[index]
                mean = features['summary'][index]['mean']
                stdev = features['summary'][index]['stdev']
                normal_prob = self.NPDF(feature, mean, stdev)
                likelihood *= normal_prob
            piorProb = features['piorProb']
            jointProbs[target] = piorProb * likelihood
        return jointProbs

    def posterioriProbabilities(self, testRow):
        """
        :param testRow: instância do conjunto de amostras teste
        :return:
        um dicionário com as probabilidades posterioris da classe

            Para cada variável em testRow:
                1. Calcular a probabilidade a priori usando a NPDF N(x; µ, σ). eg = P(caracteristica | classe)
                2. Calcular a prob pegando o produto da prob a prior e as NPDFs
                3. Multiplicar a prob pela prob a prior para calcular as probs conjuntas.
        """
        posterioriProbs = {}
        jointProbabilities = self.jointProbabilities(testRow)
        marginalProb = self.MPDF(jointProbabilities)
        for target, jointProb in jointProbabilities.items():
            posterioriProbs[target] = jointProb / marginalProb
        return posterioriProbs

    def getMap(self, testRow):
        """
        :param testRow: instância do conjunto de amostras teste
        :return:
        Uma classe com a maior/melhor probabilidade a posterior
        """
        posterioriProbs = self.posterioriProbabilities(testRow)
        mapProb = max(posterioriProbs, key=posterioriProbs.get)
        return mapProb

    def predict(self, testSet):
        """
        :param testSet: instância do conjunto de amostras teste
        :return:
        Lista de predições para a instância
        """
        mapProbs = []
        for row in testSet:
            mapProb = self.getMap(row)
            mapProbs.append(mapProb)
        return mapProbs

    def accuracy(self, testSet, predicted):
        """
        :param testSet: conjunto de amostras teste
        :param predicted: conjunto de classes previstas
        :return:
        Porcentagem resultante do desempenho do modelo   
        """
        correct = 0
        actual = [item[-1] for item in testSet]
        for x, y in zip(actual, predicted):
            if x == y:
                correct += 1
        return correct / float(len(testSet)) * 100.0

def main():
    filename = 'diabetes.csv'

    nb = GaussNB_Stratch()
    data = nb.loadCsv(filename)

    #treinamento e teste usando o algoritmo feito na mão
    trainList, testList = nb.splitDataset(data, .67)
    nb.train(trainList)
    predicted = nb.predict(testList)
    accuracy = nb.accuracy(testList, predicted)

    print('Accuracy (stratch): {0} %'.format(accuracy))

    #treinamento e teste usando a lib do scikit
    model = GaussianNB()
    model.fit(trainList[:, 0:7], trainList[:, -1])
    predicted = model.predict(testList[:, 0:7])
    print('Accuracy (scikit): {0} %'.format(accuracy_score(testList[:, -1], predicted) * 100))


if __name__ == '__main__':
    main()
