class TasksError(Exception):
    """Erreur prévue, affichée telle quelle à l'utilisateur."""


class StoreError(TasksError):
    pass
