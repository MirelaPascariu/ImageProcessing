import streamlit as st
import cv2
import numpy as np
import os

# Functions for filter
def denoise_gaussian(image):
    return cv2.GaussianBlur(image, (5, 5), 0)

def denoise_media_aritmetica(image):
    return cv2.blur(image, (3, 3))

def denoise_geometric(image, kernel_size=5):
    image = np.float32(image)
    kernel = np.ones((kernel_size, kernel_size), np.float32) / (kernel_size ** 2)
    return cv2.filter2D(image, -1, kernel)

def denoise_median(image, kernel_size=3):
    return cv2.medianBlur(image, kernel_size)

# Interface Streamlit
st.title("Atenuarea Zgomotului pentru Imagini")

# Verify folder images exist and is not  empty
if not os.path.exists('images'):
    st.error("Folderul 'images' nu există. Asigură-te că ai un folder numit 'images' cu imagini în format JPG.")
else:
    image_files = [f for f in os.listdir('images') if f.endswith('.jpg')]

    if len(image_files) == 0:
        st.error("Nu există imagini în folderul 'images'. Adaugă imagini în format JPG pentru a continua.")
    else:
        # Select image
        image_file = st.selectbox("Alege o imagine din folderul 'images'", image_files)

        image_path = os.path.join("images", image_file)
        original_image = cv2.imread(image_path)
        original_image_rgb = cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB)

        st.subheader("Imaginea Originală")
        st.image(original_image_rgb, caption="Imagine Originală", use_column_width=True)

        # Select filter
        filter_option = st.selectbox("Alege un filtru pentru aplicare", 
                                     ["Gaussian", "Media Aritmetică", "Median", "Geometric"])

        if filter_option == "Gaussian":
            processed_image = denoise_gaussian(original_image_rgb)
        elif filter_option == "Media Aritmetică":
            processed_image = denoise_media_aritmetica(original_image_rgb)
        elif filter_option == "Median":
            processed_image = denoise_median(original_image_rgb)
        elif filter_option == "Geometric":
            processed_image = denoise_geometric(original_image_rgb)

        st.subheader("Imaginea Procesată")
        st.image(processed_image, caption=f"Imagine Procesată cu Filtrul {filter_option}", use_column_width=True)
