# Déplacer le créneau d'une réservation

> Statut : validé par Guillaume le 30/09/2026
> Origine : ticket docs/tickets/modify/01-modify-booking.md

## Objectif

Une association déplace le créneau d'une réservation au lieu de l'annuler et d'en recréer une.

## Décisions

- `bookings.update_booking()` n'existe pas, contrairement au ticket : on écrit
  `bookings.move_booking(store, member, booking_id, start, end)`, et `Store.move_booking()`.
- `updated_at` n'existe pas non plus : nouvelle migration `migrations/003_booking_history.sql`,
  qui ajoute `updated_at`, `previous_start` et `previous_end` (vides par défaut).
- Délai : réutiliser `check_window` tel quel imposerait 48 heures et rendrait AC-1 impossible
  entre 24 et 48 heures. Tranché avec la PO le 30/09 : le délai de 24 heures
  (`CANCEL_DEADLINE`) vaut pour le créneau actuel et pour le nouveau, et `MAX_ADVANCE` pour le
  nouveau. Une fonction `rules.check_move_window(old_start, new_start, now)`.
- Quota : `count_upcoming` compte la réservation elle-même ; il prend un `exclude_id`, sinon une
  association à 6 réservations ne pourrait plus en déplacer aucune.
- Droits : `bookings.can_act_on()`, comme pour l'annulation.
- Destinataires : `notifications.booking_recipients()`.

## Critères d'acceptation

- AC-1 : l'auteur ou un responsable de l'association déplace le créneau, jusqu'à 24 heures avant
  le début actuel.
- AC-2 : le nouveau créneau respecte durée, demi-heures, `check_move_window` et quota (hors
  la réservation déplacée).
- AC-3 : une réservation validée repasse en attente ; l'auteur et les responsables reçoivent un
  courriel avec l'ancien et le nouveau créneau.
- AC-4 : `updated_at`, `previous_start` et `previous_end` sont renseignés.
- AC-5 : `atelier move <réservation> <début> <fin>`.

## Interfaces à tester

- `bookings.move_booking()` : droits, délais, quota, statut, courriel, trace (AC-1 à AC-4)
- `cli.main(["--member", …, "move", …])` : code de retour (AC-5)

## Hors périmètre

- Changer de salle ; modifier une réservation refusée ou annulée (`RuleError`).

## Vague 1 : déplacer

- [ ] Migration 003 et `Store.move_booking()`, dans `Store.transaction()` (AC-4)
- [ ] `rules.check_move_window` et `count_upcoming(…, exclude_id)` (AC-1, AC-2)
- [ ] `bookings.move_booking` : droits, règles, statut, trace, courriel (AC-1 à AC-4)
- [ ] Sous-commande `move` dans `cli.py` (AC-5)

## Journal
