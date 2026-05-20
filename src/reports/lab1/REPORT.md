# Звіт про розробку проекту: Open Data AI Analytics

## Описання проекту

**Назва проекту:** Аналіз відкритих даних: Екологічна та радіаційна обстановка в зоні АЕС  
(Open Data AI Analytics)

**Мета проекту:** Створення простого пайплайну для аналізу та спостереження екологічної ситуації навколо атомних електростанцій з використанням відкритих даних державного реєстру.

**Джерело даних:** [Екологічна та радіаційна обстановка в зоні розташування атомних електростанцій](https://data.gov.ua/dataset/4a9d3d56-bd95-4c3e-97e7-1cdc7bcbd445)

**Репозиторій:** https://github.com/Ssomkk/open-data-ai-analytics

**Дата звіту:** 2026-03-05

---

## Питання для аналізу

1. **Тенденції в викидах радіоактивних речовин**: Аналіз тенденцій у викидах Cs-137 та Co-60 за останні роки
2. **Порівняльний аналіз АЕС**: Порівняння середніх показників радіаційного фону між різними атомними електростанціями
3. **Оцінка допустимих рівнів**: Дослідження допустимих рівнів викидів та їх порівняння з фактичними значеннями

---

## Основні завдання та етапи розробки

### Завдання, виконані у проекті:

1. **Завантаження даних** (`feature/data_load`)
   - Створення скрипту для автоматизованого завантаження даних з платформи data.gov.ua
   - Імплементація `src/data_load.py` для керування процесом інжесту даних

2. **Аналіз якості даних** (`feature/data_quality_analysis`)
   - Розробка ноутбука `data_quality_analysis.ipynb` для перевірки цілісності та якості даних
   - Видалення дублікатів та статичних стовпців
   - Очистка даних та підготовка до аналізу

3. **Дослідницький аналіз** (`feature/data_research`)
   - Створення ноутбука `data_research.ipynb` для розвідувального аналізу даних
   - Дослідження характеристик даних та виявлення закономірностей
   - Відповіді на ключові аналітичні питання

4. **Візуалізація результатів** (`feature/visualization`)
   - Розробка ноутбука `data_visualization.ipynb` для створення інтерактивних графіків
   - Генерація 8 ключових звітів із візуалізацією:
     - Середні показники радіаційного гамма-випромінювання (IRG) за станціями
     - Порівняння індексу IRG по атомних електростанціях
     - Динаміка викидів Co-60 за роками
     - Динаміка викидів Cs-137 за роками
     - Матриця кореляції показників
     - Розподіл даних за ключовими параметрами
     - Загальні тенденції в викидах радіоактивних речовин
     - Огляд атомних електростанцій

5. **Документування змін** 
   - Створення та оновлення файлу CHANGELOG.md
   - Версіонування (v0.1.0)

---

## Структура Git-репозиторію

### Гілки розробки:

```
(venv) PS C:\Users\HP\PycharmProjects\open-data-ai-analytics> git log --oneline --graph --decorate --all
* 1b53742 (HEAD -> main) Add CHANGELOG.md
* 3a00686 (origin/main, origin/feature/visualization, feature/visualization) Add data visualization notebook and its figures
*   5e1496a Merge branch 'feature/data_research'
|\  
| * 68ab94b (origin/feature/data_research, feature/data_research) Update README.md: update questions for analysis and project description
* |   b44b6eb Merge branch 'feature/data_quality_analysis'
|\ \  
| * | 5131401 (origin/feature/data_quality_analysis, feature/data_quality_analysis) Update README.md: update questions for analysis
* | |   541eb50 Merge pull request #1 from Ssomkk/feature/data_research
|\ \ \  
| |/ /  
|/| /   
| |/    
| * 4358ed9 Add data research notebook with exploratory analysis
| * f9faa78 Update data quality analysis notebook: modify execution counts, clean data, and drop static column
|/  
*   0039e73 Merge remote-tracking branch 'origin/feature/data_quality_analysis' into feature/data_quality_analysis
|\  
| * 24bacca Add data quality analysis notebook with data cleaning and processing steps
* | 7aa5594 Add data quality analysis notebook with data cleaning and processing steps
|/  
* ac4ab9a (origin/feature/data_load, feature/data_load) Add data loading script
* 19dfa69 Add project description to README.md
* c523750 Initial commit
```

### Структура гілок:

- **main**: Основна гілка розробки з завершеними функціональностями
- **feature/data_load**: Реалізація функціональності завантаження даних
- **feature/data_quality_analysis**: Розробка аналізу якості даних та очистки
- **feature/data_research**: Дослідницький аналіз та знаходження закономірностей
- **feature/visualization**: Створення звітів та графіків для презентації результатів

### Процес розробки:

1. Кожна функціональність розроблялась у окремій гілці (`feature/*`)
2. Виконані Pull Request для інтеграції змін у main
3. Гілки були успішно merged з основною гілкою
4. Синхронізація з remote репозиторієм (origin)

---

## Артефакти проекту

### Вихідні дані:
- `data/raw/nuclear_safety_q4_2025.xlsx` - Первинні дані про радіаційну безпеку (Q4 2025)
- `data/raw/pasport-naboru-danikh.xlsx` - Паспорт набору даних (метаінформація)
- `data/raw/clean_data.csv` - Обробленні та очищені дані для аналізу

### Jupyter Notebooks (аналітика):
1. `notebooks/data_quality_analysis.ipynb` - Аналіз якості та очистка даних
2. `notebooks/data_research.ipynb` - Розвідувальний аналіз та дослідження закономірностей
3. `notebooks/data_visualization.ipynb` - Візуалізація результатів аналізу

### Звіти та графіки:
- `reports/figures/avg_irg_by_station.png` - Середній IRG по станціях
- `reports/figures/avg_irg_indx_by_station.png` - Індекс IRG по станціях
- `reports/figures/co_60_emission_by_year.png` - Динаміка Co-60
- `reports/figures/cs_137_emission_by_year.png` - Динаміка Cs-137
- `reports/figures/correlation_matrix.png` - Матриця кореляції
- `reports/figures/data_distributions.png` - Розподіл даних
- `reports/figures/emission_dynamics.png` - Загальні тенденції
- `reports/figures/irg_stations.png` - Огляд станцій

### Технічна документація:
- `README.md` - Опис проекту та питання для аналізу
- `CHANGELOG.md` - Журнал змін та версіонування
- `REPORT.md` - Цей звіт про розробку

---

## Технічний стек

- **Мова програмування**: Python 3.x
- **Бібліотеки обробки даних**: Pandas, NumPy
- **Візуалізація**: Matplotlib, Seaborn, Plotly
- **Notebook середовище**: Jupyter Notebook
- **Формати даних**: Excel (.xlsx), CSV
- **Контроль версій**: Git
- **Платформа даних**: Ukraine Open Data Portal (data.gov.ua)

---

## Основні результати аналізу

### Знайдені закономірності:

1. **Динаміка викидів радіоактивних речовин**
   - Виявлені тенденції в зміні концентрацій Cs-137 та Co-60 за часовими періодами
   - Ідентифіковані роки з максимальними та мінімальними викидами

2. **Географічне варіювання**
   - Порівняльний аналіз показує різні рівні радіаційного фону по різних АЕС
   - Виявлені станції з найвищими та найнижчими показниками

3. **Кореляційні залежності**
   - Побудована матриця кореляції для виявлення зв'язків між параметрами
   - Знайдені кореляції між метеорологічними параметрами та викидами

4. **Відповідність нормам**
   - Проведено порівняння фактичних показників з допустимими рівнями
   - Визначені періоди перевищень нормативних значень (якщо були)

---

## Висновок

Проект успішно реалізував основний функціонал для аналізу екологічної та радіаційної обстановки в зоні атомних електростанцій. Розроблено три основні компоненти (завантаження, аналіз якості, дослідження та візуалізація), які утворюють базовий пайплайн обробки даних. 

Структура Git-репозиторію демонструє правильне використання методик контролю версій з окремими гілками для кожної функціональності та їх успішною інтеграцією до основної гілки. Проект готовий до розширення функціональності та впровадження додаткових аналітичних можливостей.
