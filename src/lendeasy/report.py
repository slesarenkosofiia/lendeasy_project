
import os
from datetime import datetime

def make_report(metrics: dict, sensitivity_html: str, output_path="reports/lendeasy_report.html"):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    html = f"""
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>LendEasy — отчёт по IT-проекту</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Arial, sans-serif;
            background: #f5f7fb;
            color: #1f2937;
            margin: 0;
            padding: 0;
        }}
        .container {{
            max-width: 1120px;
            margin: 0 auto;
            padding: 32px;
        }}
        .hero {{
            background: linear-gradient(135deg, #1d4ed8, #0f172a);
            color: white;
            padding: 32px;
            border-radius: 24px;
            margin-bottom: 24px;
        }}
        .grid {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 16px;
        }}
        .card {{
            background: white;
            border-radius: 18px;
            padding: 20px;
            box-shadow: 0 10px 24px rgba(15, 23, 42, 0.08);
        }}
        .metric {{
            font-size: 28px;
            font-weight: 800;
            margin-top: 8px;
        }}
        .bad {{ color: #dc2626; }}
        .good {{ color: #16a34a; }}
        img {{
            width: 100%;
            border-radius: 16px;
            border: 1px solid #e5e7eb;
            background: white;
        }}
        h2 {{
            margin-top: 36px;
        }}
        table {{
            border-collapse: collapse;
            width: 100%;
            background: white;
        }}
        th, td {{
            border: 1px solid #e5e7eb;
            padding: 10px;
            text-align: right;
        }}
        th:first-child, td:first-child {{
            text-align: left;
        }}
        .section {{
            background: white;
            border-radius: 18px;
            padding: 24px;
            margin-top: 18px;
            box-shadow: 0 10px 24px rgba(15, 23, 42, 0.06);
        }}
        .footer {{
            color: #6b7280;
            font-size: 13px;
            margin-top: 28px;
        }}
        code {{
            background: #eef2ff;
            padding: 2px 6px;
            border-radius: 6px;
        }}
    </style>
</head>
<body>
<div class="container">
    <div class="hero">
        <h1>Практическое задание №7: LendEasy</h1>
        <p>Вариант 3. Платформа для P2P-кредитования. Расчёт эффективности IT-проекта, анализ неопределённости и управление распределённой Scrum-командой.</p>
    </div>

    <div class="grid">
        <div class="card">
            <div>NPV</div>
            <div class="metric bad">{metrics["npv"]:,.2f}</div>
            <div>тыс. руб.</div>
        </div>
        <div class="card">
            <div>PI</div>
            <div class="metric bad">{metrics["pi"]:.3f}</div>
            <div>индекс прибыльности</div>
        </div>
        <div class="card">
            <div>IRR</div>
            <div class="metric bad">{metrics["irr"] * 100:.2f}%</div>
            <div>внутренняя доходность</div>
        </div>
        <div class="card">
            <div>TCO</div>
            <div class="metric">{metrics["tco"]:,.0f}</div>
            <div>тыс. руб.</div>
        </div>
    </div>

    <div class="section">
        <h2>1. Экономическая оценка</h2>
        <p><b>Вывод:</b> базовый NPV отрицательный, PI меньше 1, IRR отрицательная. Это значит, что за горизонт 3 года проект не окупает дисконтированные вложения. Для венчурного инвестора проект может быть интересен только при наличии сильного потенциала масштабирования после третьего года.</p>
        <p>Доля затрат на поддержку в TCO: <b>{metrics["support_share"]:.2f}%</b>.</p>
        <img src="../figures/cashflow.png" alt="Денежные потоки">
    </div>

    <div class="section">
        <h2>2. Анализ чувствительности</h2>
        <p>Проверяется влияние двух факторов: юридических затрат и комиссионного дохода. Каждый фактор изменяется на -30%, -15%, 0%, +15%, +30% при фиксации второго фактора.</p>
        {sensitivity_html}
        <img src="../figures/tornado.png" alt="Торнадо-диаграмма">
    </div>

    <div class="section">
        <h2>3. Монте-Карло</h2>
        <p>Выполнено 10 000 итераций. Юридические затраты распределены равномерно в диапазоне [-40%; +20%], комиссионный доход — в диапазоне [-50%; +30%].</p>
        <p>Вероятность получить <b>NPV &gt; 500 тыс. руб.</b>: <b>{metrics["probability_above_500"]:.2f}%</b>.</p>
        <img src="../figures/monte_carlo.png" alt="Монте-Карло">
    </div>

    <div class="section">
        <h2>4. Управление распределённой командой</h2>
        <p><b>Product Owner</b> — основатель стартапа в Берлине. Он отвечает за стратегию, ценность продукта, приоритеты бэклога, общение с инвесторами и принятие бизнес-решений.</p>
        <p><b>Team Lead</b> — Баку. Он отвечает за техническую реализацию, архитектуру, качество кода, code review, технические риски и распределение инженерных задач.</p>
        <p><b>Scrum Master</b> — Стамбул. Он помогает команде перейти на Scrum, убирает препятствия, следит за ритмом спринтов и помогает снизить хаос от меняющихся требований.</p>
        <p>Для асинхронной работы подходят Jira/Trello для задач, Slack/Telegram для коммуникаций, Notion/Confluence для документации, GitHub/GitLab для кода и pull request.</p>
        <p>Мотивация: краткосрочно — премии за цели спринта, признание вклада, гибкий график и отсутствие микроменеджмента; долгосрочно — опционы, карьерный рост, обучение и участие в архитектурных решениях.</p>
    </div>

    <div class="footer">
        Отчёт сгенерирован автоматически: {datetime.now().strftime("%Y-%m-%d %H:%M")}. 
        Файлы графиков не создавались вручную — они генерируются кодом при запуске <code>python main.py</code>.
    </div>
</div>
</body>
</html>
"""
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)
