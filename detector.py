from razdel import tokenize
import math
from collections import Counter

def russian_entropy(text):
    tokens = [token.text.lower() for token in tokenize(text)]
    if not tokens:
        return 0
    counts = Counter(tokens)
    probs = [count / len(tokens) for count in counts.values()]
    return -sum(p * math.log2(p) for p in probs if p > 0)

def is_ai_russian(text):
    entropy = russian_entropy(text)
    return entropy
    #return f"Likely AI (entropy {entropy})" if entropy < 4.0 else "Likely human"  # Tune threshold