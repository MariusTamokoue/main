import argparse
from datetime import datetime
import requests
import json

def analyser_commande():
    """
    Générer un interpréteur de commande.

    Returns:
        Un objet Namespace tel que retourné par parser.parse_args().
        Cet objet aura l'attribut «symboles» représentant la liste des
        symboles à traiter, et les attributs «début», «fin» et «valeur»
        associés aux arguments optionnels de la ligne de commande.
    """
    parser = argparse.ArgumentParser('Extraction de valeurs historiques pour un ou plusieurs symboles boursiers.')
    
    parser.add_argument("symbols", nargs="+", help="Nom d'un symbole boursier")
    parser.add_argument("-h", "--help", help = "show this help message and exit")
    parser.add_argument("-d", "--date debut", help="Date recherchée la plus ancienne (format: AAAA-MM-JJ)")
    parser.add_argument("-f", "--date fin", help="Date recherchée la plus récente (format: AAAA-MM-JJ)")
    parser.add_argument("-v", "--valeur", choices=["fermeture", "ouverture", "min", "max", "volume"], default="fermeture", help="Valeur désirée")
    # Complétez le code ici
    # vous pourriez aussi avoir à ajouter des arguments dans ArgumentParser(...)

    return parser.parse_args()


def produire_historique(nom, debut, fin, valeur_desirée):
    return (debut, valeur_desirée)   

 
symbole = 'HOG'
url = f'https://pax.ulaval.ca/action/{symbole}/historique/'

params = {
    'début': '2019-02-18',
    'fin': '2019-02-24',
}

réponse = requests.get(url=url, params=params)

réponse = json.loads(réponse.text)
print(réponse)

for clé in réponse.keys():
    print(clé)
    
