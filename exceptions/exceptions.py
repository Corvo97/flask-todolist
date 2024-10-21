class UserExists(Exception):
    def __init__(self, email) -> None:
        super().__init__(f'O e-mail "{email}" já está sendo utilizado por outra pessoa.')


class UserNotFound(Exception):
    def __init__(self, user) -> None:
        super().__init__(f'O usuário {user} não está cadastrado no sistema.')


class FieldCannotBeEmpty(Exception):
    def __init__(self, func):
        super().__init__(f'A função "{func}" não aceita campos em branco.')
        
