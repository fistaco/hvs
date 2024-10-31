#!/usr/bin/env python3
import json
import os
import random
from fuzzywuzzy import fuzz


GREEN = "\033[92m"
RED = "\033[91m"
RESET = "\033[0m"


if __name__ == "__main__":
    hsk_vocab_filepath = os.path.abspath(os.path.dirname(__file__)) + os.sep + "complete-hsk-vocabulary/by-level/new/1.json"
    with open(hsk_vocab_filepath, 'r', encoding='utf-8') as file:
        vocab_items = json.load(file)

    num_correct = 0
    num_total = 0

    while True:
        vocab_entry = random.choice(vocab_items)
        forms_entry = random.choice(vocab_entry["forms"])

        pinyin = forms_entry["transcriptions"]["pinyin"]
        simplified = vocab_entry["simplified"]

        meanings = forms_entry["meanings"]
        if len(meanings) == 0 and "variant" in meanings[0]:
            continue

        try:
            user_input = input(f"{pinyin}  ({simplified})\n")
        except KeyboardInterrupt:
            correct_ratio = num_correct / num_total
            print(f"Final score: {num_correct}/{num_total}  ({correct_ratio})")

            print("Exiting.")
            exit(0)

        # TODO: Just handle this in preprocessing
        processed_meanings = []
        for meaning in meanings:
            submeanings = meaning.split(";")
            for submeaning in submeanings:
                processed_meanings.append(submeaning)

        max_score = max(
            [fuzz.ratio(user_input, meaning) for meaning in processed_meanings]
        )

        num_total += 1
        if max_score > 65:
            print(f"{GREEN}Correct{RESET}")
            num_correct += 1
        else:
            print(f"{RED}False{RESET} (similarity score = {max_score})")

        print("All translations: ", processed_meanings, "\n")
