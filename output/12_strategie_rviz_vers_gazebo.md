# Stratégie RViz → Gazebo

## Décision de cadrage

Le projet est développé en **ROS 2**.

La priorité est de produire d'abord un **MVP stable** :

> URDF simplifié + `/joint_states` + RViz animé par `sim_hexa.py`

**Gazebo est traité comme un livrable ++**, uniquement après validation du MVP.

---

## Objectif du MVP

Obtenir une démonstration minimale mais complète :

- Hexapode visible dans RViz
- URDF simplifié et lisible
- Frames cohérentes
- Noms d'articulations stables
- Publication du topic `/joint_states`
- Animation simple via `sim_hexa.py`
- Démonstration relançable facilement

Le MVP ne cherche pas à simuler la physique complète.

---

## Différence clé

| Outil | Rôle | Objectif |
|---|---|---|
| RViz | Visualisation | Vérifier la structure, les frames et l'animation visuelle |
| Gazebo | Simulation physique | Tester contacts, inerties, collisions, gravité et contrôleurs |

Phrase de synthèse :

> RViz valide la représentation et l'animation. Gazebo valide le comportement physique.

---

## Stratégie de développement

### Phase 1 — MVP RViz

Objectif : obtenir rapidement une preuve visuelle.

À produire :

- URDF simplifié
- `robot_state_publisher`
- topic `/joint_states`
- noeud `sim_hexa.py`
- animation simple des articulations
- vérification dans RViz

Critère de réussite :

> L'hexapode est visible dans RViz et ses articulations bougent correctement.

---

### Phase 2 — Préparation Gazebo

Objectif : rendre l'URDF compatible avec une simulation physique future.

À ajouter progressivement :

- géométries de collision
- masses
- inerties
- limites articulaires
- transmissions
- éléments `ros2_control`
- préparation des contrôleurs
- simplification des contacts pied / sol

Critère de réussite :

> Le modèle reste compatible RViz tout en devenant exploitable pour Gazebo.

---

### Phase 3 — Livrable Gazebo ++

Objectif : simuler le robot dans un environnement physique.

À produire :

- spawn du robot dans Gazebo
- contrôleurs actifs
- joints commandables
- contacts au sol fonctionnels
- premiers tests de stabilité
- observation du comportement simulé

Critère de réussite :

> L'hexapode est chargé dans Gazebo et ses articulations peuvent être commandées sans incohérence majeure.

---

## Points d'attention

### 1. Noms des joints

Les noms des articulations doivent rester identiques entre :

- URDF
- `/joint_states`
- `sim_hexa.py`
- RViz
- future configuration Gazebo

Exemple :

```text
leg_1_coxa_joint
leg_1_femur_joint
leg_1_tibia_joint
```

---

### 2. URDF itératif

L'URDF ne doit pas être complet dès le départ.

Ordre recommandé :

```text
visual + joints + frames
→ collision
→ inertial
→ joint limits
→ transmissions
→ ros2_control
→ Gazebo plugins
```

---

### 3. Animation RViz vs commande Gazebo

Pour RViz :

```text
sim_hexa.py → /joint_states → RViz
```

Pour Gazebo :

```text
contrôleurs / ros2_control → joints simulés → joint_state_broadcaster → /joint_states
```

Important :

> En Gazebo, il ne faut pas simplement forcer `/joint_states`. Les joints doivent être commandés via les contrôleurs.

---

## Planning synthétique

| Étape | Objectif | Livrable |
|---|---|---|
| DJ1 | Cadrage | ROS 2 confirmé, MVP prioritaire, Gazebo en livrable ++ |
| DJ2 | Interfaces ROS 2 | `/joint_states`, conventions de nommage, structure paquet |
| DJ3 | URDF + RViz | Hexapode simplifié visible dans RViz |
| DJ4 | Animation | `sim_hexa.py` publie les états articulaires |
| DJ5 | Stabilisation | Démo MVP stable + plan Gazebo ++ |

---

## Règle projet

Ne pas commencer par Gazebo.

Priorité absolue :

```text
1. Faire apparaître le robot dans RViz
2. Faire bouger les articulations
3. Stabiliser le MVP
4. Préparer Gazebo
5. Ajouter Gazebo en livrable ++
```

---

## Formulation à intégrer dans le dossier

La stratégie retenue est itérative. Le projet commence par un MVP sous RViz afin de sécuriser la structure du robot, les frames, les noms d'articulations et la publication `/joint_states`. Cette première étape permet d'obtenir rapidement une démonstration visuelle stable. Gazebo est ensuite traité comme un livrable ++, car il nécessite des éléments supplémentaires : collisions, inerties, masses, limites articulaires, contrôleurs et gestion des contacts au sol.
