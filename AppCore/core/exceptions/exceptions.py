"""
Exceções customizadas para a aplicação.
"""

class BaseSystemException(Exception):
    def __init__(self, message: str, details: dict = None):
        self.message = message
        self.details = details or {}
        super().__init__(self.message)
    

class BusinessRuleException(BaseSystemException):
    """
    Exceção levantada quando uma regra de negócio é violada.
    
    Deve ser usada quando uma operação não pode ser completada devido a
    restrições de lógica de negócio, como tentar excluir um registro que
    possui dependências, ou realizar uma ação não permitida pelo estado
    atual do sistema.
    """


class SystemErrorException(BaseSystemException):
    """
    Exceção levantada quando ocorre um erro interno do sistema.
    
    Deve ser usada para erros inesperados do sistema, como falhas de
    conexão com banco de dados, serviços externos indisponíveis, ou
    qualquer outro erro técnico que não seja causado pelo usuário.
    """


class ValidationException(BaseSystemException):
    """
    Exceção levantada quando há erro na validação de dados.
    
    Deve ser usada quando os dados fornecidos pelo usuário não atendem
    aos critérios de validação, como campos obrigatórios ausentes,
    formatos incorretos, ou valores fora do intervalo permitido.
    """


class AuthorizationException(BaseSystemException):
    """
    Exceção levantada quando há erro de autorização.
    
    Deve ser usada quando um usuário tenta acessar recursos ou executar
    ações para as quais não possui permissão, diferente de autenticação
    (que verifica identidade).
    """
        

class NotFoundException(BaseSystemException):
    """
    Exceção levantada quando um objeto não é encontrado.
    
    Deve ser usada quando uma consulta a um banco de dados ou outro
    repositório de dados não retorna o objeto esperado, indicando que
    o recurso solicitado não existe.
    """
