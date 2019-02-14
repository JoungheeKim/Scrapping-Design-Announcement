import pandas as pd
import os


def make_hyperlink(root_url, url):
    total_url = root_url + url
    return '=HYPERLINK("%s", "%s")' % (total_url.format(url), url)

def save_file(df, root_url, path, outformat='excel', name="입찰공고", sheet_name="Summary"):
    for item in df.columns:
        if "URL" in item:
            df[item] = df[item].apply(lambda x: make_hyperlink(root_url, x))

    if outformat == "csv":
        file_name_csv = name + '.csv'
        df.to_csv(os.path.join(path, file_name_csv), encoding='ms949')
        return

    else:
        file_name_excel = name + ".xlsx"
        writer = pd.ExcelWriter(os.path.join(path, file_name_excel))
        df.to_excel(writer, sheet_name=sheet_name)
        adjust_excel_column(writer.sheets[sheet_name])
        writer.save()
        writer.close()
        return

def adjust_excel_column(worksheet):
    for col in worksheet.columns:
        max_length = 0
        column = col[0].column  # Get the column name
        for cell in col:
            try:  # Necessary to avoid error on empty cells
                if len(str(cell.value)) > max_length:
                    max_length = len(cell.value)
            except:
                pass
        adjusted_width = (max_length + 2) * 1.2
        worksheet.column_dimensions[column].width = adjusted_width
    return