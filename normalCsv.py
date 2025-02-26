import os
import json
import pandas as pd

def extract_conversation(folder_path):
    conversation_data = []

    for filename in os.listdir(folder_path):
        if filename.endswith('.json'):
            file_path = os.path.join(folder_path, filename)

            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)

                grouped_conversations = {}
                for entry in data:
                    conversation_id = entry["대화셋일련번호"]

                    if conversation_id not in grouped_conversations:
                        grouped_conversations[conversation_id] = []

                    if entry["QA"] == "Q":
                        question = entry["고객질문(요청)"] if entry["고객질문(요청)"] else entry["상담사질문(요청)"]
                        grouped_conversations[conversation_id].append(question)
                    elif entry["QA"] == "A":
                        answer = entry["상담사답변"]
                        grouped_conversations[conversation_id].append(answer)

                for conversation_id, messages in grouped_conversations.items():
                    conversation_data.append({
                        "number": conversation_id,
                        "text": " ".join(messages) 
                    })

    df = pd.DataFrame(conversation_data)
    output_file_path = os.path.join(folder_path, 'normal_data.csv')
    df.to_csv(output_file_path, index=False, encoding='utf-8-sig')

folder_path = 'C:/Users/DS/Desktop/22883/dp/voicephishing/dataset/text/normal' 
extract_conversation(folder_path)
