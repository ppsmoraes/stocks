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


def brl_to_float(value: str) -> float:
    """
    Transforma um texto no formato monetário brasileiro em um valor decimal.

    Parameters
    ----------
    value : str
        Texto contendo o valor em reais.

    Returns
    -------
    float
        O valor em formato numérico.

    See Also
    --------
    float_to_brl : Transforma um valor decimal em um formato monetário brasileiro.

    Examples
    --------
    Transformando o valor 'R$ 1.234,90' em `1234.9`.

    >>> import selic
    >>> x = 'R$ 1.234,90'
    >>> num = selic.brl_to_float(x)
    >>> num
    1234.9
    """
    text: str = value.replace('R$', '').replace(',', '').replace('.', '').strip()
    number: float = int(text) / 100
    return number


def float_to_brl(value: float, *, use_trunc: bool = False) -> str:
    """
    Transforma um valor decimal em um formato monetário brasileiro.

    Parameters
    ----------
    value : float
        Valor a ser convertido.

    Returns
    -------
    str
        O valor em formato monetário brasileiro.
    use_trunc : bool, optional
        Truncar o valor ao invés de arredondar, por definição `False`

    See Also
    --------
    brl_to_float : Transforma um texto no formato monetário brasileiro em um valor decimal.

    Examples
    --------
    Transformando o valor `1234.9` em 'R$ 1.234,90'.

    >>> import selic
    >>> x = 1234.9
    >>> reais = selic.float_to_brl(x)
    >>> reais
    'R$ 1.234,90'

    Transformando o valor `1234.567` em reais.

    >>> x2 = 1234.567
    >>> x2
    1234.567
    >>> reais_aredondado = selic.float_to_brl(x)
    >>> reais_aredondado
    'R$ 1.234,57'
    >>> reais_truncado = selic.float_to_brl(x, use_trunc=True)
    >>> reais
    'R$ 1.234,56'
    """
    number: float = truncate(value, 2) if use_trunc else round(value, 2)
    digits: int = int(number * 100)
    text: str = (
        f'R$ {digits / 100:,.2f}'.replace('.', '|').replace(',', '.').replace('|', ',')
    )
    return text
