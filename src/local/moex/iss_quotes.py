"""Менеджер данных по котировкам и вспомогательные функции"""
import functools

import pandas as pd

from local.moex.iss_securities_info import aliases
from utils.data_manager import AbstractDataManager
from web import moex
from web.labels import CLOSE_PRICE
from web.labels import DATE
from web.labels import VOLUME

QUOTES_CATEGORY = 'quotes'


class QuotesDataManager(AbstractDataManager):
    """Реализует особенность загрузки и хранения 'длинной' истории котировок"""

    def __init__(self, ticker):
        super().__init__(QUOTES_CATEGORY, ticker)

    def download_all(self):
        """Загружает историю котировок, склеенную из всех тикеров аналогов

        Если на одну дату приходится несколько результатов торгов, то выбирается с максимальным оборотом
        """
        df = pd.concat(self._yield_aliases_quotes_history()).reset_index()
        df = df.loc[df.groupby(DATE)[VOLUME].idxmax()]
        return df.set_index(DATE)

    def _yield_aliases_quotes_history(self):
        """Генерирует истории котировок для все тикеров аналогов заданного тикера"""
        ticker = self.data_name
        aliases_tickers = aliases(ticker)
        for ticker in aliases_tickers:
            yield moex.quotes(ticker)

    def download_update(self):
        ticker = self.data_name
        last_date = self.value.index[-1]
        return moex.quotes(ticker, last_date)


@functools.lru_cache(maxsize=None)
def quotes(ticker: str):
    """
    Возвращает данные по котировкам из локальной версии данных, при необходимости обновляя их

    При первоначальном формировании данных используются все алиасы тикера для его регистрационного номера, чтобы
    выгрузить максимально длинную историю котировок. При последующих обновлениях используется только текущий тикер

    Parameters
    ----------
    ticker
        Тикер для которого необходимо получить данные

    Returns
    -------
    pandas.DataFrame
        В строках даты торгов.
        В столбцах [CLOSE, VOLUME] цена закрытия и оборот в штуках.
    """
    data = QuotesDataManager(ticker)
    return data.value


@functools.lru_cache(maxsize=1)
def prices(tickers: tuple):
    """
    Возвращает историю цен закрытия по набору тикеров из локальных данных, при необходимости обновляя их

    Parameters
    ----------
    tickers: tuple of str
        Список тикеров

    Returns
    -------
    pandas.DataFrame
        В строках даты торгов
    """
    df = pd.concat([quotes(ticker)[CLOSE_PRICE] for ticker in tickers], axis=1)
    df.columns = tickers
    return df


@functools.lru_cache(maxsize=1)
def volumes(tickers: tuple):
    """
    Возвращает историю объемов торгов по набору тикеров из локальных данных, при необходимости обновляя их.

    Parameters
    ----------
    tickers: tuple of str
        Список тикеров

    Returns
    -------
    pandas.DataFrame
        В строках даты торгов
    """
    df = pd.concat([quotes(ticker)[VOLUME] for ticker in tickers], axis=1)
    df.columns = tickers
    return df


if __name__ == '__main__':
    print(quotes('VSMO').loc['2018-03-19'])
