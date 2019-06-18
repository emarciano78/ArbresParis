#!/usr/bin/env python
# coding: utf-8

# In[3]:


import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


# In[4]:


pd.set_option('display.max_columns', 50)    # Force pandas à afficher plus de 8 colonnes
pd.set_option('display.width', 1000)        # Force à afficher plus de 80 colonnes


# In[5]:


df = pd.read_csv("D:\BIGDATA\Datas_arbres.csv", sep=';')


# In[8]:


print("Nombre d'arbre par ARRONDISSEMENT/NOM ARBRE")
print(df.groupby(["ARRONDISSEMENT","LIBELLEFRANCAIS"]).size().reset_index(name='NOMBRE'))

print("Nombre d'arbre par ARRONDISSEMENT")
print(df.groupby(["ARRONDISSEMENT"]).size().reset_index(name='NOMBRE'))


# In[13]:


#x = np.linspace(0, 2, 100)
x = df.groupby(["ARRONDISSEMENT"]).size().reset_index(name='NOMBRE')

plt.plot(x, x, label='linear')
#plt.plot(x, x**2, label='quadratic')
#plt.plot(x, x**3, label='cubic')

plt.xlabel('ARRONDISSEMENT')
plt.ylabel('ARBRES')

plt.title("Nombre d'arbres par arrondissement")

plt.legend()

plt.show()


# In[ ]:




