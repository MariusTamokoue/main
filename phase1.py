"""
    Phase1
     traiter les arguments de la ligne de commande, d'une part,
     puis à utiliser ces arguments pour faire appel à un serveur
     qui vous retournera l'information dont vous avez besoin
     pour produire la sortie désirée
"""
import argparse
from datetime import datetime, date
import json
import requests

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
    parser.add_argument("-d", "--date_debut", metavar="DATE", dest="date_debut",
                        help="Date recherchée la plus ancienne (format: AAAA-MM-JJ)")
    parser.add_argument("-f", "--date_fin", metavar="DATE", dest="date_fin",
                        help="Date recherchée la plus récente (format: AAAA-MM-JJ)")
    parser.add_argument("-v", "--valeur", choices=["fermeture", "ouverture", "min",
                        "max", "volume"], default="fermeture", help="Valeur désirée")
    # Complétez le code ici
    # vous pourriez aussi avoir à ajouter des arguments dans ArgumentParser(...)

    return parser.parse_args()


def produire_historique(nom, debut, fin, valeur_desirée):
    """
        Produire l'historique
        Return:
            l'historique en fonction du symbole recu, la date de debut,
            la date de fin et la valeur désirée
    """
    url = f'https://pax.ulaval.ca/action/{nom}/historique/'

    params = {
        'début': debut,
        'fin': fin,
    }
    affichage = []
    réponse = requests.get(url=url, params=params)
    if réponse.status_code == 200:
        réponse = json.loads(réponse.text)
        for valeur_date, valeurs in réponse['historique'].items():
            date_att = datetime.strptime(valeur_date, '%Y-%m-%d').date()
            valeur = valeurs.get(valeur_desirée)
            affichage.append((date_att, valeur))
    return affichage
if __name__ == '__main__':
    args = analyser_commande()
    start = args.date_debut if args.date_debut else args.date_fin
    end = args.date_fin if args.date_fin else date.today().strftime('%Y-%m-%d')
    start = date.fromisoformat(start)
    end = date.fromisoformat(end)
    for symbole in args.symbols:
        print (f'titre={symbole}: valeur={args.valeur}, début={repr(start)}, fin={repr(end)}')
        print(produire_historique(symbole, start, end, args.valeur))
