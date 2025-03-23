import pdfplumber
import csv
headers = ['NO.', 'Command', 'Explanation', 'Parameters', 'Returning']
new_tables = {}
i = 0
pdf_path = 'Programming Commands for 286.pdf'
with pdfplumber.open(pdf_path) as pdf:
    for page_index, page in enumerate(pdf.pages[0:38]):
        page_num = page_index + 1
        tables = page.extract_tables()
        if tables:
            for j, table in enumerate(tables):
                for row in table:
                    
                    index = row[0].replace('.', '').strip() if row[0] else None
                    is_header_row = index and not index.isdigit() and index != ''
                    for header, cell in zip(headers, row):
                        if not cell or cell.strip() == '':
                            is_header_row = False
                        elif not cell.startswith(header):
                            is_header_row = False
                            break

                    if is_header_row:
                        continue

                    if not index:
                        # This is a continuation of the previous row, so we need to append it to the last row in new_tables[i]
                        if new_tables[i]:
                            last_row = new_tables[i][-1]
                            for k in range(len(row))[1:]:
                                if row[k] and last_row[k]:
                                    last_row[k] += '\n' + row[k]
                                elif row[k]:
                                    last_row[k] = row[k]
                            new_tables[i][-1] = last_row
                            continue
                    elif index.isdigit():
                        index = int(index)
                        if index == 1:
                            i = page_num
                            new_tables[i] = [headers]
                    
                    new_tables[i].append(row)

for key, value in new_tables.items():
    with open(f'docs/table_{key}.csv', 'w', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(value)
