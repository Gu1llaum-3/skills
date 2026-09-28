---
name: to-questionnaire
description: Transformer les questions auxquelles l'utilisateur ne peut pas répondre seul (règles métier, juridique, chiffres, priorités produit) en questionnaire à faire remplir par une personne précise — métier, client, product owner, auteur d'un ticket — rangé dans docs/questionnaires/, puis réintégrer ses réponses. Utilise ce skill quand l'utilisateur veut préparer des questions pour quelqu'un d'autre (« fais un questionnaire pour le métier », « prépare les questions pour la PO », « il faut que je demande ça à la compta ») ou revient avec un questionnaire rempli, et chaque fois qu'un autre skill (interview, brainstorming, feature, to-spec, plan) a des questions pour le métier.
---

# To-questionnaire : faire répondre le métier

Quand une décision appartient à quelqu'un d'autre, le questionnaire sert à obtenir la réponse
de celui qui la détient, en asynchrone ou en réunion. Ce qui a de la valeur : des questions
qu'il peut comprendre sans avoir suivi la conversation, et des réponses qui reviennent
exploitables.

**On questionne l'utilisateur sur l'envoi, pas sur le sujet** : s'il connaissait le sujet, il
n'aurait pas besoin d'écrire à quelqu'un. Les questions du document visent l'écart entre ce que
sait le destinataire et ce dont l'utilisateur a besoin.

Réponds dans la langue de l'utilisateur.

## 1. Rassembler les questions

- Celles qu'`interview` a mises de côté pour le métier, avec leur hypothèse et leur caractère
  bloquant, ou celles des sections « Questions ouvertes » marquées pour un destinataire (voir
  « Dans les documents »).
- Appelé seul : demander en un échange ce que l'utilisateur doit pouvoir décider ou savoir à la
  fin. C'est la liste à couvrir.

S'il y a plusieurs destinataires, **un questionnaire par destinataire** : le ton et le contexte
dépendent de la personne.

## 2. Préciser le destinataire

En un seul échange, pour chaque destinataire qui n'est pas déjà connu : son rôle, ce qu'il sait
que l'utilisateur ne sait pas, sa relation avec lui (collègue, client externe), et l'échéance.
Rien sur le fond : si une question sur le sujet paraît nécessaire, c'est qu'elle doit aller
dans le questionnaire.

## 3. Rédiger

Écrire `docs/questionnaires/<slug>-<destinataire>.md` en suivant
[references/questionnaire.md](references/questionnaire.md) :

- les questions **les plus importantes d'abord**, les bloquantes en tête : en asynchrone, on n'a
  souvent qu'un seul passage ;
- réécrire chaque question **pour le destinataire**, dans ses mots, avec le contexte qu'il n'a
  pas : pas une copie des questions de la conversation ;
- **une idée par question** ;
- **question non bloquante** : montrer l'hypothèse retenue (« en attendant, on part sur X :
  dites-nous si c'est faux »). **Question bloquante** : la poser ouverte, pour ne pas orienter
  la réponse.

Vérifier que chaque élément de la liste de l'étape 1 est couvert, puis montrer le brouillon.

## 4. Envoyer

- **S'il y a un ticket** (celui qu'on planifie, ou la spec) : proposer de publier le
  questionnaire en commentaire avec le skill `tickets`, seulement après accord sur le texte
  exact.
- Sinon : donner le chemin du fichier. Il s'envoie par mail, par message, ou se remplit en
  réunion.

Une fois le questionnaire publié ou le chemin donné, écrire `> Statut : envoyé le JJ/MM/AAAA` en
tête du fichier : c'est ce qui dit, à la reprise, qu'une réponse est attendue.

Dans le document d'origine (cahier des charges, spec, plan), faire pointer chaque question vers
le questionnaire.

## 5. Réintégrer les réponses

Quand l'utilisateur revient avec les réponses (le fichier rempli, un mail collé, un commentaire
de ticket) :

- les recopier dans le questionnaire, qui reste la trace de qui a décidé quoi, et passer son
  statut à « répondu » ;
- les reporter dans le document d'origine : chaque réponse devient une décision, et la question
  est retirée des questions ouvertes. Une hypothèse démentie se signale avec ce qu'elle change
  déjà (un plan en cours, un ticket publié) ;
- une réponse floue, « je ne sais pas » ou une nouvelle question : la garder ouverte et le
  dire ;
- proposer de reprendre là où on s'était arrêté : l'étape 5 de `brainstorming`, `to-spec` ou
  `plan`.

## Dans les documents

Dans la section « Questions ouvertes » d'un cahier des charges, d'une spec, d'un ticket ou d'un
plan, une question pour le métier s'écrit :

```markdown
3. **[Métier : compta, bloquante]** Un avoir peut-il dépasser le montant de la commande ?
   → [questionnaire](docs/questionnaires/avoirs-compta.md)
4. **[Métier : PO]** Faut-il notifier le client par mail ? Hypothèse : oui, un mail simple.
```

Une question bloquante empêche de valider le plan qui en dépend. Une question non bloquante
laisse avancer avec son hypothèse.

## Ce que ce skill ne fait jamais

- Poser à l'utilisateur des questions sur le fond.
- Mélanger plusieurs destinataires dans un même questionnaire.
- Publier ou envoyer un questionnaire sans accord sur le texte.
- Transformer une réponse floue en décision.
