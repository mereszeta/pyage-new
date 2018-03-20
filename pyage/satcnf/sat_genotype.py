import random


class Atom(object):
    def __init__(self, value, name):
        self.value = value
        self.name = name


class Clausules(object):
    def __init__(self, clausules,shfl=True):
        self.clausules = clausules
        if not shfl:
            random.shuffle(clausules)
        self.fitness = None

    def __iter__(self):
        return iter(self.clausules)

    def __str__(self):
        names = list()
        for clausule in self.clausules:
            names.append("(")
            for atom in clausule:
                if atom[1]:
                    names.append(["!" + atom[0].name, atom[0].value])
                else:
                    names.append([atom[0].name, atom[0].value])
            names.append(")")
        return "{0}\nfitness: {1}".format("\n".join(map(str, names)), self.fitness)

    def shuffle(self):
        shuffled = [];
        for i in xrange(0, random.randint(0, self.get_count())):
            cl = self.clausules[random.randint(0, len(self.clausules) - 1)]
            to_shuffle = cl[random.randint(0, len(cl) - 1)]
            while to_shuffle  in shuffled:
                cl = self.clausules[random.randint(0, len(self.clausules) - 1)]
                to_shuffle = cl[random.randint(0, len(cl) - 1)]
            shuffled.append(to_shuffle)
            for clausule in self.clausules:
                for atom in clausule:
                    if atom[0].name == to_shuffle[0].name:
                        atom[0].value = 1 - atom[0].value

    def get_count(self):
        out = []
        for clausule in self.clausules:
            for atom in clausule:
                if atom[0].name not in out:
                    out.append(atom[0].name)
        return len(out)
