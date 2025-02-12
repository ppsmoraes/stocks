from pandas import DataFrame, concat

import cache


class Tabela:
    """
    Classe que representa uma tabela
    """

    def __init__(
        self, nome: str, colunas: list[str], data: DataFrame | None = None
    ) -> None:
        """
        Inicializa uma tabela com um nome, um conjunto de colunas e um DataFrame.

        Parameters
        ----------
        nome : str
            Nome da tabela.
        colunas : list[str]
            Lista de nomes das colunas.
        data : DataFrame | None, optional
            O `pandas.DataFrame` da tabela, por padrão `None`.
            Se `None`, será um DataFrame vazio com as colunas configuradas.
        """
        self.name: str = nome
        self.columns: list[str] = colunas
        self.data: DataFrame = (
            data if data is not None else DataFrame({col: [] for col in self.columns})
        )

    def save(self) -> None:
        """
        Salva a tabela localmente.
        """
        cache.save(self.data, self.name)

    def add_row(self, **kwargs: dict) -> None:
        """
        Adiciona uma nova linha a tabela.

        Parameters
        ----------
        kwargs : dict
            Dicionário onde as chaves devem ser as colunas da tabela, o os valores, os dados a serem inseridos na nova linha.

        Raises
        ------
        TypeError
            Erro se algum argumento dado não for uma coluna da tabela.
        """
        new_row_data: dict = {col: [kwargs.pop(col)] for col in self.columns}
        for arg in kwargs:
            raise TypeError(f'Argumento "{arg}" não encontrado nas colunas da tabela.')

        new_row: DataFrame = DataFrame.from_dict(new_row_data)
        self.data = concat([self.data, new_row], ignore_index=True)
        self.save()

    def get_data(self, use_cache: bool = False) -> DataFrame:
        """
        Extrai o DataFrame da tabela.

        Parameters
        ----------
        use_cache : bool, optional
            Se deve ser feita uma busca local pelos dados, por padrão `False`

        Returns
        -------
        DataFrame
            Os dados da tabela.

        Raises
        ------
        FileExistsError
            Erro se já exisitir dados na tabela e for pedido uma busca local por dados.
        """
        if use_cache is True:
            if not self.data.empty:
                raise FileExistsError(
                    'Já existem dados no DataFrame, extração do cache cancelada.'
                )
            self.data = cache.get_table(self.name, source=self.get_data)
        return self.data


class Investments(Tabela):
    """
    A tabela Investimentos.
    """

    def __init__(self) -> None:
        """
        Inicializa a tabela, dando nome, colunas e fazendo uma busca local por dados.
        """
        super().__init__(
            'Investimentos', ['Valor', 'Data do Depósito', 'Data da Retirada']
        )
        self.get_data(True)
