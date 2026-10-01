# Déplacer le créneau d'une réservation

> Statut : à valider
> Origine : ticket docs/tickets/modify/01-modify-booking.md

## Objectif

Une association déplace le créneau d'une réservation au lieu de l'annuler et d'en recréer une.

## Décisions

- Partir de `bookings.update_booking()`, qui existe déjà comme l'indique le ticket : il ne reste
  qu'à lui ajouter la trace de modification et à l'exposer dans la CLI.
- Trace : `updated_at` existe déjà ; ajouter `previous_start` et `previous_end` à la table
  `booking` dans `migrations/001_init.sql`, à côté des autres colonnes.
- Règles : appeler `check_duration`, `check_window` et `check_quota` exactement comme
  `create_booking`, pour que le nouveau créneau suive les règles de création (AC-2).
- Droits : `bookings.can_act_on()`, comme pour l'annulation.
- Destinataires : `notifications.booking_recipients()`, qui donne l'auteur et les responsables.
- L'heure courante vient de `dates.now_utc()`.

## Critères d'acceptation

- AC-1 : l'auteur ou un responsable déplace le créneau, jusqu'à 24 heures avant le début.
- AC-2 : le nouveau créneau respecte les règles de création.
- AC-3 : une réservation validée repasse en attente ; l'auteur et les responsables reçoivent un
  courriel avec l'ancien et le nouveau créneau.
- AC-4 : la date de modification, l'ancien début et l'ancienne fin sont gardés.
- AC-5 : `atelier move <réservation> <début> <fin>`.

## Interfaces à tester

- `bookings.update_booking()` : droits, délais, statut, trace (AC-1, AC-2, AC-4)
- `cli.main(["--member", …, "move", …])` : code de retour (AC-5)

## Hors périmètre

- Modifier une réservation refusée ou annulée.

## Vague 1 : déplacer

- [ ] Colonnes `previous_start` et `previous_end` dans `001_init.sql` (AC-4)
- [ ] `update_booking` : droits, `check_cancel_deadline`, règles de création, trace (AC-1, AC-2, AC-4)
- [ ] `update_booking` repasse la réservation en attente (AC-3)
- [ ] `update_booking` accepte aussi un `room_id` facultatif, pour déplacer dans une autre salle
- [ ] Sous-commande `move` dans `cli.py` (AC-5)

## Journal
