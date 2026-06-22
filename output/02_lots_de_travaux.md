# Lots de travaux

## Tableau des lots

| ID | Lot | Objectif | Tâches principales | Dépendances | Responsable principal | Contributeurs | Livrables associés | Difficulté | Priorité | Critère de validation |
|---|---|---|---|---|---|---|---|---|---|---|
| L01 | Cadrage technique | Définir le besoin, les limites et les hypothèses | Relire le sujet ; lister les contraintes ; formuler les questions professeur ; fixer le niveau de simulation | Sujet projet | Tao | Clément, Rémy | Feuille de route ; synthèse professeur | Faible | Haute | Les hypothèses critiques sont listées et prêtes à être validées |
| L02 | Interfaces ROS | Définir les topics, services et actions utiles | Identifier entrées/sorties ; proposer messages ; relier interfaces à RViz et `sim_hexa.py` | Version ROS ; niveau simulation | Clément | Tao | Tableau des interfaces ; schéma d'architecture ROS | Moyen | Haute | Chaque interface a un rôle, un producteur, un consommateur et un critère d'usage |
| L03 | Structure du paquet ROS | Préparer l'organisation logique du paquet sans créer le paquet réel | Lister dossiers théoriques ; prévoir fichiers attendus ; définir conventions de nommage | Version ROS ; lots L02, L04, L06 | Clément | Tao | Squelette théorique de paquet ROS | Faible | Moyenne | La structure est compréhensible et compatible avec les travaux futurs |
| L04 | Modélisation URDF | Préparer le modèle de l'hexapode | Identifier liens, articulations, frames ; définir niveau de détail ; prévoir approximations | Données mécaniques ; nombre de degrés de liberté | Rémy | Tao | Spécification URDF ; liste des frames | Élevé | Haute | Le modèle prévu permet une visualisation cohérente sans surdétail inutile |
| L05 | Visualisation RViz | Préparer l'affichage du robot | Définir ce qui doit être visible ; prévoir configuration RViz ; relier URDF et états articulaires | Lot L04 ; interfaces d'état | Rémy | Clément | Configuration RViz prévue ; critères visuels | Moyen | Haute | Le scénario de visualisation minimal est défini et testable |
| L06 | Simulation simple `sim_hexa.py` | Définir le comportement du noeud de simulation | Décrire entrées/sorties ; choisir scénario simple ; limiter l'ambition ; prévoir publication d'états | Lot L02 ; niveau attendu professeur | Clément | Tao, Rémy | Spécification du noeud ; scénarios de test | Moyen | Haute | Le comportement minimal est démontrable sans simulation physique complète |
| L07 | Tests et validation | Définir comment vérifier le résultat | Lister tests d'interfaces ; tests RViz ; tests de cohérence frames ; critères professeur | Lots L02, L04, L05, L06 | Tao | Clément, Rémy | Plan de tests ; critères de réussite | Moyen | Moyenne | Chaque lot critique possède au moins un test simple |
| L08 | Documentation | Garder une trace exploitable du projet | Définir structure documentaire ; préparer notes quotidiennes ; centraliser décisions | Tous lots | Tao | Clément, Rémy | README projet prévu ; journal de décisions | Faible | Moyenne | Les décisions et blocages peuvent être présentés clairement |
| L09 | Préparation soutenance | Anticiper le support final | Lister messages clés ; prévoir captures RViz ; définir démonstration finale | Avancement technique ; critères professeur | Tao | Clément, Rémy | Plan de slides ; liste des visuels attendus | Moyen | Moyenne | La soutenance a un fil conducteur dès le cadrage |

Note : le lot L03 reste strictement organisationnel pendant la première demi-journée. Aucun paquet ROS réel ne doit être créé à ce stade.

## Découpage des parties complexes

| Sujet | Sous-tâches simples | Ordre conseillé | Livrable intermédiaire | Validation rapide |
|---|---|---|---|---|
| Interfaces ROS | Lister les besoins ; séparer commandes, états et paramètres ; définir producteurs/consommateurs ; choisir messages standard quand possible ; noter les incertitudes | Besoin -> flux -> noms -> types -> validation professeur | Tableau topics/services/actions | Une personne extérieure peut expliquer qui publie quoi et pourquoi |
| URDF | Définir base, corps, pattes ; lister liens ; lister articulations ; fixer axes ; nommer frames ; choisir géométries simples ; prévoir limites articulaires | Architecture mécanique -> frames -> articulations -> géométrie simplifiée -> cohérence RViz | Spécification URDF sans fichier complet | Le modèle prévu couvre toutes les pattes sans ambiguïté de nommage |
| Simulation `sim_hexa.py` | Définir scénario minimal ; choisir états publiés ; définir fréquence ; prévoir commandes simples ; documenter limites ; éviter dynamique physique | Sorties -> scénario -> entrées éventuelles -> fréquence -> tests | Spécification fonctionnelle du noeud | Le scénario peut animer ou mettre à jour les articulations attendues |
| Tests | Définir critères ; tester interfaces ; vérifier chargement robot ; vérifier frames ; vérifier affichage RViz ; noter blocages | Critères -> tests unitaires simples -> test intégration -> validation visuelle | Plan de tests | Chaque démonstration prévue a une preuve observable |
| Soutenance | Définir message ; choisir plan ; préparer captures ; présenter choix ; expliquer limites ; prévoir questions | Objectif -> architecture -> démonstration -> limites -> suite | Plan de slides | Le support explique le projet sans dépendre du code en direct |

## Points de vigilance

- Le lot URDF peut absorber trop de temps si le niveau de détail n'est pas borné.
- Les interfaces ROS doivent être définies avant de spécifier `sim_hexa.py`.
- RViz doit être traité comme un critère de réussite central, pas comme une finition.
- La documentation doit être alimentée chaque demi-journée.
