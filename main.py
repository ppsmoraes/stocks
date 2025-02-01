from pandas import DataFrame

import cache
import selic


def main() -> None:
    # df: DataFrame = cache.get_table('selic', cache.is_data_up_to_date())
    # print(df.tail())

    x = 1234.99
    brl = selic.float_to_brl(x)
    print(f'brl: {brl}')
    number = selic.brl_to_float(brl)
    print(f'number: {number}')


if __name__ == '__main__':
    main()
