import os
import re
import csv
from transformers import BertTokenizer

# KoBERT 토크나이저 로드
tokenizer = BertTokenizer.from_pretrained('kykim/bert-kor-base')

def split_text_by_token(text, max_length=512):
    # 입력 텍스트를 토큰화하여 최대 길이에 맞게 분할
    tokens = tokenizer.tokenize(text)
    results = []
    current_chunk = []
    
    for token in tokens:
        current_chunk.append(token)
        
        if len(current_chunk) >= max_length:
            # 현재 청크가 max_length에 도달하면 마지막 '다', '까', '요'로 끝나는 단어를 찾기
            chunk_text = tokenizer.convert_tokens_to_string(current_chunk)
            last_valid_index = -1
            
            # 마지막 '다', '까', '요'로 끝나는 단어의 인덱스를 찾음
            for i in range(len(current_chunk) - 1, -1, -1):
                if re.search(r'(다|까|요)$', current_chunk[i]):
                    last_valid_index = i
                    break
            
            # 마지막 유효 인덱스가 발견되면 해당 지점에서 분할
            if last_valid_index != -1:
                results.append(tokenizer.convert_tokens_to_string(current_chunk[:last_valid_index + 1]))
                current_chunk = current_chunk[last_valid_index + 1:]  # 나머지 토큰을 현재 청크로 설정
    
    # 남아있는 청크를 추가
    if current_chunk:
        results.append(tokenizer.convert_tokens_to_string(current_chunk))
    
    return results

def process_text_files_to_csv(input_folder, output_csv):
    with open(output_csv, mode='w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["File Name", "text"]) 
        
        for file_name in os.listdir(input_folder):
            if file_name.endswith(".txt"):
                file_path = os.path.join(input_folder, file_name)
                with open(file_path, mode='r', encoding='utf-8') as file:
                    text = file.read()
                    chunks = split_text_by_token(text)
                    for chunk in chunks:
                        writer.writerow([file_name, chunk])  

input_folder = "C:/Users/DS/Desktop/22883/dp/voicephishing/dataset/text/phishing"  
output_csv = "phish_data.csv"  

process_text_files_to_csv(input_folder, output_csv)
