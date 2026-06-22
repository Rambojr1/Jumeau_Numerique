# Rôles de l'équipe

## Répartition retenue

La répartition suit directement l'organisation souhaitée : Tao coordonne l'architecture globale, Clément prend les interfaces ROS et la stratégie de simulation, Rémy prend l'URDF, RViz et la cohérence visuelle. Aucun ajustement imposé par le document source n'est nécessaire.

## Tao

| Élément | Définition |
|---|---|
| Rôle principal | Coordination technique et architecture globale |
| Responsabilités | Maintenir la cohérence de la feuille de route ; arbitrer le périmètre ; structurer les jalons ; préparer les points professeur ; suivre les risques ; vérifier l'alignement entre interfaces, URDF, RViz et simulation |
| Livrables attendus | Feuille de route ; planning jalons ; synthèse professeur ; tableau de suivi des risques ; schéma d'architecture ROS global |
| Points à surveiller | Ne pas centraliser toute la production ; faire valider rapidement les hypothèses ; éviter que l'équipe parte en code sans critères |
| Interactions | Travaille avec Clément sur l'architecture ROS ; travaille avec Rémy sur la cohérence URDF/RViz ; consolide les retours des deux |
| Décisions sous responsabilité | Priorités de demi-journée ; périmètre minimum viable ; arbitrages entre ambition et temps disponible ; contenu du point professeur |
| Critères de qualité | Planning réaliste ; décisions traçables ; synthèse claire ; risques suivis ; équipe capable d'expliquer le projet en moins de 5 minutes |

## Clément

| Élément | Définition |
|---|---|
| Rôle principal | Interfaces ROS, structure logique du paquet et stratégie `sim_hexa.py` |
| Responsabilités | Proposer topics, services et actions ; définir producteurs/consommateurs ; préparer la structure théorique du paquet ; spécifier le comportement minimal de `sim_hexa.py` ; préparer les scénarios de test liés aux messages |
| Livrables attendus | Tableau des interfaces ROS ; squelette théorique du paquet ; spécification du noeud `sim_hexa.py`; scénarios de test d'interfaces |
| Points à surveiller | Ne pas inventer trop d'interfaces ; privilégier les messages utiles à RViz et à la démonstration ; éviter une simulation trop ambitieuse |
| Interactions | Valide avec Tao la cohérence architecture ; fournit à Rémy les états articulaires nécessaires pour RViz ; récupère les contraintes de frames définies côté URDF |
| Décisions sous responsabilité | Interfaces minimales ; rôle exact de `sim_hexa.py` ; conventions de nommage des topics ; limites du modèle de simulation |
| Critères de qualité | Interfaces compréhensibles ; absence de doublons ; simulation spécifiée de façon testable ; structure compatible avec la version ROS validée |

## Rémy

| Élément | Définition |
|---|---|
| Rôle principal | URDF, RViz, frames et validation visuelle |
| Responsabilités | Définir les liens et articulations du robot ; choisir le niveau de détail géométrique ; proposer les frames principales ; préparer la stratégie RViz ; définir les critères de validation visuelle |
| Livrables attendus | Spécification URDF ; liste des frames ; configuration RViz prévue ; critères de validation visuelle ; liste des données mécaniques manquantes |
| Points à surveiller | Ne pas viser une fidélité CAO trop coûteuse ; rester compatible avec les états publiés par `sim_hexa.py` ; éviter les erreurs de frames |
| Interactions | Valide avec Tao le niveau de détail acceptable ; transmet à Clément les noms d'articulations utiles ; récupère les états simulés nécessaires à RViz |
| Décisions sous responsabilité | Nommage des frames ; niveau de simplification URDF ; priorités d'affichage RViz ; critères visuels minimaux |
| Critères de qualité | Modèle visualisable ; frames cohérentes ; géométrie suffisante pour comprendre l'hexapode ; critères RViz vérifiables |

## Règles de fonctionnement

- Une décision technique importante doit être notée et associée à un responsable.
- Chaque demi-journée se termine par un livrable observable ou présentable.
- Les doublons sont évités : une personne pilote, les autres contribuent.
- Les points professeur servent à valider le périmètre, pas seulement à raconter l'avancement.
