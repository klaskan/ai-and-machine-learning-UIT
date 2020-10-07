import pandas as pd
import numpy as np
from collections import namedtuple
from BinaryTree import BinaryTree

#A. Ved bruk av Pandas - les inn datafilen og legg dette i en collection av namedtuple
#read_stat() is not working since it's an older .dta format, so had to find a workaround
df = pd.read_fwf('Personer.dta', )
df = df.applymap(str)
df.columns = ["name"]

df[['First', 'Last', 'Address', 'Nr', 'City']] = df.name.str.split(';', expand=True)
df = df.drop(columns=["name"])

Personer = namedtuple('Personer', ['First', 'Last', 'Address', 'Nr', 'City'])
list_df = list(df.itertuples(name='Person', index=False))


#B. Insert dataene (namedtuples) som du hentet i det binære søketreet
binaryTree = BinaryTree()
for data in list_df:
    binaryTree.insert(value=data)

#C. Hver node i treet har en egen "level" knyttet til seg - altså nivå i treet. 
# Skriv ut nivået og verdien for rad nr 1, 10, 100, 1000, 10000, 100000 fra filen Personer.dta. 
#Legg til side denne listen av namedtuples og nivået i treet
values_to_find = [1, 10, 100, 1000, 10000, 100000]
for i in values_to_find:
    print(f"Value: {binaryTree.find(list_df[i]).value}")
    print(f"Level: {binaryTree.find(list_df[i]).level}")
    print("----------------------------------------------------------------------------------------------")






