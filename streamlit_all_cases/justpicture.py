import streamlit as st
import os
from openai import OpenAI

# Инициализируем клиент OpenAI с вашим API ключом
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

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
        # В случае ошибки возвращаем None и выводим сообщение об ошибке
        st.error(f"Error generating image: {e}")
        return None

def main():
    st.title("DALL-E Image Generator")
    prompt = st.text_input("Enter a word or phrase:", "")
    if prompt:
        image_url = generate_image(prompt)
        if image_url:
            st.image(image_url, caption=prompt)
        else:
            st.error("Error generating image")

if __name__ == "__main__":
    main()