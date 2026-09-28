# TODO

- [ ] **`/guide`**, un routeur façon `ask-matt` : « je suis dans telle situation, quel skill ? ».
  Le schéma d'enchaînement du README en est la base.
- [x] **Évaluations des déclencheurs** : `python3 evals/run_triggers.py`, à relancer après chaque
  changement de description (33/34 le 28/09/2026, un passage par phrase).
  Deux phrases de `to-spec` sont instables (« garde une trace… », « transforme ce qu'on vient de
  décider… ») : de 0 à 3 réussites sur 6 en trois passages, y compris avec la description de
  `main`. Dans un dossier vide et sans conversation, rien n'a été décidé : Claude explore au lieu
  de lancer le skill. Réécrire ces phrases avec un contexte, ou tester dans une conversation.
- [ ] **Évaluations des sorties** avec `skill-creator` : comparer avec et sans skill sur quelques
  cas réels (qualité d'un plan, d'une spec, d'un découpage en tickets).
- [ ] **Relecture de code** en fin d'`implement`, comme le `code-review` de Matt (conformité aux
  conventions du dépôt, et fidélité à la spec ou au ticket).
- [ ] **Glossaire du domaine** (`CONTEXT.md`, comme le `domain-modeling` de Matt), si les projets
  grossissent au point que le vocabulaire dérive.
- [ ] Tester `tickets` en vrai sur GitHub (sous-issues, « bloqué par », milestones), GitLab et
  Jira (versions : le connecteur sait-il les créer ?).
- [ ] **`debug`**, d'après `diagnosing-bugs` de Matt : boucle reproduire, réduire, hypothèses,
  instrumenter, pour les bugs dont la cause résiste. En attendant, `plan` prévoit une tâche de
  localisation avant le test rouge.
- [ ] Essayer la revue d'un ticket externe de `plan` sur un vrai ticket Jira écrit par la PO.
