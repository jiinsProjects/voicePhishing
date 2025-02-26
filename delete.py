import pandas as pd

augmented_df = pd.read_csv('augmented_phish.csv')

augmented_df = augmented_df.drop_duplicates(subset=['text'])

augmented_df.to_csv('final_phish.csv', index=False)

print(f"중복 제거 완료! 남은 데이터 행 수: {len(augmented_df)}")
