# Utilisation du robot hexapode

## Démarrer le robot

Dans un terminal :

```bash
source /opt/ros/jazzy/setup.bash
cd /mnt/c/Users/Clément/Documents/Travail/Robotique_Avancee/Jumeau_Numerique
colcon build --symlink-install --packages-select hexa_simulation
source install/setup.bash
ros2 launch hexa_simulation display_rviz.launch.py
```

Le robot apparaît dans RViz. Tous les joints sont à 0° (position de repos). C'est un lancement unique et simple — tous les choix se font via les topics.

---

## Trois façons de le commander


### 1. Bouger chaque joint vers une position donnée

**Ce que ça fait :** Tous les joints se déplacent ensemble vers les angles que tu as spécifiés. Le robot met quelques secondes à atteindre la cible (vitesse configurable).

**Exemple :** Mettre les trois articulations de la patte 1 aux angles 0.2, 0.5 et -0.5 radians :

```bash
ros2 topic pub --once /hexapode/joint_commands sensor_msgs/msg/JointState \
"{name: ['leg_1_coxa_joint','leg_1_femur_joint','leg_1_tibia_joint','leg_2_coxa_joint','leg_2_femur_joint','leg_2_tibia_joint','leg_3_coxa_joint','leg_3_femur_joint','leg_3_tibia_joint','leg_4_coxa_joint','leg_4_femur_joint','leg_4_tibia_joint','leg_5_coxa_joint','leg_5_femur_joint','leg_5_tibia_joint','leg_6_coxa_joint','leg_6_femur_joint','leg_6_tibia_joint'], position: [0.2,0.5,-0.5,0.2,0.5,-0.5,0.2,0.5,-0.5,0.2,0.5,-0.5,0.2,0.5,-0.5,0.2,0.5,-0.5]}"
```

Les 18 nombres correspondent aux 18 articulations (coxa, femur, tibia × 6 pattes).

---

### 2. Faire une séquence de positions (avec boucle optionnelle)

**Ce que ça fait :** Le robot exécute plusieurs positions l'une après l'autre. Il attend que la position précédente soit atteinte avant de passer à la suivante. Optionnellement, il peut refaire la même séquence indéfiniment.

**Exemple : trois positions différentes en séquence (sans boucle d'abord) :**

```bash
ros2 topic pub --once /hexapode/trajectory trajectory_msgs/msg/JointTrajectory \
"{joint_names: ['leg_1_coxa_joint','leg_1_femur_joint','leg_1_tibia_joint','leg_2_coxa_joint','leg_2_femur_joint','leg_2_tibia_joint','leg_3_coxa_joint','leg_3_femur_joint','leg_3_tibia_joint','leg_4_coxa_joint','leg_4_femur_joint','leg_4_tibia_joint','leg_5_coxa_joint','leg_5_femur_joint','leg_5_tibia_joint','leg_6_coxa_joint','leg_6_femur_joint','leg_6_tibia_joint'], points: [{positions: [0.0,0.0,-1.0,0.0,0.0,-1.0,0.0,0.0,-1.0,0.0,0.0,-1.0,0.0,0.0,-1.0,0.0,0.0,-1.0], time_from_start: {sec: 2}}, {positions: [0.2,0.5,-0.5,0.2,0.5,-0.5,0.2,0.5,-0.5,0.2,0.5,-0.5,0.2,0.5,-0.5,0.2,0.5,-0.5], time_from_start: {sec: 4}}, {positions: [-0.2,0.3,-1.2,-0.2,0.3,-1.2,-0.2,0.3,-1.2,-0.2,0.3,-1.2,-0.2,0.3,-1.2,-0.2,0.3,-1.2], time_from_start: {sec: 6}}]}"
```

Le robot va d'abord à la première position, puis à la deuxième, puis à la troisième, puis s'arrête.

**Pour activer la boucle (redémarrage indéfini) :**

```bash
ros2 topic pub --once /hexapode/set_loop sensor_msgs/msg/JointState \
"{name: ['dummy'], position: [1.0]}"
```

Ensuite, la séquence bouclera (revient à la première position et refait la séquence).

---

### 3. Arrêter le robot

**Ce que ça fait :** Le robot s'immobilise instantanément là où il est. Il n'y a plus d'interpolation ni de boucle.

**Commande :**

```bash
ros2 service call /hexapode/stop std_srvs/srv/Trigger
```

---

## Configuration au runtime (sans relancer RViz)

### Changer la vitesse de déplacement

Par défaut le robot met 1 seconde pour parcourir 1 radian (~57°). Pour que ce soit plus rapide ou plus lent :

```bash
ros2 topic pub --once /hexapode/set_speed sensor_msgs/msg/JointState \
"{name: ['dummy'], position: [2.0]}"
```

Valeurs courantes : `0.5` (très lent), `1.0` (normal), `2.0` (rapide).

### Activer ou désactiver la boucle

**Activer la boucle :**

```bash
ros2 topic pub --once /hexapode/set_loop sensor_msgs/msg/JointState \
"{name: ['dummy'], position: [1.0]}"
```

**Désactiver la boucle :**

```bash
ros2 topic pub --once /hexapode/set_loop sensor_msgs/msg/JointState \
"{name: ['dummy'], position: [0.0]}"
```

---

## Afficher le panel de contrôle avec sliders (pour le debug)

Dans un terminal différent du lancement, lance le panel de contrôle :

```bash
source /opt/ros/jazzy/setup.bash
ros2 run joint_state_publisher_gui joint_state_publisher_gui
```

Une fenêtre apparaît avec des sliders pour chaque articulation. C'est utile pour tester rapidement le URDF ou pour du debug.


Dans un autre terminal, lance le bridge pour relier le GUI au robot :

```bash
source /opt/ros/jazzy/setup.bash
cd /mnt/c/Users/Clément/Documents/Travail/Robotique_Avancee/Jumeau_Numerique
source install/setup.bash
ros2 run hexa_simulation gui_bridge
```

Maintenant, les sliders du panel contrôlent le robot en direct. Changer un angle = mouvement immédiat du robot dans RViz.

## Les 18 articulations expliquées

Chaque patte a 3 articulations. Les 6 pattes sont numérotées 1 à 6, et les 3 articulations sont toujours dans le même ordre :

| Patte | Articulation | Nom dans les commandes |
|-------|--------------|------------------------|
| 1 à 6 | Coxa (rotation) | `leg_[1-6]_coxa_joint` |
| 1 à 6 | Femur (montée/descente) | `leg_[1-6]_femur_joint` |
| 1 à 6 | Tibia (pas devant) | `leg_[1-6]_tibia_joint` |

**Limites angulaires :**
- Coxa : -45° à +45° (-0.785 à 0.785 rad)
- Femur : -57° à +57° (-1.0 à 1.0 rad)
- Tibia : -86° à +86° (-1.5 à 1.5 rad)

**Orientation :**
- Angles positifs = vers le haut / lever la patte
- Angles négatifs = vers le bas / abaisser la patte

---

## Exemple complet : marche simple

1. **Lancer le robot une seule fois :**
   ```bash
   ros2 launch hexa_simulation display_rviz.launch.py
   ```

2. **Activer la boucle :**
   ```bash
   ros2 topic pub --once /hexapode/set_loop sensor_msgs/msg/JointState \
   "{name: ['dummy'], position: [1.0]}"
   ```

3. **Envoyer une séquence de trois positions :**
   ```bash
   ros2 topic pub --once /hexapode/trajectory trajectory_msgs/msg/JointTrajectory \
   "{joint_names: ['leg_1_coxa_joint','leg_1_femur_joint','leg_1_tibia_joint','leg_2_coxa_joint','leg_2_femur_joint','leg_2_tibia_joint','leg_3_coxa_joint','leg_3_femur_joint','leg_3_tibia_joint','leg_4_coxa_joint','leg_4_femur_joint','leg_4_tibia_joint','leg_5_coxa_joint','leg_5_femur_joint','leg_5_tibia_joint','leg_6_coxa_joint','leg_6_femur_joint','leg_6_tibia_joint'], points: [{positions: [0.0,0.0,-1.0,0.0,0.0,-1.0,0.0,0.0,-1.0,0.0,0.0,-1.0,0.0,0.0,-1.0,0.0,0.0,-1.0], time_from_start: {sec: 0}}, {positions: [0.3,0.2,-0.8,0.3,0.2,-0.8,0.3,0.2,-0.8,0.3,0.2,-0.8,0.3,0.2,-0.8,0.3,0.2,-0.8], time_from_start: {sec: 2}}, {positions: [0.0,0.0,-1.0,0.0,0.0,-1.0,0.0,0.0,-1.0,0.0,0.0,-1.0,0.0,0.0,-1.0,0.0,0.0,-1.0], time_from_start: {sec: 4}}]}"
   ```

4. **Le robot va exécuter cette séquence en boucle. Ajuste la vitesse si besoin :**
   ```bash
   ros2 topic pub --once /hexapode/set_speed sensor_msgs/msg/JointState \
   "{name: ['dummy'], position: [1.5]}"
   ```

5. **Pour arrêter :**
   ```bash
   ros2 service call /hexapode/stop std_srvs/srv/Trigger
   ```
