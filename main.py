from typing import Set, Tuple

def text_to_set(file_path: str) -> Set[str]:
    """
    Reads a file and returns a set of words in the file.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
    return set(text.lower().split())

def jaccard_similarity(set1: Set[str], set2: Set[str]) -> Tuple[float, int, int]:
    """
    Computes the Jaccard Similarity between two sets and returns additional information.
    Returns a tuple containing:
    - Jaccard Similarity as a percentage
    - Number of common words
    - Number of Unique words
    """
    intersection = set1.intersection(set2)
    union = set1.union(set2)
    similarity = len(intersection) / len(union) if union else 0
    common_words = len(intersection)
    unique_words = len(union) - common_words
    return similarity * 100, common_words, unique_words


file1 = 'TestFiles/file_1.txt'
file2 = 'TestFiles/file_2.txt'

words1 = text_to_set(file1)
words2 = text_to_set(file2)

similarity_percentage, common_words_count, unique_words_count = jaccard_similarity(words1, words2)
print(f"Jaccard Similarity: {similarity_percentage:.2f}%")
print(f"Common words: {common_words_count}")
print(f"Unique words: {unique_words_count}")



