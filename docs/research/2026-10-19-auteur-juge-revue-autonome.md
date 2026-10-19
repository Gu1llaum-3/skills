# Dans un pipeline autonome, faut-il un juge distinct de l'auteur pour classer les remarques de revue et relire les corrections ?

> Recherche du 19/10/2026. Contexte : rendre autonome la fin de `implement` (revue, tri des remarques, corrections, PR en brouillon) sans que l'auteur du code juge son propre travail.

## En bref

Recommandation : oui, un juge distinct au contexte vierge, qui **classe** les remarques contre les critères du plan, et qui **relit les corrections** une fois. L'auteur ne fait que corriger. La boucle est bornée à 2 tours de correction, puis tout ce qui reste ouvert part dans la PR. Repli, si le coût ou la latence gênent : garder l'auteur pour le tri, mais imposer une règle mécanique (toute remarque qui touche un critère d'acceptation est « à corriger », jamais « à trancher ») et faire relire par un sous-agent uniquement les remarques que l'auteur écarte. Principale réserve : le juge est le même modèle que l'auteur. Le contexte vierge retire le biais de « défense de son travail », pas les angles morts partagés du modèle. Les tests et les critères vérifiables restent le vrai garde-fou.

## Comparaison

| Système | Qui écrit | Qui relit | Qui juge/trie les retours | Boucle bornée ? | Escalade humaine | Source |
|---|---|---|---|---|---|---|
| Claude Code, bonnes pratiques | Session ou agent principal | Sous-agent au contexte vierge (« adversarial review »), ou 2e session (Writer/Reviewer) | L'auteur reçoit les écarts et corrige ; la doc conseille de ne signaler que ce qui touche la correction ou les exigences | Non chiffré ; `/goal` et Stop hook servent de garde | L'humain relit les preuves (sortie de tests, commandes) | [1] |
| Claude Code Review (service géré) | Humain ou agent | Plusieurs agents en parallèle | Une étape de vérification distincte écarte les faux positifs, puis dédoublonnage et rang par gravité | Une revue par déclenchement (ouverture, push, ou `@claude review`) | Ne valide ni ne bloque jamais la PR : la fusion reste humaine | [2] |
| Plugin `/code-review` (dépôt claude-code) | (aucun) | 4 agents (2 conventions CLAUDE.md, 2 bugs) | Un sous-agent validateur **par remarque**, verdict réussi/échoué ; ce qui échoue est jeté | Une passe | Commentaires sur la PR seulement avec `--comment` | [3] |
| Harness Anthropic planner/generator/evaluator (mars 2026) | Agent générateur | Agent évaluateur séparé (teste l'appli) | L'évaluateur, avec seuils durs par critère ; « contrat » de fin négocié avant de coder | 5 à 15 itérations en design ; réduit à une passe finale quand la tâche est dans les capacités du modèle | Non décrite | [4] |
| GitHub Copilot coding agent | Copilot | Copilot code review + CodeQL, secret scanning, base d'avis de dépendances | **Copilot lui-même** corrige ce qui est signalé avant de finir, et le résume dans la PR | Non précisé | Demande une revue humaine ; l'approbation de celui qui l'a lancé ne compte pas ; workflows Actions soumis à approbation par défaut | [5][6] |
| OpenAI Codex (revue GitHub) | Humain ou Codex | Codex en revue (entraînement distinct de la génération) | Ne signale que P0/P1 ; règles dans `AGENTS.md` (section « Code Review Rules ») | Une revue par déclenchement | Correction seulement sur demande (`@codex fix …`) ; ne remplace pas les approbations | [7][8] |
| Devin + Devin Review (Cognition) | Devin | Devin Review (outil distinct), bots GitHub | Remarques classées rouge/jaune/gris, « informatives » ; Devin corrige automatiquement ce qui est signalé | Non précisé (« jusqu'à ce que les checks passent ») | Les humains relisent la PR, « pas les logs » | [9][10] |
| OpenHands (critic) | Agent | Critique LLM (score de succès + probabilité par problème) | Le critique déclenche une nouvelle passe sous un seuil (60 % global, 75 % par problème) | Oui : 3 itérations par défaut (1 à 10) | Non décrite après le plafond | [11] |
| Aider architect/editor | Architecte (décrit), éditeur (applique) | Aucun relecteur | (aucun) | (aucun) | (aucun) | [12] |
| SWE-agent, Factory, Sweep | Non trouvé : pas de séparation auteur/juge documentée dans les sources consultées | | | | | (aucun) |

## Détails

**1. L'auto-évaluation est biaisée, c'est mesuré.**
- Les LLM reconnaissent leurs propres textes et les favorisent ; plus ils se reconnaissent, plus ils se préfèrent (corrélation linéaire après fine-tuning) [13]. Vérifié (résumé du papier).
- Sans retour externe, l'auto-correction en raisonnement ne marche pas de façon fiable et dégrade parfois le résultat [14]. Le survey de Kamoi et al. conclut qu'aucun travail ne montre d'auto-correction réussie avec un retour produit par le même LLM simplement « prompté », hors tâches particulières ; elle marche avec un retour externe fiable [15].
- En code, l'auto-réparation est limitée par la qualité du retour que le modèle se donne ; un retour d'un modèle plus fort améliore nettement les résultats [16].
- Anthropic (mars 2026) : un agent qui évalue son propre travail le loue avec assurance même quand il est médiocre ; et un évaluateur trouve de vrais problèmes puis « se convainc » qu'ils ne sont pas graves et valide quand même. Rendre un évaluateur autonome sceptique est « bien plus faisable » que rendre un générateur critique de lui-même [4]. C'est exactement le cas observé chez nous (une violation de critère d'acceptation classée « à trancher »).

**2. Un relecteur produit des faux positifs : il faut un filtre, et c'est un rôle à part.**
- La doc Claude Code prévient qu'un relecteur à qui l'on demande des écarts en trouve presque toujours, même quand le travail est sain ; tout corriger mène à la sur-ingénierie. Conseil : ne signaler que ce qui touche la correction ou les exigences, le reste est optionnel [1].
- Les deux outils de revue d'Anthropic séparent « trouver » et « vérifier » : étape de vérification qui filtre les faux positifs [2], un validateur par remarque au verdict binaire [3]. La doc des sous-agents cite le motif « un relecteur qui envoie un vérificateur par remarque » [17].
- CriticGPT (OpenAI, 2024) : le critique trouve plus de bugs que des relecteurs humains payés, mais hallucine des bugs ; l'équipe humain + critique hallucine moins que le critique seul [18].
- Codex : choix assumé de la précision contre le rappel ; ne signale que P0/P1 sur GitHub ; 52,7 % des commentaires mènent à une modification ; sur les PR générées par Codex lui-même, 36 % reçoivent un commentaire, dont 46 % mènent à une modification (chiffres d'octobre-décembre 2025) [7][8].

**3. Qui corrige : partout, c'est l'auteur. Qui relit la correction : rarement documenté.**
- Writer/Reviewer, Copilot, Devin, OpenHands : le retour revient à l'agent auteur, qui corrige [1][5][10][11].
- Relecture des corrections : Claude Code Review relance une revue à chaque push si on le configure [2] ; Devin Review relit à chaque nouveau commit [10] ; l'évaluateur du harness Anthropic regrade chaque sprint [4]. Aucune source ne documente une règle d'arrêt explicite pour la boucle correction → re-revue, sauf OpenHands (3 itérations par défaut) [11]. « Building effective agents » recommande des conditions d'arrêt comme un nombre maximal d'itérations, et des points d'arrêt humains quand l'agent bloque [19].

**4. L'humain garde la fusion, partout.**
- Claude Code Review ne valide ni ne bloque une PR [2] ; Copilot exige un autre approbateur que le demandeur et une approbation pour lancer les workflows [6] ; Codex ne remplace pas les approbations requises [8] ; Cognition relit la PR, pas les journaux [10]. Copilot écrit dans le résumé de PR ce qu'il a corrigé de lui-même [5].

**5. Le coût d'un juge et quand s'en passer.**
- Harness Anthropic : 20 min et 9 $ en solo contre 6 h et 200 $ avec le harness complet ; avec Opus 4.6, l'évaluateur à chaque étape devient du surcoût sur les tâches que le modèle réussit seul, et passe à une seule passe finale [4]. Une seule passe de juge en fin de plan est donc le bon calibre pour nous.
- Le juge du même modèle que l'auteur : OpenAI utilise le même modèle de base, entraîné différemment pour la revue, et note un rappel plus faible sur le code produit par Codex que sur le code humain [7]. Probable (interprétation) : un contexte vierge ne corrige pas les angles morts communs au modèle.

**6. Points d'outillage Claude Code (vérifiés dans la doc, octobre 2026).**
- Un sous-agent peut en lancer d'autres jusqu'à trois niveaux ; un sous-agent peut être repris avec `SendMessage` en gardant son historique [17]. Un juge peut donc être relancé pour relire les corrections avec son propre contexte de tri.
- Un relecteur en lecture seule se déclare par `tools: Read, Grep, Glob` ; Bash ne peut pas être restreint par motif, il faut un hook `PreToolUse` [17].
- Un Stop hook peut bloquer la fin du tour tant qu'un contrôle échoue [20] (le plafond exact de blocages consécutifs : non lu).

## Ce que ça implique pour nos skills

**Rôles (recommandation).**
1. **Trouveurs** (inchangé) : les deux sous-agents de `review` (spec, conventions), puis `/code-review` pour les bugs. Ils ne classent pas.
2. **Juge** (nouveau, sous-agent au contexte vierge, lecture seule) : reçoit le diff, le plan avec ses critères d'acceptation, le CLAUDE.md et la liste brute des remarques des trois sources, **sans** le raisonnement de l'auteur. Pour chaque remarque, il vérifie dans le code et rend un verdict : `à corriger` / `fausse` / `rien à faire` / `déjà connu` / `à escalader`. Règles écrites dans son brief : une remarque qui viole un critère d'acceptation ou une règle citée du CLAUDE.md est `à corriger`, jamais `à escalader` ; une remarque hors critères et sans bug est `rien à faire` (contre la sur-ingénierie [1]) ; chaque verdict cite la preuve (ligne, critère, sortie de test).
3. **Auteur** (agent principal) : corrige seulement les `à corriger`, en TDD, un commit par correction, et coche dans le journal du plan. Il peut contester un verdict par écrit (une ligne), mais ne le change pas : la contestation va au juge.
4. **Relecture des corrections** : le même juge repris par `SendMessage` (il garde son tri) relit le diff des corrections seulement : chaque `à corriger` est-il réglé, rien n'a-t-il régressé (tests verts), les contestations sont-elles fondées.

**Garde-fous.**
- Boucle bornée : au plus **2 tours** correction → relecture par le juge. Ce qui reste ouvert au 3e passe en `à escalader`.
- Escalade (la seule raison de déranger l'humain avant la PR) : une remarque qui exige de changer un critère ou le périmètre du plan ; un désaccord auteur/juge persistant après un tour ; un test qu'on ne sait pas faire passer sans toucher au comportement promis ; tout ce qui touche la sécurité ou des données. Le reste ne bloque pas : la PR part en brouillon avec la liste.
- Le juge ne corrige jamais et n'écrit pas dans le dépôt (outils `Read, Grep, Glob`, Bash limité aux tests si besoin).
- Vérité terrain d'abord : les tests et le build tranchent avant le juge ; le juge s'appuie sur leur sortie.

**Ce qu'il faut écrire dans la PR brouillon** (et dans le journal du plan) : un tableau des remarques avec source (spec, conventions, `/code-review`), verdict du juge, preuve en une ligne, commit de correction ; la liste des `à escalader` en tête, avec la question à trancher ; les remarques écartées (`fausse`, `rien à faire`) visibles mais repliées ; le nombre de tours faits. Comme Copilot, dire ce qui a été corrigé sans humain [5].

**Repli (moins cher).** L'auteur trie lui-même, avec deux règles mécaniques : critère d'acceptation ou règle du CLAUDE.md touchés ⇒ `à corriger` ; et un sous-agent vérificateur relit **uniquement** les remarques que l'auteur classe `fausse`, `rien à faire` ou `à trancher`. C'est le point où le biais d'auto-évaluation coûte le plus [4][13], pour une fraction du coût.

**À vérifier avant de modifier les skills.** Ce qui renvoie aux classes actuelles de `review` (« à trancher » devient « à escalader » ?), l'étape de fin de `implement` qui laisse l'humain choisir quoi corriger, et la place de `/code-review` (avant le juge, pour qu'il trie aussi ses remarques). Scénario d'essai : rejouer le cas réel (remarque qui viole un critère d'acceptation) et observer que le juge la classe `à corriger` et que la PR la trace.

## Sources

1. Best practices for Claude Code (sections « Give Claude a way to verify its work », « Run multiple Claude sessions », « Add an adversarial review step »), https://code.claude.com/docs/en/best-practices, consulté le 19/10/2026
2. Code Review (Claude Code), https://code.claude.com/docs/en/code-review, consulté le 19/10/2026
3. Plugin code-review, commande `code-review.md`, dépôt anthropics/claude-code, https://raw.githubusercontent.com/anthropics/claude-code/main/plugins/code-review/commands/code-review.md, consulté le 19/10/2026
4. P. Rajasekaran, « Harness design for long-running application development », Anthropic Engineering, 24/03/2026, https://www.anthropic.com/engineering/harness-design-long-running-apps, consulté le 19/10/2026
5. « Copilot coding agent now automatically validates code security and quality », GitHub Changelog, 28/10/2025, https://github.blog/changelog/2025-10-28-copilot-coding-agent-now-automatically-validates-code-security-and-quality/, consulté le 19/10/2026
6. Reviewing a pull request created by Copilot, GitHub Docs, https://docs.github.com/en/copilot/how-tos/use-copilot-agents/cloud-agent/review-copilot-prs, consulté le 19/10/2026 (voir aussi https://docs.github.com/en/copilot/concepts/agents/coding-agent/about-coding-agent)
7. « A practical approach to verifying code at scale », OpenAI Alignment Blog, 01/12/2025, https://alignment.openai.com/scaling-code-verification/, consulté le 19/10/2026
8. Codex, intégration GitHub (revue de code, `AGENTS.md`, `@codex fix`), https://learn.chatgpt.com/docs/third-party/github (redirigé depuis https://developers.openai.com/codex/integrations/github), consulté le 19/10/2026
9. « Devin Review », Cognition, 21/01/2026, https://cognition.com/blog/devin-review, consulté le 19/10/2026
10. « How Cognition uses Devin to build Devin », Cognition, 27/02/2026, https://cognition.com/blog/how-cognition-uses-devin-to-build-devin, consulté le 19/10/2026
11. Critic, documentation OpenHands CLI, https://docs.openhands.dev/openhands/usage/cli/critic, consulté le 19/10/2026
12. « Separating code reasoning and editing » (architect/editor), Aider, 26/09/2024, https://aider.chat/2024/09/26/architect.html, consulté le 19/10/2026
13. A. Panickssery, S. R. Bowman, S. Feng, « LLM Evaluators Recognize and Favor Their Own Generations », arXiv:2404.13076, 2024, https://arxiv.org/abs/2404.13076, consulté le 19/10/2026
14. J. Huang et al., « Large Language Models Cannot Self-Correct Reasoning Yet », ICLR 2024, arXiv:2310.01798, https://arxiv.org/abs/2310.01798, consulté le 19/10/2026
15. R. Kamoi et al., « When Can LLMs Actually Correct Their Own Mistakes? A Critical Survey of Self-Correction of LLMs », TACL 2024, arXiv:2406.01297, https://arxiv.org/abs/2406.01297, consulté le 19/10/2026
16. T. X. Olausson et al., « Is Self-Repair a Silver Bullet for Code Generation? », ICLR 2024, arXiv:2306.09896, https://arxiv.org/abs/2306.09896, consulté le 19/10/2026
17. Subagents, documentation Claude Code, https://code.claude.com/docs/en/sub-agents, consulté le 19/10/2026
18. N. McAleese et al., « LLM Critics Help Catch LLM Bugs » (CriticGPT), arXiv:2407.00215, 2024, https://arxiv.org/abs/2407.00215, consulté le 19/10/2026
19. « Building effective agents », Anthropic Engineering, 19/12/2024, https://www.anthropic.com/engineering/building-effective-agents, consulté le 19/10/2026
20. Hooks reference (Stop), documentation Claude Code, https://code.claude.com/docs/en/hooks, consulté le 19/10/2026
