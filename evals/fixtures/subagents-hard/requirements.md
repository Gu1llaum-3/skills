# Cahier des charges : Atelier, réservation de salles pour associations

> Version 0.4, décisions du 28/09/2026 intégrées.

## 1. Contexte et objectif

### 1.1 La situation aujourd'hui

Les associations du quartier Saint-Roch partagent les quatre salles municipales de la maison
des associations. La mairie tient les réservations dans un tableur partagé entre deux agents.
Une association écrit un courriel, un agent vérifie le tableur, répond, puis note la
réservation. Le circuit prend en moyenne trois jours ouvrés.

Les problèmes relevés lors des entretiens du 12/09/2026 :

- deux associations arrivent à la même heure, parce que le tableur n'a pas été mis à jour ;
- une salle reste fermée, parce que personne n'a transmis le code de la boîte à clés ;
- les agents passent environ six heures par semaine sur les courriels de réservation ;
- les associations ne savent pas ce qui est libre avant d'écrire, et proposent souvent un
  créneau déjà pris ;
- le bilan annuel de l'occupation demande deux jours de travail à partir du tableur.

### 1.2 L'objectif

Atelier remplace le tableur par une application web. Chaque association voit le planning et
réserve elle-même un créneau libre ; un agent valide ; chacun voit le planning à jour.

### 1.3 Les indicateurs de réussite

- La mairie reçoit moins de 5 courriels de réservation par mois, trois mois après l'ouverture.
- Aucun double usage d'une salle n'est signalé sur la même période.
- Le délai moyen entre la demande et la réponse passe sous 2 jours ouvrés.
- Le bilan annuel se produit en moins d'une heure, à partir de l'export.

## 2. Public et profils

### 2.1 Les profils

L'application connaît quatre profils.

| Profil | Qui | Ce qu'il fait |
|---|---|---|
| Membre | Une personne d'une association | Consulte le planning, réserve et annule pour son association |
| Responsable | Un membre désigné par son association | Comme le membre, plus : gère les membres, voit l'historique, agit sur toutes les réservations de son association |
| Agent | Un agent de la mairie | Valide ou refuse les réservations, gère les salles, les fermetures et les codes |
| Administrateur | Le service informatique de la mairie | Crée les associations et les comptes d'agents, consulte les journaux |

### 2.2 Règles sur les comptes

- Un compte appartient à une seule association, sauf les agents et les administrateurs, qui
  n'appartiennent à aucune.
- Une association a au moins un responsable. Le dernier responsable ne peut pas quitter
  l'association sans en désigner un autre.
- Un agent ne crée jamais de réservation lui-même : il valide, refuse ou annule celles des
  associations. C'est ce qui garde la trace de qui a demandé quoi.
- Un administrateur n'agit pas sur les réservations.

### 2.3 Nombre d'utilisateurs attendus

Environ 40 associations, 300 membres actifs, 2 agents et 1 administrateur. Le pic d'usage est
en septembre, quand les associations planifient leur année.

## 3. Réservations

### 3.1 Créneaux

- Une réservation porte sur une salle, une date, une heure de début et une heure de fin.
- Les créneaux se prennent par demi-heure, entre 8 h et 23 h, tous les jours de la semaine.
- Une réservation dure au moins une heure et au plus huit heures.
- Une association peut avoir au plus 6 réservations à venir en même temps, toutes salles
  confondues. Les réservations refusées ou annulées ne comptent pas.
- On réserve au plus tôt 60 jours à l'avance et au plus tard 48 heures avant le début.
- Une réservation porte sur une seule salle. Pour deux salles, l'association fait deux
  réservations.

### 3.2 Validation

- Toute réservation est créée « en attente ».
- Un agent la valide ou la refuse. Le refus demande un motif, choisi dans une liste (créneau
  déjà attribué, salle inadaptée, fermeture, autre) avec un commentaire libre.
- Sans réponse sous 5 jours ouvrés, la réservation est validée automatiquement
  **[À valider]**.
- Deux réservations en attente peuvent se chevaucher. Une réservation validée bloque le
  créneau : les demandes en attente qui la chevauchent sont refusées avec le motif « créneau
  déjà attribué ».
- L'agent voit les demandes en attente dans l'ordre de leur création, les plus anciennes en
  premier.

### 3.3 Annulation

- L'auteur de la réservation, ou un responsable de son association, peut annuler jusqu'à
  24 heures avant le début.
- Plus tard, l'annulation passe par un agent, qui la note comme « tardive ».
- Trois annulations tardives en un trimestre suspendent les réservations de l'association
  pendant 30 jours (voir la question ouverte 3).
- Une réservation annulée libère le créneau immédiatement.

### 3.4 Modification

- L'auteur ou un responsable peut déplacer le créneau d'une réservation jusqu'à 24 heures avant
  son début.
- Le nouveau créneau suit les règles de 3.1, sauf le délai de 48 heures, remplacé par celui de
  24 heures.
- Une réservation validée que l'on déplace repasse en attente.
- On ne change pas de salle : on annule et on réserve à nouveau.

## 4. Planning

### 4.1 Affichage

- Le planning montre la semaine en cours par défaut, salle par salle.
- Les réservations validées sont en couleur pleine, celles en attente en hachuré, et les
  fermetures en gris.
- Un membre voit le nom de l'association qui occupe un créneau, jamais le nom de la personne
  qui a réservé.
- Le planning se filtre par salle et par association.

### 4.2 Navigation

- On passe d'une semaine à l'autre par des flèches, ou en choisissant une date.
- La vue « mois » montre seulement le taux d'occupation de chaque jour, pas le détail.
- Un clic sur un créneau libre ouvre le formulaire de réservation, prérempli.

### 4.3 Visibilité

- Les réservations validées d'une association sont visibles par toutes les associations
  inscrites.
- Les associations voisines voient aussi les réservations en attente, pour éviter de demander
  le même créneau.
- Un visiteur non connecté ne voit que les créneaux occupés, sans nom.

### 4.4 Impression

- Le planning s'imprime sur une page A4 paysage par semaine, en noir et blanc lisible.

## 5. Notifications

### 5.1 Courriels

| Événement | Destinataires |
|---|---|
| Création | L'auteur |
| Validation, refus | L'auteur et les responsables |
| Annulation | Tous ceux qui ont reçu la validation |
| Déplacement | L'auteur et les responsables |
| Suspension | Les responsables |

- Un rappel part 48 heures avant le début, avec le code de la boîte à clés de la salle.
- Les courriels sont en français, sans image, lisibles sur téléphone (largeur de 360 pixels).
- Chaque courriel contient un lien vers la réservation.

### 5.2 Préférences

- Un membre peut couper les courriels de création, mais pas ceux de validation, de refus ni de
  rappel.
- Un responsable peut recevoir un résumé hebdomadaire au lieu de chaque courriel.

## 6. Salles

### 6.1 Les salles

| Salle | Capacité | Équipements |
|---|---|---|
| Grande salle | 80 | Sono, vidéoprojecteur, scène |
| Salle de réunion | 20 | Écran, tableau blanc |
| Atelier | 15 | Établis, évier |
| Cuisine | 12 | Four, plaques, réfrigérateur |
| Jardin | 40 | Prises extérieures, tonnelle |

### 6.2 Horaires et fermetures

- Chaque salle a des horaires d'ouverture par jour de la semaine, inclus dans la plage de 8 h à
  23 h.
- Un agent peut fermer une salle sur une période (travaux, vacances). Les réservations validées
  sur la période sont annulées, et les associations sont prévenues avec le motif « fermeture ».
- Le jardin ferme du 1er novembre au 31 mars.

### 6.3 Équipements

- Les équipements fixes font partie de la salle : ils ne se réservent pas à part.
- Le vidéoprojecteur portable se réserve seul, pour être emporté hors de la maison des
  associations, avec un créneau de prêt d'une journée au plus.

### 6.4 Clés

- Le code de la boîte à clés change chaque mois. Un agent le saisit avant le 1er du mois.
- Le code n'apparaît que dans le courriel de rappel et dans la page de la réservation, pour
  l'auteur et les responsables.

## 7. Données et conservation

### 7.1 Durées

- Les réservations passées sont conservées 2 ans, puis anonymisées : l'association reste, le
  membre disparaît.
- Les journaux d'accès sont conservés 1 an.
- Les comptes inactifs depuis 18 mois sont désactivés, puis supprimés 6 mois plus tard, après
  un courriel d'avertissement.

### 7.2 Sauvegardes et hébergement

- Une sauvegarde complète est faite chaque nuit, et chaque sauvegarde est conservée 30 jours.
- Les données sont hébergées en France.
- Les données personnelles se limitent au nom, à l'adresse électronique et, pour les
  responsables, au téléphone.

## 8. Exports et statistiques

### 8.1 Exports

- L'agent exporte en CSV les réservations d'une période, pour le bilan annuel de la mairie.
- Le responsable exporte l'historique de son association, sur les 2 dernières années.
- Les exports ne contiennent jamais d'adresse électronique ni de téléphone.

### 8.2 Statistiques

- Le taux d'occupation par salle et par mois, et le nombre de réservations par association.
- Le nombre d'annulations tardives par association.
- Les statistiques sont réservées aux agents ; les responsables voient celles de leur
  association.

## 9. Accessibilité

- Conformité RGAA niveau AA pour les pages publiques et le parcours de réservation.
- Tout le parcours de réservation se fait au clavier.
- Les couleurs du planning ne sont jamais la seule information : le hachuré et une icône
  doublent la couleur.
- Les textes sont rédigés en langage clair (phrases courtes, pas de jargon administratif).

## 10. Parcours principaux

### 10.1 Réserver

1. Le membre ouvre le planning et choisit un créneau libre.
2. Il choisit la salle, vérifie l'heure de début et de fin, ajoute un commentaire facultatif.
3. Il confirme. La réservation est créée en attente, et il reçoit un courriel.
4. Un agent valide ; le membre et les responsables reçoivent un courriel.

### 10.2 Réserver par téléphone

Certaines associations n'ont pas de membre à l'aise avec l'informatique. Pour elles, l'agent
saisit la réservation pour l'association qui appelle, au nom de son responsable, et la valide
dans la foulée.

### 10.3 Annuler

1. Le membre ouvre la réservation, depuis le planning ou depuis le courriel.
2. Il annule, avec un motif facultatif.
3. Les destinataires de la validation reçoivent un courriel.

### 10.4 Fermer une salle

1. L'agent choisit la salle et la période, et donne le motif.
2. L'application liste les réservations touchées, et lui demande de confirmer.
3. Les réservations sont annulées, les associations prévenues (voir 7.3 pour la trace gardée).

## 11. Événements particuliers

- La fête des associations, en septembre, occupe toutes les salles un samedi : un agent la
  saisit comme une fermeture, avec le motif « fête des associations ».
- La soirée annuelle d'une association se tient dans la grande salle, de 19 h à 1 h, une fois
  par an et par association.
- Les assemblées générales de juin sont prioritaires : un agent peut refuser une autre demande
  avec le motif « assemblée générale » jusqu'à 15 jours avant.

## 12. Technique

- Application web responsive ; pas d'application mobile native.
- Connexion par lien magique envoyé par courriel ; pas de mot de passe.
- Le planning s'affiche en moins de 2 secondes sur une connexion 4G.
- Le code source est publié sous licence libre (EUPL 1.2), à la demande de la mairie.

## 13. Exploitation

- Hébergement mutualisé chez un hébergeur français, budget annuel inférieur à 300 €.
- Une sauvegarde se restaure en moins de 4 heures.
- Les mises à jour de sécurité sont appliquées sous 7 jours.
- Un agent est formé à l'administration courante en une demi-journée.

## 14. Interface

### 14.1 Pages

| Page | Qui y accède | Contenu |
|---|---|---|
| Accueil | Tous | Le planning de la semaine, en lecture seule pour un visiteur |
| Mes réservations | Membre, responsable | Les réservations à venir et passées de l'association |
| Réserver | Membre, responsable | Le formulaire, prérempli depuis le planning |
| File de validation | Agent | Les demandes en attente, les plus anciennes en premier |
| Salles | Agent | Les salles, leurs horaires, leurs fermetures, les codes |
| Association | Responsable | Les membres, l'historique, l'export |
| Administration | Administrateur | Les associations, les comptes d'agents, les journaux |

### 14.2 Formulaire de réservation

- Champs : salle, date, heure de début, heure de fin, commentaire (200 caractères au plus).
- Les heures se choisissent dans une liste, par demi-heure, pour éviter les saisies invalides.
- Le formulaire signale tout de suite un créneau qui chevauche une réservation validée, avant
  l'envoi.
- Le bouton d'envoi dit ce qui va se passer : « Demander ce créneau (en attente de
  validation) ».

### 14.3 File de validation

- Chaque demande montre l'association, la salle, le créneau, le commentaire, et les demandes
  en attente qui la chevauchent.
- L'agent valide ou refuse en un clic ; le refus ouvre la liste des motifs.
- Un compteur indique le nombre de demandes en attente depuis plus de 3 jours ouvrés.

## 15. Messages d'erreur

| Situation | Message |
|---|---|
| Créneau déjà validé pour une autre association | « Ce créneau est déjà attribué. Choisissez-en un autre. » |
| Moins de 48 heures avant le début | « On réserve au plus tard 48 heures avant le début. » |
| Plus de 60 jours avant le début | « On réserve au plus tôt 60 jours à l'avance. » |
| Quota atteint | « Votre association a déjà le nombre maximum de réservations à venir. » |
| Durée hors limites | « Une réservation dure entre 1 et 8 heures. » |
| Association suspendue | « Les réservations de votre association sont suspendues jusqu'au JJ/MM. » |
| Lien de connexion expiré | « Ce lien a expiré. Demandez-en un nouveau. » |

Tous les messages disent ce qui s'est passé et ce que l'on peut faire, sans code technique.

## 16. Droits

| Action | Membre | Responsable | Agent | Administrateur |
|---|---|---|---|---|
| Voir le planning | oui | oui | oui | oui |
| Créer une réservation | oui | oui | non | non |
| Annuler la sienne | oui | oui | oui | non |
| Annuler celles de l'association | non | oui | oui | non |
| Déplacer | la sienne | celles de l'association | non | non |
| Valider, refuser | non | non | oui | non |
| Gérer les membres | non | oui | non | non |
| Gérer les salles et fermetures | non | non | oui | non |
| Créer une association | non | non | non | oui |
| Consulter les journaux | non | non | non | oui |

## 17. Modèle de données

- **Association** : nom, adresse, date d'inscription, état (active, suspendue jusqu'au).
- **Membre** : nom, adresse électronique, téléphone (responsables), rôle, association.
- **Salle** : nom, capacité, équipements, horaires par jour.
- **Réservation** : salle, association, auteur, début, fin, statut, motif de refus, dates de
  création et de dernière modification, ancien créneau en cas de déplacement.
- **Fermeture** : salle, début, fin, motif.
- **Code de boîte à clés** : salle, mois, code.
- **Journal** : qui, quoi, quand, sur quel objet.

## 18. Jalons

1. **Socle** : comptes, associations, salles, connexion par lien magique.
2. **Réserver** : création, validation, annulation, déplacement, planning, courriels.
3. **Exploiter** : exports, statistiques, fermetures de salles, clés.
4. **Publier** : accessibilité vérifiée, mise en production, reprise du tableur existant.

Verdict d'envergure : **gros**, car le jalon 2 dépasse une session (création, validation,
annulation, déplacement et courriels sont cinq tickets au moins).

## 19. Récapitulatif des limites

| Limite | Valeur |
|---|---|
| Durée d'une réservation | 1 h à 8 h |
| Plage horaire | 8 h à 23 h |
| Réservation au plus tôt | 60 jours avant |
| Réservation au plus tard | 48 heures avant |
| Annulation ou déplacement sans agent | jusqu'à 24 heures avant |
| Réservations à venir par association | 8 |
| Validation automatique | 5 jours ouvrés |
| Conservation des réservations | 2 ans |

## 20. Hors périmètre

- Le paiement des salles : elles sont gratuites pour les associations.
- La réservation par des particuliers.
- Le prêt de matériel.
- Une application mobile native.

## 21. Questions ouvertes

1. **[À valider]** La validation automatique au bout de 5 jours ouvrés : la mairie l'accepte-t-elle ?
2. **[Métier : mairie, bloquante]** Qui saisit le code de la boîte à clés quand l'agent est absent ?
3. **[À valider]** Faut-il un export iCal du planning pour les associations ?
4. **[Métier : mairie]** La durée de conservation des réservations (2 ans) est-elle celle du
   registre de la mairie ?
5. **[À valider]** Faut-il limiter le nombre de membres par association ?
