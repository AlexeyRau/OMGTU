import streamlit as st
import requests

API_URL = "http://localhost:8000/ask"

st.set_page_config(
    page_title="Конституция РФ — База знаний",
    page_icon="⚖️",
    layout="centered"
)

st.title("⚖️ База знаний: Конституция РФ")
st.caption("Задайте вопрос — система найдёт ответ в тексте Конституции Российской Федерации")

# История чата в session_state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Отображаем историю
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if "sources" in msg:
            with st.expander("📄 Источники"):
                for s in msg["sources"]:
                    st.markdown(f"**Статья {s['article_num']}** — {s['chapter']}")

# Поле ввода
if query := st.chat_input("Введите вопрос по Конституции РФ..."):

    # Показываем вопрос пользователя
    with st.chat_message("user"):
        st.markdown(query)
    st.session_state.messages.append({"role": "user", "content": query})

    # Запрашиваем API
    with st.chat_message("assistant"):
        with st.spinner("Ищу ответ..."):
            try:
                response = requests.post(API_URL, json={"query": query})
                response.raise_for_status()
                data = response.json()

                answer = data["answer"]
                sources = data["sources"]

                st.markdown(answer)
                with st.expander("📄 Источники"):
                    for s in sources:
                        st.markdown(f"**Статья {s['article_num']}** — {s['chapter']}")

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer,
                    "sources": sources
                })

            except requests.exceptions.ConnectionError:
                st.error("❌ Не удалось подключиться к API. Убедитесь что сервер запущен.")
            except Exception as e:
                st.error(f"❌ Ошибка: {e}")