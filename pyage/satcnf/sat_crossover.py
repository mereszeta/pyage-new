import random
from pyage.core.operator import Operator
from pyage.satcnf.sat_genotype import Clausules

import logging

logger = logging.getLogger(__name__)


class AbstractCrossover(Operator):
    def __init__(self, type=Clausules, size=1000):
        super(AbstractCrossover, self).__init__(type)
        self.__size = size

    def process(self, population):
        parents = list(population)
        for i in range(len(population), self.__size):
            p1, p2 = random.sample(parents, 2)
            genotype = self.cross(p1, p2)
            population.append(genotype)


class Crossover(AbstractCrossover):
    def __init__(self, size):
        super(Crossover, self).__init__(Clausules, size)

    def cross(self, p1, p2):
        division = random.randint(1, len(p1.clausules) - 2)
        counter = 0
        new_clausules = p1.clausules[:]
        for clausule in p1:
            if counter >= division:
                counter2 = 0
                for atom in new_clausules[counter]:
                    atom[0].value = p2.clausules[counter][counter2][0].value
                    counter2 += 1
            counter += 1
        atoms = []
        # for clausule in new_clausules:
        #     for atom in clausule:
        #         if atom not in atoms:
        #             atoms.append(atom)
        # for atom in atoms:
        #     for clausule in new_clausules:
        #         for atm in clausule:
        #             if atm[0].name == atom[0].name and atm[0].value != atom[0].value:
        #                 atm[0].value = atom[0].value
        return Clausules(new_clausules, False)
