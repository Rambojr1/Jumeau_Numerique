# Procédure future de scan du robot réel

## Statut actuel

Cette procédure est préparatoire. Aucun port, baudrate, protocole, ID, modèle,
sens, offset ou zéro mécanique n'a été validé sans le robot physique.

Les fichiers `config/dynamixel_ids.yaml` et `config/joint_mapping.yaml` doivent
rester non renseignés jusqu'aux mesures réelles.

## 1. Préparation de sécurité

- Supporter mécaniquement l'hexapode.
- Prévoir une coupure d'alimentation accessible.
- Vérifier l'alimentation externe et la masse commune.
- Identifier le type électrique TTL ou RS-485 sur le matériel.
- Garantir qu'un seul maître communique sur le bus.
- Ne pas forcer une articulation.
- N'envoyer aucune écriture de registre, activation de couple ou position cible.

## 2. Identifier l'interface Linux

```bash
lsusb
ls -l /dev/serial/by-id/
python3 -m serial.tools.list_ports -v
```

Utiliser de préférence le chemin stable `/dev/serial/by-id/...`.

## 3. Prouver une première lecture

Utiliser le probe conservé dans `tools/dynamixel_readonly_probe.py` avec des
valeurs provenant du matériel ou de sa configuration réelle :

```bash
python3 tools/dynamixel_readonly_probe.py \
  --port "<PORT_REEL>" \
  --baudrate "<BAUDRATE_REEL_OU_CANDIDAT_DOCUMENTE>" \
  --protocol-version "<PROTOCOL_VERSION>" \
  --id "<ID_PHYSIQUE_CANDIDAT>"
```

La communication brute n'est validée que si le ping, le Model Number et la
lecture de Present Position réussissent plusieurs fois.

## 4. Scanner les IDs

Après validation du probe, un scanner séparé et audité devra :

1. parcourir les IDs 0 à 253 avec des pings individuels ;
2. utiliser uniquement des lectures ;
3. répéter le scan au moins trois fois ;
4. enregistrer le port, le baudrate, le protocole, la date et les modèles ;
5. écrire les résultats mesurés dans `config/dynamixel_ids.yaml` ;
6. ne jamais compléter les résultats avec des IDs mock ou supposés.

Un scan global ne prouve pas l'absence d'IDs dupliqués. Les branches ou les
servos devront être isolés physiquement pour lever cette ambiguïté.

## 5. Calibrer le mapping

Pour chaque joint URDF :

- identifier l'ID physique ;
- vérifier le modèle ;
- déterminer le sens sans forcer un servo sous couple ;
- mesurer le zéro brut dans une posture documentée ;
- déterminer l'échelle applicable au modèle ;
- mesurer les limites mécaniques sûres ;
- renseigner le YAML seulement après validation ;
- passer `calibrated` à `true` uniquement après un essai reproductible.

## 6. Porte de validation du mode réel

```bash
python3 tools/validate_joint_mapping.py --require-real-ready
```

Cette commande doit échouer tant que des champs physiques sont `null`, que
l'inventaire est vide ou que la validation matérielle n'est pas explicitement
confirmée.

Le futur bridge réel devra rester en lecture seule lors de sa première mise en
service et refuser de démarrer si cette validation échoue.
