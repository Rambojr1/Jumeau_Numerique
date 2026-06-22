# Analyse des risques

## Tableau des risques

| ID | Risque | Cause probable | Impact | Probabilité | Gravité | Criticité | Prévention | Plan de secours | Responsable |
|---|---|---|---|---|---|---|---|---|---|
| R01 | Partir trop vite dans le code sans cadrage | Volonté de produire rapidement | Interfaces incohérentes, pertes de temps | Élevée | Élevée | Élevée | Valider feuille de route avant développement | Revenir au périmètre minimum et figer les interfaces | Tao |
| R02 | Perdre du temps sur un URDF trop détaillé | Recherche de fidélité mécanique excessive | RViz retardé, modèle incomplet | Moyenne | Élevée | Élevée | Fixer un niveau de détail fonctionnel | Utiliser géométries simples et documenter les approximations | Rémy |
| R03 | Interfaces ROS mal définies | Producteurs/consommateurs non clarifiés | Simulation et visualisation incompatibles | Moyenne | Élevée | Élevée | Faire un tableau interfaces avant code | Réduire aux messages indispensables | Clément |
| R04 | Simulation trop ambitieuse | Confusion avec simulation physique complète | Retard, comportement non démontrable | Moyenne | Élevée | Élevée | Définir un scénario simple pour `sim_hexa.py` | Publier seulement des états articulaires simples | Clément |
| R05 | Mauvaise répartition du travail | Rôles flous ou doublons | Attente, travaux redondants, trous de couverture | Moyenne | Moyenne | Moyenne | Attribuer un responsable par lot | Réaffecter les lots au point quotidien | Tao |
| R06 | Absence de critères de validation | Livrables définis trop vaguement | Impossible de savoir si le projet est réussi | Moyenne | Élevée | Élevée | Définir un critère par lot et jalon | Demander critères au professeur et simplifier la démonstration | Tao |
| R07 | RViz non fonctionnel en fin de projet | URDF, frames ou états articulaires non cohérents | Perte de la preuve visuelle principale | Moyenne | Élevée | Élevée | Valider RViz dès que possible | Démonstration avec modèle simplifié et états fixes | Rémy |
| R08 | Confusion entre jumeau numérique, simulation physique complète et simple visualisation | Sujet interprété trop largement | Travail hors périmètre | Moyenne | Élevée | Élevée | Faire confirmer le niveau attendu | Recentrer sur RViz + simulation simple | Tao |
| R09 | Documentation faite trop tard | Priorité donnée au développement | Soutenance confuse, choix non justifiés | Moyenne | Moyenne | Moyenne | Documenter à chaque demi-journée | Reconstituer uniquement les décisions majeures | Tao |
| R10 | Soutenance préparée à la dernière minute | Support visuel repoussé à la fin | Message peu clair malgré un prototype correct | Moyenne | Moyenne | Moyenne | Prévoir le plan des slides dès le cadrage | Utiliser synthèse professeur comme base du support | Tao |
| R11 | Dépendance trop forte à une seule personne | Coordination ou savoir technique centralisé | Blocage si indisponibilité ou surcharge | Moyenne | Moyenne | Moyenne | Partager les décisions et fichiers de cadrage | Redistribuer les lots avec critères simples | Tao |
| R12 | Manque de validation avec le professeur | Questions non posées au bon moment | Travail sur de mauvaises hypothèses | Moyenne | Élevée | Élevée | Préparer questions courtes à chaque point | Adapter la feuille de route dès validation | Tao |
| R13 | Mauvaise gestion des frames ROS | Nommage ou axes incohérents | Robot mal affiché, articulation difficile à comprendre | Moyenne | Élevée | Élevée | Tenir une liste de frames et conventions | Repartir d'une arborescence simplifiée | Rémy |
| R14 | Perte de temps sur Gazebo si ce n'est pas demandé | Assimilation simulation = Gazebo | Retard sur RViz et `sim_hexa.py` | Moyenne | Élevée | Élevée | Demander explicitement si Gazebo est attendu | Déclarer Gazebo hors périmètre et se concentrer sur RViz | Tao |

## Trois risques prioritaires à surveiller

1. Interfaces ROS mal définies.
2. URDF trop détaillé ou incohérent.
3. Simulation trop ambitieuse par rapport au temps disponible.

## A. Parties rapides à traiter

- Squelette théorique du paquet ROS.
- Tableau initial des topics.
- Structure documentaire.
- Premier schéma d'architecture ROS.
- Planning sur cinq demi-journées.
- Liste des questions professeur.

## B. Points durs

- Cohérence URDF.
- Articulation des 18 servos si l'hexapode a 6 pattes et 3 axes par patte.
- Transformation des frames.
- Simulation réaliste sans surcomplexifier.
- Affichage propre dans RViz.
- Choix du niveau de détail acceptable.
- Correspondance entre noms d'articulations URDF et états publiés.

## C. Égarements à éviter

- Vouloir faire une simulation Gazebo complète si ce n'est pas demandé.
- Passer trop de temps sur le design visuel.
- Coder avant de définir les interfaces.
- Chercher la perfection mécanique.
- Négliger la présentation professeur.
- Confondre prototype de simulation et produit final.
- Ajouter des services ou actions ROS sans scénario d'utilisation.
