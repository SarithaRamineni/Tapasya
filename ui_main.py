import tkinter as tk
from tkinter import ttk, Text
from PIL import ImageTk, Image
import os
from tapascore import model_response
from test import tablenames, database_names

os.chdir(r'C:\Users\mmoraleszapata\OneDrive - Hitachi Vantara\Desktop\Archivos varios\Hackaton')


def process_answer(answer, agg):
    if agg == 'NONE':
        # Remove duplicates: 
        unique_ans = set(answer)
        return list(unique_ans)
    elif agg == 'COUNT':
        return f'Total values: {len(answer)}. Actual values: {answer}'
    # Then the answer is an average or a sum
    sep = answer[0]
    lis = sep.split(',')
    answer_ints = [float(x.replace(' ', '')) for x in lis]
    if agg == 'SUM':
        return f'SUM of values: {sum(answer_ints)}. Actual values: {answer}'
    elif agg == 'AVERAGE':
        return f'AVERAGE of values: {sum(answer_ints)/len(answer_ints)}. Actual values: {answer}'


def handle_confirmation():
    database = dropdown.get()
    table = dependent_dropdown.get()
    question = text.get('1.0', 'end')
    text.delete('1.0', 'end')
    answer, agg = model_response(selected_dataset=database, input_questions=question, 
                                 selected_table=table)
    clean_answer = process_answer(answer, agg)
    text.insert('1.0', f'YOU: {question}\n\nTapasya: {clean_answer}')


def update_dependent_dropdown(*args):
    selected_database = dropdown.get()
    try:
        table_names = tablenames(selected_database)
        dependent_dropdown.config(values = table_names)

    except:
        dependent_dropdown.config(values=[])  # Clear options if no valid selection

# Create the main window
root = tk.Tk()
root.title("TAPASYA")
root.geometry('800x600+50+50')
root.iconbitmap("logo.ico")


img = ImageTk.PhotoImage(Image.open('background1.png').resize((800, 300))  )
#The Pack geometry manager packs widgets in rows or columns.

panel = tk.Label(root, image = img).pack()
separator = ttk.Separator(root, orient='horizontal')
separator.pack(fill='x')
# Greeting message label
greeting_label = tk.Label(root, text="Please select a database:", font=("Helvetica", 14))
greeting_label.pack(padx=10, pady=10)

# Define options for the dropdown
options = database_names()


# Create a dropdown widget
dropdown = ttk.Combobox(root, values=options, )
dropdown.pack(padx=10, pady=10)

greeting_label = tk.Label(root, text="Please select a table:", font=("Helvetica", 14))
greeting_label.pack(padx=10, pady=10)
# Dropdown for tables
dependent_dropdown = ttk.Combobox(root, values=[])
dependent_dropdown.pack(padx=10, pady=10)


dropdown.bind("<<ComboboxSelected>>", update_dependent_dropdown)

separator = ttk.Separator(root, orient='horizontal')
separator.pack(fill='x')
text = Text(root, height=10)
text.pack()





text.insert('1.0', 'State your question')
separator = ttk.Separator(root, orient='horizontal')
separator.pack(fill='x')
# Confirmation button
confirm_button = tk.Button(root, text="Confirm Selection", command=handle_confirmation)
confirm_button.pack(pady=10)
root.mainloop()

