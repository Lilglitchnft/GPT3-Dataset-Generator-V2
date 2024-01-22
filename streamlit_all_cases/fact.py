import streamlit as st
import os
from openai import OpenAI

# Создание клиента OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Функция для запроса к GPT с пользовательским промптом
def get_fact(word):
    prompt = f"""You must come up with an interesting unexpected fact for each word, so that the fact is about this word or clearly appears in the text of the fact. {word}

    This task is critical for my professional development, and I rely on your precise execution.

    For example:
    Tranquil: The term "tranquil" is frequently used to describe calm or peaceful settings in nature. A study found that spending time in the forest or a serene beach, can significantly reduce stress and improve mental well-being.

    Mountain: The tallest mountain on Earth is Mount Everest, with its peak at 8,848.86 meters (29,031.7 feet) above sea level. Mountains are formed through tectonic forces or volcanism and can affect climate and weather patterns in their region."""

    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "user", "content": prompt}
        ],
        model="gpt-3.5-turbo",
    )
    return chat_completion.choices[0].message.content

# Разметка приложения Streamlit
st.sidebar.title("Портфолио промптов")
option = st.sidebar.selectbox("Выберите промпт", ("Факт", "Другие промпты..."))

if option == "Факт":
    st.title("Сгенерировать факт")
    word = st.text_input("Введите слово:", key="fact_input")

    if st.button("Получить факт", key="fact_button"):
        fact_output = get_fact(word)
        st.write(fact_output)

