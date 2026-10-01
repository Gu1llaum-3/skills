# Cahier des charges : Atelier, réservation de salles pour associations

> Version 0.2, décisions du 28/09/2026 intégrées.

## 1. Contexte et objectif

Les associations du quartier partagent quatre salles municipales (la grande salle, la salle
de réunion, l'atelier et la cuisine). Les réservations se font aujourd'hui par courriel auprès
de la mairie, qui tient un tableur. Les conflits sont fréquents : deux associations arrivent à
la même heure, une salle reste fermée faute de clé.

Atelier remplace le tableur par une application web : chaque association réserve elle-même un
créneau libre, la mairie valide, et chacun voit le planning à jour.

On verra que c'est réussi quand la mairie ne reçoit plus de demandes par courriel (objectif :
moins de 5 par mois après trois mois) et qu'aucun double usage d'une salle n'est signalé.

## 2. Public et profils

L'application connaît les trois profils suivants :

- **Membre** : une personne d'une association. Consulte le planning, réserve pour son
  association.
- **Responsable d'association** : un membre qui gère les membres de son association et voit
  l'historique de ses réservations.
- **Agent de la mairie** : valide ou refuse les réservations, gère les salles et leurs
  horaires d'ouverture.
- **Administrateur** : crée les associations, gère les comptes des agents, consulte les
  journaux.

Un compte appartient à une seule association, sauf les agents et les administrateurs, qui
n'appartiennent à aucune.

## 3. Réservations

### 3.1 Créneaux

- Une réservation porte sur une salle, une date, une heure de début et une heure de fin.
- Les créneaux se prennent par demi-heure, entre 8 h et 23 h.
- Une réservation dure au moins une heure et au plus huit heures.
- Une association peut avoir au plus 6 réservations à venir en même temps, toutes salles
  confondues.
- On réserve au plus tôt 60 jours à l'avance et au plus tard 48 heures avant le début.

### 3.2 Validation

- Toute réservation est créée « en attente ». Un agent la valide ou la refuse, avec un motif
  obligatoire en cas de refus.
- Sans réponse sous 5 jours ouvrés, la réservation est validée automatiquement.
- Deux réservations en attente peuvent se chevaucher ; une réservation validée bloque le
  créneau, et les demandes en attente qui la chevauchent sont refusées avec le motif « créneau
  déjà attribué ».

### 3.3 Annulation

- Le membre qui a réservé, ou le responsable de son association, peut annuler jusqu'à 24 heures
  avant le début.
- Plus tard, l'annulation passe par un agent.
- Trois annulations tardives en un trimestre suspendent les réservations de l'association
  pendant 30 jours (voir la question ouverte 7).

## 4. Planning

- Le planning montre la semaine en cours par défaut, salle par salle, avec les réservations
  validées en couleur pleine et celles en attente en hachuré.
- Un membre voit le nom de l'association qui occupe un créneau, jamais le nom de la personne.
- Le planning se filtre par salle et par association.
- Il s'imprime sur une page A4 paysage par semaine.

## 5. Notifications

- Un courriel part à la création (au membre), à la validation et au refus (au membre et au
  responsable), et à l'annulation (à tous ceux qui ont reçu la validation).
- Un rappel part 48 heures avant le début, avec le code de la boîte à clés de la salle.
- Le jour même, le planning affiche sur le créneau le nom et le téléphone du membre qui a
  réservé, pour que les autres associations puissent le joindre.
- Les courriels sont en français, sans image, lisibles sur téléphone.

## 6. Salles

- Chaque salle a un nom, une capacité, des équipements (vidéoprojecteur, cuisine, sono) et des
  horaires d'ouverture par jour de la semaine.
- Un agent peut fermer une salle sur une période (travaux, vacances) : les réservations
  validées sur cette période sont annulées et les associations prévenues.
- Le code de la boîte à clés change chaque mois ; il est saisi par un agent.

## 7. Données et conservation

- Les réservations passées sont conservées 2 ans, puis anonymisées : l'association reste, le
  membre disparaît.
- Les journaux d'accès sont conservés 1 an.
- Une sauvegarde complète est faite chaque nuit, et chaque sauvegarde est conservée 30 jours.
- Les données sont hébergées en France.

## 8. Exports et statistiques

- L'agent exporte en CSV les réservations d'une période, pour le bilan annuel de la mairie.
- Le responsable d'association exporte l'historique de son association.
- Les statistiques montrent le taux d'occupation par salle et par mois, et le nombre de
  réservations par association.
- Les exports ne contiennent jamais d'adresse électronique.

## 9. Accessibilité et technique

- Conformité RGAA niveau AA pour les pages publiques et le parcours de réservation.
- Application web responsive ; pas d'application mobile native.
- Connexion par lien magique envoyé par courriel ; pas de mot de passe.
- Temps d'affichage du planning : moins de 2 secondes sur une connexion 4G.

## 10. Exploitation

- Hébergement mutualisé chez un hébergeur français, budget annuel inférieur à 300 €.
- Une sauvegarde est restaurable en moins de 4 heures, et l'on conserve les sauvegardes des 90
  derniers jours pour pouvoir revenir sur une erreur découverte tard.
- Mises à jour de sécurité appliquées sous 7 jours.

## 11. Jalons

1. **Socle** : comptes, associations, salles, connexion par lien magique.
2. **Réserver** : création, validation, annulation, planning, courriels.
3. **Exploiter** : exports, statistiques, fermetures de salles, application mobile de
   consultation du planning pour les agents.
4. **Publier** : accessibilité vérifiée, mise en production, reprise du tableur existant.

Verdict d'envergure : **gros**, car le jalon 2 dépasse une session (création, validation,
annulation et courriels sont quatre tickets au moins).

## 12. Hors périmètre

- Le paiement des salles : elles sont gratuites pour les associations.
- La réservation par des particuliers.
- Le prêt de matériel.

## 13. Questions ouvertes

1. **[À valider]** La validation automatique au bout de 5 jours ouvrés : la mairie l'accepte-t-elle ?
2. **[Métier : mairie, bloquante]** Qui saisit le code de la boîte à clés quand l'agent est absent ?
3. **[À valider]** Faut-il un export iCal du planning ?
4. **[Métier : mairie]** La durée de conservation des réservations (2 ans) est-elle celle du
   registre de la mairie ?
5. **[À valider]** Faut-il limiter le nombre de membres par association ?
