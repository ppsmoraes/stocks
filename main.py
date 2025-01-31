from datetime import date, datetime

from pandas import DataFrame

import cache
from log import read_jsonl_bottomup
from selic import get_iof, get_ir


def use_cache() -> bool:
    today: date = date.today()
    for line in read_jsonl_bottomup('logs.jsonl'):
        if today > datetime.fromisoformat(line['timestamp']).date():
            break

        if line['message'] == 'Dados salvos localmente':
            return True

    return False


def main() -> None:
    # df: DataFrame = cache.get_table('selic', use_cache())
    # print(df.tail())

    for i in [0, 180, 181, 360, 361, 720, 721, 99999999]:
        print(f'{i}: {get_ir(i)}')


if __name__ == '__main__':
    main()
