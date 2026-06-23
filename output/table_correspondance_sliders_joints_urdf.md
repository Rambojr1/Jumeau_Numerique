#> ⚠️ Important : les IDs indiqués ici sont uniquement des IDs mock pour l’interface slider / simulation offline.
#> Ils ne correspondent pas aux IDs réels des servos Dynamixel.
#> Les IDs réels devront être mesurés sur le robot physique avec le script de scan lecture seule.

# Tableau de correspondance sliders -> joints URDF

## Hypothèse de mapping

Les fichiers fournis contiennent les joints URDF et le contrat MVP, mais pas le code exact des sliders de Clément.  
Le mapping ci-dessous propose donc une convention stable :

```text
ID mock = numéro de patte + numéro d'articulation
11 = patte 1 coxa
12 = patte 1 femur
13 = patte 1 tibia
...
63 = patte 6 tibia
```

Si les IDs mockés utilisés dans le code de Clément sont différents, il faut uniquement remplacer la colonne `ID mock slider`, pas les noms des joints URDF.

## Tableau principal

| Slider UI recommandé | ID mock slider proposé | Patte | Position robot | Articulation | Joint URDF à publier dans `/joint_states` | Link parent | Link enfant | Axe URDF | Limites URDF |
|---|---:|---|---|---|---|---|---|---|---|
| slider_leg_1_coxa | 11 | leg_1 | Avant gauche | Coxa | `leg_1_coxa_joint` | `base_link` | `leg_1_coxa_link` | `0 0 1` | -1.57 à +1.57 rad |
| slider_leg_1_femur | 12 | leg_1 | Avant gauche | Fémur | `leg_1_femur_joint` | `leg_1_coxa_link` | `leg_1_femur_link` | `0 1 0` | -1.57 à +1.57 rad |
| slider_leg_1_tibia | 13 | leg_1 | Avant gauche | Tibia | `leg_1_tibia_joint` | `leg_1_femur_link` | `leg_1_tibia_link` | `0 1 0` | -1.57 à +1.57 rad |
| slider_leg_2_coxa | 21 | leg_2 | Milieu gauche | Coxa | `leg_2_coxa_joint` | `base_link` | `leg_2_coxa_link` | `0 0 1` | -1.57 à +1.57 rad |
| slider_leg_2_femur | 22 | leg_2 | Milieu gauche | Fémur | `leg_2_femur_joint` | `leg_2_coxa_link` | `leg_2_femur_link` | `0 1 0` | -1.57 à +1.57 rad |
| slider_leg_2_tibia | 23 | leg_2 | Milieu gauche | Tibia | `leg_2_tibia_joint` | `leg_2_femur_link` | `leg_2_tibia_link` | `0 1 0` | -1.57 à +1.57 rad |
| slider_leg_3_coxa | 31 | leg_3 | Arrière gauche | Coxa | `leg_3_coxa_joint` | `base_link` | `leg_3_coxa_link` | `0 0 1` | -1.57 à +1.57 rad |
| slider_leg_3_femur | 32 | leg_3 | Arrière gauche | Fémur | `leg_3_femur_joint` | `leg_3_coxa_link` | `leg_3_femur_link` | `0 1 0` | -1.57 à +1.57 rad |
| slider_leg_3_tibia | 33 | leg_3 | Arrière gauche | Tibia | `leg_3_tibia_joint` | `leg_3_femur_link` | `leg_3_tibia_link` | `0 1 0` | -1.57 à +1.57 rad |
| slider_leg_4_coxa | 41 | leg_4 | Avant droite | Coxa | `leg_4_coxa_joint` | `base_link` | `leg_4_coxa_link` | `0 0 1` | -1.57 à +1.57 rad |
| slider_leg_4_femur | 42 | leg_4 | Avant droite | Fémur | `leg_4_femur_joint` | `leg_4_coxa_link` | `leg_4_femur_link` | `0 1 0` | -1.57 à +1.57 rad |
| slider_leg_4_tibia | 43 | leg_4 | Avant droite | Tibia | `leg_4_tibia_joint` | `leg_4_femur_link` | `leg_4_tibia_link` | `0 1 0` | -1.57 à +1.57 rad |
| slider_leg_5_coxa | 51 | leg_5 | Milieu droite | Coxa | `leg_5_coxa_joint` | `base_link` | `leg_5_coxa_link` | `0 0 1` | -1.57 à +1.57 rad |
| slider_leg_5_femur | 52 | leg_5 | Milieu droite | Fémur | `leg_5_femur_joint` | `leg_5_coxa_link` | `leg_5_femur_link` | `0 1 0` | -1.57 à +1.57 rad |
| slider_leg_5_tibia | 53 | leg_5 | Milieu droite | Tibia | `leg_5_tibia_joint` | `leg_5_femur_link` | `leg_5_tibia_link` | `0 1 0` | -1.57 à +1.57 rad |
| slider_leg_6_coxa | 61 | leg_6 | Arrière droite | Coxa | `leg_6_coxa_joint` | `base_link` | `leg_6_coxa_link` | `0 0 1` | -1.57 à +1.57 rad |
| slider_leg_6_femur | 62 | leg_6 | Arrière droite | Fémur | `leg_6_femur_joint` | `leg_6_coxa_link` | `leg_6_femur_link` | `0 1 0` | -1.57 à +1.57 rad |
| slider_leg_6_tibia | 63 | leg_6 | Arrière droite | Tibia | `leg_6_tibia_joint` | `leg_6_femur_link` | `leg_6_tibia_link` | `0 1 0` | -1.57 à +1.57 rad |

## Mapping compact pour `sim_hexa.py`

```python
SLIDER_TO_JOINT = {
    11: "leg_1_coxa_joint",
    12: "leg_1_femur_joint",
    13: "leg_1_tibia_joint",

    21: "leg_2_coxa_joint",
    22: "leg_2_femur_joint",
    23: "leg_2_tibia_joint",

    31: "leg_3_coxa_joint",
    32: "leg_3_femur_joint",
    33: "leg_3_tibia_joint",

    41: "leg_4_coxa_joint",
    42: "leg_4_femur_joint",
    43: "leg_4_tibia_joint",

    51: "leg_5_coxa_joint",
    52: "leg_5_femur_joint",
    53: "leg_5_tibia_joint",

    61: "leg_6_coxa_joint",
    62: "leg_6_femur_joint",
    63: "leg_6_tibia_joint",
}
```

## Règle de validation

Dans `/joint_states`, le champ `name` doit contenir exactement les noms des joints URDF :

```python
msg.name = list(SLIDER_TO_JOINT.values())
```

Chaque valeur de slider doit ensuite alimenter `msg.position` dans le même ordre que `msg.name`.
