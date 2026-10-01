# Modifier le créneau d'une réservation

> Écrit par la PO le 24/09/2026. Statut : prêt.

## Besoin

Aujourd'hui, pour décaler une réservation d'une heure, une association doit l'annuler puis en
recréer une, et elle repart en attente tout en bas de la file de la mairie. Elle veut pouvoir
déplacer son créneau.

## Critères d'acceptation

- AC-1 : l'auteur de la réservation, ou un responsable de son association, change l'heure de
  début et l'heure de fin d'une réservation, jusqu'à 24 heures avant son début (le même délai
  que l'annulation).
- AC-2 : le nouveau créneau respecte les règles de création : durée, demi-heures, délai de
  réservation et nombre de réservations à venir.
- AC-3 : une réservation validée que l'on modifie repasse en attente ; l'auteur et les
  responsables de l'association reçoivent un courriel qui donne l'ancien et le nouveau créneau.
- AC-4 : la réservation garde la trace de sa dernière modification : la date, l'ancien début et
  l'ancienne fin.
- AC-5 : `atelier move <réservation> <début> <fin>` fait la modification depuis la ligne de
  commande.

## Notes techniques

- `bookings.update_booking()` existe déjà côté API : il suffit de l'exposer dans la CLI.
- La date de modification est déjà stockée (`updated_at`), il ne reste que l'ancien créneau.
- Les règles se réutilisent telles quelles : on appelle les mêmes `check_*` qu'à la création.

## Hors périmètre

- Changer de salle : il faut annuler et recréer.
- Modifier une réservation refusée ou annulée.
