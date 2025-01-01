from wand.image import Image
from wand.color import Color
import os

def combine_images_with_text(text, image_dir, max_width, output_file):
    # Liste der Bilddateien entsprechend den Buchstaben im Text
    images = []
    for char in text:
        if char.strip():  # Ignoriere Leerzeichen
            char_file = os.path.join(image_dir, f"{char}.jpeg")
            if os.path.exists(char_file):
                images.append((char_file, char))
            else:
                print(f"Warnung: Bild für Buchstaben '{char}' fehlt.")
        else:
            images.append((None, "space"))

    # Öffne alle Bilder und füge sie horizontal zusammen
    combined_width = 0
    max_height = 0
    image_objects = []
    lines = []
    current_line = []

    for img_path, char in images:
        if char == "space":
            lines.append((current_line, combined_width, max_height))
            combined_width = 0
            max_height = 0
            current_line = []
            continue

        with Image(filename=img_path) as img:
            combined_width += img.width + 5  # 5 Pixel Abstand zwischen den Bildern
            max_height = max(max_height, img.height)
            current_line.append(img.clone())

    if current_line:
        lines.append((current_line, combined_width - 5, max_height))  # Entferne den letzten zusätzlichen Abstand

    # Berechne Gesamthöhe und maximale Breite der kombinierten Bilder
    total_height = sum(line[2] for line in lines) + (len(lines) - 1) * 10  # 10 Pixel Abstand zwischen Zeilen
    max_line_width = max(line[1] for line in lines)

    with Image(width=max_line_width, height=total_height, background=Color("black")) as combined_image:
        current_y = 0
        for line, line_width, line_height in lines:
            current_x = (max_line_width - line_width) // 2  # Zentriere die Zeile horizontal
            for img in line:
                combined_image.composite(img, left=current_x, top=current_y)
                current_x += img.width + 10  # 5 Pixel Abstand zwischen Bildern
            current_y += line_height + 20  # 10 Pixel Abstand zwischen Zeilen

        # Falls Breite zu groß ist, skalieren
        if combined_image.width > max_width:
            scale_factor = max_width / combined_image.width
            new_height = int(combined_image.height * scale_factor)
            combined_image.resize(max_width, new_height)

        # Speichern des Ergebnisses
        combined_image.save(filename=output_file)
        print(f"Ausgabebild gespeichert unter: {output_file}")

# Parameter
text_to_render = "ich behaupte dass der converter funktioniert"
input_directory = "/your/dir/of/pictures"  # Pfad zum Verzeichnis mit Buchstabenbildern
max_image_width = 3072
output_image_path = "output.png"

combine_images_with_text(text_to_render, input_directory, max_image_width, output_image_path)

