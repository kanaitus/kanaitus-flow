# kanaitus-flow 📊✨

[Русский](#русский) | [English](#english)

---

## Русский

**kanaitus-flow** — это современное веб-приложение для интерактивного экспресс-анализа, очистки данных и машинного обучения (Data EDA, Cleaning & ML Studio). Оно создано для того, чтобы автоматизировать рутинные задачи аналитика без необходимости писать код в Jupyter Notebook с нуля.

### 🧠 Концепция создания и роль автора
Этот проект является демонстрацией современного подхода к разработке — **AI-Assisted Development**. 
* **Автор идеи, системный архитектор и дирижер проекта:** kanaitus
* **Реализация кода:** Разработано в тесном сотрудничестве с передовым ИИ-помощником.

> **Как это создавалось:** 
> Автор полностью спроектировал продукт, продумал его логику работы, спроектировал стек технологий, разработал концепцию UI/UX (стиль iOS, Glassmorphism, светлая/темная тема) и управлял процессом написания кода ИИ-ассистентом, проводя ревью кода, отладку багов, оптимизацию и финальное тестирование продукта.

---

### ✨ Основные возможности (Features)
* 🎨 **Премиальный Дизайн:** Эффект матового стекла (Glassmorphism), плавная анимация Lottie, поддержка светлой и темной тем.
* 🌓 **Локализация:** Полная поддержка русского и английского языков в интерфейсе.
* 📊 **Авто-Дашборд:** Мгновенный подсчет метрики качества данных (Data Quality Score), автогенерация гистограмм распределения и матрицы корреляций (Plotly).
* 🛠 **Студия Очистки:** Удаление дубликатов, заполнение пропущенных значений (средним, медианой или модой) и фильтрация выбросов по методу IQR в один клик.
* 📈 **Студия Машинного Обучения (ML Studio):** 
  * Обучение классификаторов и регрессоров (Random Forest, Decision Trees, Logistic/Linear Regression, SVM, Gradient Boosting) без единой строчки кода.
  * Интерактивная настройка гиперпараметров (shuffle, random state, количество деревьев, глубина и др.) с помощью ползунков.
  * Автоматический препроцессинг (LabelEncoding категориальных признаков).
  * Подробный отчет по метрикам качества (Accuracy, Precision, Recall, F1 / MSE, R², MAE) и графики важности признаков (Feature Importance).
* 📓 **Экспорт в Jupyter Notebook:** Приложение автоматически отслеживает все выполненные шаги по очистке данных и генерирует готовый файл `.ipynb` для скачивания, чтобы вы могли продолжить разработку в профессиональной среде на чистом Python/Pandas.
* 📉 **Интерактивная Визуализация:** Самостоятельное построение графиков (Scatter, Line, Bar, Boxplot) с гибким выбором осей.
* 💾 **Экспорт данных:** Скачивание очищенной таблицы в формате CSV.

---

### 🛠 Стек технологий
* **Python 3**
* **Streamlit** (Интерфейс веб-приложения)
* **Pandas** (Анализ и трансформация таблиц)
* **Scikit-Learn** (Построение и оценка моделей машинного обучения)
* **Plotly** (Интерактивные графики)
* **Streamlit-Lottie** (Анимации)

---

### 🚀 Быстрый старт

1. Склонируйте репозиторий:
```bash
git clone https://github.com/your-username/kanaitus-flow.git
cd kanaitus-flow
```

2. Установите зависимости:

**Для Mac/Linux:**
```bash
pip install -r requirements.txt
```

**Для Windows:**
```bash
python -m venv venv
# Активация окружения:
# В PowerShell:
.\venv\Scripts\Activate.ps1
# В командной строке (CMD):
.\venv\Scripts\activate.bat
pip install -r requirements.txt
```

3. Запустите приложение:
```bash
streamlit run app.py
```

---
---

## English

**kanaitus-flow** is a modern web application for interactive exploratory data analysis, cleaning, and machine learning (Data EDA, Cleaning & ML Studio). It is designed to automate routine analytical tasks without writing boilerplate code in Jupyter Notebooks.

### 🧠 Creation Concept & Author's Role
This project demonstrates the power of the modern **AI-Assisted Development** paradigm.
* **Product Visionary, System Architect & Conductor:** kanaitus
* **Code Implementation:** Developed in close collaboration with a cutting-edge AI assistant.

> **How it was built:** 
> The author fully designed the product concept, structured the data processing workflows, chose the technology stack, designed the UI/UX (iOS-like feel, Glassmorphism, dark/light themes), and orchestrated the development process with the AI assistant by conducting code reviews, debugging, styling optimization, and final testing.

---

### ✨ Features
* 🎨 **Premium UI/UX:** Glassmorphism effect, smooth Lottie animations, and seamless dark/light mode integration.
* 🌓 **Localization:** Full out-of-the-box support for Russian and English languages.
* 📊 **Automated Dashboard:** Instant Data Quality Score calculation, distribution histograms, and interactive correlation matrices (Plotly).
* 🛠 **Data Cleaning Studio:** Drop duplicates, fill missing values, and filter outliers using the IQR method in a single click.
* 📈 **Machine Learning Studio (ML Studio):**
  * Train classification and regression models (Random Forest, Decision Trees, Logistic/Linear Regression, SVM, Gradient Boosting) in the browser.
  * Adjust hyperparameters dynamically (shuffle, random state, number of estimators, max depth, etc.) using slider widgets.
  * Automatic dataset preprocessing (LabelEncoding for categorical values).
  * Comprehensive validation metrics (Accuracy, Precision, Recall, F1 / MSE, R², MAE) and interactive feature importance plots.
* 📓 **Jupyter Notebook Export:** The application automatically tracks every cleaning operation performed on the data and compiles them into a ready-to-run `.ipynb` file, letting you transition smoothly into a professional local IDE.
* 📉 **Manual Visualization:** Build custom charts (Scatter, Line, Bar, Boxplot) with dynamic axis selection.
* 💾 **Data Export:** Download the cleaned dataset as a CSV file.

---

### 🛠 Tech Stack
* **Python 3**
* **Streamlit** (Web framework)
* **Pandas** (Data manipulation & cleaning)
* **Scikit-Learn** (Machine learning model building & validation)
* **Plotly** (Interactive data visualization)
* **Streamlit-Lottie** (JSON animations)

---

### 🚀 Quick Start

1. Clone the repository:
```bash
git clone https://github.com/your-username/kanaitus-flow.git
cd kanaitus-flow
```

2. Install dependencies:

**For Mac/Linux:**
```bash
pip install -r requirements.txt
```

**For Windows:**
```powershell
python -m venv venv
# Activate the environment:
# In PowerShell:
.\venv\Scripts\Activate.ps1
# In CMD:
.\venv\Scripts\activate.bat
pip install -r requirements.txt
```

3. Run the app:
```bash
streamlit run app.py
```

---

## ☁️ Deployment / Развертывание
The app is configured and ready for free hosting on [Streamlit Community Cloud](https://share.streamlit.io/). Just connect your GitHub repository, choose `app.py` as the entrypoint, and hit **Deploy**.

