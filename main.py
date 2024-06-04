import datetime

from index import Projet, Tache, Membre, Jalon, Risque, EmailNotificationStrategy, SMSNotificationStrategy
def main():
    # Créer un projet
    projet = Projet(
      "Développement d'une application web",
       "Projet pour développer une application web pour la gestion des tâches",
        datetime.date(2024, 7, 1),
        datetime.date(2024, 12, 1)
    )

    # Ajouter des membres de l'équipe
    membre1 = Membre("Mor", "Développeuse")
    membre2 = Membre("Moukhtar", "Designer")
    projet.ajouter_membre_equipe(membre1)
    projet.ajouter_membre_equipe(membre2)
    projet.set_notification_strategy(EmailNotificationStrategy())
    projet.notifier(
        "Vous avez ete ajouté a l'equipe",
        [membre1.nom,membre2.nom]
    )

    # Ajouter des tâches
    tache1 = Tache(
        "Conception",
        "Conception de l'interface utilisateur",
        datetime.date(2024, 6, 1),
        datetime.date(2024, 6, 30),
        membre2,
        "En cours"
    )
    tache2 = Tache(
        "Développement backend",
        "Développement de l'API",
        datetime.date(2024, 7, 1),
        datetime.date(2024, 8, 31),
        membre1,
        "Non commencé"
    )
    projet.ajouter_tache(tache1)
    projet.ajouter_tache(tache2)


    # Ajouter un risque
    risque1 = Risque("Retard dans le développement", 0.3, 0.7)
    projet.ajouter_risque(risque1)

    # Enregistrer un changement
    projet.enregistrer_changement("Changement de la date de livraison du prototype")

    # Définir une stratégie de notification (Email)
    projet.set_notification_strategy(EmailNotificationStrategy())
    projet.notifier(
        "Le projet a été mis à jour avec de nouvelles informations.",
        membre1.nom
    )

    # Changer la stratégie de notification (SMS)
    projet.set_notification_strategy(SMSNotificationStrategy())
    projet.notifier(
        "La date de livraison du prototype a été changée.",
        membre1.nom
    )
    # Ajouter des jalon
    jalon1 = Jalon("Phase 1 Terminée ","2024-12-12")
    projet.ajouter_jalon(jalon1)

    projet.definir_budget(250000)

    projet.generer_rapport_performance()


if __name__ == "__main__":
    main()