from pyage.core.emas import EmasAgent
from pyage.core.operator import Operator
from pyage.satcnf.sat_genotype import Clausules
from pyage.satcnf.sat_genotype import Atom
from pyage.core.inject import Inject
import random


class EmasInitializer(object):
    def __init__(self, clausules, energy, size):
        self.clausules = clausules
        self.energy = energy
        self.size = size

    @Inject("naming_service")
    def __call__(self):
        agents = {}
        for i in range(self.size):
            agent = EmasAgent(Clausules(self.clausules), self.energy, self.naming_service.get_next_agent())
            agents[agent.get_address()] = agent
        return agents


def root_agents_factory(count, type):
    def factory():
        agents = {}
        for i in range(count):
            agent = type('R' + str(i))
            agents[agent.get_address()] = agent
        return agents

    return factory


class ClausulesInitializer(object):
    def __init__(self, clausules_nr, max_clausule_length, number_of_atoms, seed):
        self.clausules_nr = clausules_nr
        self.max_clausule_length = max_clausule_length
        self.number_of_atoms = number_of_atoms

    def __call__(self):
        wereAllAtomsUsed = False
        alphabet = list("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")
        atoms_list = []
        atms = []
        for i in xrange(0, self.number_of_atoms):
            letter = alphabet[random.randint(0, len(alphabet)-1)]
            while letter in atms:
                letter = alphabet[random.randint(0, len(alphabet)-1)]
            atms.append(letter)
            atoms_list.append([Atom(random.randint(0, 1), letter), 0])
        values = []
        while not wereAllAtomsUsed:
            clausules_list = list()
            for clausule in xrange(0, self.clausules_nr):
                used_in_clausule = []
                atoms_in_clausule = self.max_clausule_length
                new_clausule = list()
                for h in xrange(atoms_in_clausule):
                    atom_index = random.randint(0, atoms_in_clausule - 1)
                    while atoms_list[atom_index][0].name in used_in_clausule:
                        atom_index = random.randint(0, atoms_in_clausule - 1)
                    my_tuple = [atoms_list[atom_index][0], random.randint(0,1)]
                    used_in_clausule.append(atoms_list[atom_index][0].name)
                    atoms_list[atom_index][1] = 1
                    new_clausule.append(my_tuple)
                clausules_list.append(new_clausule)
            wereAllAtomsUsed = True
            for atom, wasUsed in atoms_list:
                if wasUsed == 0:
                    wereAllAtomsUsed = False

            random.seed()
        return clausules_list


class TheInitializer(Operator):
    def __init__(self, size, clausules):
        super(TheInitializer, self).__init__(Clausules)
        self.size = size
        self.clausules = clausules
        self.population = generate(size, clausules)

    def __call__(self, *args, **kwargs):
        return self.population

    def process(self, population):
        for i in xrange(self.size):
            population.append(self.population[i])


def generate(size, clausules):
    population = []
    for _ in xrange(size):
        population.append(Clausules(clausules))
    return population
