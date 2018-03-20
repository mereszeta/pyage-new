# coding=utf-8
import logging
import os

from matplotlib.pyplot import errorbar, savefig
from numpy import average, std

from pyage.core.statistics import Statistics

logger = logging.getLogger(__name__)


class StepStatisticsWithStdDev(Statistics):
    def __init__(self, output_file_name='fitness_pyage.txt', plot=True,
                 plot_file_name='plot.png', take_max_as_best=True, use_abs=True):
        self.history = []
        self.fitness_output = open(output_file_name, 'a')
        self.take_max_as_best = take_max_as_best
        self.plot_file_name = plot_file_name
        self.use_abs = use_abs
        self.plot = plot

    def __del__(self):
        self.fitness_output.close()

    def append(self, best_fitness, step_count):
        self.fitness_output.write(str(step_count - 1) + ';' + str(best_fitness) + '\n')
        self.fitness_output.flush()
        os.fsync(self.fitness_output)

    def update(self, step_count, agents):
        try:
            fitnesses = [a.get_fitness() for a in agents]
            best_fitness = max(fitnesses) if self.take_max_as_best else min(fitnesses)
            avg_fitness = average(fitnesses)
            std_dev = std(fitnesses)
            logger.debug(best_fitness)
            self.history.append((best_fitness, avg_fitness, std_dev))
            self.append(best_fitness, step_count)
        except:
            logging.exception("")

    def summarize(self, agents):
        try:
            logger.debug(self.history)
            best_agent = max(agents, key=lambda a: a.get_fitness())
            best_genotype = best_agent.get_best_genotype()
            self.fitness_output.write("best genotype:\n%s\n" % best_genotype)
            average = []
            std_dev = []
            for (_, avg, stddev) in self.history:
                if self.use_abs:
                    avg = abs(avg)
                average.append(avg)
                std_dev.append(stddev)
            steps = range(1, len(average) + 1)
            logger.debug("STATISTICS START\n============================================================")
            logger.debug("Size: " + str(len(average)))
            logger.debug("Averages: " + str(average))
            logger.debug("Standard deviations: " + str(std_dev))
            if self.plot:
                logger.debug("Plotting results: errorbar")
                errorbar(steps, average, std_dev)
                logger.debug("Plotting results: savefig")
                savefig(self.plot_file_name)
            logger.debug("Done!")
            logger.debug("STATISTICS END\n============================================================")
        except Exception as e:
            logging.exception(e)