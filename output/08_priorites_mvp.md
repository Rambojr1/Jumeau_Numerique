# Priorités MVP - Jumeau numérique hexapode

## Objectif du MVP

Obtenir une démonstration minimale mais complète : un hexapode visible dans RViz, animé par des états articulaires publiés par un noeud simple `sim_hexa.py`.

Priorité absolue : **URDF simplifié + `/joint_states` + RViz qui bouge**.

## 1. Valider le périmètre avec le professeur

Objectif : éviter de partir sur une simulation trop ambitieuse ou hors sujet.

Questions à valider :

- ROS 1 ou ROS 2 ?
- RViz seulement ou Gazebo attendu ?
- URDF fidèle ou simplifié ?
- `sim_hexa.py` doit-il juste publier des positions articulaires ?

Résultat attendu :

- Le niveau attendu du projet est clair.
- Gazebo est confirmé comme attendu ou hors périmètre.
- Le niveau de détail de l'URDF est défini.
- Le rôle minimal de `sim_hexa.py` est validé.

## 2. Définir les interfaces ROS minimales

Objectif : définir uniquement les échanges nécessaires au MVP.

Interfaces prioritaires :

- Topic principal : `/joint_states`.
- Message associé : `sensor_msgs/JointState`.
- Topic de commande simple éventuel : `/hexa/cmd_mode`.
- Pas de services/actions au MVP sauf demande explicite.

Résultat attendu :

- Les noms des articulations publiés dans `/joint_states` correspondent exactement aux noms définis dans l'URDF.
- Les interfaces sont simples, testables et compréhensibles par toute l'équipe.

## 3. Faire un URDF simplifié

Objectif : créer un modèle suffisamment clair pour représenter l'hexapode dans RViz.

Éléments à prévoir :

- Corps central.
- 6 pattes.
- 3 articulations par patte si l'hexapode est bien en 18 DOF.
- Géométries simples : boîtes, cylindres ou formes basiques.
- Frames propres.
- Noms d'articulations cohérents et réutilisables dans `sim_hexa.py`.

Résultat attendu :

- Le robot peut être chargé dans RViz.
- La structure générale de l'hexapode est visible.
- Les articulations principales sont identifiables.

## 4. Afficher le robot dans RViz

Objectif : obtenir rapidement une preuve visuelle que le modèle fonctionne.

Actions minimales :

- Charger l'URDF.
- Afficher `robot_state_publisher`.
- Vérifier les frames.
- Voir l'hexapode complet immobile.

Résultat attendu :

- Le robot apparaît entièrement dans RViz.
- Les frames sont cohérentes.
- Aucun élément essentiel n'est absent ou mal rattaché.

## 5. Faire `sim_hexa.py` minimal

Objectif : animer l'hexapode sans chercher une simulation physique complète.

Fonctions minimales :

- Publier des messages `sensor_msgs/JointState`.
- Animer les articulations avec un mouvement simple.
- Exemple MVP : mouvement périodique des pattes ou posture repos/marche lente.
- Pas de physique.
- Pas de cinématique inverse complexe au départ.

Résultat attendu :

- RViz reçoit des états articulaires.
- Les articulations bougent visuellement.
- La démonstration est simple à relancer.

## Checklist MVP

- Périmètre validé avec le professeur.
- Version ROS confirmée.
- `/joint_states` défini comme interface centrale.
- URDF simplifié chargé dans RViz.
- Frames vérifiées.
- `sim_hexa.py` publie des états articulaires.
- L'hexapode bouge dans RViz.
- Les limites du MVP sont clairement expliquées.
