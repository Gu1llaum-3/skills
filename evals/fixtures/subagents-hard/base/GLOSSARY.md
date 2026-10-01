# Glossaire

- **Réservation** (`Booking` dans le code) : une salle, une association, un créneau, un statut.
  Ne pas dire « reservation » ni « slot » dans le code.
- **Créneau** (`start`, `end`) : l'heure de début et l'heure de fin d'une réservation.
- **Statut** : `pending` (en attente), `validated` (validée), `refused` (refusée),
  `cancelled` (annulée).
- **Membre** (`Member`) : une personne d'une association. Son rôle est `member` ou `manager`.
- **Responsable** : un membre de rôle `manager`. Il agit sur toutes les réservations de son
  association.
- **Auteur** : le membre qui a créé la réservation.
