class TerminalException(Exception):
    """Базовое исключение терминала"""
    pass

class UserInputError(TerminalException):
    """Ошибка ввода пользователя"""
    pass

class FileProcessingError(TerminalException):
    """Ошибка при работе с файлом JSON/XML"""
    pass
