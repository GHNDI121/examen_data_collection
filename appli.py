import streamlit as st
import pandas as pd
from scraping import scrape
import streamlit.components.v1 as components
from visualisation import Visualisation, traitement_de_donnees

# En-tête principal
st.markdown("<h1 style='text-align: center; color: black;'>DATA APP : Ghoulam Ndiaye</h1>", unsafe_allow_html=True)


# Menu latéral
page = st.sidebar.selectbox("Menu", ["Données Stockées", "Scraping", "Formulaire", "Visualisation"])

# Fonction de loading des données
def load_(dataframe, title, key) :
    st.markdown("""
    <style>
    div.stButton {text-align:center}
    </style>""", unsafe_allow_html=True)

    if st.button(title,key):
      
        st.subheader('Display data dimension')
        st.write('Data dimension: ' + str(dataframe.shape[0]) + ' rows and ' + str(dataframe.shape[1]) + ' columns.')
        st.dataframe(dataframe)

# définir quelques styles liés aux box
st.markdown('''<style> .stButton>button {
    font-size: 12px;
    height: 3em;
    width: 25em;
}</style>''', unsafe_allow_html=True)


# PAGE 1 : Données stockées
if page == "Données Stockées":
    st.markdown("""
    cette page vous permet de télécharger les données scrappées par web-scraper sur les motos et autos de Dakar-auto.
    * **Data source:** [Dakar-auto](https://dakar-auto.com/)
    """)
    load_(pd.read_csv('data/location_auto.csv'), 'location_auto', '1')
    load_(pd.read_csv('data/vente_auto.csv'), 'vente_auto', '2')
    load_(pd.read_csv('data/vente_moto.csv'), 'vente_moto', '3')
    

# PAGE 2 : Scraping
elif page == "Scraping":
    st.markdown("""
    cette page vous permet de scraper les données sur les motos et autos de Dakar-auto grace à selenium tout en indexant le nombre de page que nous voulons scraper.
    * **Python libraries:** base64, pandas, streamlit  
    * **Data source:** [Dakar-auto](https://dakar-auto.com/)
    """)

    # Input nombre de pages par catégorie
    nb_voitures = st.number_input("Pages à scraper (voitures)", 1, 2753, 1, key="pages_voitures")
    # --- Scraping Voitures ---
    if st.button("Scraper les VOITURES", key="scrape_voitures"):
        url_voitures = 'https://dakar-auto.com/senegal/voitures-4?page='
        data_voitures = scrape(url_voitures, nb_voitures)
        df_voitures = pd.DataFrame(data_voitures)[[
            'marque', 'année', 'prix', 'adresse', 'kilométrage', 'boite', 'carburant', 'propriétaire'
        ]]
        st.session_state['voitures_data'] = df_voitures
        st.dataframe(df_voitures)
        
    nb_motos = st.number_input("Pages à scraper (motos)", 1, 54, 1, key="pages_motos")
    # --- Scraping Motos ---
    if st.button("Scraper les MOTOS", key="scrape_motos"):
        url_motos = 'https://dakar-auto.com/senegal/motos-and-scooters-3?page='
        data_motos = scrape(url_motos, nb_motos)
        df_motos = pd.DataFrame(data_motos)[[
            'marque', 'année', 'prix', 'adresse', 'kilométrage', 'propriétaire'
        ]]
        st.session_state['motos_data'] = df_motos
        st.dataframe(df_motos)
        
    nb_location = st.number_input("Pages à scraper (location)", 1, 8, 1, key="pages_location")
    # --- Scraping Location ---
    if st.button("Scraper la LOCATION", key="scrape_location"):
        url_location = 'https://dakar-auto.com/senegal/location-de-voitures-19?page='
        data_location = scrape(url_location, nb_location)
        df_location = pd.DataFrame(data_location)[[
            'marque', 'année', 'prix', 'adresse', 'propriétaire'
        ]]
        st.session_state['location_data'] = df_location
        st.dataframe(df_location)

# PAGE 3 : Formulaire
elif page == "Formulaire":
    st.markdown("""
        cette page vous permet de remplir un formulaire dans le but d'etre recontacter afin de vous aider dans votre projet d'achat ou de location de véhicule.
        * **Data source:** https://ee.kobotoolbox.org/i/ZckCl6XF
        """)
    components.html(
        """<iframe src="https://ee.kobotoolbox.org/i/ZckCl6XF" width="100%" height="700" frameborder="0"></iframe>""",
        height=700
    )

# PAGE 4 : visualisation
elif page == "Visualisation":
    st.markdown("""
        cette page vous permet de visualiser les données scrappées par selenium sur les motos et autos de Dakar-auto.
        * **Data source:** [Dakar-auto](https://dakar-auto.com/)
        """)

    source = st.selectbox("Choisir une source", ["Voitures", "Motos", "Locations"])

    if source == "Voitures":
        df = pd.read_csv('data/vente_auto.csv')
        df = traitement_de_donnees(df)
        df = pd.DataFrame(df)[[
            'marque', 'année', 'prix', 'adresse', 'kilométrage', 'boite', 'carburant', 'propriétaire'
        ]]
    elif source == "Motos":
        df = pd.read_csv('data/vente_moto.csv')
        df = traitement_de_donnees(df)
        df = pd.DataFrame(df)[[
            'marque', 'année', 'prix', 'adresse', 'kilométrage', 'propriétaire'
        ]]
    elif source == "Locations":
        df = pd.read_csv('data/location_auto.csv')
        df = traitement_de_donnees(df)
        df = pd.DataFrame(df)[[
            'marque', 'année', 'prix', 'adresse', 'propriétaire'
        ]]
    else:
        st.warning("Aucune donnée disponible.")
        st.stop()

    vis = Visualisation(df)

    st.subheader("Aperçu des données")
    st.dataframe(vis.get_dataframe())

    st.subheader("Prix moyen par marque")
    st.bar_chart(vis.prix_moyen_par_marque())

    st.subheader("Répartition des années")
    st.line_chart(vis.repartition_annees())

    fig = vis.plot_distribution_kilometrage()
    if fig is not None:
        st.subheader("Distribution du kilométrage")
        st.pyplot(fig)
    else:
        st.warning("Aucune donnée de kilométrage disponible.")
