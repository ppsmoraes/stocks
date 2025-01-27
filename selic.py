from pandas import DataFrame, read_csv


def get_historic_data() -> DataFrame:
    """
    Extrai os dados histórios da taxa SELIC da API do Banco Central do Brasil.

    Returns
    -------
    DataFrame
        Valores diários da taxa SELIC.

    Raises
    ------
    ConnectionError
        Erro ao tentar acessar o a API do BCB.
    """
    url: str = 'https://api.bcb.gov.br/dados/serie/bcdata.sgs.11/dados?formato=csv'

    try:
        data: DataFrame = read_csv(
            url,
            sep=';',
            index_col='data',
            parse_dates=True,
            date_format=r'%d/%m/%Y',
            decimal=',',
        )
    except Exception as e:
        raise ConnectionError(e)

    data['valor'] = data['valor'] / 100
    return data
