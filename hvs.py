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

    while True:
        vocab_entry = random.choice(vocab_items)
        forms_entry = random.choice(vocab_entry["forms"])
        pinyin = forms_entry["transcriptions"]["pinyin"]
        simplified = vocab_entry["simplified"]

        try:
            user_input = input(f"{pinyin}  ({simplified})\n")
        except KeyboardInterrupt:
            print("Exiting.")
            exit(0)

        max_score = max(
            [fuzz.ratio(user_input, meaning) for meaning in forms_entry["meanings"]]
        )

        if max_score > 65:
            print(f"{GREEN}Correct{RESET}")
        else:
            print(f"{RED}False{RESET} (similarity score = {max_score})")

        print("All translations: ", forms_entry["meanings"], "\n")
