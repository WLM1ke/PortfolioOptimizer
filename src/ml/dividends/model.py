"""ML-модель для предсказания дивидендов"""
import pandas as pd

from ml import hyper
from ml.dividends import cases
from ml.model_base import AbstractModel
from utils.aggregation import Freq

PARAMS = {
    "data": {"freq": Freq.yearly, "lags": 1},
    "model": {
        "bagging_temperature": 0.693_136_332_371_617_3,
        "depth": 9,
        "ignored_features": (),
        "l2_leaf_reg": 33.008_409_248_832_26,
        "learning_rate": 0.280_123_730_430_554_6,
        "one_hot_max_size": 100,
        "random_strength": 0.196_523_325_357_101_2,
    },
}

# Максимальное количество лагов, для которого осуществляется поиск оптимальной ML-модели
MAX_LAGS = 4


def lags():
    """Список лагов для оптимизации - должны быть больше 0"""
    return [lag for lag in range(1, MAX_LAGS + 1)]


class DividendsModel(AbstractModel):
    """Содержит прогноз дивидендов с помощью ML-модели"""

    PARAMS = PARAMS

    @staticmethod
    def _learn_pool_params(*args, **kwargs):
        """Параметры для создания catboost.Pool для обучения"""
        return cases.learn_pool_params(*args, **kwargs)

    @staticmethod
    def _predict_pool_func(*args, **kwargs):
        """catboost.Pool с данными для предсказания"""
        return cases.predict_pool(*args, **kwargs)

    def _make_data_space(self):
        """Пространство поиска параметров данных модели"""
        space = {
            "freq": hyper.make_choice_space("freq", Freq),
            "lags": hyper.make_choice_space("lags", lags()),
        }
        return space

    def _check_data_space_bounds(self, params: dict):
        """Проверка, что параметры лежал не около границы вероятностного пространства"""
        lag = params["data"]["lags"]
        if lag == MAX_LAGS:
            print(f"\nНеобходимо увеличить MAX_LAGS до {MAX_LAGS + 1}")

    @property
    def prediction_mean(self):
        """pd.Series с прогнозом дивидендов"""
        return self._prediction

    @property
    def prediction_std(self):
        """pd.Series с прогнозом дивидендов"""
        return pd.Series(self.std, list(self.positions))


if __name__ == "__main__":
    from trading import POSITIONS, DATE

    pred = DividendsModel(tuple(sorted(POSITIONS)), pd.Timestamp(DATE))
    print(pred)
    # pred.find_better_model()
    pred.learning_curve()
