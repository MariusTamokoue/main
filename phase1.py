import argparse
from datetime import datetime, date
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
    parser = argparse.ArgumentParser(
        'Extraction de valeurs historiques pour un ou plusieurs symboles boursiers.')
    parser.add_argument("symbols", nargs="+", help="Nom d'un symbole boursier")
    #parser.add_argument("-h", "--help", help = "show this help message and exit")
    parser.add_argument(
     "-d", "--date_debut", help="Date recherchée la plus ancienne (format: AAAA-MM-JJ)")
    parser.add_argument("-f", "--date_fin", help="Date recherchée la plus récente 
                        "(format: AAAA-MM-JJ)")
    parser.add_argument("-v", "--valeur", choices=["fermeture", "ouverture", "min",
                        "max", "volume"], default="fermeture", help="Valeur désirée")
    # Complétez le code ici
    # vous pourriez aussi avoir à ajouter des arguments dans ArgumentParser(...)

    return parser.parse_args()


def produire_historique(nom, debut, fin, valeur_desirée):
    #symbole = 'GOOG'
    url = f'https://pax.ulaval.ca/action/{nom}/historique/'

    params = {
        'début': debut,
        'fin': fin,
    }

    réponse = requests.get(url=url, params=params)

    if réponse.status_code == 200:
        réponse = json.loads(réponse.text)
        #print(réponse)
        affichage = []
      
        for valeur_date, valeurs in réponse['historique'].items(): 
            try:
                date = datetime.strptime(valeur_date, '%Y-%m-%d').date()
            except ValueError:
                continue  
            valeur = valeurs.get(valeur_desirée)
            
            if valeur is not None:
                affichage.append((date, valeur))         
        #print (affichage)
        return affichage
    else:
        print(f'Erreur lors de la requête: {réponse.status_code}')
        return None
    
def afficher_historique(nom, debut, fin, valeur_desirée, réponse):
    print (f'titre={nom}: valeur={valeur_desirée}, début={debut}, fin={fin}')
    print(réponse)
        
if __name__ == '__main__':
    args = analyser_commande()
    start = args.date_debut if args.date_debut else date.today().isoformat()
    end = args.date_fin if args.date_fin else date.today().isoformat()
    
    for symbole in args.symbols:
        historique = produire_historique(symbole,start, end, args.valeur)
        if historique is not None:
            afficher_historique(symbole, start, end, args.valeur, historique)