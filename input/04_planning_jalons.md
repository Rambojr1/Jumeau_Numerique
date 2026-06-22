# Planning et jalons

## Planning sur 5 demi-journées

### Demi-journée 1 : cadrage, lots, rôles, risques, planning

| Élément | Contenu |
|---|---|
| Objectif principal | Organiser le projet avant tout développement |
| Tâches à faire | Comprendre le sujet ; définir hypothèses ; découper les lots ; attribuer les rôles ; définir jalons ; analyser les risques ; préparer la synthèse professeur |
| Livrables produits | Feuille de route ; lots de travaux ; rôles ; planning jalons ; livrables par personne ; analyse risques ; synthèse professeur |
| Point professeur suivant | Présenter les choix d'organisation, les hypothèses à valider et les objectifs de la demi-journée 2 |
| Critères de réussite | Chaque membre sait quoi produire ; les décisions à valider sont claires ; les risques prioritaires sont connus |
| Risques associés | Cadrage trop vague ; oubli des critères de validation ; répartition déséquilibrée |

### Demi-journée 2 : interfaces ROS + squelette paquet

| Élément | Contenu |
|---|---|
| Objectif principal | Formaliser les interfaces et l'organisation technique |
| Tâches à faire | Valider version ROS ; définir topics/services/actions ; établir schéma d'architecture ; préparer structure théorique du paquet ; fixer conventions de nommage |
| Livrables produits | Tableau interfaces ROS ; schéma architecture ; squelette théorique du paquet ; décisions validées |
| Point professeur suivant | Présenter interfaces retenues, choix techniques et blocages éventuels sur ROS |
| Critères de réussite | Les interfaces couvrent visualisation et simulation simple ; aucune interface inutile majeure |
| Risques associés | Interfaces mal définies ; dépendance à une version ROS non confirmée ; structure trop détaillée trop tôt |

### Demi-journée 3 : URDF + RViz

| Élément | Contenu |
|---|---|
| Objectif principal | Construire la base de visualisation du robot |
| Tâches à faire | Définir modèle URDF simplifié ; organiser frames ; préparer chargement RViz ; vérifier cohérence entre noms d'articulations et interfaces |
| Livrables produits | URDF simplifié prévu ou commencé selon validation ; liste frames ; configuration RViz prévue ; critères visuels |
| Point professeur suivant | Présenter avancement visuel, choix de simplification et éventuelles limites mécaniques |
| Critères de réussite | Le niveau de détail est borné ; les frames et articulations sont cohérentes ; RViz reste prioritaire |
| Risques associés | URDF trop ambitieux ; confusion frames ; manque de données mécaniques |

### Demi-journée 4 : simulation simple + tests

| Élément | Contenu |
|---|---|
| Objectif principal | Démontrer un fonctionnement simple et vérifiable |
| Tâches à faire | Implémenter ou finaliser le comportement minimal de `sim_hexa.py` selon les choix validés ; relier états simulés à RViz ; exécuter tests d'interfaces et validation visuelle |
| Livrables produits | Noeud de simulation simple ; rapport de tests ; liste des corrections ; scénario de démonstration |
| Point professeur suivant | Présenter ce qui fonctionne, ce qui reste fragile et les objectifs de stabilisation |
| Critères de réussite | Une démonstration minimale est observable ; les tests principaux passent ; les limites sont expliquées |
| Risques associés | Simulation trop ambitieuse ; RViz non fonctionnel ; tests faits trop tard |

### Demi-journée 5 : stabilisation + documentation + soutenance

| Élément | Contenu |
|---|---|
| Objectif principal | Stabiliser le résultat et préparer la présentation finale |
| Tâches à faire | Corriger les points critiques ; compléter documentation ; préparer support visuel ; répéter démonstration ; formaliser limites et perspectives |
| Livrables produits | Documentation finale ; support de soutenance ; démonstration stabilisée ; bilan risques |
| Point professeur suivant | Présenter le résultat final ou l'état prêt pour soutenance |
| Critères de réussite | Démonstration claire ; support lisible ; rôles et choix techniques explicables |
| Risques associés | Soutenance préparée trop tard ; documentation incomplète ; démonstration instable |

## Découpage détaillé de la première demi-journée

| Créneau | Objectif | Action concrète | Responsable | Résultat attendu |
|---|---|---|---|---|
| 0h00 - 0h30 | Compréhension sujet et hypothèses | Lire le sujet ; isoler contraintes ; noter questions professeur | Tao | Liste d'hypothèses et contraintes projet |
| 0h30 - 1h15 | Découpage lots | Transformer les grandes tâches en lots pilotables | Tao | Tableau des lots avec responsables et critères |
| 1h15 - 2h00 | Rôles et livrables | Attribuer périmètres Tao/Clément/Rémy ; définir productions attendues | Tao | Rôles clairs et livrables par personne |
| 2h00 - 2h45 | Planning et jalons | Répartir les lots sur cinq demi-journées ; définir jalons | Tao | Planning réaliste et jalons vérifiables |
| 2h45 - 3h30 | Analyse des risques | Identifier risques temps/qualité ; définir prévention et secours | Tao | Tableau des risques priorisés |
| 3h30 - 4h00 | Synthèse professeur | Préparer une page orale : choix, questions, prochaine étape | Tao | Synthèse courte prête à présenter |

## Jalons projet

| ID | Nom du jalon | Moment prévu | Résultat attendu | Preuve concrète de validation | Risque si non atteint | Responsable |
|---|---|---|---|---|---|---|
| J01 | Cadrage validé | Fin demi-journée 1 | Périmètre, rôles, lots et risques définis | Documents de cadrage disponibles dans `output` | Départ désorganisé, perte de temps | Tao |
| J02 | Interfaces définies | Fin demi-journée 2 | Topics/services/actions et architecture documentés | Tableau interfaces relu par l'équipe | Simulation et RViz incompatibles | Clément |
| J03 | Modèle visuel cadré | Fin demi-journée 3 | URDF/RViz suffisamment définis pour visualiser l'hexapode | Liste frames et scénario RViz validés | RViz inutilisable ou incohérent | Rémy |
| J04 | Simulation simple démontrable | Fin demi-journée 4 | `sim_hexa.py` produit un comportement minimal observable | Scénario de test et observation RViz | Pas de démonstration fonctionnelle | Clément |
| J05 | Projet stabilisé et présentable | Fin demi-journée 5 | Documentation, démonstration et support visuel prêts | Support de soutenance et checklist finale | Présentation confuse ou incomplète | Tao |
