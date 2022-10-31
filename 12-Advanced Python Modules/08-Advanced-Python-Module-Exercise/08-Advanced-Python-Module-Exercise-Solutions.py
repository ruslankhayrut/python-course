import re
import os


phones = []

# walk through all folders
for folder_name, subfolders, files in os.walk('extracted_content'):

    # go through every file for current folder
    for file in files:
        file_name = f'{folder_name}/{file}'

        # search each file for phone number
        with open(file_name, 'r') as data:
            match = re.search(r"\d{3}-\d{3}-\d{4}", data.read())
            if match:
                phones.append(match.group())

print(phones)
