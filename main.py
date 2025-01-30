from datetime import date, datetime

from pandas import DataFrame

import cache
from log import read_jsonl_bottomup


def use_cache() -> bool:
    today: date = date.today()
    for line in read_jsonl_bottomup('logs.jsonl'):
        if today > datetime.fromisoformat(line['timestamp']).date():
            break

        if line['message'] == 'Dados salvos localmente':
            return True

    return False


def main() -> None:
    df: DataFrame = cache.get_table('selic', use_cache())
    print(df.tail())


if __name__ == '__main__':
    main()
