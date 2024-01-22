import streamlit as st
import os
import json
from openai import OpenAI

# Создание клиента OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

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

# Разметка приложения Streamlit
st.title("Math Problem Solver")
problem = st.text_area("Enter a math problem:", key="math_input")

if st.button("Solve the problem", key="math_button"):
    solution = solve_math_problem(problem)
    st.write("Answer:", solution)  # Display only the answer part