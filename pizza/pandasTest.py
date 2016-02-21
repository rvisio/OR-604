import csv, timeit
import pandas as pd

start = timeit.default_timer()
data = pd.read_csv("OR 604 Dominos Daily Demand.csv", low_memory=False)
stop = timeit.default_timer()
print 'pandasTest.py took ' + str(stop - start) + ' seconds to read csv'

start = timeit.default_timer()
df = data.groupby(['Store Number']).mean()
stop = timeit.default_timer()
print 'pandasTest.py took ' + str(stop - start) + ' seconds to caclulate mean'

print df.head
