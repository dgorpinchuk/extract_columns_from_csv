import wx
import pandas as pd
import os

class CSVColumnExtractor(wx.Frame):
    def __init__(self, *args, **kw):
        super(CSVColumnExtractor, self).__init__(*args, **kw)

        self.columns = []
        self.max_height = 600  # Set a reasonable max height for the window
        self.InitUI()

    def InitUI(self):
        panel = wx.Panel(self)

        # Main layout
        self.vbox = wx.BoxSizer(wx.VERTICAL)

        # Instruction text
        instruction_text = wx.StaticText(panel, label="Введите названия столбцов по одному. Введите 'готово', когда закончите")
        self.vbox.Add(instruction_text, flag=wx.EXPAND | wx.ALL, border=10)

        # Text input for column name
        self.column_input = wx.TextCtrl(panel)
        self.vbox.Add(self.column_input, flag=wx.EXPAND | wx.ALL, border=10)

        # Button to add column
        add_button = wx.Button(panel, label="Добавить столбец")
        add_button.Bind(wx.EVT_BUTTON, self.OnAddColumn)
        self.vbox.Add(add_button, flag=wx.EXPAND | wx.ALL, border=10)

        # Listbox to display added columns, make it vertically stretchable
        self.column_list = wx.ListBox(panel)
        self.vbox.Add(self.column_list, proportion=1, flag=wx.EXPAND | wx.ALL, border=10)

        # Button to finish column entry
        finish_button = wx.Button(panel, label="Готово")
        finish_button.Bind(wx.EVT_BUTTON, self.OnFinish)
        self.vbox.Add(finish_button, flag=wx.EXPAND | wx.ALL, border=10)

        panel.SetSizer(self.vbox)

        # Set initial window size and position
        self.SetTitle('CSV Column Extractor')
        self.SetSize((400, 200))  # Initial size
        self.Centre()

    def OnAddColumn(self, event):
        col_name = self.column_input.GetValue().strip()
        if col_name.lower() == 'готово':
            return
        if col_name:
            self.columns.append(col_name)
            self.column_list.Append(col_name)
            self.column_input.Clear()

            # Dynamically adjust the window size when a new column is added
            current_size = self.GetSize()
            new_height = current_size[1] + 30  # Increase height by 30 pixels per new column

            # Limit the height to a maximum to avoid excessive growth
            if new_height <= self.max_height:
                self.SetSize(current_size[0], new_height)

            # Resize and refresh layout to adjust the ListBox size
            self.Layout()

    def OnFinish(self, event):
        if not self.columns:
            wx.MessageBox('Необходимо добавить хотя бы один столбец.', 'Ошибка', wx.OK | wx.ICON_ERROR)
            return

        # Show file dialog to select CSV file
        with wx.FileDialog(self, "Выберите CSV файл", wildcard="CSV files (*.csv)|*.csv",
                           style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:

            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return  # User cancelled

            csv_file = fileDialog.GetPath()

        if not csv_file or not os.path.exists(csv_file):
            wx.MessageBox('Файл не был выбран. Завершение...', 'Ошибка', wx.OK | wx.ICON_ERROR)
            return

        # Try to open the CSV and extract columns
        try:
            df = pd.read_csv(csv_file, usecols=self.columns)
            wx.MessageBox('Столбцы извлечены успешно', 'Информация', wx.OK | wx.ICON_INFORMATION)

            # Ask to remove duplicates
            dlg = wx.MessageDialog(None, "Удалить дублирующиеся строки?", "Вопрос", wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)
            remove_duplicates = dlg.ShowModal() == wx.ID_YES
            dlg.Destroy()

            if remove_duplicates:
                df = df.drop_duplicates()
                wx.MessageBox('Дубликаты удалены', 'Информация', wx.OK | wx.ICON_INFORMATION)

            # Convert 'UID' column to string type if exists
            if 'UID' in df.columns:
                df = df.astype({"UID": str})

            # Save the result to the same directory as the input file
            input_dir = os.path.dirname(csv_file)  # Get the input file's directory
            output_file = os.path.join(input_dir, "result.xlsx")  # Save the result in the same folder
            df.to_excel(output_file, index=False)
            wx.MessageBox(f'Итоговый файл сохранен как {output_file}', 'Информация', wx.OK | wx.ICON_INFORMATION)

            # Close the window after processing is complete
            self.Close()

        except Exception as e:
            wx.MessageBox(f'Возникла ошибка: {e}', 'Ошибка', wx.OK | wx.ICON_ERROR)

def main():
    app = wx.App(False)
    frame = CSVColumnExtractor(None)
    frame.Show()
    app.MainLoop()

if __name__ == "__main__":
    main()
