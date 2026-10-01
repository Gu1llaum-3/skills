class AtelierError(Exception):
    """Erreur prévue, affichée telle quelle à l'utilisateur."""


class RuleError(AtelierError):
    """Une règle métier n'est pas respectée."""


class NotFound(AtelierError):
    pass


class Forbidden(AtelierError):
    pass
