import pandas as pd

poke_df = pd.read_csv('Pokemon.csv')
print(poke_df[['HP', 'Attack', 'Defense']].describe())
