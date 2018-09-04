"""Глобальные параметры"""

from pathlib import Path

import pandas as pd

import metrics

# Количество колонок в распечатках без переноса на несколько страниц
pd.set_option('display.max_columns', 20)
pd.set_option('display.width', None)

# Путь к данным - данные состоящие из нескольких серий хранятся в отдельных директориях внутри базовой директории
DATA_PATH = Path(__file__).parents[1] / 'data'

# Путь к отчетам
REPORTS_PATH = Path(__file__).parents[1] / 'reports'

# Какой класс используется для метрик дивидендов BaseDividendsMetrics или MLDividendsMetrics
DIVIDENDS_METRICS = metrics.MLDividendsMetrics

# Параметр для доверительных интервалов
T_SCORE = 2.0

# Множитель, для переходя к после налоговым значениям
AFTER_TAX = 1 - 0.13

# Максимальный объем операций в долях портфеля
MAX_TRADE = 0.006

# Минимальный оборот акции - преимущества акции квадратичо снижаются при приближении оборота к данному уровню
VOLUME_CUT_OFF = 5.1 * MAX_TRADE
