import os
import whisper
import torch

# Whisper 모델 로드
device = "cuda" if torch.cuda.is_available() else "cpu"
model = whisper.load_model("large").to(device)  # 모델을 GPU로 로드

# 음성 파일 경로
input_dir = "C:/Users/DS/Desktop/22883/DP/voicephishing/dataset/voice/phishing/loan"
output_dir = "C:/Users/DS/Desktop/22883/DP/voicephishing/dataset/text/phishing/loan"

# 출력 폴더 생성
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# GPU 사용 가능 여부 확인
print(f"Using device: {device}")

# 특정 파일 범위만 처리1101m                                                        
for file_name in os.listdir(input_dir):
    if file_name.endswith(".mp3"):  # mp3 파일만 처리
        # 파일 이름에서 숫자 추출
        file_number = int(file_name.split('_')[1].split('.')[0])  # aud_77.mp3 -> 77
        if (8 <= file_number <= 9):  # aud_77.mp3 ~ aud_99.mp3 범위만 처리
            input_file_path = os.path.join(input_dir, file_name)
            output_file_name = os.path.splitext(file_name)[0] + ".txt"  # 확장자를 .txt로 변경
            output_file_path = os.path.join(output_dir, output_file_name)

            try:
                # Whisper를 이용한 음성 파일 텍스트 변환
                print(f"Processing {file_name}...")
                result = model.transcribe(input_file_path)  # device 인자는 제거

                # 텍스트 파일 저장
                with open(output_file_path, "w", encoding="utf-8") as f:
                    f.write(result["text"])

                print(f"Saved transcription to {output_file_path}")
            except Exception as e:
                print(f"Failed to process {file_name}: {e}")
