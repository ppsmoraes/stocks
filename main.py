from pandas import DataFrame

import cache


def main() -> None:
    df: DataFrame = cache.get_table('selic')
    print(df.head())


if __name__ == '__main__':
    main()
