import tkinter as tk
from tkinter import filedialog
import pandas as pd
import logging
import sys

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

try:
    # Set up the tkinter root window and hide it
    root = tk.Tk()
    root.withdraw()  # Hide the root window of tkinter

    # Show the file dialog to allow the user to select an Excel file
    file_path = filedialog.askopenfilename(
        title="Select an Excel file",
        filetypes=[("Excel files", "*.xlsx *.xls")]
    )

    if not file_path:
        logging.warning("No file selected.")
        sys.exit("No file selected.")

    logging.info(f"File selected: {file_path}")

    # Read the Excel file, skipping the first 5 rows
    logging.info("Reading Excel file with pandas.")
    try:
        data = pd.read_excel(file_path, engine='openpyxl', skiprows=5)
    except Exception as e:
        logging.error("Error reading Excel file.", exc_info=True)
        raise

    logging.info("Excel file read successfully.")

    # Drop the first column, assumed to be at index 0
    try:
        data = data.iloc[:, 1:]
    except Exception as e:
        logging.error("Error dropping the first column.", exc_info=True)
        raise

    logging.info("First column dropped.")

    # Extract columns
    try:
        selected_columns = data[["UID", "Логин", "Фамилия", "Имя", "Отчество", "Почта для рассылок", "Дата рождения", "Телефон", "ВУЗ", "Город проживания"]]
    except KeyError as e:
        logging.error("Required columns not found in the Excel file.", exc_info=True)
        raise

    logging.info("Columns extracted.")

    # Remove duplicates
    try:
        unique_data = selected_columns.drop_duplicates()
    except Exception as e:
        logging.error("Error removing duplicates.", exc_info=True)
        raise

    logging.info("Duplicates removed from data.")

    # Save the result to a new CSV file
    try:
        unique_data.to_csv("output.csv", index=False)
    except Exception as e:
        logging.error("Error saving to CSV file.", exc_info=True)
        raise

    logging.info("Output saved to output.csv")

except Exception as e:
    logging.critical("Unexpected error occurred.", exc_info=True)
