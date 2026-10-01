# Outils d'un audit de versions

Les commandes de l'étape 2, les champs utiles de leurs sorties, et les pièges connus (état de
septembre 2026). Lire la section du gestionnaire du projet, puis celles des images et des pièges.

## pnpm

- `pnpm outdated --format json -r --long` : un objet par paquet direct, `current`, `wanted`
  (dans l'intervalle), `latest`, `isDeprecated`, `dependencyType`, et avec `-r`
  `dependentPackages[{name, location}]` (quels workspaces l'utilisent). `isDeprecated` ne
  regarde que la version `latest` : le script voit aussi la version installée.
- `pnpm audit --json [--prod]` : `advisories{id: {module_name, vulnerable_versions,
  patched_versions, patched_versions_unpublished, severity, github_advisory_id, url,
  findings[{version, paths, dev}]}}`. Récursif par défaut dans un workspace.
  `patched_versions_unpublished: true` : aucun correctif publié, il faut remplacer le paquet.
  pnpm ≥ 11 appelle l'endpoint `bulk` du registre ; pnpm 10 appelle encore les anciens
  endpoints `/audits`, dont npm a annoncé le retrait en 2026 : ils répondent encore en
  septembre 2026, mais une erreur `ERR_PNPM_AUDIT_BAD_RESPONSE 410` vient de là. `--prod`
  ignore les `devDependencies`, même quand un bundler les intègre au build.
- `pnpm why <paquet> --json -r` : quel paquet direct tire une transitive.
- `pnpm list --json --depth Infinity -r` : toutes les versions installées, que le script lit
  (`--list`) pour OSV et pour séparer directs et transitifs.
- pnpm ≥ 11.16 : `pnpm outdated --include-github-actions` couvre aussi les actions des
  workflows.

## npm

- `npm outdated --json --long` : `{wanted, latest, dependent}`, et `current` seulement si
  `node_modules` est installé.
- `npm audit --json [--omit=dev]` : `vulnerabilities{nom: {severity, isDirect, via[{source,
  url, range}], fixAvailable}}`. Compte les paquets vulnérables, pas les avis (pnpm compte les
  avis) : dédoublonner par GHSA ou CVE avant de comparer.
- `npm view <paquet>@<version> engines peerDependencies deprecated --json` : la compatibilité
  d'une version visée.

## Yarn

- Berry (≥ 2) : `yarn npm audit --all --recursive --json` ; pas de `outdated` intégré, utiliser
  `npx npm-check-updates --jsonUpgraded --packageManager yarn`.
- Classic (1.x) : `yarn audit --json` passe par les endpoints retirés ; passer à OSV.

## Aller plus loin, avec accord

- `npx npm-check-updates --jsonUpgraded --target minor --packageManager pnpm --workspaces
  --root` : la plus haute version dans la majeure actuelle ; `--peer` tient compte des
  `peerDependencies`, `--enginesNode` de `engines.node`. Exclut les paquets dépréciés par
  défaut.
- `npx knip --dependencies --reporter json` : les dépendances inutilisées, à supprimer plutôt
  qu'à monter.
- `npx renovate --platform=local --dry-run=lookup` : versions disponibles de tout ce que
  Renovate sait lire (`.nvmrc`, `packageManager`, Dockerfile, compose, npm) ; ni failles ni fins
  de vie.

Ces outils se téléchargent : les proposer, ne pas les lancer sans accord.

## Images Docker

- **Failles** : `trivy image --format json --severity HIGH,CRITICAL <image>`
  (`Results[].Vulnerabilities[{VulnerabilityID, PkgName, InstalledVersion, FixedVersion,
  Severity}]`), sinon `grype <image> -o json --only-fixed`, sinon `docker scout cves <image>`
  (compte Docker requis ; `docker scout recommendations` propose une image de base plus
  récente). OSV ne connaît pas les images.
- **Tags disponibles** sur Docker Hub, sans compter dans les pulls :
  `https://hub.docker.com/v2/namespaces/library/repositories/<image>/tags?page_size=100&name=<préfixe>&ordering=last_updated`
  (`name`, `digest`, `last_updated`). Ailleurs : `skopeo list-tags docker://<image>` ou `crane
  ls`.
- Un scanner s'épingle à une version connue : trivy 0.69.4 a été compromis en mars 2026
  (GHSA-69fq-xp46-6x23).

## endoflife.date

API v1, lue par le script : `https://endoflife.date/api/v1/products/<produit>/`
(`releases[{name, isLts, isEol, eolFrom, isMaintained, latest{name, link}}]`). Noms utiles :
`nodejs`, `pnpm`, `yarn`, `bun`, `deno`, `postgresql`, `redis`, `valkey`, `mongodb`, `mysql`,
`mariadb`, `nginx`, `alpine-linux`, `debian`, `ubuntu`, `python`, `rabbitmq`, `elasticsearch`,
`keycloak`, `traefik`, `nextjs`, `react`, `angular`, `vue`, `nuxt`. La liste complète :
`/api/v1/products/`. **Absents** : npm, typescript, nestjs, prisma ; pour eux, la maintenance
se juge par le registre et le dépôt (le script le fait pour les paquets npm).

## Pièges

1. **Pas de lockfile, pas d'audit** (`AUDIT_NO_LOCKFILE`). `pnpm install --lockfile-only
   --ignore-scripts` en crée un, mais écrit dans le projet : demander d'abord.
2. **Options qui écrivent** : `pnpm audit --fix` (ajoute des overrides), `--ignore` et
   `--ignore-unfixable` (écrivent `auditConfig`), `npm audit fix`. Aucune avant l'étape 5.
3. **`--ignore-registry-errors`** fait sortir `pnpm audit` en 0 même quand le registre a
   échoué : un faux feu vert.
4. **Registre privé ou proxy** (Artifactory, Verdaccio) : l'audit peut rendre 410 ou rien. Les
   paquets privés sont `unknown` dans deps.dev : c'est attendu, pas une faille.
5. **Date de dernière version** : `time[dist-tags.latest]` dans le registre, jamais
   `time.modified` (`request` : modifié en 2026, dernière version en 2020).
6. **Tag partiel** (`postgres:16`) : le cycle est connu, pas le patch. Pour le patch réel, lire
   la version dans le conteneur s'il tourne déjà (`docker compose exec <service> postgres
   --version`), sans en démarrer un.
7. **Limites de débit** : GitHub sans authentification, 60 requêtes par heure (le script passe
   par `gh`) ; Docker Hub, 100 pulls par 6 heures sans compte. OSV n'en a pas.
