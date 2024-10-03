import pandas as pd
import tkinter as tk
from tkinter import filedialog

def main():
    # Step 1: Ask user for column names one by one
    columns = []
    col_count = 0
    print("Введите названия столбцов по одному. Введите 'готово', когда закончите")

    while True:
        col_name = input("Введите название столбца: ").strip()
        col_count += 1
        print(f"🔸Название столбца {col_count}: {col_name}")
        if col_name.lower() == 'готово':
            break
        columns.append(col_name)

    # Step 2: Use a modal window to select the CSV file
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    root.attributes('-topmost', True)  # Bring window to front
    root.lift()  # Lift the window above others
    root.focus_force()  # Focus on the window
    csv_file = filedialog.askopenfilename(title="Выберите CSV файл", filetypes=[("Файлы CSV", "*.csv")])

    if not csv_file:  # If no file was selected
        print("Файл не был выбран. Завершение...")
        return

    try:
        # Step 3: Open the CSV file and extract specified columns
        df = pd.read_csv(csv_file, usecols=columns)
        print("Столбцы извлечены успешно")

        # Step 4: Ask to remove duplicates
        remove_duplicates = input("Удалить дублирующиеся строки? (д/н): ").strip().lower()
        if remove_duplicates == 'д':
            df = df.drop_duplicates()
            print("Дубликаты удалены")

        # Check if column 'UID' exists in the DataFrame
        if 'UID' in df.columns:
            # Convert the 'UID' column to string type
            df = df.astype({"UID": str})

        # Step 5: Save the result as result.xlsx
        output_file = "result.xlsx"
        df.to_excel(output_file, index=False)
        print(f"Итоговый файл сохранен")

    except Exception as e:
        print(f"❌ Возникла ошибка: {e}")

if __name__ == "__main__":
    main()
