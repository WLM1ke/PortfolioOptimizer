"""Хранение и обновление локальной версии данных по дивидендам"""
from local.dividends.dohod_ru import dividends_dohod as dohod
from local.dividends.smart_lab_ru import dividends_smart_lab as smart_lab
from local.dividends.sqlite import monthly_dividends
