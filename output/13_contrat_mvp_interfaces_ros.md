# Contrat MVP - Interfaces ROS Hexapode (V0)

## 1) Décisions de cadrage

| Point | Décision | Responsable validation | Statut |
|---|---|---|---|
| Version ROS | ROS 2 | Tao | À valider |
| Périmètre MVP | RViz d'abord, Gazebo en livrable ++ | Tao | À valider |
| Interface centrale | /joint_states uniquement au départ | Clément | À valider |
| Critère de réussite MVP | Hexapode visible + articulations qui bougent dans RViz | Équipe | À valider |

## 2) Tableau des interfaces ROS (MVP)

| ID | Interface (topic/service/action) | Type ROS | Message/Type | Producteur | Consommateur | Objectif fonctionnel | Fréquence cible | Priorité MVP | Critère de test |
|---|---|---|---|---|---|---|---|---|---|
| IF-01 | /joint_states | Topic | sensor_msgs/msg/JointState | sim_hexa.py | robot_state_publisher, RViz | Publier les positions articulaires de l'hexapode | 20-50 Hz | Haute | Les joints bougent visuellement dans RViz |
| IF-02 | /robot_description | Topic (param utilisé par RSP) | URDF (string) | launch/config | robot_state_publisher | Charger la description du robot | N/A | Haute | Le robot apparaît complet dans RViz |
| IF-03 | /tf | Topic | tf2_msgs/msg/TFMessage | robot_state_publisher | RViz | Publier les transforms entre frames | Selon pipeline ROS | Haute | Arbre TF cohérent, pas de frame orpheline |
| IF-04 | /hexa/cmd_mode (optionnel) | Topic | std_msgs/msg/String | opérateur/noeud simple | sim_hexa.py | Changer un mode d'animation simple (repos/marche) | 1-5 Hz | Basse (optionnel) | Le mode change sans casser la démo |

Règle MVP:
- Pas de services/actions tant que IF-01, IF-02 et IF-03 ne sont pas stables.

## 3) Conventions de nommage des articulations (à figer avec Rémy)

| Patte | Coxa joint       | Fémur joint       | Tibia joint       |
|-------|------------------|-------------------|-------------------|
| leg_1 | leg_1_coxa_joint | leg_1_femur_joint | leg_1_tibia_joint |
| leg_2 | leg_2_coxa_joint | leg_2_femur_joint | leg_2_tibia_joint |
| leg_3 | leg_3_coxa_joint | leg_3_femur_joint | leg_3_tibia_joint |
| leg_4 | leg_4_coxa_joint | leg_4_femur_joint | leg_4_tibia_joint |
| leg_5 | leg_5_coxa_joint | leg_5_femur_joint | leg_5_tibia_joint |
| leg_6 | leg_6_coxa_joint | leg_6_femur_joint | leg_6_tibia_joint |

Règles:
- Les noms doivent être strictement identiques dans URDF, sim_hexa.py, /joint_states et RViz.
- Toute modification de nom doit être validée par Clément + Rémy.

## 4) Frames principales (V0)

| Frame | Parent | Rôle | Responsable |
|---|---|---|---|
| base_link | world ou map selon choix | Corps principal du robot | Rémy |
| leg_i_coxa_link | base_link | Segment proximal patte i | Rémy |
| leg_i_femur_link | leg_i_coxa_link | Segment intermédiaire patte i | Rémy |
| leg_i_tibia_link | leg_i_femur_link | Segment distal patte i | Rémy |

## 5) Plan de test rapide MVP

| Test ID | Test | Entrée | Résultat attendu | Responsable |
|---|---|---|---|---|
| T-01 | Chargement URDF | Launch de base | Robot visible dans RViz | Rémy |
| T-02 | Publication états | sim_hexa.py actif | /joint_states publié sans erreur | Clément |
| T-03 | Animation visuelle | Mouvement périodique | Articulations visibles en mouvement | Clément + Rémy |
| T-04 | Cohérence TF | Robot + RSP | Pas de rupture dans l'arbre TF | Rémy |
| T-05 | Démo relançable | Redémarrage complet | Même résultat en moins de 2 min | Équipe |

## 6) Dépendances et handoff entre rôles

| Producteur | Livrable | Consommateur | Impact si manquant |
|---|---|---|---|
| Tao | Validation périmètre et priorités | Clément, Rémy | Risque de hors-sujet/surconception |
| Clément | Tableau interfaces + contrat des joints | Rémy | URDF/RViz bloqués ou incohérents |
| Rémy | Noms joints + frames validés | Clément | sim_hexa.py publie des noms incompatibles |

## 7) Statut de validation

| Élément | Tao | Clément | Rémy | Date |
|---|---|---|---|---|
| Périmètre MVP | [ ] | [ ] | [ ] | |
| Interfaces MVP | [ ] | [ ] | [ ] | |
| Noms des joints | [ ] | [ ] | [ ] | |
| Frames principales | [ ] | [ ] | [ ] | |
| Critères de test | [ ] | [ ] | [ ] | |
