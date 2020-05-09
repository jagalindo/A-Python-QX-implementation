import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('./result.csv', sep='|')



plt.savefig('time_evolution.png')
