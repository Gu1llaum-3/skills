# brainstorming et to-spec : la relecture confiée à un sous-agent

> Statut : terminé le 29/09/2026
> Origine : cadrage du 29/09/2026 (scénario d'essai de docs/plans/brainstorming-superpowers.md)

## Objectif

Dans le scénario d'essai « plateforme avec chat, paiements et statistiques », le cahier des
charges (352 lignes) est sorti avec des contradictions : « deux reproches » suivis de trois, « six
cas » pour un tableau de cinq, un renvoi à la mauvaise question. Claude l'avait écrit d'un seul
jet, sans le relire vraiment. Un sous-agent au contexte vierge a tout trouvé en une lecture. La
relecture d'un document long passe donc par un tel sous-agent, et vérifie aussi les renvois
internes.

## Décisions

- `brainstorming`, étape 4 : le cahier des charges écrit, un sous-agent d'exploration au contexte
  vierge le relit (le chemin du fichier et les vérifications, rien d'autre). Il rapporte chaque
  problème avec ses lignes. Claude corrige ce qui est fondé ; ce qui demande une décision de
  l'utilisateur devient **[À valider]**. Puis seulement, le document est montré.
- Cinq vérifications : les trous, les contradictions, les phrases à double lecture, **les renvois
  internes** (numéros de questions ou de sections, nombres annoncés : « trois cas », « question
  3 »), la taille.
- L'étape 5 garde « la même relecture qu'à l'étape 4 » : le sous-agent relit chaque nouvelle
  version.
- La synthèse du petit outil reste relue par Claude lui-même : elle ne vit que dans la
  conversation, et le scénario d'essai des photos a montré que ça suffit.
- `to-spec` : sous-agent pour la forme « spec et tickets », avec le brouillon dans son brief ; un
  ticket seul reste relu par Claude. Mêmes cinq vérifications.

## Critères d'acceptation

- AC-1 : l'étape 4 de `brainstorming` fait relire le cahier des charges par un sous-agent au
  contexte vierge avant de le montrer, avec les cinq vérifications, renvois internes compris.
- AC-2 : la sortie du petit outil ne renvoie plus à la relecture de l'étape 4 : elle est relue
  par Claude, avec les mêmes points.
- AC-3 : `to-spec` fait relire par un sous-agent une spec de la forme « spec et tickets » ; un
  ticket seul reste relu par Claude.
- AC-4 : aucun renvoi d'un autre skill vers ces étapes n'est cassé ; `TODO.md` note l'essai à
  refaire ; un seul commit en français sur `main`.

## Interfaces à tester

- `brainstorming/SKILL.md`, `to-spec/SKILL.md` : relecture, `grep` des renvois (AC-1 à AC-4).
- Scénario d'essai : rejouer le scénario 2 (plateforme) en autorisant la lecture de
  `~/.claude/skills/`, puis faire chercher les contradictions par un sous-agent neuf ; on
  attend 0 contradiction et 0 renvoi faux (AC-1).

## Hors périmètre

- Une relecture par sous-agent pour les plans (`plan`) : non observé en essai.
- Changer le modèle de cahier des charges.

## Vague 1 : une relecture qui trouve vraiment

- [x] `brainstorming` : étape 4 (sous-agent, cinq vérifications), sortie du petit outil relue
  par Claude (AC-1, AC-2) : vérification prévue : relecture, `wc -l`
- [x] `to-spec` : étape 3, sous-agent pour la forme « spec et tickets » (AC-3) : vérification
  prévue : relecture
- [x] `TODO.md`, vérification des renvois, commit unique (AC-4) : vérification prévue :
  `grep -rn "étape 4\|relecture" --include='*.md'`, `git show --stat`

## Journal

**Vague 1 (29/09/2026)**

- Livré : `brainstorming` étape 4 (sous-agent au contexte vierge, brief à cinq vérifications dont
  les renvois internes, corrections sans détail, [À valider] pour ce qui demande une décision) ;
  sortie du petit outil relue par Claude, renvois internes compris ; `to-spec` étape 3 (sous-agent
  pour la forme « spec et tickets », brouillon dans le brief ; ticket seul relu par Claude) ;
  `TODO.md` (essai coché avec son résultat, essai à rejouer).
- Vérifié : `grep` des renvois (aucun skill ne renvoie à l'étape 4 de `brainstorming` ; « la même
  relecture qu'à l'étape 4 » de l'étape 5 désigne bien le sous-agent) ; 118 et 115 lignes.
- Non vérifié : le scénario rejoué (ligne de `TODO.md`).

**Retours de revue (29/09/2026)** : deux sous-agents, spec et conventions ; aucune violation,
aucun renvoi cassé.

- Corrigés : R-1 et R-4, un point [À valider] ou [Métier : …] n'est pas un trou, mais une
  contradiction qui le touche se rapporte ; R-2, la synthèse du petit outil vérifie aussi la
  taille ; R-3, un brief complet dans `to-spec` (rien d'autre, rien d'inventé, limite de mots) ;
  R-5, le nom de la forme « une spec et plusieurs tickets ».
- Écarté : R-6, vérifications écrites dans les deux skills : chacune est adaptée à son document
  (jalons, critères) ; les fusionner ferait pointer un skill vers l'autre.

## Réalisé

- AC-1 à AC-4 : atteints, vérifiés par relecture, `grep` des renvois et les deux sous-agents de
  revue. Le scénario rejoué reste à faire (`TODO.md`).
