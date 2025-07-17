# Installer selenium et webdriver_manager si besoin :
# pip install selenium webdriver-manager pandas

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd
import re


def scrape_annonces(base_url, nb_pages):
    """
    Scrape les annonces depuis un site web.
    
    Args:
        base_url (str): L'URL de base (ex: 'https://dakar-auto.com/senegal/voitures-4?page=')
        nb_pages (int): Nombre de pages à parcourir
    
    Returns:
        list: Liste de dictionnaires contenant les informations des annonces
    """
    options = Options()
    options.add_argument('--headless')  # exécute sans interface graphique
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.set_page_load_timeout(60)

    all_data = []

    for page in range(1, nb_pages + 1):
        url = f"{base_url}{page}"
        try:
            driver.get(url)
            time.sleep(2)
        except Exception as e:
            print(f"Erreur de chargement de la page {url} : {e}")
            continue

        try:
            links = driver.find_elements(By.CSS_SELECTOR, "h2.listing-card__header__title a")
            detail_urls = [link.get_attribute("href") for link in links]
        except Exception as e:
            print(f"Erreur lors de la récupération des liens sur la page {page} : {e}")
            continue

        for detail_url in detail_urls:
            try:
                driver.get(detail_url)
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "h1"))
                )
                time.sleep(1)

                marque = driver.find_element(By.CSS_SELECTOR, "h1.listing-item__title").text.strip()
                prix_raw = driver.find_element(By.CSS_SELECTOR, "h4.listing-item__price").text.strip()
                adresse = driver.find_element(By.CSS_SELECTOR, "span.listing-item__address-location").text.strip()
                proprietaire = driver.find_element(By.CSS_SELECTOR, "h4.listing-item-sidebar__author-name").text.strip()

                atts = driver.find_elements(By.CSS_SELECTOR, "ul.listing-item__attribute-list li")
                kilometrage_raw = atts[0].text if len(atts) > 0 else ""
                année_raw = atts[1].text if len(atts) > 1 else ""
                boite = atts[2].text if len(atts) > 2 else ""
                carburant = atts[3].text if len(atts) > 3 else ""

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
                    "boite": boite.replace("Boîte", "").strip(),
                    "carburant": carburant.replace("Carburant", "").strip(),
                    "propriétaire": proprietaire,
                    "url": detail_url
                })
                time.sleep(1)  # Pause pour éviter de surcharger le serveur

            except Exception as e:
                print(f"Erreur dans le scraping de l'annonce {detail_url} : {e}")
                continue

        print(f"Page {page} terminée : {len(detail_urls)} annonces récupérées")

    driver.quit()
    return all_data


# Exemple d'utilisation
#if __name__ == "__main__":
 #   annonces = scrape_annonces("https://dakar-auto.com/senegal/voitures-4?page=", 1)
 #   df = pd.DataFrame(annonces)
 #   print(df.head())


# Exemple d'utilisation :
# data = scrape_annonces('https://dakar-auto.com/senegal/voitures-4?page=', 5)
# https://dakar-auto.com/senegal/voitures-4 -> page 1 à 2753
# https://dakar-auto.com/senegal/motos-and-scooters-3 -> page 1 à 54
# https://dakar-auto.com/senegal/location-de-voitures-19 -> page 1 à 8

