# Cadrage d'utilisation de l'IA générative / Codex

## Objectif

Ce document définit comment utiliser une IA générative, comme Codex, pour aider l'équipe à avancer plus vite sans perdre le contrôle du projet.

L'IA doit servir à :

- clarifier les termes techniques ;
- organiser les tâches ;
- prioriser le MVP ;
- identifier les risques et blocages ;
- produire des résumés compréhensibles par l'équipe ;
- aider à préparer les livrables.

L'IA ne doit pas remplacer la compréhension personnelle du projet. Chaque membre doit pouvoir expliquer ce qu'il fait, pourquoi il le fait et comment son travail s'intègre dans le projet global.

## Règles générales d'utilisation

- Toujours donner le contexte avant de demander une réponse technique.
- Utiliser uniquement son prénom, pas d'informations personnelles inutiles.
- Joindre les fichiers utiles au cadrage avant de commencer.
- Demander une réponse structurée en Markdown.
- Faire reformuler les termes flous avant de commencer une tâche.
- Demander une méthode orientée MVP et temps minimum.
- Vérifier les propositions de l'IA avec l'équipe ou le professeur si elles touchent au périmètre du projet.
- Ne pas demander de développement complet si le besoin est seulement du cadrage.
- Ne pas copier une réponse sans la comprendre.

## 1. Prompt de création du projet

À utiliser au début, pour donner le contexte personnel à l'IA.

```text
Je suis [PRENOM UNIQUEMENT].

Voici les fichiers liés à l'organisation de l'équipe. Tu vas lire les données et les utiliser comme contexte de travail pour cette session, mais uniquement ce qui me concerne.

Tu dois retenir :
- mon rôle ;
- mes responsabilités ;
- mes livrables ;
- mes dépendances avec les autres membres ;
- les priorités MVP ;
- les règles d'organisation projet.

Tu ne dois pas utiliser les informations qui ne sont pas utiles à mon travail.
Tu dois m'aider à avancer vite, clairement, et avec des livrables compréhensibles par l'équipe.

Fichiers joints :
- 03_roles_equipe.md
- 05_livrables_par_personne.md
- 08_priorites_mvp.md
- 09_organisation_projet.md
- sujets_projets.pdf
```

## 2. Prompt avant de commencer un bloc

À utiliser avant un gros bloc de travail : interfaces ROS, URDF, RViz, simulation, tests, documentation ou soutenance.

```text
Avant de commencer ce bloc, donne-moi des explications sur chaque terme complexe, flou ou important du bloc suivant :

[INSERER LE BLOC TRAVAILLE]

Quel serait la méthode la plus efficace pour réaliser ces tâches dans un temps minimum ?

Voici le contexte :
- Contraintes logicielles : [INSERER LES CONTRAINTES LOGICIELLES]
- Langage utilisé : [INSERER LE LANGAGE]
- Architecture de fichiers et dossiers : [INSERER L'ARCHITECTURE]
- Objectif MVP : [INSERER L'OBJECTIF MVP]
- Livrable attendu : [INSERER LE LIVRABLE]

Organise l'ordre des tâches à prioriser dans ce bloc afin d'atteindre le MVP le plus vite possible.

Rends cela sous la forme d'un fichier Markdown clair avec :
- vocabulaire à comprendre ;
- méthode recommandée ;
- ordre des tâches ;
- résultat attendu ;
- points de vigilance ;
- mini checklist de fin de bloc.
```

## 3. Prompt avant de commencer une tâche

À utiliser avant une tâche précise à réaliser.

```text
Avant de commencer cette tâche, aide-moi à la cadrer :

Tâche :
[INSERER LA TACHE]

Donne-moi :
- les packages ou outils nécessaires ;
- l'architecture de fichiers concernée ;
- les limites possibles ;
- le temps estimé ;
- les points durs possibles ;
- les zones de flou ;
- les choses qui pourront me bloquer lors de sa réalisation.

Dis-moi comment m'organiser à l'avance pour terminer cette tâche le plus vite possible, avec un niveau maximal de clarté pour mon équipe et pour la compréhension du projet final.

Rends la réponse en Markdown avec :
- résumé de la tâche ;
- prérequis ;
- méthode rapide ;
- ordre d'exécution ;
- risques ;
- critères de réussite ;
- résumé final à partager à l'équipe.
```

## 4. Prompt pendant un blocage

À utiliser si un problème dure plus de 15 minutes.

```text
Je suis bloqué depuis plus de 15 minutes sur ce problème :

Bloc concerné :
[INSERER LE BLOC]

Tâche concernée :
[INSERER LA TACHE]

Erreur ou problème observé :
[COPIER L'ERREUR OU DECRIRE LE PROBLEME]

Ce que j'ai déjà essayé :
[LISTER LES TESTS]

Contexte :
- Version ROS : [A COMPLETER]
- Fichiers concernés : [A COMPLETER]
- Commandes lancées : [A COMPLETER]
- Résultat attendu : [A COMPLETER]
- Résultat obtenu : [A COMPLETER]

Aide-moi à :
- formuler un ticket Notion clair ;
- identifier les causes probables ;
- proposer trois tests rapides ;
- choisir le meilleur plan de secours compatible avec le MVP.
```

## 5. Prompt pour produire un résumé d'équipe

À utiliser à la fin d'un bloc ou d'une demi-journée.

```text
À partir de ce que j'ai fait, rédige un résumé court pour l'équipe.

Travail réalisé :
[INSERER CE QUI A ETE FAIT]

Bloc concerné :
[INSERER LE BLOC]

Résultat obtenu :
[INSERER LE RESULTAT]

Blocages ou limites :
[INSERER LES LIMITES]

Prochaine action :
[INSERER LA SUITE]

Le résumé doit être compréhensible par quelqu'un qui n'a pas fait la tâche.
Il doit expliquer :
- l'utilisation ;
- le fonctionnement ;
- ce qui est terminé ;
- ce qui reste à valider.
```

## 6. Format attendu des réponses IA

Demander de préférence un format Markdown avec :

- une section "Résumé" ;
- une section "Termes à comprendre" ;
- une section "Méthode recommandée" ;
- une section "Ordre des tâches" ;
- une section "Risques / blocages possibles" ;
- une section "Critères de réussite" ;
- une section "Résumé à partager à l'équipe".

## 7. Points de vigilance

- L'IA peut proposer des solutions trop ambitieuses : toujours revenir au MVP.
- L'IA peut inventer des détails non confirmés : vérifier avec le professeur.
- L'IA peut produire une architecture trop complexe : garder une structure répétable et claire.
- L'IA peut générer du code avant le cadrage : demander d'abord une explication et une méthode.
- L'IA peut oublier les contraintes du projet : rappeler les fichiers et le rôle personnel au début de chaque session.

## 8. Checklist d'utilisation rapide

Avant d'utiliser l'IA :

- Mon prénom et mon rôle sont indiqués.
- Les fichiers utiles sont joints.
- Le bloc ou la tâche est clairement nommé.
- Le contexte logiciel est précisé.
- Le livrable attendu est indiqué.
- Le niveau MVP est rappelé.

Après la réponse IA :

- Je comprends les termes importants.
- Je sais quelle tâche faire en premier.
- Je sais quoi livrer.
- Je connais les risques principaux.
- Je peux expliquer mon travail à l'équipe.
- Si un blocage dépasse 15 minutes, je crée un ticket Notion.
