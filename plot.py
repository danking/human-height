import os
import shutil
import pandas as pd
import matplotlib.pyplot as plt
import urllib.request

if not os.path.exists('BMX_J.XPT'):
    print('downloading BMX_J.XPT ...')
    with urllib.request.urlopen('https://wwwn.cdc.gov/Nchs/Nhanes/2017-2018/BMX_J.XPT') as remote, \
         open('BMX_J.XPT', 'wb') as local:
        shutil.copyfileobj(remote, local)

if not os.path.exists('DEMO_J.XPT'):
    print('downloading DEMO_J.XPT ...')
    with urllib.request.urlopen('https://wwwn.cdc.gov/Nchs/Nhanes/2017-2018/DEMO_J.XPT') as remote, \
         open('DEMO_J.XPT', 'wb') as local:
        shutil.copyfileobj(remote, local)

print('Plotting ...')

df = pd.read_sas('BMX_J.XPT', format='xport')
df = df.set_index('SEQN')

age = pd.read_sas('DEMO_J.XPT', format='xport')
age = age.set_index('SEQN')

data = df.join(age)[['BMXHT', 'RIDAGEYR', 'RIAGENDR']]
data = data[data['RIDAGEYR'] > 18]
data['height_in'] = data['BMXHT'] * 0.393701
men = data[data['RIAGENDR'] == 1]
women = data[data['RIAGENDR'] == 2]


plt.hist(data['height_in'], bins=100, label='all', alpha=1)
plt.hist(men['height_in'], bins=100, label='men', alpha=0.5)
plt.hist(women['height_in'], bins=100, label='women', alpha=0.5)
plt.legend(loc='upper right')
plt.show()
