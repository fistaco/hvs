#!/usr/bin/env python3
import json
import random
from fuzzywuzzy import fuzz


GREEN = "\033[92m"
RED = "\033[91m"
RESET = "\033[0m"

# Terms that are often used in hanzi definitions that are not a useful translation for studying
INDIRECT_DEFINITION_TERMS = [
    "variant of",
    "surname"
]


def contains_indirect_def(text):
    """Returns whether the given `text` contains a term indicating an indirect definition."""
    return any(term in text for term in INDIRECT_DEFINITION_TERMS)


def filter_meanings(meanings):
    """Filters meanings that are not direct definitions of a word."""
    return [m for m in meanings if not contains_indirect_def(m)]


def normalize_meanings(meanings):
    """Normalizes meanings to a list of simple single terms."""
    normalized = []
    for meaning in meanings:
        # Split by semicolons and strip whitespace
        parts = [part.strip() for part in meaning.split(';')]
        normalized.extend(parts)
    return normalized


if __name__ == "__main__":
    with open('complete-hsk-vocabulary/by-level/new/1.json', 'r', encoding='utf-8') as file:
        vocab_items = json.load(file)

    while True:
        vocab_entry = random.choice(vocab_items)
        forms_entry = random.choice(vocab_entry["forms"])
        pinyin = forms_entry["transcriptions"]["pinyin"]
        simplified = vocab_entry["simplified"]

        # Only use vocab entries with direct definitions
        all_meanings = forms_entry["meanings"]
        filtered_meanings = filter_meanings(all_meanings)
        processed_meanings = normalize_meanings(filtered_meanings)
        if not filtered_meanings:
            continue

        try:
            user_input = input(f"{pinyin}  ({simplified})\n")
        except KeyboardInterrupt:
            print("Exiting.")
            exit(0)

        max_score = max(
            [fuzz.ratio(user_input, meaning) for meaning in processed_meanings]
        )

        if max_score > 65:
            print(f"{GREEN}Correct{RESET}")
        else:
            print(f"{RED}False{RESET} (similarity score = {max_score})")

        print("All translations: ", all_meanings, "\n")
