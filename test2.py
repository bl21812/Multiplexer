from ElevenBitMultiplexer import ElevenBitMultiplexer
import matplotlib.pyplot as plt

elevenMulti1 = ElevenBitMultiplexer(100)
elevenMulti1.runSim()

gens = [i for i in range(1, elevenMulti1.gen)]
plt.plot(gens, elevenMulti1.bestPerGen, 'r-')
plt.show()
