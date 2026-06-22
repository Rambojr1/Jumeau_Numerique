# hexa_simulation

MVP ROS 2 d'un hexapode pour validation URDF dans RViz.

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
