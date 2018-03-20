from pyage.core.operator import Operator
from pyage.satcnf.sat_genotype import Clausules
import logging

logger = logging.getLogger(__name__)


class Evaluator(Operator):
    def __init__(self):
        super(Evaluator, self).__init__(Clausules)

    def process(self, population):
        for genotype in population:
            genotype.fitness = self.evaluate(genotype)

    def evaluate(self, genotype):
        fitnesses = list()
        for clausule in genotype:
            sum = 0
            for h in clausule:
                if h[1]:
                    sum += 1 - h[0].value
                else:
                    sum += h[0].value
            if sum > 0:
                fitnesses.append(1)
            else:
                fitnesses.append(0)
        evaluated = 0
        for cf in fitnesses:
            evaluated += cf
        res = evaluated
        return (float(res) / len(fitnesses)) ** 2
