import os
import requests
import pandas as pd
from bs4 import BeautifulSoup


class Questions:
    def __init__(self, url):
        self.url = url

    def find_questions(self):
        with requests.get(self.url, verify=False) as f:
            soup = BeautifulSoup(f.content, "html.parser")

        text = soup.find_all("li", {"data-type": "question"})

        # Find the questions
        questions = []
        for i in text:
            question = i.find("div", {"class": "tile"})
            questions.append(question.find("p").text.strip())

        all_choices = []
        for i in text:
            # Choice is a text
            choices = [j.text.strip() for j in i.find_all("span")]
            if len(choices) == 0:
                # Choice is a text with picture
                choices = [j.text.strip() for j in i.find_all("div", {"class":
                "subbuzz-quiz__answer__text bold xs-text-4 md-text-3"})]
                if len(choices) == 0:
                    # Choice is a picture
                    # TODO: Find a way to make sure there's 6 or generalize
                    # this...
                    choices = [i+1 for i in range(6)]
            all_choices.append(choices)
        return dict(zip(questions, all_choices))

    def find_combinations(self, arr):
        n = len(arr)
        indices = [0 for i in range(n)]
        combinations = []
        while True:
            # current combination
            combination = []
            for i in range(n):
                combination.append(arr[i][indices[i]])
            combinations.append(combination)

            next = n - 1
            while (next >= 0 and
                   (indices[next] + 1 >= len(arr[next]))):
                next -= 1

            # no combinations left
            if (next < 0):
                return combinations

            indices[next] += 1
            for i in range(next + 1, n):
                indices[i] = 0

    def find_all_possible_combinations(self):
        questions = self.find_questions()

        # Save the questions as a csv
        if "output" not in os.listdir():
            os.system("mkdir output")
        questions = pd.DataFrame(questions)
        questions.to_csv("output/questions.csv", index=False)

   
        all_options = []
        reference = {}
        for i in range(len(questions.columns)):
            options = []
            for j in range(len(questions.index) // 2):
                for k in range(2):
                    # For each choice
                    try:
                        question = '//*[@id="mod-quiz-personality-1"]/ol/li[{0}]/fieldset/div/div[{1}]/div[{2}]'.format(i+1, j+1, k+1)
                        options.append(question)
                        reference[question] = questions.iloc[2*j + k, i]
                    except:
                        # Incase the number of grids is odd
                        pass
            all_options.append(options)

        combinations = self.find_combinations(all_options)
        text_combinations = [[reference[j] for j in i] for i in combinations]

        print("Going through {0} combinations".format(len(text_combinations)))
        return combinations, text_combinations

