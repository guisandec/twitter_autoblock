import pyautogui
import cv2
import numpy as np
import time

def find_button(screenshot, button_template):
    """
    Busca la ubicación de un botón en una captura de pantalla.

    Args:
        screenshot (numpy.ndarray): La captura de pantalla en formato NumPy.
        button_template (str): La ruta a la imagen de la plantilla del botón.

    Returns:
        list: Lista de coordenadas (x, y) de los centros de los botones encontrados.
    """
    template = cv2.imread(button_template)
    if template is None:    
        print(f"Error: No se pudo cargar la plantilla {button_template}")
        return []

    template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
    screenshot_gray = cv2.cvtColor(np.array(screenshot), cv2.COLOR_BGR2GRAY)

    result = cv2.matchTemplate(screenshot_gray, template_gray, cv2.TM_CCOEFF_NORMED)
    threshold = 0.8  # Ajusta este valor según sea necesario
    loc = np.where(result >= threshold)

    button_centers = []
    for pt in zip(*loc[::-1]):
        button_center = (pt[0] + template.shape[1] // 2, pt[1] + template.shape[0] // 2)
        button_centers.append(button_center)

    return button_centers

def find_closest_button(button_centers, screen_center):
    """
    Encuentra el botón más cercano al centro de la pantalla.

    Args:
        button_centers (list): Lista de coordenadas (x, y) de los centros de los botones encontrados.
        screen_center (tuple): Coordenadas (x, y) del centro de la pantalla.

    Returns:
        tuple: Las coordenadas (x, y) del botón más cercano al centro de la pantalla, o None si no se encuentra.
    """
    closest_button = None
    min_distance = float('inf')

    # eliminar de la lista los botones que no estén en la parte derecha de la pantalla
   

    for button_center in button_centers:
        distance = np.linalg.norm(np.array(button_center) - np.array(screen_center))
        if distance < min_distance:
            min_distance = distance
            closest_button = button_center

    return closest_button

button_templates = ["./boton_1.png", "./boton_2.png", "./boton_3.png"]  # Reemplaza con las rutas a tus plantillas de botones

repeat = input("¿Cuántas veces deseas repetir el proceso?")  # Número de veces que se repetirá el proceso

screen_width, screen_height = pyautogui.size()
screen_center = (screen_width // 2, screen_height // 2)

for i in range(int(repeat)):
    print(f"Repetición {i + 1}/{repeat}")
    screenshot = pyautogui.screenshot()
    screenshot_np = np.array(screenshot)
    print(">Buscando el botón 1 más cercano al centro de la pantalla")
    button_1_centers = find_button(screenshot, button_templates[0])
    print (button_1_centers)
    button_1_location = find_closest_button(button_1_centers, screen_center)

    if button_1_location:
        print(f"{i + 1}/{repeat}>>Botón 1 encontrado en: {button_1_location}")
     
        pyautogui.moveTo(button_1_location)
        pyautogui.click()
        time.sleep(0.6)  # Espera un segundo antes de buscar los siguientes botones   

        for template_path in button_templates[1:]:
            screenshot = pyautogui.screenshot()
            print(f"{i + 1}/{repeat}>>Buscando botón en {template_path}")
            button_location = find_button(screenshot, template_path)
            if button_location:
                print(f"{i + 1}/{repeat}>>>Botón encontrado en: {button_location[0]}")
                pyautogui.moveTo(button_location[0])
                pyautogui.click()
                time.sleep(0.6)  # Espera un segundo antes de hacer clic nuevamente
            else:
                print(f"{i + 1}/{repeat}>>Botón no encontrado en: {template_path}")
                break
    else:
        print(f"{i + 1}/{repeat}>>Botón 1 no encontrado")
        break

print("Proceso completado")