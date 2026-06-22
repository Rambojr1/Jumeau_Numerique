# Livrables par personne

## Tableau de répartition

| Personne | Rôle | Livrables attendus | Format du livrable | Deadline approximative | Critères de qualité | Dépendances avec les autres membres |
|---|---|---|---|---|---|---|
| Tao | Coordination technique et architecture globale | Document de cadrage ; planning 5 demi-journées ; jalons ; synthèse professeur ; tableau de suivi des risques ; schéma d'architecture ROS global | Markdown ; tableau ; schéma simple | Cadrage : fin demi-journée 1 ; architecture consolidée : demi-journée 2 | Clair, court, validable par le professeur ; décisions et risques traçables | Reçoit les contraintes interfaces de Clément et les contraintes URDF/RViz de Rémy |
| Clément | Interfaces ROS, structure logique du paquet, stratégie `sim_hexa.py` | Tableau des topics/services/actions ; squelette théorique du paquet ROS ; spécification du script `sim_hexa.py` ; scénarios de tests d'interfaces | Tableaux Markdown ; schéma logique ; fiche de spécification | Interfaces : demi-journée 2 ; simulation : demi-journée 4 | Interfaces minimales et cohérentes ; pas de surconception ; simulation simple et testable | Dépend de la version ROS validée par Tao ; fournit à Rémy les noms d'articulations et états publiés |
| Rémy | URDF, RViz, frames et validation visuelle | Spécification URDF ; liste des frames ; fichier launch prévu ; configuration RViz prévue ; critères de validation visuelle | Liste structurée ; tableau de frames ; fiche RViz | Spécification : demi-journée 3 ; validation visuelle : demi-journée 4 | Modèle suffisamment fidèle pour comprendre l'hexapode ; frames cohérentes ; RViz priorisé | Dépend des interfaces de Clément ; fournit à Tao les risques mécaniques et visuels |

## Livrables de cadrage attendus en fin de première demi-journée

| Livrable | Responsable | Utilité immédiate |
|---|---|---|
| Feuille de route | Tao | Poser le périmètre et les hypothèses à valider |
| Lots de travaux | Tao | Répartir le projet en blocs pilotables |
| Rôles équipe | Tao | Éviter les doublons et zones floues |
| Planning jalons | Tao | Sécuriser les cinq demi-journées |
| Analyse des risques | Tao | Anticiper les pertes de temps et plans de secours |
| Synthèse professeur | Tao | Préparer le point d'avancement |

## Livrables techniques à spécifier, pas à finaliser en première demi-journée

| Type de livrable | Responsable principal | Statut attendu en première demi-journée |
|---|---|---|
| Tableau des topics/services/actions | Clément | Besoin identifié, contenu détaillé prévu pour demi-journée 2 |
| Schéma d'architecture ROS | Tao | Structure globale esquissée |
| Squelette théorique de paquet ROS | Clément | Dossiers et fichiers attendus listés, sans création réelle |
| Spécification URDF | Rémy | Informations manquantes et niveau de détail à valider |
| Fichier launch prévu | Rémy | Besoin noté, pas de fichier technique créé |
| Configuration RViz prévue | Rémy | Critères visuels définis |
| Spécification du script `sim_hexa.py` | Clément | Rôle du noeud et niveau de simulation à clarifier |
| Rapport de tests | Tao | Critères de test définis, exécution future |
| Slides de soutenance | Tao | Plan de support anticipé |
| Tableau de suivi des risques | Tao | Risques initiaux priorisés |
