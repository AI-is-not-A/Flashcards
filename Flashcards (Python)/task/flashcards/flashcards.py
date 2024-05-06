import io
import os
import random
import argparse

parser = argparse.ArgumentParser(
    prog="Flashcards Maker",
    description="Memorize everything!"
)
parser.add_argument('-imp', '--import_from')
parser.add_argument('-exp', '--export_to')

args = parser.parse_args()

log = io.StringIO()


class Flashcards:

    def __init__(self):
        self.cards = []

    def check_if_card_exists(self, term):
        for card in self.cards:
            if card.term == term:
                return card

    def check_if_definition_exists(self, definition):
        for card in self.cards:
            if card.definition == definition:
                return card

    def get_cards_with_most_mistakes(self):
        max_mistakes = 0
        for card in self.cards:
            if card.mistakes > max_mistakes:
                max_mistakes = card.mistakes
        if max_mistakes == 0:
            return []
        cards = []
        for card in self.cards:
            if card.mistakes == max_mistakes:
                cards.append(card)
        return cards

    def print_log(self, message):
        print(message)
        log.write(message + "\n")

    def add(self):
        self.print_log("The card:")
        while True:
            term = input()
            log.write(term + "\n")
            if self.check_if_card_exists(term):
                self.print_log(f'The card "{term}" already exists. Try again:')
                continue
            break

        self.print_log("The definition of the card:")
        while True:
            definition = input()
            log.write(definition + "\n")
            if self.check_if_definition_exists(definition):
                self.print_log(f'The definition "{definition}" already exists. Try again:')
                continue
            break

        new_card = Card(term, definition, 0)
        self.cards.append(new_card)
        self.print_log(f'The pair ("{term}":"{definition}") has been added.\n')

    def add_cards(self):
        self.print_log("Input the number of cards:")
        n_cards = int(input())
        log.write(str(n_cards) + "\n")
        for i in range(1, n_cards + 1):

            self.print_log(f"The term for card #{i}:")
            while True:
                term = input()
                log.write(term + "\n")
                if self.check_if_card_exists(term):
                    self.print_log(f'The term "{term}" already exists. Try again:')
                    continue
                break

            self.print_log(f"The definition for card #{i}:")
            while True:
                definition = input()
                log.write(definition + "\n")
                if self.check_if_definition_exists(definition):
                    self.print_log(f'The definition "{definition}" already exists. Try again:')
                    continue
                break

            new_card = Card(term, definition, 0)
            self.cards.append(new_card)

    def remove_card(self):
        self.print_log("Which card?")
        term = input()
        log.write(term + "\n")
        card = self.check_if_card_exists(term)
        if card:
            self.cards.remove(card)
            self.print_log("The card has been removed\n")
        else:
            self.print_log(f'Can\'t remove "{term}": there is no such card\n')

    def import_cards(self, file_name=""):
        if file_name == "":
            self.print_log("File name:")
            file_name = input()
        log.write(file_name + "\n")
        if os.path.exists(file_name):
            try:
                with open(file_name, "r") as file:
                    lines = file.readlines()
                    for line in lines:
                        term, definition, mistakes = line.strip().split(":")
                        card_with_same_term = self.check_if_card_exists(term)
                        if card_with_same_term:
                            card_with_same_term.definition = definition
                            card_with_same_term.mistakes = int(mistakes)
                        else:
                            self.cards.append(Card(term, definition, int(mistakes)))
                    self.print_log(f"{len(lines)} cards have been loaded.\n")
            except Exception as e:
                self.print_log(e)
        else:
            self.print_log("File not found.\n")

    def export_cards(self, file_name=""):
        if file_name == "":
            self.print_log("File name:")
            file_name = input()
        log.write(file_name + "\n")
        try:
            with open(file_name, "w") as file:
                for card in self.cards:
                    file.write(f"{card.term}:{card.definition}:{card.mistakes}\n")
                self.print_log(f"{len(self.cards)} cards have been saved.\n")
        except Exception as e:
            self.print_log(e)

    def ask(self):
        if len(self.cards) == 0:
            self.print_log("There is no card\n")
            return
        self.print_log("How many times to ask?")
        n_ask = int(input())
        log.write(str(n_ask) + "\n")
        for i in range(n_ask):
            random_card = random.choice(self.cards)
            self.print_log(f'Print the definition of "{random_card.term}":')
            response = input()
            log.write(response + "\n")
            if random_card.check_response(response):
                self.print_log("Correct!")
            else:
                random_card.mistakes += 1
                card_with_same_response = self.check_if_definition_exists(response)
                if card_with_same_response:
                    self.print_log(f'Wrong. The right answer is "{random_card.definition}", '
                                   f'but your definition is correct for "{card_with_same_response.term}".')
                else:
                    self.print_log(f'Wrong. The right answer is "{random_card.definition}".')
        self.print_log("\n")

    def log(self):
        self.print_log("File name:")
        file_name = input()
        log.write(file_name + "\n")
        try:
            with open(file_name, "w") as file:
                file.write(log.getvalue())
            self.print_log(f"The log has been saved.\n")
        except Exception as e:
            self.print_log(e)

    def hardest_card(self):
        cards = self.get_cards_with_most_mistakes()
        if len(cards) == 0:
            self.print_log("There are no cards with errors.\n")
        elif len(cards) == 1:
            self.print_log(
                f'The hardest card is "{cards[0].term}". You have {cards[0].mistakes} errors answering it.\n')
        else:
            message = f'The hardest cards are "{cards[0].term}'
            for i in range(1, len(cards)):
                message += f', "{cards[i].term}"'
            self.print_log(message + ".\n")

    def reset_stats(self):
        for card in self.cards:
            card.mistakes = 0
        self.print_log("Card statistics have been reset.\n")

    def start(self):
        if args.import_from is not None:
            self.import_cards(args.import_from)

        while True:
            self.print_log(
                "Input the action (add, remove, import, export, ask, exit, log, hardest card, reset stats):\n")
            command = input()
            log.write(command + "\n")
            if command == "add":
                self.add()
            if command == "remove":
                self.remove_card()
            if command == "import":
                self.import_cards()
            if command == "export":
                self.export_cards()
            if command == "ask":
                self.ask()
            if command == "exit":
                if args.export_to is not None:
                    self.export_cards(args.export_to)
                self.print_log("Bye bye!")
                exit()
            if command == "log":
                self.log()
            if command == "hardest card":
                self.hardest_card()
            if command == "reset stats":
                self.reset_stats()


class Card:

    def __init__(self, term, definition, mistakes):
        self.term = term
        self.definition = definition
        self.mistakes = mistakes

    def __str__(self):
        return f'Card:\n{self.term}\nDefinition:\n{self.definition}'

    def check_response(self, response):
        if response == self.definition:
            return True


def main():
    flashcards = Flashcards()
    flashcards.start()


if __name__ == "__main__":
    main()
