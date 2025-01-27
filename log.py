from datetime import datetime
from json import dumps


def log(level: str, message: str) -> None:
    """
    Salva um registro.

    Parameters
    ----------
    level : str
        O nível do registro.
    message : str
        A mensagem a ser salva.
    """
    log_entry = {
        'timestamp': datetime.today().isoformat(),
        'level': level,
        'message': message,
    }

    with open('logs.jsonl', 'a') as file:
        file.write(dumps(log_entry) + '\n')
