# Exemple d'utilisation :
# data = scrape_annonces('https://dakar-auto.com/senegal/voitures-4?page=', 5)
# https://dakar-auto.com/senegal/voitures-4 -> page 1 à 2753
# https://dakar-auto.com/senegal/motos-and-scooters-3 -> page 1 à 54
# https://dakar-auto.com/senegal/location-de-voitures-19 -> page 1 à 8

# importer les packages
import pandas as pd
from requests import get # récupérer le code html de la page
from bs4 import BeautifulSoup as bs  # stocker le code html dans un object beautifulsoup
import time
import re



def scrape(base_url, nb_pages):
    """
    Scrape les annonces depuis un site web (version BeautifulSoup).
    Args:
        base_url (str): L'URL de base (ex: 'https://dakar-auto.com/senegal/voitures-4?page=')
        nb_pages (int): Nombre de pages à parcourir
    Returns:
        pd.DataFrame: DataFrame contenant les informations des annonces
    """
    all_data = []
    for p in range(1, nb_pages + 1):
        url = f'{base_url}{p}'
        print(f"Scraping page: {url}")
        try:
            code_html = get(url, timeout=10)
            soup = bs(code_html.content, 'html.parser')
            containers = soup.find_all('div', class_='listings-cards__list-item mb-md-3 mb-3')
        except Exception as e:
            print(f"Erreur chargement page {url}: {e}")
            continue

        for container in containers:
            try:
                url_container = 'https://dakar-auto.com' + container.find('a', class_="listing-card__aside__inner d-block")['href']
                hc_container = get(url_container)
                soup_container = bs(hc_container.content, 'html.parser')
                marque = re.split(r'\s\d{4}\b', soup_container.find('h1', class_='listing-item__title').span.text.strip())[0].strip()
                prix_raw = soup_container.find('h4', class_='listing-item__price font-weight-bold text-uppercase mb-2').text.strip()
                adresse = soup_container.find('span', class_='province font-weight-bold d-inline-block').text.strip()
                proprietaire = soup_container.find('h4', class_='listing-item-sidebar__author-name').text.strip()
                ul_tag = soup_container.find('ul', class_='listing-item__attribute-list list-inline')
                if ul_tag:
                    li_tags = ul_tag.find_all('li', class_='listing-item__attribute list-inline-item')
                    lines = [li.get_text(strip=True) for li in li_tags]
                    kilometrage_raw = lines[0] if len(lines) > 0 else ""
                    année_raw = lines[1] if len(lines) > 1 else ""
                    boite = lines[2] if len(lines) > 2 else ""
                    carburant = lines[3] if len(lines) > 3 else ""
                else:
                    kilometrage_raw = année_raw = boite = carburant = ""

                prix = int(re.sub(r'[^\d]', '', prix_raw)) if prix_raw else None
                annee_match = re.search(r'\d{4}', année_raw)
                année = int(annee_match.group()) if annee_match else None
                km_match = re.search(r'\d+', kilometrage_raw.replace(" ", ""))
                kilometrage = int(km_match.group()) if km_match else None

                all_data.append({
                    "marque": marque,
                    "année": année,
                    "prix": prix,
                    "adresse": adresse,
                    "kilométrage": kilometrage,
                    "boite": boite.replace("Boîte", "").strip() if boite else None,
                    "carburant": carburant.replace("Carburant", "").strip() if carburant else None,
                    "propriétaire": proprietaire,
                    "url": url_container
                })
                time.sleep(0.5)
            except Exception as e:
                print(f"Erreur sur annonce: {e}")
                continue
        print(f"Page {p} terminée : {len(containers)} annonces récupérées")
    return pd.DataFrame(all_data)




