# TODO

- [x] **`/next`** (d'abord noté `/guide`), un routeur façon `ask-matt` : lit la conversation, ou
  l'état du projet, et dit quel skill lancer.
- [x] **Évaluations des déclencheurs** : `python3 evals/run_triggers.py`, à relancer après chaque
  changement de description (34/36 le 28/09/2026, un passage par phrase).
  Deux phrases de `to-spec` sont instables (« garde une trace… », « transforme ce qu'on vient de
  décider… ») : de 0 à 3 réussites sur 6 en trois passages, y compris avec la description de
  `main`. Dans un dossier vide et sans conversation, rien n'a été décidé : Claude explore au lieu
  de lancer le skill. Réécrire ces phrases avec un contexte, ou tester dans une conversation.
- [x] **Comparer `brainstorming` avec celui de superpowers**
  ([obra/superpowers](https://github.com/obra/superpowers/tree/main/skills/brainstorming)) : pas
  de sous-skill pour le cahier des charges (ses trois chemins existent déjà : `/poc`, `/feature`,
  `/brainstorming`), mais un chemin annoncé avec un chemin court pour un petit outil, le
  découpage d'emblée, le dit et le supposé, les approches et la relecture du document.
- [x] Essayer `/brainstorming` sur un petit script (chemin du petit outil attendu), puis sur une
  plateforme à plusieurs sous-systèmes (découpage signalé à l'étape 2). Le 29/09/2026 : les deux
  chemins marchent, mais le cahier des charges de la plateforme avait des contradictions : sa
  relecture passe par un sous-agent (`docs/plans/relecture-sous-agent.md`).
- [ ] Rejouer la plateforme avec la relecture par sous-agent, en autorisant la lecture de
  `~/.claude/skills/` (en `-p`, le modèle de cahier des charges était refusé) ; attendu : 0
  contradiction et 0 renvoi faux pour un sous-agent neuf.
- [ ] **Étudier `differential-review` de Trail of Bits**
  ([trailofbits/skills](https://github.com/trailofbits/skills/tree/main/plugins/differential-review/skills/differential-review)) :
  à intégrer quelque part (`review` ?) ou à garder en skill à part.
- [x] **Fins de phase de `next`** (point 5 de l'audit) : un arbre ordonné (continuer, `/clear`,
  `/to-spec` pour la passation, sous-agent, `/compact`), pas de décision de session au milieu
  d'une phase.
- [ ] **Évaluations des sorties** avec `skill-creator` : comparer avec et sans skill sur quelques
  cas réels (qualité d'un plan, d'une spec, d'un découpage en tickets).
- [x] **Relecture de code** en fin d'`implement` : `review`, d'après le `code-review` de Matt
  (fidélité à la spec ou au ticket, et conformité aux conventions du dépôt).
- [x] **Glossaire du domaine** : `domain-modeling`, appelé par `interview`, et vérifié par
  `onboard`.
- [ ] Essayer `/onboard` sur un projet existant qui a déjà un `CLAUDE.md`, pour voir si la mise à
  l'épreuve trouve de vrais problèmes sans noyer sous les remarques.
- [ ] Tester `tickets` en vrai sur GitHub (sous-issues, « bloqué par », milestones), GitLab et
  Jira (versions : le connecteur sait-il les créer ?).
- [x] **`debug`**, d'après `diagnosing-bugs` de Matt : une boucle qui échoue avant toute
  hypothèse, pour les bugs dont la cause résiste ; `plan` l'appelle pour un bug de cause inconnue.
- [ ] Essayer la revue d'un ticket externe de `plan` sur un vrai ticket Jira écrit par la PO.
- [x] **`/architecture`**, d'après `improve-codebase-architecture` et `codebase-design` de Matt :
  le vocabulaire des modules profonds va dans ses `references/`, sans skill à part.
- [ ] Essayer `/architecture` sur un projet existant qui a un historique git fourni : les pistes
  viennent-elles des zones qui changent, et le rapport HTML s'ouvre-t-il ?
- [x] **`/retro`**, d'après `retro` de Matt : les règles de jugement vont dans
  `docs/conventions.md`, lu par `review`.
- [ ] Essayer `/retro` à la fin d'une vraie session laborieuse : chaque piste cite-t-elle un
  moment de la session, sans conseils généraux ?
- [ ] Essayer `/poc` sur une question de règle métier (démo de logique attendue) et sur un écran
  d'un projet existant (variantes d'interface attendues).
