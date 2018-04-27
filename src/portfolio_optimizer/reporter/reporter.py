"""Хранение истории стоимости портфеля и составление отчетов"""

import pandas as pd
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm, inch
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import Frame, Paragraph

from portfolio_optimizer import Portfolio
from portfolio_optimizer.reporter import portfolio_structure
from portfolio_optimizer.reporter import value_dynamics, dividends_dynamics
from portfolio_optimizer.settings import REPORTS_PATH

# Наименование файла отчета
REPORT_NAME = str(REPORTS_PATH / 'report.pdf')

# Каталог с данными
REPORTS_DATA_PATH = REPORTS_PATH / 'data'

# Лис с данными
SHEET_NAME = 'Data'

# Стили pdf-файла
BLOCK_HEADER_STYLE = ParagraphStyle('Block_Header', fontName='Helvetica-Bold', spaceAfter=10)
TABLE_LINE_COLOR = colors.black
TABLE_LINE_WIDTH = 0.5
BOLD_FONT = 'Helvetica-Bold'


def read_data(report_name: str):
    data = pd.read_excel(REPORTS_DATA_PATH / f'{report_name}.xlsx',
                         sheet_name=SHEET_NAME,
                         header=0,
                         index_col=0,
                         converters={'Date': pd.to_datetime})
    return data


def make_report(report_name: str, portfolio: Portfolio, years: int = 5):
    """Формирует отчет"""
    page_width, page_height = A4
    margin = cm
    blank_width = (page_width - 2 * margin) / 3
    blank_height = (page_height - 2 * margin) / 3

    frame_l1 = Frame(margin, margin + blank_height * 2,
                     blank_width * 1.7, blank_height,
                     leftPadding=0, bottomPadding=0,
                     rightPadding=0, topPadding=6,
                     showBoundary=0)
    frame_r1 = Frame(margin + blank_width * 1.7, margin + blank_height * 2,
                     blank_width * 1.3, blank_height,
                     leftPadding=0, bottomPadding=0,
                     rightPadding=0, topPadding=6,
                     showBoundary=0)
    frame_l2 = Frame(margin, margin + blank_height,
                     blank_width, blank_height,
                     leftPadding=0, bottomPadding=0,
                     rightPadding=0, topPadding=6,
                     showBoundary=0)
    frame_l3 = Frame(margin, margin,
                     blank_width, blank_height,
                     leftPadding=0, bottomPadding=0,
                     rightPadding=0, topPadding=6,
                     showBoundary=0)

    canvas = Canvas(REPORT_NAME, pagesize=(page_width, page_height))

    canvas.setFont('Helvetica-Bold', size=14)
    canvas.setFillColor(colors.darkblue)
    canvas.drawString(margin, margin * 1.1 + 3 * blank_height, f'PORTFOLIO REPORT: {portfolio.date}')
    canvas.setStrokeColor(colors.darkblue)
    canvas.line(margin, margin + 3 * blank_height, margin + blank_width * 3, margin + 3 * blank_height)
    canvas.setStrokeColor(colors.black)
    canvas.setLineWidth(0.5)
    canvas.line(margin, margin + 2 * blank_height, margin + blank_width * 3, margin + 2 * blank_height)
    canvas.line(margin, margin + blank_height, margin + blank_width * 3, margin + blank_height)

    data = read_data('report')
    names_style = ParagraphStyle('title', fontName='Helvetica-Bold', spaceAfter=10)

    name1l = Paragraph('Last Month Change and Inflow', names_style)
    table1l = value_dynamics.make_flow_table(data[-61:])

    name1r = Paragraph('Portfolio Dividends', names_style)
    table1r = dividends_dynamics.make_dividends_table(data)

    name2 = Paragraph('Portfolio Return', names_style)
    table2 = value_dynamics.make_dynamics_table(data[-61:])

    image1 = value_dynamics.make_plot(data[-61:], blank_width / inch * 2, blank_height / inch)
    image1.drawOn(canvas, margin + blank_width, margin + blank_height)

    frame_l1.addFromList([name1l, table1l], canvas)
    frame_l2.addFromList([name2, table2], canvas)
    frame_r1.addFromList([name1r, table1r], canvas)

    portfolio_structure.portfolio_structure_block(port, canvas, margin, margin, blank_width * 3, blank_height)

    canvas.save()


# TODO: сделать прокладывание пути
# TODO: поправить кривой круг


if __name__ == '__main__':
    POSITIONS = dict(BANEP=200,
                     MFON=55,
                     SNGSP=235,
                     RTKM=0,
                     MAGN=0,
                     MSTT=4435,
                     KBTK=9,
                     MOEX=0,
                     RTKMP=1475 + 312 + 39,
                     NMTP=0,
                     TTLK=0,
                     LSRG=561 + 0 + 80,
                     LSNGP=81,
                     PRTK=70,
                     MTSS=749,
                     AKRN=795,
                     MRKC=0 + 0 + 36,
                     GAZP=0,
                     AFLT=0,
                     MSRS=699,
                     UPRO=1267,
                     PMSBP=1188 + 322 + 219,
                     CHMF=0,
                     GMKN=166 + 28,
                     VSMO=73,
                     RSTIP=87,
                     PHOR=0,
                     MRSB=0,
                     LKOH=123,
                     ENRU=319 + 148,
                     MVID=264 + 62)
    CASH = 596_156 + 470_259 + 481_849
    DATE = '2018-04-19'
    port = Portfolio(date=DATE,
                     cash=CASH,
                     positions=POSITIONS)
    make_report('qqq', port)