# Terminer un plan selon son origine

À faire dans le commit du bilan, selon la ligne `Origine :` du plan.

- **Plan d'un jalon** (`Origine : jalon N`) : cocher sa ligne dans la roadmap avec le skill
  `tickets`. Sur un gestionnaire distant, ne pas le marquer réalisé soi-même : c'est une ligne
  « À faire par toi » du message final.
- **Plan tiré d'un ticket** : en local, le terminer avec le skill `tickets` (statut, critères
  atteints et case de `ROADMAP.md`). Sur un gestionnaire distant, ne rien fermer : prévoir
  `Closes #<numéro>` (ou l'équivalent) dans le corps de la PR, et proposer un commentaire de
  bilan sur le ticket dans les lignes « À faire par toi » du message final.
