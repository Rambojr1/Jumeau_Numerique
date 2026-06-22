# Feuille de route - Projet 1 : Jumeau numérique

## Résumé du besoin projet

Le projet consiste à développer un paquet ROS permettant de visualiser un hexapode dans RViz et de simuler son fonctionnement de façon simple. Le travail doit couvrir la définition des interfaces logicielles ROS, la préparation d'un modèle URDF, l'affichage dans RViz et un noeud de simulation nommé `sim_hexa.py`. L'équipe travaille à trois sur cinq demi-journées. La première demi-journée ne doit pas lancer le développement : elle sert à cadrer le travail, répartir les responsabilités, définir les jalons, identifier les livrables et anticiper les risques. Une soutenance avec support visuel est à préparer pour la fin du projet.

## Objectif global du jumeau numérique

Obtenir un prototype ROS cohérent permettant de représenter l'hexapode, de publier ou simuler des états articulaires simples, et de visualiser le résultat dans RViz avec des critères de validation clairs.

## Périmètre précis de la première demi-journée

La première demi-journée est consacrée à l'organisation du projet. Elle doit produire les documents de cadrage nécessaires pour éviter de partir trop vite dans le code, clarifier les choix à valider avec le professeur et sécuriser les cinq demi-journées de travail.

## Inclus dans la première demi-journée

- Lecture du sujet et identification des contraintes.
- Définition des hypothèses à valider.
- Découpage des lots de travaux.
- Répartition des rôles entre Tao, Clément et Rémy.
- Planning réaliste sur cinq demi-journées.
- Définition des jalons, livrables et critères de validation.
- Analyse des risques orientée temps, qualité et réussite du projet.
- Préparation d'une synthèse courte pour le professeur.

## Explicitement exclu

- Création réelle d'un paquet ROS.
- Écriture d'un URDF complet.
- Écriture du script `sim_hexa.py`.
- Implémentation de topics, services ou actions.
- Développement Gazebo ou simulation physique complète.
- Tests techniques réels dans ROS.
- Production des slides finales de soutenance.
- Recherche d'informations hors sujet ou dépendances externes.

## Contraintes projet identifiées

- Équipe de trois personnes : Tao, Clément, Rémy.
- Durée totale : cinq demi-journées.
- Première demi-journée réservée au cadrage.
- Point professeur à chaque début de journée complète : succès, blocages, choix techniques, objectifs.
- Feuille de route ajustable chaque jour selon l'avancement.
- Soutenance finale avec support visuel à prévoir.
- Sujet limité au Projet 1 : jumeau numérique de l'hexapode.

## Hypothèses de départ à valider rapidement

| Hypothèse                                         | Position de départ                                                 | Validation attendue                                                                              |
| -------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------ |
| Version ROS utilisée                              | À confirmer avant tout choix d'interface ou structure de paquet    | ROS 2                                                                                            |
| Disponibilité du modèle mécanique de l'hexapode | Incertaine                                                          | Vérifier si un modèle CAO, des plans ou des dimensions existent                                |
|                                                    |                                                                     |                                                                                                  |
| Existence de mesures CAO                           | Non confirmée                                                      | Demander si la précision géométrique est évaluée                                            |
| Niveau attendu de simulation                       | Simple modèle de fonctionnement, non simulation physique complète | Clarifier si `sim_hexa.py` publie seulement des états articulaires ou simule des trajectoires |
| Matériel réellement disponible                   | Oui                                                                 | Identifier si l'hexapode réel, des servos ou une documentation matérielle sont accessibles     |
| Niveau de détail attendu dans RViz                | Fonctionnel avant esthétique                                       | Confirmer le niveau de fidélité visuelle attendu                                               |
| Niveau attendu pour `sim_hexa.py`                | Noeud simple de démonstration                                      | Clarifier les entrées, sorties et scénarios minimaux attendus                                  |

## Cinq décisions à prendre dès la première demi-journée

1. Version ROS cible.
2. Niveau de fidélité du modèle URDF.
3. Interfaces ROS minimales à documenter.
4. Niveau de simulation attendu pour `sim_hexa.py`.
5. Statut de Gazebo : hors périmètre ou extension éventuelle.

## Cinq livrables à sortir avant la fin de la première demi-journée

1. Feuille de route validable.
2. Tableau des lots de travaux.
3. Répartition claire des rôles.
4. Planning avec jalons sur cinq demi-journées.
5. Analyse des risques avec plans de secours.
