from math import trunc

from pandas import DataFrame, read_csv


def truncate(number: float, decimals: int = 0) -> float:
    """
    Função para truncar um número com uma dada quantidade de casas decimais.

    Parameters
    ----------
    number : float
        O número a ser truncado.
    decimals : int, optional
        A quantidade de casas decimais que serão mantidas, por padrão 0.

    Returns
    -------
    float
        O valor truncado.
    """
    factor: int = 10**decimals
    return trunc(number * factor) / factor


def get_iof(days: int) -> float:
    """
    Calcula o percentual de IOF baseado na quantidade de dias corridos que o valor foi depositado.

    Parameters
    ----------
    days : int
        Quantidade de dias corridos a partir do dia do depósito.

    Returns
    -------
    float
        Percentual de IOF.
    """
    if days > 29:
        return 0
    return truncate(1 - (days / 30), 2)


# Essa função não é a forma mais legível para humanos, mas é mais eficiente. Considere reformulá-la num futuro.
def get_ir(days: int) -> float:
    """
    Calcula o percentual de IR baseado na quantidade de dias corridos que o valor foi depositado.

    Parameters
    ----------
    days : int
        Quantidade de dias corridos a partir do dia do depósito.

    Returns
    -------
    float
        Percentual de IR
    """

    def discount_rate(semester: int) -> int:
        """
        Função auxiliar para calcular a taxa de desconto do IR.

        Parameters
        ----------
        semester : int
            Semestres. Contabilizados sempre em 180 dias.

        Returns
        -------
        int
            A taxa de desconto do IR.
        """
        if semester > 3:
            return 3
        elif semester > 2:
            return 2
        else:
            return semester

    base: float = 0.225
    discount: float = 0.025
    semester: int = (days - 1) // 180

    return base - discount * discount_rate(semester)


def get_historic_selic() -> DataFrame:
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
