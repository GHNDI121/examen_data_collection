import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import re
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
        if 'kilométrage' in self.df.columns and 'année' in self.df.columns:
            df_plot = self.df.dropna(subset=['kilométrage', 'année'])
            if df_plot.empty:
                return None
            # Calcul de la moyenne du kilométrage par année
            km_par_annee = df_plot.groupby('année')['kilométrage'].mean().sort_index()
            fig, ax = plt.subplots(figsize=(8, 5))
            sns.barplot(x=km_par_annee.index.astype(int), y=km_par_annee.values, ax=ax, palette='tab10')
            ax.set_title('Moyenne du kilométrage par année')
            ax.set_xlabel('Année')
            ax.set_ylabel('Kilométrage moyen')
            return fig
        return None

    def get_dataframe(self):
        return self.df



def traitement_de_donnees(df):
    # Nettoyage de la colonne 'prix'
    if 'prix' in df.columns:
        df['prix'] = df['prix'].apply(lambda x: int(re.sub(r'[^\d]', '', x)) if isinstance(x, str) and re.sub(r'[^\d]', '', x) != '' else None)

    # Gestion des variantes de colonne année
    annee_col = None
    for col in df.columns:
        if col.lower() in ['année', 'annee', 'année', 'annee']:
            annee_col = col
            break
    if annee_col:
        df['année'] = df[annee_col].apply(lambda x: int(re.search(r'\d{4}', str(x)).group()) if isinstance(x, str) and re.search(r'\d{4}', str(x)) else None)
    # Gestion des variantes de colonne 'kilométrage'
    km_col = next((col for col in df.columns if col.lower() in ['kilométrage', 'kilometrage']), None)
    # Nettoyage de la colonne 'kilométrage'
    if km_col:
        df['kilométrage'] = df[km_col].apply(
            lambda x: int(re.search(r'\d+', str(x).replace(" ", "")).group()) if isinstance(x, str) and re.search(r'\d+', str(x).replace(" ", "")) else None
        )

    # Liste des colonnes à afficher (seulement celles présentes)
    colonnes_affichage = [c for c in [
        "marque", "année", "annee", "prix", "adresse", "kilométrage", "boite", "carburant", "propriétaire"
    ] if c in df.columns]

    # Si 'année' a été créée à partir de 'annee', on préfère afficher 'année'
    if 'année' in df.columns and 'annee' in colonnes_affichage:
        colonnes_affichage = [c for c in colonnes_affichage if c != 'annee']

    return df[colonnes_affichage]

