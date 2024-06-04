import unittest
import datetime
from index import Projet, Tache, Equipe, Membre, Jalon, Risque, Changement, EmailNotificationStrategy, SMSNotificationStrategy, PushNotificationStrategy

class TestProjet(unittest.TestCase):

    def setUp(self):
        # Préparer un projet pour les tests

        self.projet = Projet(
            "Développement d'une application web",
            "Projet pour développer une application web pour la gestion des tâches",
             datetime.date(2024, 10, 1),
             datetime.date(2024, 12, 1)
        )
        self.membre1 = Membre("Mor", "Développeur")
        self.membre2 = Membre("Moukhtar", "Designer")
        self.tache1 = Tache(
            "Conception",
            "Conception de l'interface utilisateur",
            datetime.date(2024, 6, 1),
            datetime.date(2024, 6, 30),
            self.membre2,
            "En cours"
        )
        self.tache2 = Tache(
            "Développement backend",
            "Développement de l'API",
            datetime.date(2024, 7, 1),
            datetime.date(2024, 8, 31),
            self.membre1,
            "Non commencé"
        )

    def test_ajouter_membre_equipe(self):
        self.projet.ajouter_membre_equipe(self.membre1)
        self.projet.ajouter_membre_equipe(self.membre2)
        self.assertEqual(len(self.projet.equipe.obtenir_membre()), 2)
        self.assertEqual(self.projet.equipe.obtenir_membre()[0].nom, "Mor")
        self.assertEqual(self.projet.equipe.obtenir_membre()[1].nom, "Moukhtar")


    def test_ajouter_tache(self):
        self.projet.ajouter_tache(self.tache1)
        self.projet.ajouter_tache(self.tache2)
        self.assertEqual(len(self.projet.taches), 2)
        self.assertEqual(self.projet.taches[0].nom, "Conception")
        self.assertEqual(self.projet.taches[1].nom, "Développement backend")

    def test_ajouter_jalon(self):
        jalon = Jalon("Prototype fini", datetime.date(2024, 9, 15))
        self.projet.ajouter_jalon(jalon)
        self.assertEqual(len(self.projet.jalons), 1)
        self.assertEqual(self.projet.jalons[0].nom, "Prototype fini")

    def test_ajouter_risque(self):
        risque = Risque("Retard dans le développement", 0.3, 0.7)
        self.projet.ajouter_risque(risque)
        self.assertEqual(len(self.projet.risques), 1)
        self.assertEqual(self.projet.risques[0].description, "Retard dans le développement")

    def test_enregistrer_changement(self):
        self.projet.enregistrer_changement("Changement de la date de livraison du prototype")
        self.assertEqual(len(self.projet.changements), 1)
        self.assertEqual(self.projet.changements[0].description, "Changement de la date de livraison du prototype")

    def test_generer_rapport_performance(self):
        self.projet.ajouter_tache(self.tache1)
        self.projet.ajouter_jalon(Jalon("Prototype fini", datetime.date(2024, 9, 15)))
        self.projet.ajouter_risque(Risque("Retard dans le développement", 0.3, 0.7))
        self.projet.definir_budget(1000000)
        self.projet.ajouter_membre_equipe(self.membre1)
        self.projet.generer_rapport_performance()


    def test_notifier_email(self):
        self.projet.set_notification_strategy(EmailNotificationStrategy())
        self.projet.notifier(
            "Le projet a été mis à jour avec de nouvelles informations.",
            [self.membre1.nom, self.membre2.nom]
        )

    def test_notifier_sms(self):
        self.projet.set_notification_strategy(SMSNotificationStrategy())
        self.projet.notifier(
            "La date de livraison du prototype a été changée.",
            [self.membre1.nom, self.membre2.nom]
        )

    def test_notifier_push(self):
        self.projet.set_notification_strategy(PushNotificationStrategy())
        self.projet.notifier(
            "Nouveau jalon ajouté.",
            [self.membre1.nom, self.membre2.nom]
        )

    def test_enregistrement_changement(self):
        self.projet.enregistrer_changement("Des Changements ont ete effectués")



if __name__ == "__main__":
    unittest.main()
