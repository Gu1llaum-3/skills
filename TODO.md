# TODO

- [x] **`/next`** (d'abord noté `/guide`), un routeur façon `ask-matt` : lit la conversation, ou
  l'état du projet, et dit quel skill lancer.
- [x] **Évaluations des déclencheurs** : `python3 evals/run_triggers.py`, à relancer après chaque
  changement de description (34/36 le 28/09/2026, un passage par phrase).
  Deux phrases de `to-spec` sont instables (« garde une trace… », « transforme ce qu'on vient de
  décider… ») : de 0 à 3 réussites sur 6 en trois passages, y compris avec la description de
  `main`. Dans un dossier vide et sans conversation, rien n'a été décidé : Claude explore au lieu
  de lancer le skill. Réécrire ces phrases avec un contexte, ou tester dans une conversation.
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
- [ ] **`debug`**, d'après `diagnosing-bugs` de Matt : boucle reproduire, réduire, hypothèses,
  instrumenter, pour les bugs dont la cause résiste. En attendant, `plan` prévoit une tâche de
  localisation avant le test rouge.
- [ ] Essayer la revue d'un ticket externe de `plan` sur un vrai ticket Jira écrit par la PO.
