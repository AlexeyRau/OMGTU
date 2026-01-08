
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_squared_error

# Настройка страницы
st.set_page_config(page_title="Портал Вечности", layout="wide")
st.title("🔮 Дашборд: Прогноз Гармонии Бессмертия")
st.markdown("---")

# 1. Загрузка данных
uploaded_file = st.file_uploader("📁 Загрузите portal_data.csv", type="csv")

if uploaded_file:
    try:
        # Загрузка и предобработка (как в ЛР №2)
        df = pd.read_csv(uploaded_file, encoding='windows-1251', sep='|')

        # Быстрая очистка
        for col in df.select_dtypes(include='object').columns:
            df[col] = pd.to_numeric(df[col].replace(['-', 'Не определено', 'не определено', ''], np.nan), errors='coerce')

        st.success(f"✅ Загружено {df.shape[0]} строк, {df.shape[1]} столбцов")

        # Вкладки
        tab1, tab2, tab3 = st.tabs(["📊 Данные", "🤖 Модель", "🔮 Прогноз"])

        with tab1:
            st.subheader("Предпросмотр данных")
            st.dataframe(df.head(10))

            col1, col2 = st.columns(2)
            with col1:
                st.subheader("Типы данных")
                dtype_df = pd.DataFrame({
                    'Столбец': df.columns,
                    'Тип': df.dtypes.values,
                    'Пропуски': df.isna().sum().values
                })
                st.dataframe(dtype_df)

            with col2:
                st.subheader("Основные статистики")
                st.dataframe(df.describe())

            # Визуализация
            if st.checkbox("Показать графики распределения"):
                num_cols = df.select_dtypes(include=np.number).columns
                if len(num_cols) > 0:
                    selected_col = st.selectbox("Выберите столбец", num_cols)
                    fig, ax = plt.subplots(figsize=(8, 5))
                    ax.hist(df[selected_col].dropna(), bins=20, edgecolor='black', alpha=0.7)
                    ax.set_title(f"Распределение {selected_col}")
                    st.pyplot(fig)

        with tab2:
            st.subheader("Обучение модели Random Forest")

            if 'Гармония Бессмертия' in df.columns:
                # Подготовка данных
                X = df.select_dtypes(include=np.number).drop(columns=['Гармония Бессмертия'], errors='ignore')
                y = df['Гармония Бессмертия']

                # Разделение
                X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

                # Параметры
                col1, col2 = st.columns(2)
                with col1:
                    n_trees = st.slider("Количество деревьев", 10, 200, 100)
                with col2:
                    max_depth = st.slider("Максимальная глубина", 3, 20, 10)

                if st.button("🚀 Обучить модель", type="primary"):
                    with st.spinner("Обучение модели..."):
                        model = RandomForestRegressor(
                            n_estimators=n_trees,
                            max_depth=max_depth,
                            random_state=42,
                            n_jobs=-1
                        )
                        model.fit(X_train, y_train)

                        # Предсказания
                        y_pred = model.predict(X_test)

                        # Метрики
                        r2 = r2_score(y_test, y_pred)
                        rmse = np.sqrt(mean_squared_error(y_test, y_pred))
                        mae = mean_squared_error(y_test, y_pred)

                        st.success(f"✅ Модель обучена!")

                        # Показать метрики
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("R² на тесте", f"{r2:.4f}")
                        with col2:
                            st.metric("RMSE", f"{rmse:.4f}")
                        with col3:
                            st.metric("MAE", f"{mae:.4f}")

                        # График
                        fig, ax = plt.subplots(figsize=(8, 6))
                        ax.scatter(y_test, y_pred, alpha=0.5, s=20)
                        ax.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', lw=2)
                        ax.set_xlabel("Фактические значения")
                        ax.set_ylabel("Прогноз модели")
                        ax.set_title("Предсказания vs Факт")
                        st.pyplot(fig)

                        # Сохраняем модель
                        joblib.dump(model, 'portal_model.joblib')
                        st.session_state['model'] = model
                        st.session_state['feature_names'] = X.columns.tolist()
            else:
                st.warning("❌ В данных нет столбца 'Гармония Бессмертия'")
                st.write("Доступные столбцы:", list(df.columns))

        with tab3:
            st.subheader("Прогнозирование новых данных")

            if 'model' in st.session_state:
                model = st.session_state['model']

                # Два режима
                mode = st.radio("Режим:", ["Загрузить файл", "Ввести вручную"])

                if mode == "Загрузить файл":
                    pred_file = st.file_uploader("📁 Загрузите CSV для прогноза", type="csv")

                    if pred_file:
                        pred_df = pd.read_csv(pred_file, encoding='windows-1251', sep='|')

                        # Та же очистка
                        for col in pred_df.select_dtypes(include='object').columns:
                            pred_df[col] = pd.to_numeric(pred_df[col].replace(['-', 'Не определено'], np.nan), errors='coerce')

                        # Убедимся в совпадении признаков
                        expected_features = st.session_state['feature_names']
                        missing = [f for f in expected_features if f not in pred_df.columns]

                        if missing:
                            st.error(f"Отсутствуют признаки: {missing}")
                        else:
                            if st.button("🔮 Выполнить прогноз", type="primary"):
                                predictions = model.predict(pred_df[expected_features])

                                # Результаты
                                results = pd.DataFrame({
                                    'ID': range(len(predictions)),
                                    'Прогноз_Гармонии': predictions,
                                    'Статус_портала': np.where(predictions > 0.9, '✅ Стабилен', '⚠️ Требует внимания')
                                })

                                st.success(f"✅ Прогноз для {len(predictions)} объектов")
                                st.dataframe(results)

                                # Скачать
                                csv = results.to_csv(index=False)
                                st.download_button(
                                    label="📥 Скачать CSV",
                                    data=csv,
                                    file_name="portal_predictions.csv",
                                    mime="text/csv"
                                )
                else:
                    # Ручной ввод
                    st.info("Введите значения признаков:")

                    if 'feature_names' in st.session_state:
                        features = st.session_state['feature_names']
                        input_data = {}

                        cols_per_row = 3
                        for i, feature in enumerate(features[:6]):  # Первые 6 признаков для примера
                            if i % cols_per_row == 0:
                                col1, col2, col3 = st.columns(3)

                            with [col1, col2, col3][i % cols_per_row]:
                                input_data[feature] = st.number_input(
                                    feature[:20],
                                    value=float(df[feature].mean()) if feature in df.columns else 0.0
                                )

                        if st.button("🔮 Предсказать"):
                            input_df = pd.DataFrame([input_data])
                            prediction = model.predict(input_df)[0]

                            st.metric("Прогноз Гармонии", f"{prediction:.4f}")
                            if prediction > 0.95:
                                st.success("✅ Портал в отличном состоянии!")
                            elif prediction > 0.9:
                                st.warning("⚠️ Портал требует наблюдения")
                            else:
                                st.error("🔴 Критическое состояние!")
            else:
                st.info("👈 Сначала обучите модель во вкладке '🤖 Модель'")

    except Exception as e:
        st.error(f"❌ Ошибка: {str(e)}")
        st.write("Проверьте формат файла (кодировка: windows-1251, разделитель: |)")
else:
    st.info("👈 Пожалуйста, загрузите CSV файл с данными портала")
    st.write("Ожидаемый формат: кодировка windows-1251, разделитель '|'")

# Футер
st.markdown("---")
st.caption("Дашборд для лабораторных работ | Портал Вечности | Для запуска: streamlit run dashboard.py")
