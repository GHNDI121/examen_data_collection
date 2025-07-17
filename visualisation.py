import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

class Visualisation:
    def __init__(self, df):
        self.df = df

    def prix_moyen_par_marque(self, top_n=10):
        if 'marque' in self.df.columns and 'prix' in self.df.columns:
            return self.df.groupby('marque')['prix'].mean().sort_values(ascending=False).head(top_n)
        return pd.Series()

    def repartition_annees(self):
        if 'année' in self.df.columns:
            return self.df['année'].value_counts().sort_index()
        return pd.Series()

    def plot_distribution_kilometrage(self):
        if 'kilométrage' in self.df.columns:
            fig, ax = plt.subplots()
            sns.histplot(self.df['kilométrage'], bins=30, kde=True, ax=ax)
            return fig
        return None

    def get_dataframe(self):
        return self.df
