# coding=utf-8
import logging
import sys

from pyage.core import address
from pyage.core.agent.agent import generate_agents, Agent

from pyage.core.agent.aggregate import AggregateAgent
from pyage.core.emas import EmasService
from pyage.core.locator import GridLocator
from pyage.core.migration import ParentMigration
from pyage.core.stats.extra_gnuplot import StepStatisticsWithStdDev
from pyage.core.stats.gnuplot import StepStatistics, TimeStatistics
from pyage.core.stop_condition import StepLimitStopCondition

from pyage.satcnf.sat_crossover import Crossover
from pyage.satcnf.sat_eval import Evaluator
from pyage.satcnf.sat_init import EmasInitializer, ClausulesInitializer, root_agents_factory, TheInitializer
from pyage.satcnf.sat_naming_service import NamingService
from pyage.satcnf.sat_mutation import Mutation1, Mutation2
from pyage.satcnf.sat_selection import TournamentSelection

logger = logging.getLogger(__name__)

args = sys.argv
use_emas = args[3]
mutation_prob = args[4]
mutation_func = args[5]
em = "emas" if use_emas == '1' else "evol"
logger.error(em)
filename = args[6] + "_" + em + "_" + str(mutation_prob) + "_" +str(mutation_func) + ".txt"
agents_count = 10

if em == "emas":
    agents = root_agents_factory(agents_count, AggregateAgent)
    agg_size = 40
    clausules_nr = 500
    max_clausule_length = 5
    number_of_atoms = 5
    clausules = ClausulesInitializer(clausules_nr, max_clausule_length=max_clausule_length,
                                     number_of_atoms=number_of_atoms, seed=900)()
    aggregated_agents = EmasInitializer(clausules=clausules, size=agg_size, energy=40)

    emas = EmasService

    minimal_energy = lambda: 10
    reproduction_minimum = lambda: 100
    migration_minimum = lambda: 120
    newborn_energy = lambda: 100
    transferred_energy = lambda: 40

    budget = 0
    evaluation = lambda: Evaluator()
    crossover = lambda: Crossover(size=30)
    mutation = lambda: Mutation1(probability=float(mutation_prob)) if int(mutation_func) == 1 \
        else Mutation2(probability=float(mutation_prob))
else:
    minimal_energy = lambda: 10
    reproduction_minimum = lambda: 100
    migration_minimum = lambda: 120
    newborn_energy = lambda: 100
    transferred_energy = lambda: 40

    budget = 0
    agents = generate_agents("agent", agents_count, Agent)
    clausules_nr = 50
    max_clausule_length = 4
    number_of_atoms = 4
    operators = lambda: [Evaluator(), TournamentSelection(size=50, tournament_size=50),
                         Crossover(size=100),
                         Mutation1(probability=float(mutation_prob)) if int(mutation_func) == 1
                         else Mutation2(probability=float(mutation_prob))]
    initializer = lambda: TheInitializer(size=100, clausules=ClausulesInitializer(clausules_nr=clausules_nr,
                                                                                   max_clausule_length=max_clausule_length,
                                                                                   number_of_atoms=number_of_atoms,
                                                                                   seed=1000)())

stop_condition = lambda: StepLimitStopCondition(500)

address_provider = address.SequenceAddressProvider

migration = ParentMigration
locator = GridLocator

stats = lambda: StepStatisticsWithStdDev(filename)

naming_service = lambda: NamingService(starting_number=1)
