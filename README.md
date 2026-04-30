# Open Data AI Analytics

Аналіз екологічної та радіаційної обстановки в зоні розташування атомних електростанцій України на основі відкритих державних даних.

**Джерело даних:** [data.gov.ua — Ядерна безпека АЕС](https://data.gov.ua/dataset/4a9d3d56-bd95-4c3e-97e7-1cdc7bcbd445)

---

## Структура проєкту

```
open-data-ai-analytics/
│
├── data/                        # Спільний том: сирі та очищені дані
│   └── raw/
│       ├── nuclear_safety_q4_2025.xlsx
│       ├── pasport-naboru-danikh.xlsx
│       └── clean_data.csv
│
├── data_load/                   # Сервіс 1: завантаження + SQLite БД
│   ├── app.py
│   ├── Dockerfile
│   └── requirements.txt
│
├── data_quality_analysis/       # Сервіс 2: перевірка якості
│   ├── app.py
│   ├── Dockerfile
│   └── requirements.txt
│
├── data_research/               # Сервіс 3: дослідження даних + графіки
│   ├── app.py
│   ├── Dockerfile
│   └── requirements.txt
│
├── visualization/               # Сервіс 4: візуалізація
│   ├── app.py
│   ├── Dockerfile
│   └── requirements.txt
│
├── web/                         # Сервіс 5: веб-інтерфейс (Flask)
│   ├── app.py
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── templates/
│   │   ├── base.html
│   │   ├── index.html
│   │   ├── data.html
│   │   ├── quality.html
│   │   ├── research.html
│   │   └── visualizations.html
│   └── static/
│       ├── css/style.css
│       └── js/main.js
│
├── reports/                     # Результати (також у Docker-томі)
│   └── lab1/
│       ├── quality_report.json
│       ├── research_report.json
│       └── figures/             # 13 PNG-графіків
│
├── db/                          # Директорія для ініціалізації БД
├── .env                         # Змінні середовища
├── compose.yaml                 # Docker Compose
└── README.md
```

---

## Опис сервісів

| Сервіс | Контейнер | Опис |
|---|---|---|
| `data_load` | `data_load` | Завантажує XLSX з data.gov.ua, створює SQLite БД |
| `data_quality` | `data_quality` | Очищує дані, зберігає `quality_report.json` |
| `data_research` | `data_research` | EDA, PCA, кореляції, зберігає `research_report.json` + PNG |
| `visualization` | `visualization` | Генерує зведені графіки (emission dynamics, boxplot) |
| `web` | `web` | Flask-веб-інтерфейс, відображає всі результати |

---

## Порти

| Сервіс | Порт |
|---|---|
| Веб-інтерфейс | **http://localhost:5000** |

---

## Спільні томи

| Том | Призначення |
|---|---|
| `shared_data` | Сирі XLSX, очищений CSV, SQLite БД |
| `shared_reports` | JSON-звіти та PNG-графіки |

---

## Запуск

### Повний запуск (Docker) — Рекомендований спосіб

Для запуску всіх модулів у контейнерах за однією командою:

```bash
docker compose up --build
```

**Як це працює:**
1. Docker завантажує базові image Python 3.11
2. Встановлює залежності з `requirements.txt` кожного модуля
3. Запускає сервіси в порядку залежностей:
   - `data_load` — завантажує XLSX з data.gov.ua, створює SQLite БД
   - `data_quality_analysis` — очищує дані, збирає якість у JSON
   - `data_research` — генерує графіки й статистику
   - `visualization` — додаткові графіки
   - `web` — Flask-інтерфейс на http://localhost:5000

**Проглядати логи окремого сервісу:**

```bash
docker compose logs -f data_load      # логи завантаження
docker compose logs -f data_quality   # логи якості
docker compose logs -f data_research  # логи дослідження
docker compose logs -f web            # логи веб-сервісу
```

**Переглянути запущені контейнери:**

```bash
docker ps
```

### Доступ до результатів

Після успішного запуску:

- **Веб-інтерфейс:** http://localhost:5000
- **Звіти (JSON):** `reports/lab1/quality_report.json`, `research_report.json`
- **Графіки (PNG):** `reports/lab1/figures/*.png`
- **База даних (SQLite):** `data/nuclear_safety.db` (у спільному томі)
- **Очищені дані (CSV):** `data/raw/clean_data.csv` (у спільному томі)

### Очищення та перезапуск

**Зупинка контейнерів (без видалення даних):**

```bash
docker compose down
```

**Повне очищення (видалення контейнерів, образів, томів, даних):**

```bash
docker compose down -v
docker system prune -a
```

### Перегляд результатів без Docker

Після першого `docker compose up --build`, результати будуть у:
```bash
reports/lab1/quality_report.json
reports/lab1/research_report.json
reports/lab1/figures/*.png
data/nuclear_safety.db
data/raw/clean_data.csv
```

Можна переглянути їх локально або у веб-інтерфейсі на порту 5000.

---

## Локальний запуск (без Docker)

```bash
# 1. Встановити залежності
pip install flask pandas openpyxl

# 2. Запустити веб-додаток
python web/app.py
```

Відкрийте **http://localhost:5000**

> Дані та графіки будуть зчитані безпосередньо з `data/raw/` та `reports/lab1/`.

---

## Порядок запуску контейнерів

```
data_load
    └─→ data_quality
            ├─→ data_research ─┐
            └─→ visualization  ├─→ web
                               └─┘
```

Кожен сервіс запускається лише після успішного завершення попереднього (`condition: service_completed_successfully`).

---

## Технічний стек

- **Python 3.11**, pandas, matplotlib, seaborn, scikit-learn
- **Flask 3.1** — веб-інтерфейс
- **SQLite** — база даних
- **Docker / Docker Compose** — контейнеризація

---

## Docker архітектура

### Сервіси та їх ролі

| Сервіс | Образ | Функція | Вихідні файли |
|---|---|---|---|
| `data_load` | `python:3.11-slim` | Завантаження XLSX з data.gov.ua, створення SQLite DB | `data/nuclear_safety.db` |
| `data_quality` | `python:3.11-slim` | Очищення, фільтрація, перевірка целісності | `reports/lab1/quality_report.json` |
| `data_research` | `python:3.11-slim` | EDA, PCA, статистика, 11 графіків | `reports/lab1/research_report.json` + PNG файли |
| `visualization` | `python:3.11-slim` | Додаткові графіки (emission dynamics, boxplot) | `reports/lab1/visualization_report.json` + PNG |
| `web` | `python:3.11-slim` | Flask-інтерфейс, display результатів | HTTP на порту 5000 |

### Спільні томи

- **`shared_data`** — містить: XLSX-файли, очищений CSV, SQLite DB
- **`shared_reports`** — містить: JSON-звіти, PNG-графіки

### Порядок залежностей

```
data_load
    ↓
    ├─ data_quality ──┐
    ├─ visualization ─┤
    └─ data_research ─┴─ web
```

Кожен сервіс чекає успішного завершення попередника (`condition: service_completed_successfully` у `compose.yaml`).

### Переменні середовища

Визначені в `.env`:

```dotenv
DATA_DIR=/app/data/raw              # спільна папка даних
REPORTS_DIR=/app/reports/lab1       # спільна папка звітів
DB_PATH=/app/data/nuclear_safety.db # SQLite БД
PORT=5000                            # порт веб-інтерфейсу
```

### Health Check

Веб-сервіс має вбудований health check:

```dockerfile
HEALTHCHECK --interval=30s --timeout=10s --start-period=15s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/')" || exit 1
```

---

## Структура даних

### Вхідні дані

**Джерело:** [data.gov.ua — Ядерна безпека](https://data.gov.ua/dataset/c445c6ea-f0c3-4167-abb1-5afb4a0e5499)

**XLSX-файли:**
- `nuclear_safety_q4_2025.xlsx` — основні дані про викиди та радіацію
- `pasport-naboru-danikh.xlsx` — метаінформація

### Вихідна структура даних

**Після `data_quality_analysis`:**
- `clean_data.csv` — очищений і нормалізований набір
- Операції: вилучення пропусків, заміна типів, видалення аномалій

**JSON-звіти:**

```
reports/lab1/
  ├── quality_report.json          # Якість: rows, columns, missing, duplicates, dtypes
  ├── research_report.json         # Статистика: describe, PCA, station analysis, yearly trends
  ├── visualization_report.json    # Метаінформація про графіки
  └── figures/                     # 13 PNG-графіків
      ├── data_distributions.png
      ├── cs_137_emission_by_year.png
      ├── co_60_emission_by_year.png
      ├── emission_dynamics.png
      ├── irg_stations.png
      ├── correlation_matrix.png
      ├── pca_2d.png
      └── ... (та ще 6 графіків)
```

---

## Лабораторна робота 3: Контейнеризація

### Завдання

Цей проект виконує вимоги Лабораторної роботи 3 на курсі **"Середовище та компоненти розробки у моделюванні та аналізі даних"**:

✅ **Контейнеризація модулів:** Кожен модуль має окремий Dockerfile  
✅ **Docker Compose:** Один файл для запуску усіх сервісів  
✅ **Spільні томи:** Обмін результатами між контейнерами  
✅ **Docker Мережа:** Internal bridge network для взаємодії  
✅ **Залежності спосіб:** Послідовне запущення сервісів  
✅ **Локальна демонстрація:** `docker compose up --build` — одна команда  

### Скріншоти та звіти

Для завершення лабораторної роботи необхідне подання:

1. **Код:** Всі файли `.py`, `Dockerfile`, `compose.yaml`
2. **Скріншоти:**
   - `docker ps` — список контейнерів
   - `docker compose up --build` — лог запуску
   - http://localhost:5000 — веб-інтерфейс у браузері
3. **README.md** — інструкція запуску
4. **Звіт:** Описання архітектури, труднощей, рішень

---
