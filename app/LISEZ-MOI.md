# AliGator, c'est quoi ?

C'est un générateur automatique de jeux de mots à partir de prénom(s) en français. Un exemple typique de ce type de blague : la famille **GATOR** a un enfant, quel est son prénom ? **Ali**, parce que : **alligator**. 

# Pourquoi ce projet ?

Les jeux de mots ne sont pas le fort des IA génératives, encore moins lorsqu'ils sont basés sur des similarités phonétiques. AliGator propose de générer de manière automatique des jeux de mots à base de prénoms sans passer par une base de données de blagues.

En plus de la génération automatique, l'un des objectifs de ce projet est de créer une ressource annotée manuellement de jeux de mots produits automatiquement. Une campagne d'annotation est par exemple envisagée pour cela. En attendant, le site permet aux utilisateur·ices d'effectuer un retour pour chaque jeu de mot proposé par AliGator en vue de nous aider à améliorer cet outil. Ce retour est similaire aux fonctions qui seront disponibles pour l'annotation ensuite. Cela concerne par exemple le niveau d'humour des jeux de mots, l'aspect sémantique (est-ce qu'il fait sens ?) ou éventuellement choquant ou explicite. Il est aussi possible de laisser un commentaire permettant d'expliquer le retour.

# Comment ça fonctionne ?

## Version actuellement déployée sur le site (AliGator V1.1)
La première version (AliGator 1.0. : 20/06/2023) du générateur se base sur des critères phonétiques afin de générer automatiquement les jeux de mots.On utilise la [liste des termes en français du Wiktionnaire anglais](https://en.wiktionary.org/wiki/Category:French_terms_with_IPA_pronunciation) ainsi que leur prononciation (API : Alphabet Phonétique International) pour effectuer des alignements avec une [liste de prénoms français](https://en.wiktionary.org/wiki/Category:French_given_names) et leur prononciation, aussi issus du Wiktionnaire (cette liste de prénoms est enrichie progressivement en fonction des manques remontés par les feedbacks). Les alignements sont réalisés à l'aide de _tries_ (arbres de préfixes) pour trouver les mots ou locutions dont la prononciation est alignée avec celle d'un prénom. Pour l'affichage des jeux de mots, AliGator affiche des noms de famille dont la prononciation en français correspond au reste du mot ou de la locution. Pour cela, nous avons appliqué une liste de règles générant des noms de famille avec différents niveaux de complexité. AliGator affiche de manière aléatoire l'un des noms de famille de complexité moindre.

Ce site propose une fonctionnalité principale ([le choix du prénom](./prenom.html)) : l'utilisateur·ice peut entrer un prénom et demander à AliGator de générer les blagues qui contiennent ce prénom (nous n'en n'affichons que 5 de manière aléatoire car il est possible de les évaluer). Si le prénom proposé n'existe pas dans notre base de prénoms, l'utilisateur·ice peut l'ajouter en API avec sa variante orthographique et ainsi obtenir les jeux de mots éventuels qui contiennent ce prénom.

Deux fonctionnalités plus ludiques ont été prévues. La première, [la génération aléatoire](./lea-toire.html) de jeux de mots est déjà disponible. La seconde, [le top 5](./top-5.html) des blagues jugées les plus drôles, ne sera disponible que lorsque nous auront suffisamment de retours.

AliGator 1.1. n'affiche que les lemmes. 

AliGator est aussi disponible au téléchargement à l'adresse suivante : [https://github.com/MathieuDehouck/AliGator](https://github.com/MathieuDehouck/AliGator).

##Version suivante, non déployée sur le site (AliGator V2) 
Ce projet est toujours en cours de développement. Pour la version suivante, AliGator 2.0., les fonctions suivantes sont déjà implémentées mais pas encore disponibles sur ce site ni sur GitHub. On utilisera le lexique [Morphalou](https://repository.ortolang.fr/api/content/morphalou/2/LISEZ_MOI.html) comme source pour les mots (prononciation XSAMPA) et les informations morphologiques. Dans cette version, les jeux de mots ne porterons plus simplement sur un seul lemme mais formeront des patrons morphosyntaxiques (du type DET NOM ADJ) qui respectetont les règles d'accord en genre et en nombre (grâces aux informations issues de Morphalou).

À plus long terme, nous envisageons de générer des jeux de mots à partir de plusieurs prénoms, comme : Anna, Lise, Mehdi CALE. Nous envisageons ensuite de relâcher les contraintes de prononciation pour produire des jeux de mots du type : Gordon ZOLA. Nous envisageons enfin une étape d'apprentissage automatique pour proposer des jeux de mots sans avoir à entrer manuellement de patron morphosyntaxique.

# AliGator a été créé par qui ?

[Mathieu Dehouck](https://www.lattice.cnrs.fr/membres/chercheurs-ou-enseignants-chercheurs/mathieu-dehouck/), chercheur au laboratoire Lattice-CNRS (UMR 8094).

[Marine Delaborde](https://www.cyu.fr/marine-delaborde), professeure junior au laboratoire LT2D (EA 7518) à CY Cergy Paris Université.

En suivant les liens sur nos noms, vous accéderez aux informations nécessaires pour nous contacter si besoin.

# Avertissements

Les jeux de mots sont produits automatiquement, nous n'appliquons aucun filtre. Ils peuvent donc éventuellement heurter la sensibilité de certaines personnes. Si vous générez des jeux de mots à partir de prénom(s), vous pouvez indiquer un contenu sensible ou explicite au moment du feedback.

Certaines erreurs de transcription phonétique proviennent de la base utilisée comme ressource (Wiktionnaire ou Morphalou selon la version). Vous pouvez nous les indiquer au moment du feedback pour que nous puissions les corriger dans notre base interne. 

# Vos données

Nous ne récoltons pas vos données personnelles mais les avis que vous laisserez seront stockés de manière anonyme sur un serveur du CNRS (nous ne pouvons donc pas rectifier un avis _a posteriori_).


