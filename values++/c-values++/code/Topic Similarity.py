import openai
import numpy as np
from numpy import dot
from numpy.linalg import norm
import json

# 设置 OpenAI API 密钥
openai.api_key = ''
openai.api_base = ""  # 替换为你的 API 密钥

# 使用 OpenAI 的 Embeddings API 获取文本嵌入向量
def text_to_vector_openai(text):
    try:
        response = openai.Embedding.create(
            input=text,
            model="text-embedding-ada-002"  # 使用的模型
        )

        # 返回嵌入向量
        embedding = response.data[0].embedding
        return np.array(embedding)

    except Exception as e:
        print(f"Error fetching embeddings: {e}")
        return None  # 或者返回一个零向量 np.zeros(1536) 根据模型维度调整

# 计算两个向量的余弦相似度
def cosine_similarity(vec1, vec2):
    norm_vec1 = np.linalg.norm(vec1)
    norm_vec2 = np.linalg.norm(vec2)

    if norm_vec1 == 0 or norm_vec2 == 0:
        return 0  # 如果任一向量是零向量，返回相似度 0

    return dot(vec1, vec2) / (norm_vec1 * norm_vec2)

# 读取 JSON 文件并返回所有文本
def read_texts_from_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        return data

# 文件路径
view_json_file =r''
dialogues_json_file =r''

# 读取 JSON 文件中的文本数据
print("Reading and processing texts from JSON files...")
views = read_texts_from_json(view_json_file)
dialogues = read_texts_from_json(dialogues_json_file)

# 检查短文本和对话数量是否一致
if len(views) != len(dialogues):
    raise ValueError("The number of short texts (views) and dialogues must be the same!")

# 批量计算相似度
similarities = []
for i in range(0, len(views)):
    if not views[i] or not dialogues[i]:  # 检查文本是否有效
        print(f"Skipping empty text for index {i}.")
        continue  # 跳过空文本

    # 获取短文本和对话的嵌入向量
    short_text_vector = text_to_vector_openai(views[i])
    long_document_vector = text_to_vector_openai(dialogues[i])

    # 检查向量是否有效
    if short_text_vector is None or long_document_vector is None:
        print(f"Skipping invalid vector for index {i}.")
        continue

    # 计算余弦相似度
    similarity = cosine_similarity(short_text_vector, long_document_vector)
    similarities.append(similarity)
    print(f"Cosine similarity between short text {i + 1} and dialogue {i + 1}: {similarity:.4f}")

# 输出所有相似度结果
print("All cosine similarities:", similarities)
