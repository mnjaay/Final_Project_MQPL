from abc import ABC, abstractmethod
import datetime

"""
Module de gestion de projet avec des classes .
"""


class Projet:
    """Classe représentant un projet avec ses attributs et méthodes associés."""

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
        """Ajoute un nouveau risque au projet."""
        self.risques.append(risque)

    def ajouter_jalon(self, jalon):
        """Ajoute un nouveau jalon au projet."""
        self.jalons.append(jalon)

    def enregistrer_changement(self, description):
        """Ajoute un nouveau changement au projet."""
        changement = Changement(
            description,
            self.versions,
            datetime.date.today())
        self.changements.append(changement)

    def ajouter_membre_equipe(self, membre):
        """Ajoute un nouveau membre dans l'equipe au projet."""
        self.equipe.ajouter_membre(membre)

    def definir_budget(self, budget):
        """Met à jour le budget du projet."""
        self.budget = budget

    def generer_rapport_performance(self):
        """Génère un rapport de performance du projet."""
        print(f"| Rapport d'activité du projet '{self.nom}'")
        print(f"| version {self.versions}")
        print(f"| Date :  {self.date_debut} à {self.date_fin}")
        print(f"| Budget : {self.budget} XOF")
        for tache in self.taches:
            print(
                f"| - {tache.nom} ({tache.date_debut}, {tache.date_fin}), "
                f"Responsable : {tache.responsable.nom}, "
                f"Statut : {tache.statut}"
            )
        print("| Jalons : ")
        for jalon in self.jalons:
            print(f"| - {jalon.nom} ({jalon.date})")
        print("| Risques : ")
        for risque in self.risques:
            print(
                f"| - {risque.description} "
                f"(Probabilité : {risque.probabilite}, "
                f"Impact : {risque.impact})"
            )
        print("| Chemin Critique : ")
        for tache in self.chemin_critique:
            print(f"- {tache.nom} ({tache.date_debut}, {tache.date_fin})")

    def calculer_chemin_critique(self):
        """Calcule le chemin critique."""
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
            self.notification_context.notifier(message, destinataires)


class Tache:
    """
    Classe représentant une tache avec ses attributs et méthodes associés.
    """

    def __init__(self, nom, description, date_debut, date_fin, responsable, statut):
        """Initialise une nouvelle tache."""
        self.nom = nom
        self.description = description
        self.date_debut = date_debut
        self.date_fin = date_fin
        self.responsable = responsable
        self.statut = statut
        self.dependances = []

    def mettre_a_jour_statut(self, statut):
        """Met à jour le statut de la tâche."""
        self.statut = statut

    def ajouter_dependance(self, tache):
        """Ajoute une dépendance à la tâche."""
        self.dependances.append(tache)


class Equipe:
    """Classe représentant une équipe et ses méthodes associées."""

    def __init__(self):
        """Initialise une nouvelle équipe."""
        self.membres = []

    def ajouter_membre(self, membre):
        """Ajoute un nouveau membre à l'équipe."""
        self.membres.append(membre)

    def obtenir_membre(self):
        """Obtient les membres de l'équipe."""
        return self.membres


class Membre:
    """Classe représentant un membre d'équipe."""

    def __init__(self, nom, role):
        """Initialise un nouveau membre."""
        self.nom = nom
        self.role = role


class Jalon:
    """Classe représentant un jalon dans le projet."""

    def __init__(self, nom, date):
        """Initialise un nouveau jalon."""
        self.nom = nom
        self.date = date


class Risque:
    """Classe représentant un risque dans le projet."""

    def __init__(self, description, probabilite, impact):
        """Initialise un nouveau risque."""
        self.description = description
        self.probabilite = probabilite
        self.impact = impact


class Changement:
    """Classe représentant un changement dans le projet."""

    def __init__(self, description, version, date):
        """Initialise un nouveau changement."""
        self.description = description
        self.version = version
        self.date = date


class NotificationContext:
    """Classe représentant le contexte de notification."""

    def __init__(self, strategy):
        """Initialise le contexte de notification."""
        self.strategy = strategy

    def notifier(self, message, destinataires):
        """Envoie une notification selon la stratégie définie."""
        if self.strategy:
            self.strategy.envoyer(message, destinataires)


class NotificationStrategy(ABC):
    """Interface pour les stratégies de notification."""

    @abstractmethod
    def envoyer(self, message, destinataire):
        """Méthode pour envoyer une notification."""
        pass


class EmailNotificationStrategy(NotificationStrategy):
    """Stratégie de notification par email."""

    def envoyer(self, message, destinataire):
        """Envoie une notification par email."""
        print(f"Notification envoyée à {destinataire} par Email: {message}")


class SMSNotificationStrategy(NotificationStrategy):
    """Stratégie de notification par SMS."""

    def envoyer(self, message, destinataire):
        """Envoie une notification par SMS."""
        print(f"Notification envoyée à {destinataire} par SMS: {message}")


class PushNotificationStrategy(NotificationStrategy):
    """Stratégie de notification par push."""

    def envoyer(self, message, destinataire):
        """Envoie une notification par push."""
        print(f"Notification envoyée à {destinataire} par Push: {message}")
