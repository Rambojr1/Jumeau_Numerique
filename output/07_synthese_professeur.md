# Synthèse professeur - Projet 1 : Jumeau numérique

## 1. Compréhension du sujet

Nous devons développer un paquet ROS permettant de visualiser l'hexapode dans RViz et de simuler simplement son fonctionnement. Le projet couvre les interfaces ROS, l'URDF, un noeud `sim_hexa.py` et une soutenance finale. La première demi-journée est réservée au cadrage : feuille de route, lots, jalons, livrables, rôles et risques.

## 2. Choix d'organisation

- Tao pilote la coordination technique, la feuille de route et les points professeur.
- Clément pilote les interfaces ROS, la structure logique du paquet et la stratégie `sim_hexa.py`.
- Rémy pilote l'URDF, RViz, les frames et la validation visuelle.
- Le projet est découpé en lots : cadrage, interfaces, structure paquet, URDF, RViz, simulation, tests, documentation, soutenance.

## 3. Planning sur 5 demi-journées

| Demi-journée | Objectif |
|---|---|
| 1 | Cadrage, lots, rôles, risques, planning |
| 2 | Interfaces ROS + squelette paquet |
| 3 | URDF + RViz |
| 4 | Simulation simple + tests |
| 5 | Stabilisation + documentation + soutenance |

## 4. Premiers risques identifiés

- Interfaces ROS mal définies.
- URDF trop détaillé ou trop long à stabiliser.
- Simulation trop ambitieuse par rapport au temps disponible.
- RViz non fonctionnel en fin de projet.
- Documentation et soutenance préparées trop tard.

## 5. Questions à poser

- Quelle version de ROS doit être utilisée ?
- Le niveau attendu est-il RViz uniquement ou RViz + simulation plus avancée ?
- Le modèle URDF doit-il être géométriquement fidèle ou seulement fonctionnel ?
- Le comportement de `sim_hexa.py` doit-il simuler les moteurs, les trajectoires ou seulement publier des états articulaires ?
- Gazebo est-il attendu ou hors périmètre ?
- Quels critères précis valident le projet ?

## 6. Objectifs de la prochaine demi-journée

- Valider les hypothèses critiques avec le professeur.
- Définir le tableau des topics, services et actions.
- Produire un premier schéma d'architecture ROS.
- Définir la structure théorique du paquet sans créer encore de livrable technique complet.

## Mini checklist pour le point d'avancement

- Périmètre du projet confirmé.
- Rôles Tao / Clément / Rémy validés.
- Planning en cinq demi-journées présenté.
- Trois risques prioritaires annoncés.
- Questions professeur posées avant développement.
