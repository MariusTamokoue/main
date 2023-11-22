"""
    Phase2
     conserver l'historique des transactions effectuées dans le temps,
     à savoir quand a-t-on acheté ou vendu quoi et à quel prix, ainsi
     qu'à calculer des rendements historiques pour nos investissements.
"""
import phase1
from datetime import datetime, timedelta


class Bourse:
    def prix(symbole, dateEnter):
        if dateEnter > datetime.now().date:
            raise TimeoutError("La date spécifié est postérieur à la date du jour")
            
        historique = phase1.produire_historique(symbole, dateEnter)
        
        prix_fermeture = None
        
        for date_historique, prix_historique in historique:
            if date_historique <= dateEnter:
                prix_fermeture = prix_historique
                
        return prix_fermeture