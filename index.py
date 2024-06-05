import datetime
from abc import ABC, abstractmethod


class Projet:
    """Classe représentant un
     projet avec ses attributs et méthodes associés."""

    def __init__(self, nom, description, date_debut, date_fin):
        """Initialise un nouveau projet."""
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
        """Définit la stratégie de notification du projet."""
        self.notification_context = NotificationContext(notification_strategy)

    def ajouter_tache(self, tache):
        """Ajoute une nouvelle tâche au projet."""
        self.taches.append(tache)
        self.chemin_critique.append(tache)

    def ajouter_risque(self, risque):
        """Ajoute un nouveau risque  au projet."""

        self.risques.append(risque)

    def ajouter_jalon(self, jalon):
        """Ajoute un nouveau jalon  au projet."""
        self.jalons.append(jalon)

    def enregistrer_changement(self, description):
        """Ajoute un nouveau changement  au projet."""

        changement = Changement(
            description,
            self.versions,
            datetime.date.today())

        self.changements.append(changement)

    def ajouter_membre_equipe(self, membre):
        """Ajoute un nouveau membre dans l'equipe  au projet."""
        self.equipe.ajouter_membre(membre)

    def definir_budget(self, budget):
        """definir le bidget du projet."""
        self.budget = budget

    def generer_rapport_performance(self):
        """genrer un rapport de performance du projet."""

        print("| Rapport d'activite du projet '{}'".format(self.nom))
        print("| version {}".format(self.versions))
        print("| Date :  {} a {}".format(self.date_debut, self.date_fin))
        print("| Budget : {} XOF".format(self.budget))
        print("| Taches : ")
        for tache in self.taches:
            print(
                "| - {} ({}, {}), Responsable : {}, Statut : {}".format(
                    tache.nom,
                    tache.date_debut,
                    tache.date_fin,
                    tache.responsable.nom,
                    tache.statut,
                )
            )
        print("| Jalons : ")
        for jalon in self.jalons:
            print("| - {} ({})".format(jalon.nom, jalon.date))
        print("| Risque : ")
        for risque in self.risques:
            print(
                "| - {} (Probabilite :{}, Impact : {})".format(
                    risque.description, risque.probabilite, risque.impact
                )
            )
        print("| Chemin Critique : ")

        for tache in self.chemin_critique:
            print("- {} ({}, {}) ".format(
                tache.nom,
                tache.date_debut,
                tache.date_fin))

    def calculer_chemin_critique(self):
        """
        Calculer le chemin critique.
        """

        for tache in self.taches:
            if not tache.dependances:
                self.chemin_critique.append([tache])
            else:
                for dep in tache.dependances:
                    for chemin in self.chemin_critique:
                        if chemin[-1] == dep:
                            nouveau_chemin = list(chemin)
                            nouveau_chemin.append(tache)
                            self.chemin_critique.append(nouveau_chemin)

        chemin_critique = max(self.chemin_critique, key=len)
        self.chemin_critique = chemin_critique

        print("Chemin critique:")
        for tache in self.chemin_critique:
            print(f"- {tache.nom} ({tache.date_debut}, {tache.date_fin})")

    def notifier(self, message, destinataires):
        """Envoie une notification selon la stratégie définie."""
        if self.notification_context is not None:
            (self.notification_context.notifier(message, destinataires))


class Tache:
    """
    Classe représentant une tache avec ses attributs et méthodes associés.
    """

    def __init__(
            self,
            nom,
            description,
            date_debut,
            date_fin,
            responsable,
            statut):
        """Initialise une nouvelle tache."""

        self.nom = nom
        self.description = description
        self.date_debut = date_debut
        self.date_fin = date_fin
        self.responsable = responsable
        self.statut = statut
        self.dependances = []

    def mettre_a_jour_statut(self, statut):
        self.statut = statut

    def ajouter_dependance(self, tache):
        self.dependances.append(tache)


class Equipe:
    """Cree la classe Equipe et ses methodes et attribut
    ."""

    def __init__(self):
        """Initialise un nouveau membre."""
        self.membres = []

    def ajouter_membre(self, membre):
        """ajoute un nouveau membre."""
        self.membres.append(membre)

    def obtenir_membre(self):
        """obtenir les membres."""
        return self.membres


class Membre:
    """la classe membre avec ses methodes et attribut"""

    def __init__(self, nom, role):
        """initialise la classe membre"""
        self.nom = nom
        self.role = role


class Jalon:
    """la classe jalon avec ses methodes et attribut"""

    def __init__(self, nom, date):
        """initialise la classe jalon"""
        self.nom = nom
        self.date = date


class Risque:
    """la classe risque avec ses methodes et attribut"""

    def __init__(self, description, probabilite, impact):
        """initialise la classe risque"""
        self.description = description
        self.probabilite = probabilite
        self.impact = impact


class Changement:
    """la classe Changement avec ses methodes et attribut"""

    def __init__(self, description, version, date):
        """initialise la classe changement"""
        self.description = description
        self.version = version
        self.date = date


class NotificationContext:
    """la classe NotificationContext avec ses methodes et attribut"""

    def __init__(self, strategy):
        """initialise la classe NotificationContext"""
        self.strategy = strategy

    def notifier(self, message, destinataires):
        """Notifier les membres avec un message"""
        if self.strategy:
            self.strategy.envoyer(message, destinataires)


class NotificationStrategy(ABC):
    """l'interface NotificationStrategy  avec ses methodes"""

    @abstractmethod
    def envoyer(self, message, destinataire):
        pass


class EmailNotificationStrategy(NotificationStrategy):
    """la Classe EmailNotificationStrategy
    qui herite de NotificationStrategy"""

    def envoyer(self, message, destinataire):
        """La methode envoyer par email"""
        print("Notification envoyée à {} par Email: {}"
              .format(destinataire, message))


class SMSNotificationStrategy(NotificationStrategy):
    """la Classe SMSNotificationStrategy qui herite de NotificationStrategy"""

    def envoyer(self, message, destinataire):
        """La methode envoyer par sms"""
        print("Notification envoyée à {} par SMS: {}"
              .format(destinataire, message))


class PushNotificationStrategy(NotificationStrategy):
    """la Classe PushNotificationStrategy qui herite de NotificationStrategy"""

    def envoyer(self, message, destinataire):
        """La methode envoyer par push"""
        print("Notification envoyée à {} par Push: {}"
              .format(destinataire, message))
