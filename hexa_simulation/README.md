# hexa_simulation

MVP ROS 2 d'un hexapode PhantomX pour visualisation dans RViz.

---

## Prérequis

- Ubuntu (ou WSL)
- ROS 2 Jazzy installé
- colcon, robot_state_publisher, rviz2, joint_state_publisher_gui

Installation rapide :

```bash
sudo apt-get update
sudo apt-get install -y \
  ros-jazzy-robot-state-publisher \
  ros-jazzy-joint-state-publisher-gui \
  ros-jazzy-rviz2 \
  python3-colcon-common-extensions
```

---

## Lancement

```bash
source /opt/ros/jazzy/setup.bash
cd chemin/vers/le/dossier/Jumeau_Numerique
colcon build --symlink-install --packages-select hexa_simulation
source install/setup.bash
ros2 launch hexa_simulation display_rviz.launch.py
```

Par défaut, le noeud `sim_hexa` est lancé : il écoute les commandes sur le topic `/hexapode/joint_commands`.

Mode sliders (debug URDF, sans topic externe) :

```bash
ros2 launch hexa_simulation display_rviz.launch.py use_gui:=true
```

---

## Interface ROS — pour le groupe commande

### Topic à publier

| Champ      | Valeur                         |
|------------|-------------------------------|
| Topic      | `/hexapode/joint_commands`     |
| Type       | `sensor_msgs/msg/JointState`   |
| Fréquence  | libre                          |

Seuls `name` et `position` sont obligatoires.  
Les joints absents du message conservent leur position courante.

### Noms des 18 joints

```
leg_1_coxa_joint   leg_1_femur_joint   leg_1_tibia_joint
leg_2_coxa_joint   leg_2_femur_joint   leg_2_tibia_joint
leg_3_coxa_joint   leg_3_femur_joint   leg_3_tibia_joint
leg_4_coxa_joint   leg_4_femur_joint   leg_4_tibia_joint
leg_5_coxa_joint   leg_5_femur_joint   leg_5_tibia_joint
leg_6_coxa_joint   leg_6_femur_joint   leg_6_tibia_joint
```

### Limites angulaires (rad)

| Articulation | Min    | Max   |
|-------------|--------|-------|
| coxa        | -0.785 | 0.785 |
| femur       | -1.000 | 1.000 |
| tibia       | -1.500 | 1.500 |

Les valeurs hors limites sont clampées automatiquement.

---

### Choisir le mode de contrôle

#### Mode interpolation (défaut)

Le noeud interpole chaque articulation vers la cible à `joint_speed` rad/s.  
Adapté pour des commandes ponctuelles ou basse fréquence.

```bash
ros2 launch hexa_simulation display_rviz.launch.py joint_speed:=1.0
```

**Vitesse par joint optionnelle** : si le champ `velocity` est fourni dans le message avec une valeur > 0, il remplace `joint_speed` pour ce joint uniquement.

#### Mode trajectoire séquentielle — `/hexapode/trajectory`

Envoyer une liste de waypoints sur ce topic. Le robot exécute chaque waypoint l'un après l'autre de manière fluide, attend d'être arrivé, puis passe au suivant.

| Champ  | Valeur                              |
|--------|-------------------------------------|
| Topic  | `/hexapode/trajectory`              |
| Type   | `trajectory_msgs/msg/JointTrajectory` |

Seuls `joint_names` et `points[].positions` sont utilisés.  
Une commande `/hexapode/joint_commands` interrompt la séquence en cours.

Paramètres de lancement associés :

| Paramètre          | Défaut | Rôle |
|--------------------|--------|------|
| `joint_speed`      | 1.0    | Vitesse d'interpolation entre waypoints (rad/s) |
| `loop_trajectory`  | false  | Reboucle indéfiniment sur la séquence |
| `waypoint_threshold` | 0.02 | Seuil en rad pour valider un waypoint atteint |

Exemple : 3 waypoints en boucle sur les fémurs

```bash
ros2 launch hexa_simulation display_rviz.launch.py loop_trajectory:=true joint_speed:=1.0
```

```bash
ros2 topic pub --once /hexapode/trajectory trajectory_msgs/msg/JointTrajectory \
  "{joint_names: ['leg_1_femur_joint','leg_2_femur_joint','leg_3_femur_joint','leg_4_femur_joint','leg_5_femur_joint','leg_6_femur_joint'], \
    points: [\
      {positions: [0.8, 0.8, 0.8, 0.8, 0.8, 0.8]}, \
      {positions: [-0.8,-0.8,-0.8,-0.8,-0.8,-0.8]}, \
      {positions: [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]}  \
    ]}"
```

#### Mode direct (`trajectory_mode:=true`)

Positions appliquées immédiatement sans interpolation.  
Adapté si le groupe commande génère sa propre trajectoire et envoie à ≥ 20Hz.

```bash
ros2 launch hexa_simulation display_rviz.launch.py trajectory_mode:=true
```

---

### Exemples CLI

Déplacer tous les tibias vers -0.8 rad :

```bash
ros2 topic pub --once /hexapode/joint_commands sensor_msgs/msg/JointState \
  "{name: ['leg_1_tibia_joint','leg_2_tibia_joint','leg_3_tibia_joint','leg_4_tibia_joint','leg_5_tibia_joint','leg_6_tibia_joint'], \
    position: [-0.8,-0.8,-0.8,-0.8,-0.8,-0.8]}"
```

Idem avec vitesse par joint à 2.0 rad/s :

```bash
ros2 topic pub --once /hexapode/joint_commands sensor_msgs/msg/JointState \
  "{name: ['leg_1_tibia_joint','leg_2_tibia_joint','leg_3_tibia_joint','leg_4_tibia_joint','leg_5_tibia_joint','leg_6_tibia_joint'], \
    position: [-0.8,-0.8,-0.8,-0.8,-0.8,-0.8], \
    velocity: [2.0,2.0,2.0,2.0,2.0,2.0]}"
```

Remettre tout à zéro :

```bash
ros2 topic pub --once /hexapode/joint_commands sensor_msgs/msg/JointState \
  "{name: ['leg_1_coxa_joint','leg_1_femur_joint','leg_1_tibia_joint','leg_2_coxa_joint','leg_2_femur_joint','leg_2_tibia_joint','leg_3_coxa_joint','leg_3_femur_joint','leg_3_tibia_joint','leg_4_coxa_joint','leg_4_femur_joint','leg_4_tibia_joint','leg_5_coxa_joint','leg_5_femur_joint','leg_5_tibia_joint','leg_6_coxa_joint','leg_6_femur_joint','leg_6_tibia_joint'], \
    position: [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]}"
```

**Arrêter le robot** (séquence ou mouvement en cours) :

```bash
ros2 service call /hexapode/stop std_srvs/srv/Trigger
```

Le robot s'immobilise à sa position actuelle et attend une nouvelle commande.

---

## Commandes après modification

Rebuild standard :

```bash
source /opt/ros/jazzy/setup.bash
cd chemin/vers/le/dossier/Jumeau_Numerique
colcon build --symlink-install --packages-select hexa_simulation
source install/setup.bash
ros2 launch hexa_simulation display_rviz.launch.py
```

Vérification du topic de sortie :

```bash
ros2 topic echo /joint_states --once
```

Vérification du topic de commande (depuis un autre terminal) :

```bash
ros2 topic echo /hexapode/joint_commands
```

Rebuild propre :

```bash
rm -rf build install log
colcon build --symlink-install --packages-select hexa_simulation
source install/setup.bash
ros2 launch hexa_simulation display_rviz.launch.py
```

---

## Fonctionnalités actuelles

- URDF PhantomX (corps 250×125mm, 6 pattes coxa/femur/tibia)
- Noeud `sim_hexa` : écoute `/hexapode/joint_commands`, interpole vers les cibles à vitesse contrôlée, publie sur `/joint_states` à 50Hz
- Visualisation RViz préconfigurée (RobotModel + TF, outil MoveCamera par défaut)
- Mode debug sliders disponible via `use_gui:=true`

## Fonctionnalités visées

- Réception de séquences de marche complètes depuis le groupe commande
- Validation mécanique avec détection de collision (à décider en équipe)
- Extension éventuelle vers simulation physique Gazebo (hors MVP)

---

## Dépannage rapide

- Erreur package introuvable : vérifier `source install/setup.bash`
- Erreur d'encoding URDF : vérifier que le fichier est en UTF-8
- Aucun mouvement après publication : vérifier les noms des joints avec `ros2 topic echo /hexapode/joint_commands`
- Aucun affichage dans RViz : vérifier que `Fixed Frame` est `base_link`


## Prérequis

- Ubuntu via WSL
- ROS 2 Jazzy installé
- Outils de build ROS 2 : colcon
- Paquets ROS utilisés par ce projet :
  - joint_state_publisher_gui
  - robot_state_publisher
  - rviz2

Installation rapide (si besoin):

```bash
sudo apt-get update
sudo apt-get install -y \
  ros-jazzy-joint-state-publisher-gui \
  ros-jazzy-robot-state-publisher \
  ros-jazzy-rviz2 \
  python3-colcon-common-extensions
```

## Lancement

Depuis WSL, à la racine de votre workspace :

```bash
source /opt/ros/jazzy/setup.bash
cd chemin/vers/le/dossier/Jumeau_Numerique
colcon build --symlink-install --packages-select hexa_simulation
source install/setup.bash
ros2 launch hexa_simulation display_rviz.launch.py
```

## Commandes après chaque modification

Modif classique (URDF, Python, launch, RViz):

```bash
source /opt/ros/jazzy/setup.bash
cd chemin/vers/le/dossier/Jumeau_Numerique
colcon build --symlink-install --packages-select hexa_simulation
source install/setup.bash
ros2 launch hexa_simulation display_rviz.launch.py
```

Vérification rapide du topic :

```bash
source /opt/ros/jazzy/setup.bash
cd chemin/vers/le/dossier/Jumeau_Numerique
source install/setup.bash
ros2 topic echo /joint_states --once
```

Rebuild propre (si comportement incohérent) :

```bash
source /opt/ros/jazzy/setup.bash
cd chemin/vers/le/dossier/Jumeau_Numerique
rm -rf build install log
colcon build --symlink-install --packages-select hexa_simulation
source install/setup.bash
ros2 launch hexa_simulation display_rviz.launch.py
```

## Fonctionnalités actuelles

- Chargement URDF depuis hexa_simulation/urdf/hexapode.urdf
- Publication des transforms via robot_state_publisher
- Contrôle manuel des 18 articulations via joint_state_publisher_gui
- Visualisation RViz préconfigurée (RobotModel + TF)
- Noeud sim_hexa.py disponible (animation sinusoïdale), non lancé par défaut


## Dépannage rapide

- Erreur package introuvable : vérifier source install/setup.bash
- Erreur de lancement sur URDF : vérifier que le fichier est en UTF-8
- Aucun mouvement dans RViz : ouvrir la fenêtre GUI et bouger les sliders
