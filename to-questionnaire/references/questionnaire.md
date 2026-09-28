# Modèle de questionnaire

Pour un destinataire qui n'a pas suivi la conversation : il doit comprendre pourquoi il le
reçoit, pour quand, et pouvoir répondre sans rien demander de plus.

```markdown
# <Titre : le sujet, du point de vue du destinataire>

> Statut : envoyé le JJ/MM/AAAA | répondu le JJ/MM/AAAA
> De : <l'utilisateur> — Pour : <le destinataire, son rôle>
> Réponse souhaitée : avant le JJ/MM/AAAA

**Pourquoi ce questionnaire :** la décision qui en dépend, en une ou deux phrases.
**Ce qu'on fera de vos réponses :** où elles vont (le cahier des charges, la spec, le ticket).

## Contexte

Un paragraphe pour quelqu'un qui n'a pas suivi le projet : assez pour bien répondre, pas une
page.

## Comment répondre

Sous chaque question, après le `>`. Compter environ <durée>. Une réponse partielle ou « je ne
sais pas » est utile : signalez ce dont vous n'êtes pas sûr plutôt que de sauter la question.

## <Thème>

### <Question bloquante, posée ouverte>

_Pourquoi c'est important : ce que la réponse change._

>

### <Question non bloquante>

_En attendant, on part sur : <hypothèse>. Dites-nous si c'est faux._

>

## Autre chose ?

Y a-t-il quelque chose qu'on n'a pas demandé et qu'on devrait savoir ?

>
```

Règles :

- Un `##` par thème dès qu'il y a plus de quatre ou cinq questions ; sinon, une seule liste.
- Une idée par question : « qui valide et sous quel délai ? » fait deux questions.
- La ligne « pourquoi c'est important » seulement là où la question pourrait être mal lue ou
  appeler une réponse expéditive.
- Pas de jargon technique : le vocabulaire du destinataire, pas celui du code.
