import os
import subprocess
import streamlit as st
from ultralytics import YOLO
import warnings
warnings.filterwarnings("ignore", category=Warning)

# Используйте магию Streamlit, чтобы избежать повторной загрузки модели при каждом изменении страницы
@st.cache(allow_output_mutation=True)
def load_model(model_path):
    return YOLO(model_path)

def process_video(uploaded_video, model):
    # Создание временного файла для загруженного видео
    with open("temp_video.avi", "wb") as f:
        f.write(uploaded_video.getbuffer())
    
    # Используйте модель для обнаружения знаков и получите путь к обработанному видео
    output_video_path = model.predict(source="temp_video.avi", show=True, save=True)

    # Получение пути к сохраненному обработанному видео
    processed_video_path = f'runs/detect/predict{len(os.listdir("runs/detect"))}/temp_video.avi'
    
    # Конвертация формата в MP4
    result_out_path = f'runs/detect/predict{len(os.listdir("runs/detect"))}/temp_video.mp4'
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'panic', '-i', processed_video_path, result_out_path])
    
    return result_out_path

def main():
    st.title("Детекция дорожных знаков с использованием YOLOv8")

    model_path = 'C:/Users/kurop/OneDrive/Desktop/KURS_SAMSUNG/runs/detect/predict/train6/weights/best.pt'
    uploaded_video = st.file_uploader("Загрузите видео для обработки", type=["mp4", "avi"])
    
    is_processing = False
    result_video_path = None  # Инициализируем переменную result_video_path

    if uploaded_video is not None:
        video_model = load_model(model_path)

        if st.button("Запустить обнаружение дорожных знаков"):
            is_processing = True
            processing_placeholder = st.empty()  # Создаем пустой элемент
            processing_placeholder.markdown('<img src="https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExeXA2eTh4enQwMGJpZXhzMmRoYW41OHA4YzJpd2JmYnZyOTQ3ZDVycSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/uIJBFZoOaifHf52MER/giphy.gif">', unsafe_allow_html=True)
            result_video_path = process_video(uploaded_video, video_model)
            is_processing = False

    if not is_processing and result_video_path: 
        st.video(result_video_path)
        processing_placeholder.empty()  # Удаляем гифку после вывода видео

if __name__ == "__main__":
    main()
