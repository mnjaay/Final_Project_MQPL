import datetime
from abc import ABC, abstractmethod

class Projet:
    def __init__(self, nom, description, date_debut, date_fin):
        self.nom = nom
        self.description = description
        self.date_debut = date_debut
        self.date_fin = date_fin
        self.budget = 0.0
        self.taches = []
        self.equipe = Equipe()
        self.risques = []
        self.jalons = []
        self.versions = 1
        self.changements = []
        self.chemin_critique = []
        self.notification_context = NotificationContext(None)

    def set_notification_strategy(self, notification_strategy):
        self.notification_context = NotificationContext(notification_strategy)

    def ajouter_tache(self, tache):
        self.taches.append(tache)
        self.chemin_critique.append(tache)

    def ajouter_risque(self, risque):
        self.risques.append(risque)

    def ajouter_jalon(self, jalon):
        self.jalons.append(jalon)

    def enregistrer_changement(self, description):
        changement = Changement(description, self.versions, datetime.date.today())
        self.changements.append(changement)

    def ajouter_membre_equipe(self, membre):
        self.equipe.ajouter_membre(membre)

    def definir_budget(self, budget):
        self.budget = budget

    def generer_rapport_performance(self):
        print(f"--------------------------------------------------------------------------------- ")

        print(f"| Rapport d'activite du projet '{self.nom}'")
        print(f"| version {self.versions}")
        print(f"| Date :  {self.date_debut} a {self.date_fin}")
        print(f"| Budget : {self.budget} XOF")
        print(f"| Taches : ")
        for tache in self.taches:
            print(f"| - {tache.nom} ({tache.date_debut} a {tache.date_fin}) , Responsable : {tache.responsable.nom} , Statut : {tache.statut}")
        print(f"| Jalons : ")
        for jalon in self.jalons:
            print(f"| - {jalon.nom} ({jalon.date})")
        print(f"| Risque : ")
        for risque in self.risques:
            print(f"| - {risque.description} (Probabilite :{risque.probabilite} Impact : {risque.impact})")
        print(f"| Chemin Critique : ")

        for tache in self.chemin_critique:
            print(f"| - {tache.nom} ({tache.date_debut} a {tache.date_fin}) ")

        print(f"--------------------------------------------------------------------------------- ")


    def calculer_chemin_critique(self):
        pass

    def notifier(self, message, destinataires):
        if self.notification_context is not None:
            self.notification_context.notifier(message, destinataires)


class Tache:
    def __init__(self, nom, description, date_debut, date_fin, responsable, statut):
        self.nom = nom
        self.description = description
        self.date_debut = date_debut
        self.date_fin = date_fin
        self.responsable = responsable
        self.statut = statut
        self.dependances = []

    def modifier_statut(self, statut):
        self.statut = statut

    def ajouter_dependance(self, tache):
        self.dependances.append(tache)


class Equipe:
    def __init__(self):
        self.membres = []

    def ajouter_membre(self, membre):
        self.membres.append(membre)

    def obtenir_membre(self):
        return self.membres


class Membre:
    def __init__(self, nom, role):
        self.nom = nom
        self.role = role


class Jalon:
    def __init__(self, nom, date):
        self.nom = nom
        self.date = date


class Risque:
    def __init__(self, description, probabilite, impact):
        self.description = description
        self.probabilite = probabilite
        self.impact = impact


class Changement:
    def __init__(self, description, version, date):
        self.description = description
        self.version = version
        self.date = date


class NotificationContext:
    def __init__(self, strategy):
        self.strategy = strategy

    def notifier(self, message, destinataires):
        if self.strategy:
            self.strategy.envoyer(message, destinataires)


class NotificationStrategy(ABC):
    @abstractmethod
    def envoyer(self, notification, destinataire):
        pass


class EmailNotificationStrategy(NotificationStrategy):
    def envoyer(self, message, destinataire):
        # Envoyer un email à destinataire avec le message
        print(f"Notification envoyée à {destinataire} par Email: {message}")


class SMSNotificationStrategy(NotificationStrategy):
    def envoyer(self, message, destinataire):
        # Envoyer un SMS à destinataire avec le message
        print(f"Notification envoyée à {destinataire} par SMS: {message}")


class PushNotificationStrategy(NotificationStrategy):
    def envoyer(self, message, destinataire):
        # Envoyer une notification push à destinataire avec le message
        print(f"Notification envoyée à {destinataire} par Push: {message}")


