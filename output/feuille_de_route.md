# Feuille de route globale - Jumeau numérique hexapode

## 1. Contexte du projet

Le projet consiste à développer un paquet ROS  permettant de visualiser l'hexapode dans RViz et de simuler son fonctionnement avec un noeud `sim_hexa.py`.

## 2. Objectif global

L'objectif final est de construire un jumeau numérique ROS 2 de l'hexapode selon une progression maîtrisée :

- obtenir un MVP fonctionnel dans RViz ;
- animer le robot via le topic `/joint_states` ;
- développer un URDF simplifié au départ ;
- faire évoluer l'URDF vers un modèle fidèle à la réalité ;
- stabiliser les interfaces ROS 2 ;
- préparer Gazebo comme objectif final et livrable avancé.

Le MVP prioritaire est :

```text
URDF simplifié + /joint_states + RViz animé par sim_hexa.py
```

## 3. Stratégie technique retenue

La stratégie est itérative : sécuriser d'abord une démonstration RViz, puis enrichir progressivement le modèle et la simulation.

| Étape                       | Objectif                                                       | Résultat attendu                                                   |
| ---------------------------- | -------------------------------------------------------------- | ------------------------------------------------------------------- |
| 1. MVP RViz                  | Obtenir rapidement un robot visible et animé                  | Hexapode affiché dans RViz avec mouvements articulaires simples    |
| 2. Interfaces ROS 2          | Stabiliser les échanges entre les composants                  | Topics, messages et noms d'articulations cohérents                 |
| 3. URDF itératif            | Construire le modèle par niveaux de détail                   | Version simplifiée, puis ajout des éléments mécaniques fidèles |
| 4. Animation `sim_hexa.py` | Publier des états articulaires exploitables                   | Messages `sensor_msgs/JointState` envoyés sur `/joint_states`  |
| 5. Enrichissement progressif | Ajouter les éléments nécessaires à une simulation avancée | Limites, collisions, inerties, masses et transmissions              |
| 6. Passage vers Gazebo       | Préparer la simulation physique                               | Robot exploitable avec contrôleurs et contacts sol                 |

## 4. Périmètre du MVP

Le MVP inclut uniquement les éléments nécessaires à une démonstration visuelle stable :

- URDF simplifié ;
- frames cohérentes ;
- noms d'articulations stables ;
- topic `/joint_states` ;
- message `sensor_msgs/JointState` ;
- `robot_state_publisher` ;
- RViz ;
- noeud `sim_hexa.py`.

Critère MVP :

> L'hexapode est visible dans RViz et ses articulations bougent correctement avec les états publiés par `sim_hexa.py`.

Éléments exclus du MVP :

- simulation physique complète ;
- contacts pied / sol ;
- inerties détaillées ;
- contrôleurs Gazebo ;
- cinématique inverse complexe ;
- actions ROS 2 avancées.

## 5. Évolution vers Gazebo

Gazebo est l'objectif final de simulation avancée. Il intervient après stabilisation du MVP RViz.

Pour passer de RViz à Gazebo, le projet ajoute progressivement :

- géométries de collision ;
- inerties ;
- masses ;
- limites articulaires ;
- transmissions ;
- `ros2_control` ;
- contrôleurs ;
- gestion des contacts pied / sol.

Différence de rôle :

| Outil  | Rôle               | Utilisation dans le projet                                                 |
| ------ | ------------------- | -------------------------------------------------------------------------- |
| RViz   | Visualisation       | Valider la structure, les frames et l'animation                            |
| Gazebo | Simulation physique | Tester le comportement avec gravité, contacts, collisions et contrôleurs |

Règle technique :

> RViz valide la représentation et l'animation. Gazebo valide le comportement physique.

## 6. Lots de travaux

| Lot                        | Objectif                                              | Responsable     | Livrable                                 | Critère de validation                                                  |
| -------------------------- | ----------------------------------------------------- | --------------- | ---------------------------------------- | ----------------------------------------------------------------------- |
| Cadrage technique          | Définir le besoin, les limites et l'ordre de travail | Tao             | Feuille de route globale                 | L'équipe sait quoi produire, dans quel ordre et avec quel périmètre  |
| Interfaces ROS 2           | Définir les échanges entre les composants           | Clément        | Tableau topics/messages/services/actions | Chaque interface a un rôle, un producteur, un consommateur et un type  |
| Structure du paquet        | Organiser les fichiers du projet ROS 2                | Clément        | Architecture de paquet                   | Les dossiers et fichiers sont nommés selon leur fonction               |
| Modélisation URDF         | Décrire le robot en version simplifiée puis fidèle | Rémy           | URDF itératif + liste des frames        | Le modèle couvre le corps, les pattes, les joints et les frames utiles |
| Visualisation RViz         | Afficher le robot et vérifier les frames             | Rémy           | Configuration RViz                       | Le robot est visible, complet et cohérent                              |
| Simulation `sim_hexa.py` | Publier des états articulaires simples               | Clément        | Noeud de simulation                      | `/joint_states` anime les joints définis dans l'URDF                 |
| Tests et validation        | Vérifier la chaîne MVP                              | Tao             | Plan de tests + résultats               | RViz affiche le robot animé sans incohérence majeure                  |
| Documentation              | Garder une trace des choix techniques                 | Tao             | Documentation projet                     | Les décisions, limites et usages sont compréhensibles par l'équipe   |
| Préparation soutenance    | Préparer le support et la démonstration             | Tao             | Slides + scénario oral                  | Le projet est présentable avec une démonstration claire               |
| Extension Gazebo           | Préparer le livrable avancé                         | Clément, Rémy | Plan Gazebo + éléments URDF avancés   | Le modèle devient compatible avec contrôleurs et simulation physique  |

## 7. Rôles de l'équipe

| Personne | Rôle                                                             | Responsabilités principales                                                                      | Livrables clés                                                                  |
| -------- | ----------------------------------------------------------------- | ------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------- |
| Tao      | Coordination, architecture globale, planning, risques, soutenance | Organiser le projet, maintenir la cohérence technique, suivre les risques, préparer les points  | Feuille de route, planning, jalons, risques, synthèse, support de soutenance    |
| Clément | Interfaces ROS 2, structure paquet,`sim_hexa.py`                | Définir les topics/messages, organiser le paquet, spécifier et développer la simulation simple | Tableau interfaces, architecture paquet, spécification et noeud `sim_hexa.py` |
| Rémy    | URDF, frames, RViz, validation visuelle                           | Définir le modèle robot, nommer les joints et frames, configurer RViz, vérifier l'affichage    | URDF itératif, liste des frames, configuration RViz, validation visuelle        |

Principe de fonctionnement :

- une personne pilote chaque lot ;
- les autres contribuent selon les dépendances ;
- chaque décision technique importante est documentée ;
- chaque livrable doit être compréhensible par toute l'équipe.

## 8. Planning sur 5 demi-journées

| Demi-journée | Objectif                                                      | Tâches principales                                                                | Livrables                                                  |
| ------------- | ------------------------------------------------------------- | ---------------------------------------------------------------------------------- | ---------------------------------------------------------- |
| DJ1           | Cadrage, lots, rôles, risques, planning                      | Structurer le projet, répartir les rôles, définir MVP et jalons                 | Feuille de route, lots, rôles, risques, planning          |
| DJ2           | Interfaces ROS 2 + structure paquet                           | Définir `/joint_states`, messages, noms de joints, architecture de fichiers     | Tableau interfaces, schéma architecture, structure paquet |
| DJ3           | URDF MVP + RViz                                               | Construire l'URDF simplifié, organiser les frames, charger le robot dans RViz     | URDF MVP, liste frames, configuration RViz                 |
| DJ4           | `sim_hexa.py` + tests RViz                                  | Publier `sensor_msgs/JointState`, animer les joints, tester la chaîne complète | Noeud `sim_hexa.py`, tests RViz, démo MVP               |
| DJ5           | Stabilisation, documentation, soutenance, préparation Gazebo | Corriger, documenter, préparer la soutenance, planifier l'extension Gazebo        | Documentation finale, support visuel, plan Gazebo          |

## 9. Jalons

| ID  | Jalon                                  | Moment  | Résultat attendu                                                                 | Responsable     |
| --- | -------------------------------------- | ------- | --------------------------------------------------------------------------------- | --------------- |
| J01 | Cadrage validé                        | Fin DJ1 | Périmètre, rôles, lots, risques et MVP définis                                | Tao             |
| J02 | Interfaces définies                   | Fin DJ2 | Interfaces ROS 2 et conventions de nommage stabilisées                           | Clément        |
| J03 | Modèle visuel cadré                  | Fin DJ3 | URDF MVP et RViz opérationnels                                                   | Rémy           |
| J04 | Simulation simple démontrable         | Fin DJ4 | `sim_hexa.py` anime le robot dans RViz via `/joint_states`                    | Clément        |
| J05 | Projet stabilisé et présentable      | Fin DJ5 | Démo MVP, documentation et support de soutenance prêts                          | Tao             |
| J06 | Préparation Gazebo / livrable avancé | Fin DJ5 | Plan d'ajout collisions, inerties, transmissions,`ros2_control` et contrôleurs | Clément, Rémy |

## 10. Livrables attendus

### Par personne

| Personne | Livrables                                                                                                                            |
| -------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| Tao      | Feuille de route globale, planning, jalons, suivi des risques, documentation de synthèse, support de soutenance                     |
| Clément | Tableau interfaces ROS 2, structure du paquet, spécification `sim_hexa.py`, noeud de simulation, préparation contrôleurs Gazebo |
| Rémy    | URDF MVP, liste des frames, configuration RViz, validation visuelle, enrichissements URDF pour Gazebo                                |

### Par demi-journée

| Demi-journée | Livrables                                                                            |
| ------------- | ------------------------------------------------------------------------------------ |
| DJ1           | Feuille de route, lots, rôles, planning, risques                                    |
| DJ2           | Interfaces ROS 2, architecture paquet, conventions de nommage                        |
| DJ3           | URDF MVP, frames, configuration RViz                                                 |
| DJ4           | `sim_hexa.py`, animation `/joint_states`, tests RViz                             |
| DJ5           | Documentation finale, support de soutenance, démonstration stabilisée, plan Gazebo |

## 11. Organisation projet

Règles de travail :

- chaque bloc est découpé en tâches simples ;
- la personne assignée comprend son bloc avant de commencer ;
- chaque bloc produit un court résumé d'utilisation et de fonctionnement ;
- blocage supérieur à 15 minutes = ticket Notion ;
- le ticket Notion contient le problème, les captures, les erreurs, les tests déjà réalisés et le contexte ;
- push GitHub toutes les heures en backup ;
- un livrable présentable est produit à chaque fin de demi-journée ;
- les décisions techniques sont documentées ;
- les fichiers sont nommés selon leur fonction ;
- l'architecture reste répétable et claire ;
- le MVP reste prioritaire sur les fonctionnalités avancées.

Structure de paquet cible :

```text
hexa_simulation/
├── package.xml
├── CMakeLists.txt
├── scripts/
│   └── sim_hexa.py
├── urdf/
│   └── hexapode.urdf
├── launch/
│   └── display.launch.py
├── rviz/
│   └── hexapode.rviz
├── config/
│   └── params.yaml
└── docs/
    └── architecture.md
```

## 12. Risques principaux

| Risque                        | Impact                                                            | Prévention                                                             | Plan de secours                                                                         |
| ----------------------------- | ----------------------------------------------------------------- | ----------------------------------------------------------------------- | --------------------------------------------------------------------------------------- |
| URDF trop ambitieux           | Retard sur RViz et perte de temps sur les détails mécaniques    | Commencer par un URDF MVP avec géométries simples                     | Garder uniquement corps, pattes, joints principaux et frames utiles                     |
| Noms de joints incohérents   | `/joint_states` ne correspond pas à l'URDF, animation bloquée | Définir une convention unique utilisée partout                        | Renommer les joints dans l'URDF et `sim_hexa.py` avant d'ajouter des fonctionnalités |
| RViz non fonctionnel          | Aucune preuve visuelle du MVP                                     | Tester RViz dès que l'URDF MVP existe                                  | Réduire le modèle à une version minimale affichable                                  |
| Simulation trop complexe      | Retard sur la démonstration MVP                                  | Limiter `sim_hexa.py` à la publication de `sensor_msgs/JointState` | Remplacer la marche complexe par un mouvement périodique simple                        |
| Passage Gazebo prématuré    | Blocage sur collisions, inerties, contrôleurs et contacts        | Finaliser RViz avant Gazebo                                             | Repousser Gazebo au livrable avancé et documenter le plan d'intégration               |
| Documentation faite trop tard | Soutenance moins claire, décisions difficiles à expliquer       | Documenter chaque fin de demi-journée                                  | Produire une synthèse courte par lot avec objectif, fonctionnement et limites          |

## 13. Synthèse finale

Le projet suit une stratégie itérative : RViz d'abord pour sécuriser la structure, les frames, les noms d'articulations et l'animation via `/joint_states`, puis enrichissement progressif jusqu'à Gazebo. Le MVP reste prioritaire afin de garantir une démonstration fonctionnelle avant d'ajouter la simulation physique.
