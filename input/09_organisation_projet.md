# Organisation du projet

## Socle commun

Chaque bloc de travail doit être découpé en tâches simples, puis en petites manipulations ou implémentations. La personne assignée doit comprendre son bloc, ses tâches et ce qu'elle implémente avant de commencer.

Pour chaque bloc, la personne responsable produit un résumé court expliquant :

- l'objectif du bloc ;
- son utilisation ;
- son fonctionnement ;
- ce qui a été fait ;
- ce qui reste à faire ou à valider.

Une seule phrase peut suffire si le sujet est simple. L'objectif est que toute l'équipe puisse comprendre le travail réalisé, même si une seule personne l'a produit.

## Gestion des blocages

Règle principale :

- Si un problème dure plus de 15 minutes, il devient un blocage.

Action à faire :

- Créer un ticket sur Notion.
- Décrire le problème avec un maximum de précision.
- Ajouter les captures d'écran utiles.
- Ajouter les commandes lancées si nécessaire.
- Ajouter les erreurs observées.
- Expliquer ce qui a déjà été testé.
- En parler à l'équipe.

Objectif :

- Ne pas perdre une demi-journée sur un problème isolé.
- Rendre le blocage visible.
- Permettre à un autre membre de reprendre ou d'aider rapidement.

## Sauvegarde et suivi GitHub

Règles :

- Push sur GitHub toutes les heures en backup.
- Les livrables sont produits et stabilisés par demi-journée.
- Chaque push doit correspondre à un état compréhensible du projet.
- Les fichiers doivent être nommés clairement selon leur fonction.

Objectif :

- Éviter la perte de travail.
- Garder un historique exploitable.
- Faciliter la reprise par un autre membre.

## Architecture de projet

Règles :

- Toujours respecter une architecture répétable et claire.
- Nommer chaque fichier selon sa fonction.
- Éviter les fichiers fourre-tout.
- Regrouper les éléments par rôle : description robot, simulation, lancement, configuration RViz, documentation, tests.
- Garder les conventions de nommage cohérentes entre URDF, topics ROS et scripts.

Objectif :

- Rendre le projet lisible.
- Réduire les erreurs de chemin ou de nommage.
- Permettre une démonstration fiable.

## Fonctionnement par bloc

Pour chaque bloc, définir :

- responsable ;
- objectif ;
- tâches ;
- petites manipulations à réaliser ;
- livrable attendu ;
- critère de validation ;
- résumé à partager à l'équipe.

Exemple de résumé attendu :

> Bloc URDF : j'ai défini la structure simplifiée du robot avec un corps central, six pattes et des articulations nommées pour correspondre aux futurs messages `/joint_states`.

## Rythme de travail conseillé

| Moment | Action |
|---|---|
| Début de demi-journée | Relire objectifs, blocages et livrables attendus |
| Pendant le travail | Découper les tâches, documenter les décisions, créer un ticket si blocage de plus de 15 minutes |
| Toutes les heures | Push GitHub de backup |
| Fin de demi-journée | Stabiliser les livrables, écrire les résumés, préparer le point professeur |

## Règles de qualité

- Une tâche terminée doit être compréhensible par l'équipe.
- Un fichier doit avoir un rôle clair.
- Un blocage doit être visible rapidement.
- Un livrable doit être présentable à la fin de la demi-journée.
- Une décision technique doit être documentée.
- Le MVP reste prioritaire sur les fonctionnalités avancées.
