import streamlit as st
import os
from openai import OpenAI
import json


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
    user_input = st.text_input("Введите слово:", "Uncertainty")
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
    word = st.text_input("Введите слово:", "Bus")
    if st.button("Получить факт", key="fact_button"):
        fact_output = get_fact(word)
        st.write(fact_output)
# Функция для запроса к GPT с математической задачей
def solve_math_problem(problem):
    prompt = (f"you have to solve a math problem, you are a math teacher. "
              f"Give the answer in the form of json, where the first object is a chain of thoughts and the second is a direct answer to the problem. "
              f"In the object of thought you fully comprehend and solve the problem, in the object of the answer you give the answer to the problem without further ado. "
              f"This is very important for my career, take a deep breath and solve this problem: {problem}\n\n"
              f"Example:\n"
              f"Solve the problem:\n"
              f"{'{'}\n"
              f"\"thoughts\":{ '{'}\n"
              f"\"step1\":\"Vasya has 15 apples\",\n"
              f"\"step2\":\"He shares the apples with 3 friends\",\n"
              f"\"step3\":\"He gives each friend 3 apples\",\n"
              f"\"step4\":\"Total apples given to friends = 3 friends * 3 apples each = 9 apples\",\n"
              f"\"step5\":\"Apples remaining with Vasya = 15 apples - 9 apples = 6 apples\"\n"
              f"{'}'},\n"
              f"\"answer\":\"6\"\n"
              f"{'}'}")
    
    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "user", "content": prompt}
        ],
        model="gpt-3.5-turbo",
    )
    
    # Получение и обработка JSON-ответа
    full_response = chat_completion.choices[0].message.content
    try:
        response_json = json.loads(full_response)
        answer = response_json.get("answer", "No answer found")
    except json.JSONDecodeError:
        answer = "Error parsing JSON response"

    return answer

def tab_math():
    st.title("Краткий ответ с chain of thoughts")
    problem = st.text_area("Напишите задачу:", "У Алекса было 200 долларов. Он потратил 30 долларов на рубашку, 46 долларов на брюки, 38 долларов на пальто, 11 долларов на носки и 18 долларов на пояс. Он также купил пару обуви, но потерял чек. У него осталось 16 долларов из бюджета. Сколько Алекс заплатил за обувь?")
    if st.button("Решить задачу", key="math_button"):
        solution = solve_math_problem(problem)
        st.write("Answer:", solution)

def sidebar_comments_for_fact():
    st.sidebar.title("Комментарий")
    st.sidebar.write("Идея этого промпта, в том, что людям легче запомнить новое иностранное слово, если существует информация, с которой ее можно связать. Некоторые слова лучше подходят для формирования факта, но даже в крайних случаях LLM с этим промптом не склонна галлюцинировать. Вы можете ознакомиться с тестами промпта по ссылке: https://app.promptfoo.dev/eval/f:8c895caa-6a00-4d1c-842f-48bf8953cf41/.")
                     
def sidebar_comments_for_visualization():
    st.sidebar.title("Комментарий")
    st.sidebar.write("Если вы делаете приложения для изучения иностранных слов, то вам наверняка потребуется сделать карточку для каждого слова. С помощью этого промпта можно автоматически наполнить сайт валидными изображениями даже самых абстрактных слов. Сейчас этот промпт используется на сайте: https://langpilot.com.")

# Функция для отображения содержимого в зависимости от выбранной вкладки
def sidebar_comments_for_math():
    st.sidebar.title("Комментарий")
    st.sidebar.write(
    "Вы могли слышать, что такая концепция, как chain of thoughts, может серьезно повысить количество правильных ответов на математические задачи.\n"
    "Но представьте, что вам требуется дать ответ без лишних слов.\n"
    "Чтобы это сделать, мы можем упаковать ответ LLM в json, где будет два объекта: 1) размышления, 2) ответ.\n\n"
    "{\n"
    "  \"thoughts\": {\n"
    "    \"step1\": \"...\",\n"
    "    \"step2\": \"...\",\n"
    "    \"step3\": \"...\"\n"
    "  },\n"
    "  \"answer\": \"...\"\n"
    "}\n"
)

# Функция для отображения содержимого в зависимости от выбранной вкладки
def display_tab_content():
    if st.session_state.current_tab == "fact":
        sidebar_comments_for_fact()
        tab_fact()
    elif st.session_state.current_tab == "visualize":
        sidebar_comments_for_visualization()
        tab_visualize()
    elif st.session_state.current_tab == "math":
        sidebar_comments_for_math()
        tab_math()

# Инициализация состояния сессии
if 'current_tab' not in st.session_state:
    st.session_state.current_tab = "visualize"

# Создаем три столбца
col1, col2, col3 = st.columns(3)

# В первом столбце размещаем кнопку для генерации фактов
with col1:
    if st.button("🎨 Визуализация слов"):
        st.session_state.current_tab = "visualize"

with col2:
    if st.button("💡 Краткое решение"):
        st.session_state.current_tab = "math"

with col3:
    if st.button("🔍 Генерация фактов"):
        st.session_state.current_tab = "fact"
# Используйте Markdown для создания подвала
st.markdown("""
    <style>
    .footer {
        font-size: 16px;
        color: #000; /* Изменение цвета текста на черный */
        background-color: #ddf1ff;
        padding: 10px;
        position: fixed;
        bottom: 0;
        width: 100%;
        text-align: left;
        border-radius: 10px; /* Добавление закругленных краев */
    }
    </style>
    <div class="footer">
        Темченко Сергей: &nbsp;&nbsp;ebyuxrot@gmail.com / <a href="https://t.me/N3VERZzz">Telegram</a>
    </div>
""", unsafe_allow_html=True)



# Отображение содержимого
display_tab_content()