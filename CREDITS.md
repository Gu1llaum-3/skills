# Crédits

Les skills suivants sont des adaptations en français de skills de Matt Pocock
(https://github.com/mattpocock/skills) :

| Skill ici | Source |
|---|---|
| `tdd` | `skills/engineering/tdd` |
| `interview` | `skills/productivity/grilling` |
| `adr` | `skills/engineering/domain-modeling/ADR-FORMAT.md` |
| `research` | `skills/engineering/research` |
| `to-spec` | `skills/engineering/to-spec` |
| `to-tickets` | `skills/engineering/to-tickets` |
| `to-questionnaire` | `skills/productivity/to-questionnaire` |
| `domain-modeling` | `skills/engineering/domain-modeling` (hors ADR) |
| `wtf` | `skills/productivity/wait-what` |
| `next` | `skills/engineering/ask-matt` |
| `review` | `skills/engineering/code-review` |
| `debug` | `skills/engineering/diagnosing-bugs` |
| `onboard/references/writing-for-agents.md` | `skills/productivity/writing-for-agents` |
| `poc/references/logic-demo.md`, `ui-variants.md` | `skills/engineering/prototype` |
| `wizard` (et son `template.sh`, traduit) | `skills/engineering/wizard` |
| `git-guardrails` | `skills/misc/git-guardrails-claude-code` |
| `retro` | `skills/engineering/retro` |
| `architecture` | `skills/engineering/improve-codebase-architecture` et `skills/engineering/codebase-design` |

Ils sont distribués sous la licence suivante :

```
MIT License

Copyright (c) 2026 Matt Pocock

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## Idées reprises

Pour `upgrade`, sans reprise de texte : de `supply-chain-risk-auditor` de Trail of Bits
(https://github.com/trailofbits/skills), les faits tirés d'un script plutôt que du modèle, le
« non évaluable » qui n'est jamais un feu vert, le seuil de 730 jours sans version et le
remplaçant vérifié dans le registre ; de `audit-outdated` de kubetail
(https://github.com/kubetail-org/kstack), les tags flottants à part et la date de chaque source ;
de `update-deps` de Mozilla (https://github.com/mozilla/bedrock), la cohérence des versions entre
fichiers et les montées écartées qu'on ne repropose pas.

Pour le juge de `review` (`agents/review-judge.md`) et la fin autonome d'`implement`, sans
reprise de texte : l'évaluateur séparé de l'auteur, plus facile à rendre sceptique, de
« Harness design for long-running application development » d'Anthropic
(https://www.anthropic.com/engineering/harness-design-long-running-apps) ; la boucle bornée de la
critique d'OpenHands ; la PR en brouillon de GitHub Copilot coding agent. Sources dans
`docs/research/2026-10-19-auteur-juge-revue-autonome.md`.

Sans traduction, quelques idées du skill `brainstorming` de superpowers, de Jesse Vincent
(https://github.com/obra/superpowers, licence MIT) : le chemin annoncé au départ, qu'on ne fait
que monter, le découpage d'emblée en sous-systèmes, la reformulation qui sépare le dit du
supposé, les 2 ou 3 approches et la relecture du document avant de le montrer. Elles sont dans
`brainstorming`, `feature` et `to-spec`.
