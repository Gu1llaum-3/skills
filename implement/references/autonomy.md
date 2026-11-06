# La section « Autonomie » d'un projet

Un projet qui veut avancer sans attendre l'utilisateur entre deux tickets le dit dans une section
`## Autonomie` de son `CLAUDE.md`. Elle est lue par `plan` (validation du plan), `implement`
(journal, fin du plan) et `/ticket-chain` (enchaînement des tickets d'une spec). **Sans cette
section, rien ne change** : le plan attend le feu vert de l'utilisateur, les décisions autonomes
ne vont que dans le journal du plan, et `implement` finit par une PR en brouillon.

La section vaut accord permanent entre `plan` et `implement`, pour les seuls tickets qu'elle
couvre. Elle ne change rien aux autres sources (cahier des charges, conversation, POC).

## Les entrées

Une ligne par entrée ; une entrée absente prend sa valeur par défaut.

| Entrée | Ce qu'elle dit | Par défaut |
|---|---|---|
| **Plan sans validation** | les tickets dont le plan se valide seul : `tickets cadrés` (écrits par `to-spec` ou `to-tickets`, avec leurs critères) ou `non` | `non` |
| **Journal** | le fichier des décisions du projet | `docs/journal.md` |
| **Fin** | `PR en brouillon`, ou `fusion locale` (squash merge dans la branche principale) | `PR en brouillon` |
| **Pied de commit** | la ligne qui cite le ticket dans le commit de squash | `Ticket: <ref>` |
| **Vérification** | la commande de vérification complète, et comment lancer des tests ciblés | celles que trouve `implement` |
| **Chemins sensibles** | un fichier de préfixes de chemins (un par ligne, `#` pour les commentaires) dont la modification demande une relecture de sécurité avant fusion | aucun |
| **À demander** | ce qui arrête le travail pour attendre l'utilisateur | questions métier (règles, chiffres, juridique), ajout hors périmètre, action irréversible ou hors du dépôt (service externe, secret, suppression de données) |

`/ticket-chain` exige `Fin : fusion locale` et une commande de vérification écrite.

## Le journal du projet

Avec la section, chaque décision autonome (`> Décision autonome` d'`implement`, point tranché
seul par `plan`, remarque « À décider » tranchée par l'enchaînement) s'écrit **aussi** dans le
journal du projet, en tête des entrées, dans ce format :

```markdown
## AAAA-MM-JJ · <ticket> · <titre court>

- **Contexte** : ce qui a posé question.
- **Décision** : ce qui a été retenu.
- **Alternatives** : ce qui a été écarté, et pourquoi.
- **Sources** : recherches, documentation, ADR liés.
- **À revoir si** : la condition qui remettrait la décision en cause.
```

Le journal du plan garde sa ligne courte, avec un renvoi vers l'entrée. Une décision qui coche les
trois critères d'un ADR en reçoit un en plus (skill `adr`).

## Exemple (projet inventé)

```markdown
## Autonomie

- Plan sans validation : tickets cadrés
- Journal : docs/journal.md
- Fin : fusion locale
- Pied de commit : Ticket: <ref>
- Vérification : `just verify` ; tests ciblés : `just test <fichier>`, `just lint`
- Chemins sensibles : .claude/sensitive-paths.txt
- À demander : règles de réservation et de remboursement, tout ajout hors du cahier des
  charges, action irréversible ou hors du dépôt
```

Et son fichier de chemins sensibles :

```
# Comptes et sessions
src/auth
src/sessions
# Paiement des réservations
src/payments
```
