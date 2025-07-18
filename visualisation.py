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
        if 'kilométrage' in self.df.columns:
            fig, ax = plt.subplots()
            sns.histplot(self.df['kilométrage'], bins=30, kde=True, ax=ax)
            return fig
        return None

    def get_dataframe(self):
        return self.df



def traitement_de_donnees(df):
    # Nettoyage de la colonne 'prix'
    if 'prix' in df.columns:
        df['prix'] = df['prix'].apply(lambda x: int(re.sub(r'[^\d]', '', x)) if isinstance(x, str) and re.sub(r'[^\d]', '', x) != '' else None)

    # Fusion et nettoyage des variantes de colonne année
    annee_cols = [col for col in df.columns if col.lower() in ['année', 'annee']]
    if annee_cols:
        # On crée une nouvelle colonne 'année' en priorisant la première colonne non nulle trouvée
        def extract_annee(row):
            for col in annee_cols:
                val = row[col]
                if pd.notnull(val):
                    if isinstance(val, int):
                        return val
                    match = re.search(r'\d{4}', str(val))
                    if match:
                        return int(match.group())
            return None
        df['année'] = df.apply(extract_annee, axis=1)
        # Supprimer toutes les autres colonnes année/annee sauf 'année'
        for col in annee_cols:
            if col != 'année':
                df.drop(columns=col, inplace=True)

    # Gestion des variantes de colonne 'kilométrage'
    km_cols = [col for col in df.columns if col.lower() in ['kilométrage', 'kilometrage']]
    if km_cols:
        def extract_km(row):
            for col in km_cols:
                val = row[col]
                if pd.notnull(val):
                    if isinstance(val, int):
                        return val
                    match = re.search(r'\d+', str(val).replace(" ", ""))
                    if match:
                        return int(match.group())
            return None
        df['kilométrage'] = df.apply(extract_km, axis=1)
        for col in km_cols:
            if col != 'kilométrage':
                df.drop(columns=col, inplace=True)

    # Liste des colonnes à afficher (seulement celles présentes)
    colonnes_affichage = [c for c in [
        "marque", "année", "prix", "adresse", "kilométrage", "boite", "carburant", "propriétaire"
    ] if c in df.columns]

    return df[colonnes_affichage]

