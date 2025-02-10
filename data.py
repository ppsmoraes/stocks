from pandas import DataFrame, concat

import cache


def default_investiments() -> DataFrame:
    return DataFrame({'Valor': [], 'Data do Depósito': [], 'Data de Retirada': []})


def get_investiments() -> DataFrame:
    return cache.get_table('investimentos', source=default_investiments)


def add_row(table_name, **kwargs) -> DataFrame:
    map_tables: dict = {'investimento': get_investiments()}
    try:
        table: DataFrame = map_tables[table_name]
    except KeyError:
        raise KeyError(f'A tabela "{table_name}" não está mapeada.')

    data = {col: [kwargs.pop(col)] for col in table.columns}
    for _ in kwargs:
        raise TypeError(f'Argumento "{_}" não encontrado nas colunas da tabela.')

    new_row = DataFrame.from_dict(data)
    return concat([table, new_row], ignore_index=True)
