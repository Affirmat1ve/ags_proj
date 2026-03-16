from razdel import tokenize
import math
from collections import Counter
from typing import List

def russian_entropy(text: str) -> float:
    """
    Рассчитывает энтропию Шеннона для русского текста.

    Используется для оценки разнообразия лексики: чем выше значение,
    тем более разнообразен текст. Низкая энтропия может указывать
    на потенциально AI-генерированный контент.

    :param text: входной текст на русском языке.
    :return: значение энтропии в битах на токен (0.0 для пустого текста).
    """
    tokens: List[str] = [token.text.lower() for token in tokenize(text)]
    if not tokens:
        return 0
    counts: Counter = Counter(tokens)
    probs = [count / len(tokens) for count in counts.values()]
    return -sum(p * math.log2(p) for p in probs if p > 0)

def is_ai_russian(text):
    """
    Анализирует русский текст на предмет вероятной AI-генерации.

    Использует энтропийный анализ как эвристический метод:
    тексты с низкой энтропией часто имеют признаки искусственной
    генерации (повторяющиеся паттерны, предсказуемая структура).

    :param text: текст для анализа на русском языке.
    :return: значение энтропии текста.
    
    Интерпретация результата:
        - < 4.0 : вероятно AI-генерированный текст
        - >= 4.0: вероятно человеческий текст
        
    Примечание: порог 4.0 является эмпирическим и может
    требовать калибровки для конкретных типов контента.
    """
    entropy = russian_entropy(text)
    return entropy
    #return f"Likely AI (entropy {entropy})" if entropy < 4.0 else "Likely human"  # Tune threshold