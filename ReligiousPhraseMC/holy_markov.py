import re
import random


class Markov(object):
    def __init__(self, open_file):
        self.cache = {}
        self.open_file = open_file
        self.words = self.file_to_words()
        self.word_size = len(self.words)
        self.database()

    def file_to_words(self):
        self.open_file.seek(0)
        data = self.open_file.read()
        words = data.split()
        return words

    def triples(self):
        """ Generates triples from the given data string. So if our string were
                "What a lovely day", we'd generate (What, a, lovely) and then
                (a, lovely, day).
        """

        if len(self.words) < 3:
            return

        for i in range(len(self.words) - 2):
            yield (self.words[i], self.words[i + 1], self.words[i + 2])

    def database(self):
        for w1, w2, w3 in self.triples():
            key = (w1, w2)
            if key in self.cache:
                self.cache[key].append(w3)
            else:
                self.cache[key] = [w3]

    def generate_markov_text(self, size=25):
        seed = random.randint(0, self.word_size - 3)
        seed_word, next_word = self.words[seed], self.words[seed + 1]
        w1, w2 = seed_word, next_word
        gen_words = []
        for i in range(size):
            gen_words.append(w1)
            w1, w2 = w2, random.choice(self.cache[(w1, w2)])
        gen_words.append(w2)

        return ' '.join(gen_words)


class OldTestaPassagesMarkov(Markov):
    passage_num_pattern = re.compile(r'\d+:\d+')
    passage_numbers = set()

    def __init__(self, filename='sources/old testament.txt'):
        super().__init__(open_file=open(filename))
    
    def generate_markov_text(self, seed_word='', min_words=25):
        
        # Process a user given seed_word
        seed_word_locations = [idx for idx, word in enumerate(self.words)
                                    if word.lower() == seed_word.lower()]
            
        if seed_word_locations:
            seed = random.choice(seed_word_locations)
        else:
            print(seed_word + ' is not in Old Testament')
            seed = random.randint(0, self.word_size - 3)
            
        w1, w2 = self.words[seed], self.words[seed + 1]
        gen_words = [w1, w2]
        # go until we have enough words and end in a period
        while w2[-1] != '.' or len(gen_words) < min_words:
            w1, w2 = w2, random.choice(self.cache[(w1, w2)])
            if self.passage_num_pattern.findall(w2):
                # Avoid adding passage numbers to the middle of the passage.
                # Also end a sentence when a passage number would have gone in.
                new_w1 = w1.replace(':', '.').replace(';', '.')
                gen_words[-1] = new_w1
            else:                
                gen_words.append(w2)

        return ' '.join(gen_words)

    def twitter_message(self, line_length=140):
        if not self.passage_numbers:
            for word in self.words:
                found_pattern = self.passage_num_pattern.findall(word)
                if found_pattern:
                    self.passage_numbers.add(found_pattern[0])

        passage_num = random.sample(self.passage_numbers, 1)[0]
        message = ''
        min_words = 15
        while len(message) > line_length or len(message) < 1:
            message = self.generate_markov_text(seed_word=passage_num, min_words=min_words)
            message = message.replace(passage_num+' ', '')

        return message


if __name__ == '__main__':
    bible_gen = OldTestaPassagesMarkov(open('sources/Old testament.txt'))
    for _ in range(10):
        print(bible_gen.twitter_message())