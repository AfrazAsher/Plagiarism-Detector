from typing import Set, Tuple, List

def text_to_set(file_path: str) -> Set[str]:
    """
    Reads a file and returns a set of words in the file.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
    return set(text.lower().split())

def text_to_list(file_path: str) -> List[str]:
    """
    Reads a file and returns a list of words in the file.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
    return text.lower().split()

def jaccard_similarity(set1: Set[str], set2: Set[str]) -> Tuple[float, int, int]:
    """
    Computes the Jaccard Similarity between two sets and returns additional information.
    Returns a tuple containing:
    - Jaccard Similarity as a percentage
    - Number of common words
    - Number of words that are not common
    """
    intersection = set1.intersection(set2)
    union = set1.union(set2)
    similarity = len(intersection) / len(union) if union else 0
    common_words = len(intersection)
    unique_words = len(union) - common_words
    return similarity * 100, common_words, unique_words

def lcs(X: List[str], Y: List[str]) -> Tuple[int, float, int]:
    """
    Computes the Longest Common Subsequence (LCS) between two lists of words and returns additional information.
    Returns a tuple containing:
    - Length of LCS
    - LCS Similarity as a percentage (based on the shorter of the two lists)
    - Number of words that are not in the LCS
    """
    m, n = len(X), len(Y)
    L = [[0] * (n + 1) for _ in range(m + 1)]

    # Build the LCS table
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if X[i - 1] == Y[j - 1]:
                L[i][j] = L[i - 1][j - 1] + 1
            else:
                L[i][j] = max(L[i - 1][j], L[i][j - 1])

    # LCS length
    lcs_length = L[m][n]

    # Calculate similarity
    shortest_length = min(m, n)
    similarity_percentage = (lcs_length / shortest_length * 100) if shortest_length else 0

    # Calculate non-LCS words
    non_lcs_words = max(m, n) - lcs_length

    return lcs_length, similarity_percentage, non_lcs_words

def levenshtein_distance(s1: str, s2: str) -> Tuple[int, float, int, int]:
    """
    Computes the Levenshtein distance between two strings and returns additional information.
    Returns a tuple containing:
    - Levenshtein distance
    - Similarity percentage
    - Number of matching characters
    - Number of differing characters
    """
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)

    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    
    distance = previous_row[-1]
    total_chars = max(len(s1), len(s2))
    similarity_percentage = (1 - distance / total_chars) * 100
    matches = total_chars - distance
    differences = distance

    return distance, similarity_percentage, matches, differences

# Example usage
file1 = 'TestFiles/file_1.txt'
file2 = 'TestFiles/file_2.txt'

# Convert text to sets and lists of words
words1_set = text_to_set(file1)
words2_set = text_to_set(file2)
words1_list = text_to_list(file1)
words2_list = text_to_list(file2)

# Calculate Jaccard Similarity and additional info
similarity_percentage, common_words_count, unique_words_count = jaccard_similarity(words1_set, words2_set)
print(f"Jaccard Similarity: {similarity_percentage:.2f}%")
print(f"Common words: {common_words_count}")
print(f"Unique words: {unique_words_count}")

# Calculate LCS and additional info
lcs_length, lcs_similarity_percentage, non_lcs_words = lcs(words1_list, words2_list)
print(f"LCS Length: {lcs_length}")
print(f"LCS Similarity: {lcs_similarity_percentage:.2f}%")
print(f"Non-LCS words: {non_lcs_words}")

# Calculate Levenshtein Distance between two strings (join words for sentence-level comparison)
lev_distance, lev_similarity, matches, differences = levenshtein_distance(' '.join(words1_list), ' '.join(words2_list))
print(f"Levenshtein Distance: {lev_distance}")
print(f"Levenshtein Similarity: {lev_similarity:.2f}%")
print(f"Matching characters: {matches}")
print(f"Differing characters: {differences}")
