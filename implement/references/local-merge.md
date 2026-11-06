# Fin locale et relecture de sécurité

Pour un projet dont la section `## Autonomie` du `CLAUDE.md` dit `Fin : fusion locale`
([autonomy.md](autonomy.md)). La fusion remplace la PR : ni push ni PR.

## Relecture de sécurité

Quand la section nomme un fichier de chemins sensibles : le lire (un préfixe de chemin par ligne,
`#` pour les commentaires), puis lister les fichiers du diff (`git diff --name-only
<merge-base>`). Si l'un commence par un de ces préfixes, la relecture de sécurité se fait à
l'étape 1 de « Fin du plan », avant la fusion :

- appeler le Skill tool avec « security-review » s'il est disponible dans la session ;
- sinon, lancer l'outil Agent (`general-purpose`, contexte vierge, au premier plan) avec la
  consigne ci-dessous.

Ses constats passent au juge de `review` avec ceux de `/code-review` (axe `bug`, le constat
commençant par « sécurité : »). Ils suivent ensuite le même chemin que les autres remarques.

Consigne du sous-agent :

> Relis le diff `<commande du diff>` comme une revue de sécurité avant fusion, en lecture seule
> (`git diff`, `git show`, lecture des fichiers ; ne modifie rien, ne change pas de branche).
> Rapporte seulement les vulnérabilités exploitables introduites ou laissées par ce diff, avec
> fichier, ligne et un scénario d'attaque concret (qui attaque, avec quelle requête, pour obtenir
> quoi), en confiance élevée. Catégories : authentification et sessions (jetons, expiration,
> révocation, fixation, comparaison en temps constant, second facteur), autorisation et
> isolation (propriétaire, droits d'administration par opération, identifiant devinable),
> injections (requête construite, en-têtes, HTML non nettoyé, chemins), redirections ouvertes,
> CSRF et cookies, webhooks et signatures, secrets ou données personnelles dans les logs, les
> URL, les réponses d'erreur ou le front, validation des entrées (taille, format), en-têtes de
> sécurité. Écarte le bruit : déni de service par volume, bonne pratique sans attaque,
> dépendances (leurs outils d'audit les couvrent), problème hors du diff. Les règles du
> `CLAUDE.md` du projet sont des invariants : leur violation est une remarque.

## Fusionner

Seulement si « À décider » est vide. Sinon : pas de fusion, la branche reste, et la première
ligne du message final dit pourquoi (les « À décider » à trancher avant la fusion).

Le commit de squash a **exactement l'arbre vérifié**. D'où cet ordre, qui remplace celui des
étapes 3 et 4 de « Fin du plan » :

1. Commiter le bilan sur la branche (étape 4), avec ce que prévoit
   [ending-by-origin.md](ending-by-origin.md) en fin locale : le ticket terminé et la case de la
   roadmap cochée. Arbre de travail propre (`git status --porcelain` vide).
2. Si la branche principale a bougé depuis le départ de la branche, la fusionner dans la branche
   du plan (merge).
3. Lancer la vérification complète (comme en fin de vague), puis relever l'empreinte de l'arbre
   vérifié : `git rev-parse HEAD^{tree}`. Rouge après un effort raisonnable : pas de fusion,
   corriger la ligne de la vérification dans le bilan, et le dire en tête du message final.
4. `git switch <principale>`, puis `git merge --squash <branche du plan>`, et vérifier que
   l'arbre indexé (`git write-tree`) est l'empreinte relevée. Si la branche principale a bougé
   entre-temps, revenir à l'étape 2.
5. Commiter : un seul commit au format du dépôt, qui décrit le changement (pas « squash »), avec
   le pied de commit de la section (par défaut `Ticket: <ref>` ; sans ticket, `Refs: <chemin du
   plan>`).
6. Supprimer la branche du plan (`git branch -D`, la fusion par squash ne la marque pas comme
   fusionnée), après avoir vérifié que le commit de squash est sur la branche principale.
7. Ticket sur un gestionnaire distant : le fermer maintenant, selon
   [ending-by-origin.md](ending-by-origin.md).

Le message final donne le commit de squash à la place du lien de PR.
