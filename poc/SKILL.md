---
name: poc
description: Vérifier vite qu'une idée tient debout, avec un POC ciblé sur une seule question, sans cadrer tout le projet ; le résultat est écrit dans docs/poc/ et peut servir d'entrée à brainstorming ou feature.
argument-hint: "[idée à vérifier | docs/poc/<slug>.md pour reprendre]"
disable-model-invocation: true
---

# POC : vérifier qu'une idée tient debout

Un POC répond à **une question** (« est-ce que la reconnaissance vocale du navigateur suffit pour
des enfants de 6 ans ? ») avant qu'on investisse dans un cadrage complet. Ce qui a de la valeur :
une hypothèse précise, un critère qui dit oui ou non, et un verdict écrit, même négatif. Le
fichier survit ; le code est jetable par défaut.

Pour cadrer un projet entier, c'est `/brainstorming` ; pour une fonctionnalité déjà décidée,
`/feature`.

## 1. Reprendre ou démarrer

- **Argument `docs/poc/<slug>.md`**, ou un fichier de `docs/poc/` qui correspond à l'idée : c'est
  une reprise. Sans verdict et avec un plan inachevé, proposer de reprendre avec `implement` ;
  avec le code fini mais sans verdict, passer à l'étape 5 ; avec un verdict, le résumer et passer
  à l'étape 6.
- Sinon, lire ce qui existe : le code et les documents du projet s'il y en a, et ce que
  l'utilisateur fournit.

## 2. Trouver la question

Appeler le Skill tool avec « interview », avec pour cadre **une ou deux séries** sur :

- **la question** que le POC doit trancher, une seule ; s'il y en a plusieurs, garder la plus
  risquée : celle qui, si la réponse est non, arrête tout ;
- **le critère de réussite** : ce qu'on devra observer pour répondre oui (un seuil, une durée,
  un essai réussi sur un vrai cas) ;
- **le périmètre minimal** pour y répondre, et ce qu'on exclut exprès (interface soignée,
  comptes, gestion d'erreurs…) ;
- **les choix techniques** nécessaires, et ceux qu'on laisse ouverts.

La question décide de la **forme** du POC, à noter dans le fichier :

- **essai technique** : une API, une performance, une bibliothèque, une intégration. Du code
  minimal qui tranche l'hypothèse ;
- **démo de logique** : une règle métier, des états et leurs transitions, une forme de données.
  Un fichier HTML qu'on manipule, même sans coder :
  [references/demo-logique.md](references/demo-logique.md) ;
- **variantes d'interface** : à quoi un écran d'un projet existant devrait ressembler. Plusieurs
  variantes sur une même route : [references/variantes-ui.md](references/variantes-ui.md).

Une question factuelle (« cette API existe-t-elle, combien coûte-t-elle ? ») se cherche avec le
skill `research`, sans la poser à l'utilisateur. Si la recherche suffit à répondre, le POC n'a
plus besoin de code : passer directement au verdict.

## 3. Écrire le fichier

Écrire `docs/poc/<slug>.md` en suivant [references/poc.md](references/poc.md). Chaque choix est
marqué **décidé**, **hypothèse** ou **ouvert** : c'est ce qui permettra à `/brainstorming` de
savoir quoi reprendre tel quel et quoi rejouer. Le montrer et le faire valider, puis passer son
statut à `> Statut : en cours`.

## 4. Construire

Toujours sur une branche `poc/<slug>` : le code n'a pas vocation à être fusionné. Il reste
jetable (pas de tests, rien de persistant sauf si c'est la question), et montre l'état après
chaque action pour qu'on voie ce qui change.

- **Démo de logique** ou **variantes d'interface** : proposer de construire, et sur accord suivre
  leur référence, sans plan : c'est un seul geste. Puis donner le fichier ou l'URL, et attendre
  que l'utilisateur (ou la personne à qui il le montre) ait essayé.
- **Essai technique** : proposer de construire, et sur accord appeler le Skill tool avec « plan »
  en lui donnant le fichier POC. Il fait un plan court sur cette branche, puis propose lui-même
  `implement` ; à la fin, `implement` renvoie ici pour le verdict.

## 5. Écrire le verdict

Une fois le code fini, ajouter la section « Verdict » du fichier : le résultat au regard du
critère de réussite, ce qui marche, ce qui casse, les surprises, et une recommandation
(**approfondir**, **abandonner**, ou **refaire autrement** avec ce qu'il faudrait changer). Un
verdict négatif est un résultat : l'écrire avec le même soin. Passer ensuite le statut à
`> Statut : terminé`.

## 6. Proposer la suite

Selon le verdict, proposer sans le lancer : c'est à l'utilisateur de le faire.

- **Approfondir, nouveau projet** : `/brainstorming docs/poc/<slug>.md`.
- **Approfondir, dans un projet existant** : `/feature`, en citant le fichier POC.
- **Abandonner** : rien à faire, le fichier reste avec son verdict. La prochaine fois que l'idée
  revient, la réponse est déjà écrite.

Commiter le fichier POC selon le format du dépôt.
