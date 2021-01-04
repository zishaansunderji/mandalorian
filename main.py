from questions import Questions
from quiz import Quiz
import pandas as pd
import numpy as np

def main():
    url = "https://www.buzzfeed.com/alliehayes/the-mandalorian-character-quiz"
    combinations, combinations_in_text = Questions(url).find_all_possible_combinations()

    q = pd.read_csv("output/questions.csv")
    ref = dict(zip([i for i in range(len(q.columns))], q.columns))

    output = {i: [] for i in q.columns}
    output["Results"] = []

    count = 0
    i = 0
    cache = []
    while (count < len(combinations)):
        i = int(np.random.random() * len(combinations))
        while (i in cache):
            i = int(np.random.random() * len(combinations))
        result = Quiz(url, combinations[i]).solve()

        print(result)


if __name__ == '__main__':
    main()
