#!/usr/bin/env python3
import json
import os
import random
from fuzzywuzzy import fuzz
import argparse


INCORRECT_ENTRIES_FILEPATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), "incorrect_entries.json")


def parse_args():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='subcommand')

    quiz_parser = subparsers.add_parser('quiz')
    quiz_parser.set_defaults(subcommand='quiz')

    review_parser = subparsers.add_parser('review')
    review_parser.set_defaults(subcommand='review')

    return parser.parse_args()


GREEN = "\033[92m"
RED = "\033[91m"
RESET = "\033[0m"


def save_vocab_entries(filepath: str, entries: dict):
    """
    Save the vocabulary entries to a JSON file.
    :param filepath: The path of the file to save the entries to.
    :param entries: A dictionary containing the vocabulary entries.
    """
    with open(filepath, 'w', encoding='utf-8') as file:
        json.dump(entries, file, ensure_ascii=False)


def quiz(vocab_entries):
    """
    Quiz the user on the given vocabulary entries.
    """
    if not vocab_entries:
        print("No vocabulary entries to quiz on! Exiting.")
        exit(0)

    num_correct = 0
    num_total = 0
    incorrect_entries = []

    while True:
        vocab_entry = random.choice(vocab_entries)
        forms_entry = random.choice(vocab_entry["forms"])

        pinyin = forms_entry["transcriptions"]["pinyin"]
        simplified = vocab_entry["simplified"]

        meanings = forms_entry["meanings"]
        if len(meanings) == 1 and "variant" in meanings[0]:
            continue

        try:
            user_input = input(f"{pinyin}  ({simplified})\n")
        except KeyboardInterrupt:
            correct_ratio = num_correct / num_total
            print(f"Final score: {num_correct}/{num_total}  ({correct_ratio})")

            print(f"Saving incorrect entries to {INCORRECT_ENTRIES_FILEPATH}")
            save_vocab_entries(INCORRECT_ENTRIES_FILEPATH, incorrect_entries)

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
            incorrect_entries.append(vocab_entry)

        print("All translations: ", processed_meanings, "\n")



if __name__ == "__main__":
    args = parse_args()

    dir_name = os.path.abspath(os.path.dirname(__file__))

    vocab_entries_filepath = None
    if args.subcommand == "quiz":
        vocab_entries_filepath = dir_name + os.sep + "complete-hsk-vocabulary/by-level/new/1.json"
    elif args.subcommand == "review":
        vocab_entries_filepath = INCORRECT_ENTRIES_FILEPATH
    else:
        print("Invalid subcommand")
        exit(1)

    with open(vocab_entries_filepath, 'r', encoding='utf-8') as file:
        vocab_entries = json.load(file)
    quiz(vocab_entries)
