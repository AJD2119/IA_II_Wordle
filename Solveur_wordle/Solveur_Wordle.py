import os
from collections import defaultdict, Counter

# ---------- Load wordlist ----------
def load_wordlist():
    file_path = os.path.join(os.path.dirname(__file__), "..", "word_list.txt")
    with open(file_path, "r", encoding="utf-8") as f:
        words = [w.strip().lower() for w in f if len(w.strip()) == 5]
    print(f"Loaded {len(words)} words from word_list.txt")
    return words

# ---------- CSP Wordle solver ----------
class WordleSolver:
    def __init__(self, wordlist):
        self.candidates = list(wordlist)
        self.fixed = {}
        self.forbidden_pos = defaultdict(set)
        self.min_count = defaultdict(int)
        self.max_count = {}

    def apply_feedback(self, guess, fb):
        seen = defaultdict(int)
        for ch, f in zip(guess, fb):
            if f in "GY":
                seen[ch] += 1
        for ch, n in seen.items():
            self.min_count[ch] = max(self.min_count[ch], n)
        for i, (g, f) in enumerate(zip(guess, fb)):
            if f == 'G':
                self.fixed[i] = g
            elif f == 'Y':
                self.forbidden_pos[i].add(g)
            elif f == 'B':
                if self.min_count[g] == 0:
                    self.max_count[g] = 0
                else:
                    self.max_count[g] = self.min_count[g]
                self.forbidden_pos[i].add(g)
        self.filter()

    def matches(self, word):
        for i, l in self.fixed.items():
            if word[i] != l:
                return False
        for i, forb in self.forbidden_pos.items():
            if word[i] in forb:
                return False
        wc = Counter(word)
        for ch, c in self.min_count.items():
            if wc[ch] < c:
                return False
        for ch, c in self.max_count.items():
            if wc[ch] > c:
                return False
        return True

    def filter(self):
        self.candidates = [w for w in self.candidates if self.matches(w)]

    def suggest(self):
        freq = Counter()
        for w in self.candidates:
            for ch in set(w):
                freq[ch] += 1
        scored = []
        for w in self.candidates:
            score = sum(freq[ch] for ch in set(w))
            scored.append((score, w))
        scored.sort(reverse=True)
        return [w for _, w in scored[:5]]
