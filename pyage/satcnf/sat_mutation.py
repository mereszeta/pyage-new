import logging
import random
from pyage.core.operator import Operator
from pyage.satcnf.sat_genotype import Clausules
from pyage.satcnf.sat_genotype import Atom

logger = logging.getLogger(__name__)


class AbstractMutation(Operator):
    def __init__(self, type, probability):
        super(AbstractMutation, self).__init__()
        self.probability = probability

    def process(self, population):
        for genotype in population:
            if random.random() < self.probability:
                self.mutate(genotype)


class Mutation1(AbstractMutation):
    def __init__(self, probability):
        super(Mutation1, self).__init__(Clausules, probability)
        self.probability = probability

    def mutate(self, genotype):
        rand_claus = genotype.clausules[random.randint(0, len(genotype.clausules) - 1)]
        shuffle(rand_claus)


class Mutation2(AbstractMutation):
    def __init__(self, probability):
        super(Mutation2, self).__init__(Clausules, probability)
        self.probability = probability

    def mutate(self, genotype):
        for clausule in genotype.clausules:
            rand = random.random()
            if rand < self.probability:
                shuffle(clausule)


def shuffle(clausule):
    shuffled = []
    for _ in xrange(0, random.randint(0, get_count(clausule))):
        to_shuffle = clausule[random.randint(0, len(clausule) - 1)][0]
        while to_shuffle in shuffled:
            to_shuffle = clausule[random.randint(0, len(clausule) - 1)][0]
        shuffled.append(to_shuffle)
        for cls in clausule:
            if cls[0].name == to_shuffle.name:
                cls[0].value = 1 - cls[0].value


def get_count(clausule):
    out = []
    for atom in clausule:
        if atom[0].name not in out:
            out.append(atom[0].name)
    return len(out)
