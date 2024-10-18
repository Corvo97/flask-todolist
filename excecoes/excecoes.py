class UsuarioExistente(Exception):
    def __init__(self, usuario) -> None:
        super().__init__(f'O nome {usuario} já está sendo utilizado por outra pessoa.')


class UsuarioInexistente(Exception):
    def __init__(self, usuario) -> None:
        super().__init__(f'O usuário {usuario} não está cadastrado no sistema.')


class CampoEmBranco(Exception):
    def __init__(self, func):
        super().__init__(f'A função "{func}" não aceita campos em branco.')
        
