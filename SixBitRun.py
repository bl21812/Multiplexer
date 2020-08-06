from SixBitMultiplexer import SixBitMultiplexer
import matplotlib.pyplot as plt

sixMulti1 = SixBitMultiplexer(100)
sixMulti1.runSim()

gens = [i for i in range(1, 2001)]
plt.plot(gens, sixMulti1.bestPerGen, 'r-')
plt.show()
