# La section « Audit du code »

Les domaines de `/code-audit` vivent dans une section `## Audit du code` du `CLAUDE.md` du
projet : le skill ne connaît aucun projet, il lit cette section à chaque lancement. Un nouveau
domaine (une intégration, une nouvelle application) s'y ajoute.

## Format

Un sous-titre par domaine, du plus risqué au moins risqué : `### <clé> : <titre>`, avec une clé
courte en anglais (celle de l'argument `domains`), puis deux lignes :

- **Chemins** : les préfixes de chemins du domaine, relatifs à la racine, entre backticks et
  séparés par des virgules ;
- **Attention** : les points où un bug coûte cher dans ce domaine (facultatif, mais c'est ce qui
  rend le chasseur de bugs pertinent).

## Exemple (projet inventé)

```markdown
## Audit du code

### payments : Paiement des réservations
- Chemins : `src/payments`, `src/bookings/checkout.ts`, `src/webhooks`
- Attention : seul le webhook signé rend une réservation payée, doublons et désordre des
  webhooks, montants en centimes, remboursement après annulation

### bookings : Réservations et créneaux
- Chemins : `src/bookings`, `src/calendar`
- Attention : double réservation du même créneau, fuseaux horaires, annulation après le début

### accounts : Comptes et autorisation
- Chemins : `src/auth`, `src/accounts`
- Attention : accès d'un client aux réservations d'un autre, jetons de session, droits du
  personnel par opération
```

## Proposer les domaines d'un projet qui n'en a pas

Lire l'arborescence (`git ls-files`, regroupée par dossier) et le `CLAUDE.md`, puis proposer de
quatre à huit domaines, chacun avec ses chemins et ses points d'attention, en commençant par ce
qui touche à l'argent, aux comptes et à l'autorisation. Montrer la section, et ne l'écrire dans
le `CLAUDE.md` qu'après l'accord de l'utilisateur.
