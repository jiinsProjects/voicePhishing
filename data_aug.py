import pandas as pd
import random
import pickle
import re
from tqdm import tqdm  # tqdm 라이브러리 추가

# wordnet 파일 로딩
wordnet = {}
with open(r"C:\Users\DS\Desktop\22883\dp\wordnet.pickle", "rb") as f:
    wordnet = pickle.load(f)

# 한글만 남기고 나머지 삭제
def get_only_hangul(line):
    parseText = re.compile('[^ㄱ-ㅎㅏ-ㅣ가-힣\s]').sub('', line)
    return parseText

# Synonym replacement
def synonym_replacement(words, n):
    new_words = words.copy()
    random_word_list = list(set([word for word in words]))
    random.shuffle(random_word_list)
    num_replaced = 0
    for random_word in random_word_list:
        synonyms = get_synonyms(random_word)
        if len(synonyms) >= 1:
            synonym = random.choice(synonyms)
            new_words = [synonym if word == random_word else word for word in new_words]
            num_replaced += 1
        if num_replaced >= n:
            break
    return new_words

def get_synonyms(word):
    try:
        synonyms = [syn for syn in wordnet[word]]
        return synonyms
    except KeyError:
        return []  # 단어가 없으면 빈 리스트 반환

# Random deletion
def random_deletion(words, p):
    if len(words) == 1:
        return words
    new_words = [word for word in words if random.uniform(0, 1) > p]
    if len(new_words) == 0:
        return [words[random.randint(0, len(words)-1)]]
    return new_words

# Random swap
def random_swap(words, n):
    new_words = words.copy()
    for _ in range(n):
        random_idx_1 = random.randint(0, len(new_words)-1)
        random_idx_2 = random.randint(0, len(new_words)-1)
        new_words[random_idx_1], new_words[random_idx_2] = new_words[random_idx_2], new_words[random_idx_1]
    return new_words

# Random insertion
def random_insertion(words, n):
    new_words = words.copy()
    for _ in range(n):
        add_word(new_words)
    return new_words

def add_word(new_words):
    max_attempts = 10  # 최대 시도 횟수
    for _ in range(max_attempts):
        random_word = random.choice(new_words)
        synonyms = get_synonyms(random_word)
        if synonyms:  # 동의어가 있다면
            random_synonym = random.choice(synonyms)
            random_idx = random.randint(0, len(new_words) - 1)
            new_words.insert(random_idx, random_synonym)
            return  # 단어 삽입 후 종료
    # 동의어를 찾지 못한 경우 로그 출력 (디버깅용)
    print(f"No synonyms found for words in: {new_words}")

# EDA 함수 (증강 기법 적용)
def EDA(sentence, alpha_sr=0.1, alpha_ri=0.1, alpha_rs=0.1, p_rd=0.1, num_aug=9):
    words = sentence.split(' ')
    words = [word for word in words if word != ""]
    num_words = len(words)

    augmented_sentences = []
    num_new_per_technique = int(num_aug / 4) + 1

    n_sr = max(1, int(alpha_sr * num_words))
    n_ri = max(1, int(alpha_ri * num_words))
    n_rs = max(1, int(alpha_rs * num_words))

    # Synonym replacement
    for _ in range(num_new_per_technique):
        a_words = synonym_replacement(words, n_sr)
        augmented_sentences.append(' '.join(a_words))

    # Random insertion
    for _ in range(num_new_per_technique):
        a_words = random_insertion(words, n_ri)
        augmented_sentences.append(' '.join(a_words))

    # Random swap
    for _ in range(num_new_per_technique):
        a_words = random_swap(words, n_rs)
        augmented_sentences.append(" ".join(a_words))

    # Random deletion
    for _ in range(num_new_per_technique):
        a_words = random_deletion(words, p_rd)
        augmented_sentences.append(" ".join(a_words))

    augmented_sentences = [get_only_hangul(sentence) for sentence in augmented_sentences]
    random.shuffle(augmented_sentences)

    if num_aug >= 1:
        augmented_sentences = augmented_sentences[:num_aug]
    else:
        keep_prob = num_aug / len(augmented_sentences)
        augmented_sentences = [s for s in augmented_sentences if random.uniform(0, 1) < keep_prob]

    augmented_sentences.append(sentence)

    return augmented_sentences

# CSV 파일 로딩
df = pd.read_csv(r'C:\Users\DS\Desktop\22883\dp\phish_data.csv')

# 데이터 증강 적용
augmented_data = []
for index, row in tqdm(df.iterrows(), total=len(df), desc="Processing", smoothing=0):  # tqdm으로 진행 상황 표시
    text = row['text']
    if not text or len(text.strip()) == 0:  # 텍스트가 비어 있다면 건너뜀
        continue
    augmented_sentences = EDA(text, num_aug=5)
    augmented_data.extend(augmented_sentences)

# 증강된 데이터를 새로운 DataFrame으로 저장
augmented_df = pd.DataFrame(augmented_data, columns=['text'])
augmented_df.to_csv('augmented_phish.csv', index=False)
