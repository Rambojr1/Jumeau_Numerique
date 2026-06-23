# Hypothèses historiques d'IDs PhantomX V2 / Mark II

## Statut de ces informations

Les IDs de cette page proviennent de configurations PhantomX existantes. Ils
constituent uniquement un profil historique de comparaison nommé
`phantomx_v2_kurte`.

Ils ne sont pas les IDs garantis du robot réel et ne doivent jamais être copiés
automatiquement dans `config/joint_mapping.yaml`.

## Profil hypothétique

| Patte | Articulation | ID hypothétique |
|---|---|---:|
| Right Front | Coxa | 2 |
| Right Front | Femur | 4 |
| Right Front | Tibia | 6 |
| Right Middle | Coxa | 14 |
| Right Middle | Femur | 16 |
| Right Middle | Tibia | 18 |
| Right Rear | Coxa | 8 |
| Right Rear | Femur | 10 |
| Right Rear | Tibia | 12 |
| Left Front | Coxa | **1 ou 19** |
| Left Front | Femur | 3 |
| Left Front | Tibia | 5 |
| Left Middle | Coxa | 13 |
| Left Middle | Femur | 15 |
| Left Middle | Tibia | 17 |
| Left Rear | Coxa | 7 |
| Left Rear | Femur | 9 |
| Left Rear | Tibia | 11 |

Le profil décrit 18 articulations. La coxa avant gauche possède deux variantes
historiques acceptées, mais un robot réel ne devrait normalement retenir qu'une
seule de ces deux valeurs.

## Quatre niveaux à ne pas confondre

### ID hypothétique

Valeur trouvée dans une configuration ou un projet tiers. Elle sert seulement
à orienter une comparaison.

### ID détecté

Adresse ayant réellement répondu sur le bus lors d'un scan daté, avec un port,
un baudrate et un protocole enregistrés. Une détection globale ne prouve pas à
elle seule l'absence d'IDs dupliqués.

### ID mappé

ID détecté puis associé physiquement à une articulation URDF précise après un
essai individuel et reproductible.

### ID calibré

ID mappé pour lequel le sens, le zéro brut, l'échelle et les limites ont été
mesurés sur le robot réel.

Un ID peut donc être détecté sans être mappé, et mappé sans être calibré.

## Pourquoi ne pas remplir le mapping depuis Internet

- Les lots de fabrication et les interventions précédentes peuvent changer les
  IDs.
- Plusieurs firmwares ou variantes de câblage PhantomX existent.
- La variante Left Front Coxa `1/19` montre déjà que le profil n'est pas unique.
- Un même ID peut être attribué à deux servos et rester ambigu pendant un scan
  global.
- Un inventaire d'IDs ne donne ni le sens, ni le zéro, ni l'offset mécanique.

Remplir le mapping à partir d'Internet pourrait déplacer le mauvais joint dans
RViz et, lors d'une future commande, présenter un risque matériel.

## Procédure réelle recommandée

### 1. Sécurité et branchement

1. Supporter mécaniquement l'hexapode.
2. Prévoir une coupure d'alimentation accessible.
3. Vérifier le bus TTL, l'alimentation externe et la masse commune.
4. Garantir qu'un seul maître utilise le bus.
5. Ne lancer aucune commande de couple ou de position.

### 2. Valider un servo avec le probe

```bash
python3 tools/dynamixel_readonly_probe.py \
  --port "<PORT_REEL>" \
  --baudrate "<BAUDRATE_CANDIDAT_DOCUMENTE>" \
  --protocol-version 1.0 \
  --id "<ID_CANDIDAT_MATERIEL>"
```

Ne lancer le scan complet qu'après plusieurs lectures réussies de
`Present Position`.

### 3. Lancer le scanner vers un nouveau fichier

Installer les dépendances hors ROS :

```bash
python3 -m pip install dynamixel-sdk PyYAML
```

Créer au préalable un répertoire de résultats séparé, puis lancer :

```bash
mkdir -p scan_results

python3 tools/dynamixel_readonly_scan.py \
  --port "<PORT_REEL>" \
  --baudrate "<BAUDRATE_REEL>" \
  --protocol-version 1.0 \
  --start-id 0 \
  --end-id 253 \
  --repetitions 3 \
  --format yaml \
  --output "scan_results/scan_<DATE>.yaml" \
  --compare-profile phantomx_v2_kurte \
  --strict-readonly-check
```

Le scanner crée uniquement le chemin donné par `--output`, refuse d'écraser un
fichier existant et refuse explicitement les fichiers
`config/dynamixel_ids.yaml` et `config/joint_mapping.yaml`.

`--timeout-ms` peut enregistrer une valeur demandée dans le rapport, mais les
appels haut niveau du SDK conservent leur calcul interne du timeout de paquet.

### 4. Interpréter la comparaison

Le rapport distingue :

- les IDs hypothétiques retrouvés ;
- les IDs hypothétiques fixes manquants ;
- les IDs inattendus ;
- la présence de LF coxa `1`, `19`, des deux, ou d'aucun ;
- les réponses stables et instables sur les répétitions.

La conclusion `compatible_with_hypothesis` signifie seulement que l'inventaire
ressemble au profil. Elle ne valide pas le mapping moteur → articulation.

### 5. Vérifier les doublons puis mapper

1. Répéter le scan plusieurs fois.
2. Isoler les branches ou les servos pour exclure les IDs dupliqués.
3. Identifier physiquement chaque articulation.
4. Renseigner manuellement l'inventaire réel après revue des résultats.
5. Calibrer séparément sens, zéro, échelle et limites.
6. Ne passer `hardware_validated` ou `calibrated` à `true` qu'après validation
   reproductible sur le robot.
