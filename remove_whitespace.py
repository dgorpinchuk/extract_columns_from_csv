import csv
from pathlib import Path

# Specify the input and output CSV file paths
input_path = Path('input')
if not input_path.exists():
    input_path.mkdir()

output_path = Path('output')
if not output_path.exists():
    output_path.mkdir()

filename = 'season8_24_25.csv'

input_csv_file = input_path / filename
output_csv_file = output_path / filename

# List of column names to strip whitespace from
columns_to_strip = ['Фамилия', 'Имя', 'Отчество']

# Open the input CSV file for reading
with open(input_csv_file, mode='r', newline='', encoding='utf-8') as infile:
    # Create a CSV reader object
    reader = csv.DictReader(infile)
    # Get the field names from the input file
    fieldnames = reader.fieldnames

    # Open the output CSV file for writing
    with open(output_csv_file, mode='w', newline='', encoding='utf-8') as outfile:
        # Create a CSV writer object
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        # Write the header to the output file
        writer.writeheader()

        # Iterate over each row in the input file
        for row in reader:
            # Strip whitespace from the specified columns
            for col in columns_to_strip:
                if col in row and row[col] is not None:
                    row[col] = row[col].strip()
            # Write the modified row to the output file
            writer.writerow(row)

print(f"Whitespace removed from columns {columns_to_strip} and new file saved as '{output_csv_file}'.")
