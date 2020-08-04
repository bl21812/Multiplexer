from ParseTree import ParseTree
import random
import copy

# Remember to call fitness function and store in Tree.fit for new trees/changed ones

class SixBitMultiplexer:

    def __init__(self, popSize):
        self.popSize = popSize
        self.pop = []
        for i in range(popSize):
            if i < (popSize / 2):
                self.pop.append(ParseTree('grow', 5))
            else:
                self.pop.append(ParseTree('full', 5))
        self.best = self.pop[0]  # Best solution tree
        self.bestVal = 0  # Number of tests passed
        self.bestPerGen = []  # Fitness of best solution in each gen

    def runSim(self):
        gen = 1
        pNodeMutate = 0.1
        pNodeCross = 0.1
        while gen <= 2000 and self.bestVal < 64:  # Max iterations or perfect sol reached
            self.pop.sort(key=lambda x: x.fit, reverse=True)  # Sort population by descending fitness
            if self.pop[0].fit > self.bestVal:  # Set gbest if applicable
                self.bestVal = self.pop[0].fit
                self.best = self.pop[0]
            self.bestPerGen.append(self.pop[0].fit)  # Add to gen best list
            if random.random() < 0.05:  # Low chance of mutation instead of recombination
                for i in range(1, self.popSize):  # Mutate each and update fitness, keeping best sol
                    self.pop[i].mutate(pNodeMutate)
                    self.pop[i].fit = self.pop[i].fitness()
            else:  # Recombination
                newGenTemp = copy.deepcopy(self.pop)  # Placeholder to not mess with memory of initial pop
                newGen = []
                for i in range(int(self.popSize / 2)):  # Tournament selection and recombination
                    choices1 = []
                    for j in range(10):
                        choices1.append(newGenTemp[random.randint(0, self.popSize - 1)])
                    choices1.sort(key=lambda x: x.fit, reverse=True)
                    choices2 = []
                    for j in range(10):
                        choices2.append(newGenTemp[random.randint(0, self.popSize - 1)])
                    choices2.sort(key=lambda x: x.fit, reverse=True)
                    choices1[0].recombine(choices2[0], pNodeCross)
                    newGen.append(choices1[0])  # Add to actual new generation
                    newGen.append(choices2[0])
                    choices1[0].fit = choices1[0].fitness()
                    choices2[0].fit = choices2[0].fitness()
                newGen.sort(key=lambda x: x.fit, reverse=True)  # Sort new generation by descending fitness
                self.pop = self.pop[0:1] + newGen[:self.popSize - 1]  # Replace population, with new generation (minus worst) + best of old generation
            gen += 1
        print('Best solution, with a fitness of ' + str(self.bestVal) + "/64: ")
        print(self.best)
