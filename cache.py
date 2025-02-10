from collections.abc import Callable
from datetime import date, datetime
from os import makedirs
from os import remove as remove_file
from os import rmdir
from os import system as os_sys
from os import walk as os_walk
from os.path import abspath, curdir
from os.path import exists as path_exists
from os.path import join as path_join
from platform import system as pf_sys

from pandas import DataFrame, read_parquet

from log import log, read_jsonl_bottomup


def _get_temp_path() -> str:
    """
    Calcula o caminho absoluto da pasta temporária.

    Returns
    -------
    str
        Caminho absoluta da pasta temporária
    """
    return path_join(abspath(curdir), '.temp')


def delete_temp_folder() -> None:
    """
    Rotina que apaga a pasta temporária.
    """
    temp_path: str = _get_temp_path()

    if path_exists(temp_path):
        for root, dirs, files in os_walk(temp_path, topdown=False):
            for file in files:
                remove_file(path_join(root, file))
            for dir in dirs:
                rmdir(path_join(root, dir))

        rmdir(temp_path)


def get_table(
    table_name: str,
    *,
    use_cache: bool = True,
    source: Callable[[], DataFrame] | None = None,
) -> DataFrame:
    """
    Leitura de uma tabela.

    Parameters
    ----------
    table_name : str
        O nome da tabela.
    use_cache : bool, optional
        Use `False` para forçar a leitura no banco de dados.
        `True` para usar os arquivos locais.
        Por padrão é `True`.
    source : Callable | None, optional
        Função que extrai os dados da fonte original.
        Parâmetro obrigatório, caso `use_cache = False` ou se o a tabela não existir localmente.
        Por padrão é `None`.

    Returns
    -------
    DataFrame
        Tabela em formato pandas.

    Raises
    ------
    ValueError
        Erro caso `use_cache = False` ou se o a tabela não existir localmente e `source` não ser informado.
    """
    # Getting the paths
    temp_path: str = _get_temp_path()
    table_path: str = path_join(temp_path, f'{table_name}.parquet')

    # If possible, avoid read from the API
    if use_cache and path_exists(table_path):
        log('INFO', f'Dados locais da tabela {table_name} utilizados')
        return read_parquet(table_path)

    if source is None:
        log(
            'ERROR',
            f'Cache da tabela {table_name} não utilizado e fonte não fornecida.',
        )
        raise ValueError('Cache não utilizado e fonte não fornecida.')

    try:
        log('INFO', f'Extração de dados da tabela {table_name} da fonte iniciada')
        df: DataFrame = source()
        log('INFO', f'Extração de dados da tabela {table_name} da fonte concluída')
    except ConnectionError as e:
        log('ERROR', str(e))
        raise e

    # Saving localy
    if not df.empty:
        if not path_exists(temp_path):
            makedirs(temp_path)
            if pf_sys() == 'Windows':
                os_sys(f'attrib +h "{temp_path}"')
        df.to_parquet(table_path)
        log('INFO', f'Dados da tabela {table_name} salvos localmente')

    return df


def is_table_up_to_date(table_name: str) -> bool:
    """
    Verifica se os dados locais foram atualizados na data atual.

    Parameters
    ----------
    table_name : str
        O nome da tabela.

    Returns
    -------
    bool
        `True` se os dados locais tiverem sidos atualizados, `False` caso constrário.
    """
    today: date = date.today()
    for line in read_jsonl_bottomup('logs.jsonl'):
        if today > datetime.fromisoformat(line['timestamp']).date():
            break

        if line['message'] == f'Dados da tabela {table_name} salvos localmente':
            return True

    return False
