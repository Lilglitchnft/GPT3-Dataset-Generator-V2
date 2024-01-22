import streamlit as st
import os
from openai import OpenAI

# Инициализируем клиент OpenAI с вашим API ключом
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

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

def gpt_transform(prompt):
    try:
        # Отправляем запрос к GPT с заданным промптом через chat/completions
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "user", "content": prompt}
            ],
            model="gpt-3.5-turbo",
        )
        # Возвращаем контент последнего сообщения от модели
        return chat_completion.choices[0].message.content.strip()
    except Exception as e:
        st.error(f"Error processing prompt with GPT: {e}")
        return None

def generate_image(prompt):
    try:
        # Запрос к DALL-E для генерации изображения
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024",
            quality="standard",
            n=1,
        )
        # Получаем URL изображения
        image_url = response.data[0].url
        return image_url
    except Exception as e:
        st.error(f"Error generating image: {e}")
        return None

def tab_visualize():
    st.title("Визуализация для словаря")
    user_input = st.text_input("Введите слово:", "")
    if st.button("Сгенерировать изображение"):
        gpt_prompt = f"""You will be receiving a variety of words, and your duty is to respond in English with the most valid object that can be used to create an image to represent this word.

In this way:
1. Words denoting Concrete Objects will correspond to themselves:
   - Chair - chair.
   - Mountain - mountain.
   - Apple - apple.

2. Words denoting Actions and Movements should be represented in process:
   - Running - a person running.
   - Building - workers on a construction site engaged in erecting a building.
   - Drawing - a person painting with a brush on a canvas.

3. Words denoting Emotions and Feelings should be described similarly:
   - Happiness - smiling faces of people rejoicing in something.
   - Sadness - a person with a bowed head and a sad expression.
   - Fear - a person with a frightened expression, looking to the side.

4. Words denoting Abstract Concepts should be represented in a tangible personification:
   - Freedom - a bird flying in the sky.
   - Time - an hourglass.
   - Culture - a monument.
   - Introspection - a person looking through a magnifying glass into a mirror.
   - Parallax - images of nature with a clear separating line down the middle.
   - Dissonance - musical notes in a chaotic arrangement.

5. Words denoting Historical and Cultural References need to be expressed with some recognizable symbolism:
   - Renaissance - an image of artworks from the Renaissance era.
   - Buddhism - a statue of Buddha.
   - Rock-n-Roll - The Beatles.
   - Poliudie - an image of an ancient Russian prince in traditional attire, accompanied by his warriors or retinue, collecting taxes from peasants.

6. Words denoting Historical, fictional, or real personalities will correspond to themselves:
- Sherlock Holmes - Sherlock Holmes.
- Albert Einstein - Albert Einstein.
- Elon Musk - Elon Musk.

Be specific and unambiguous. When processing requests for the visualization of words, each word should correspond to strictly one description of the image. For example, for the word "Field," define one specific type of field (e.g., a green meadow) and use it as the standard visualization for this word.

This is very important for my career, please be attentive and do the best you can.

here is the word you need to process {user_input}"""

        transformed_prompt = gpt_transform(gpt_prompt)
        if transformed_prompt:
            st.text(f"GPT-3 Transformed Prompt: {transformed_prompt}")
            image_url = generate_image(transformed_prompt)
            if image_url:
                st.image(image_url, caption=transformed_prompt)
            else:
                st.error("Error generating image")


def tab_fact():
    st.title("Сгенерировать факт")
    word = st.text_input("Введите слово:", key="fact_input")
    if st.button("Получить факт", key="fact_button"):
        fact_output = get_fact(word)
        st.write(fact_output)

def sidebar_comments_for_fact():
    st.sidebar.title("Комментарий для Генерации фактов")
    st.sidebar.write("Комментарий к вкладке 'Генерация фактов'.")

def sidebar_comments_for_visualization():
    st.sidebar.title("Комментарий для Визуализации слов")
    st.sidebar.write("Комментарий к вкладке 'Визуализация слов'.")

# Функция для отображения соответствующего комментария и содержимого
def display_tab_content():
    if st.session_state.current_tab == "fact":
        sidebar_comments_for_fact()
        tab_fact()
    elif st.session_state.current_tab == "visualize":
        sidebar_comments_for_visualization()
        tab_visualize()

# Инициализация состояния сессии
if 'current_tab' not in st.session_state:
    st.session_state.current_tab = "fact"

# Кнопки для выбора вкладок
if st.button("Генерация фактов"):
    st.session_state.current_tab = "fact"
if st.button("Визуализация слов"):
    st.session_state.current_tab = "visualize"

# Отображение содержимого в зависимости от выбранной вкладки
display_tab_content()