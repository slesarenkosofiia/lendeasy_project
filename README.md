
# LendEasy — оценка эффективности IT-проекта

Практическое задание №7, вариант 3: платформа для P2P-кредитования **LendEasy**.

## Что делает проект

Проект автоматически:

1. Загружает исходные данные из `data/variant3_data.csv`.
2. Рассчитывает:
   - TCO;
   - долю затрат на поддержку;
   - NPV;
   - PI;
   - IRR.
3. Строит графики:
   - `figures/cashflow.png`;
   - `figures/tornado.png`;
   - `figures/monte_carlo.png`.
4. Выполняет анализ чувствительности.
5. Выполняет Монте-Карло на 10 000 итераций с `seed=42`.
6. Генерирует красивый HTML-отчёт:
   - `reports/lendeasy_report.html`.

## Важно

Папки `figures/` и `reports/` изначально почти пустые.  
Картинки и HTML-отчёт создаются автоматически после запуска:

```bash
python main.py
```

Это сделано специально, чтобы проект выглядел как полноценная аналитическая работа, а не как набор готовых картинок.

## Установка и запуск на Mac

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py
```

После запуска откроется файл:

```text
reports/lendeasy_report.html
```

## Структура проекта

```text
lendeasy_project/
├── data/
│   └── variant3_data.csv
├── figures/
│   └── .gitkeep
├── reports/
│   └── .gitkeep
├── notebooks/
│   └── LendEasy_Analysis.ipynb
├── src/
│   └── lendeasy/
│       ├── __init__.py
│       ├── calculations.py
│       ├── visuals.py
│       └── report.py
├── main.py
├── requirements.txt
└── README.md
```

## Вывод по проекту

В базовом сценарии проект финансово непривлекателен за горизонт 3 года, так как NPV отрицательный, PI меньше 1, а IRR отрицательная. Однако для венчурного инвестора проект может быть интересен, если есть потенциал масштабирования, роста клиентской базы и увеличения комиссионного дохода после третьего года.
