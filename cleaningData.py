import os
import re

dir = "C:/Users/DS/Desktop/22883/dp/voicephishing/dataset/text/phishing"

def clean_file(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        lines = file.readlines()

    clean_lines = [(re.sub(r"[^가-힣\s]", "", line)).replace(" 네","") for line in lines]

    with open(file_path, "w", encoding="utf-8") as file:
        file.writelines(clean_lines)

for file_name in os.listdir(dir):
    file_path = os.path.join(dir, file_name) 
    if os.path.isfile(file_path): 
        clean_file(file_path)  
        print(f"{file_name} 수정 완료")


