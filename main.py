from pandas import DataFrame

import cache
import calcs


def main() -> None:
    df: DataFrame = cache.get_table(
        'selic',
        use_cache=cache.is_table_up_to_date('selic'),
        source=calcs.get_historic_selic,
    )
    print(df.tail())

    # x = 1234.99
    # brl = calcs.float_to_brl(x)
    # print(f'brl: {brl}')
    # number = calcs.brl_to_float(brl)
    # print(f'number: {number}')


if __name__ == '__main__':
    main()
