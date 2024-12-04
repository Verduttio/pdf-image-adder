import os
from tkinter import Tk, Label, Button, Entry, filedialog, messagebox
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from PIL import Image
from io import BytesIO


def add_stamp_to_pdf(input_path, output_path, stamp_image_path, x, y):
    reader = PdfReader(input_path)
    writer = PdfWriter()

    image = Image.open(stamp_image_path)
    stamp_pdf = BytesIO()
    c = canvas.Canvas(stamp_pdf)

    width, height = image.size
    c.drawImage(stamp_image_path, x, y, width=100, height=50)
    c.save()

    stamp_pdf.seek(0)
    stamp_reader = PdfReader(stamp_pdf)

    for i, page in enumerate(reader.pages):
        if i == 4:
            page.merge_page(stamp_reader.pages[0])
        writer.add_page(page)

    with open(output_path, "wb") as output_file:
        writer.write(output_file)


def process_all_pdfs_in_folder(input_folder, output_folder, stamp_image_path, x, y):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        if filename.endswith(".pdf"):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, filename)
            add_stamp_to_pdf(input_path, output_path, stamp_image_path, x, y)

    messagebox.showinfo("Gotowe", "Przetwarzanie zakończone!")


def select_input_folder():
    folder = filedialog.askdirectory()
    input_folder_entry.delete(0, "end")
    input_folder_entry.insert(0, folder)


def select_output_folder():
    folder = filedialog.askdirectory()
    output_folder_entry.delete(0, "end")
    output_folder_entry.insert(0, folder)


def select_stamp_image():
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.png")])
    stamp_image_entry.delete(0, "end")
    stamp_image_entry.insert(0, file_path)


def start_processing():
    input_folder = input_folder_entry.get()
    output_folder = output_folder_entry.get()
    stamp_image = stamp_image_entry.get()
    try:
        x = int(x_entry.get())
        y = int(y_entry.get())
    except ValueError:
        messagebox.showerror("Błąd", "Podaj prawidłowe współrzędne!")
        return

    if not input_folder or not output_folder or not stamp_image:
        messagebox.showerror("Błąd", "Wszystkie pola muszą być wypełnione!")
        return

    process_all_pdfs_in_folder(input_folder, output_folder, stamp_image, x, y)


# Tworzenie GUI
root = Tk()
root.title("Dodawanie Pieczątki do PDF")

Label(root, text="Folder wejściowy:").grid(row=0, column=0, sticky="e")
input_folder_entry = Entry(root, width=50)
input_folder_entry.grid(row=0, column=1)
Button(root, text="Wybierz", command=select_input_folder).grid(row=0, column=2)

Label(root, text="Folder wyjściowy:").grid(row=1, column=0, sticky="e")
output_folder_entry = Entry(root, width=50)
output_folder_entry.grid(row=1, column=1)
Button(root, text="Wybierz", command=select_output_folder).grid(row=1, column=2)

Label(root, text="Obraz pieczątki:").grid(row=2, column=0, sticky="e")
stamp_image_entry = Entry(root, width=50)
stamp_image_entry.grid(row=2, column=1)
Button(root, text="Wybierz", command=select_stamp_image).grid(row=2, column=2)

Label(root, text="Współrzędne (x):").grid(row=3, column=0, sticky="e")
x_entry = Entry(root, width=10)
x_entry.grid(row=3, column=1, sticky="w")

Label(root, text="Współrzędne (y):").grid(row=4, column=0, sticky="e")
y_entry = Entry(root, width=10)
y_entry.grid(row=4, column=1, sticky="w")

Button(root, text="Generuj", command=start_processing).grid(row=5, column=0, columnspan=3, pady=10)

root.mainloop()
