from collections.abc import Iterator
from datetime import datetime
from json import dumps, loads


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


def read_reversed_json_from_buffer(buffer: bytearray) -> dict:
    """
    Ler um `.json` de forma inversa.

    Parameters
    ----------
    buffer : bytearray
        O `.json` invertido a ser lido.

    Returns
    -------
    dict
        Retorna o `.json` em formato de dicionário do python.
    """
    buffer.reverse()
    line: str = buffer.decode('utf-8')
    return loads(line)


def read_jsonl_bottomup(file_path: str) -> Iterator[dict]:
    """
    Ler um `.jsonl` começando pela última linha.

    Parameters
    ----------
    file_path : str
        O caminho do arquivo `.jsonl`

    Yields
    ------
    Iterator[dict]
        Gera um interador com cada linha, da última até a primeira.
    """
    with open(file_path, 'rb') as file:
        file.seek(0, 2)  # Move the cursor to the end of the file
        pointer_location: int = file.tell()

        buffer: bytearray = bytearray()

        while pointer_location >= 0:
            file.seek(pointer_location)
            pointer_location -= 1
            new_byte: bytes = file.read(1)

            if new_byte == b'\n':
                if buffer:
                    yield read_reversed_json_from_buffer(buffer)
                    buffer = bytearray()
            else:
                buffer.extend(new_byte)

        if buffer:
            yield read_reversed_json_from_buffer(buffer)
