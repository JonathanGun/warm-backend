from typing import List, Optional, Dict, Tuple
from dataclasses import dataclass
from collections import defaultdict
import csv
from itertools import chain

@dataclass
class Category:
    name: str
    symptoms: List[Tuple[int, str]]


class Classifier:
    def __init__(self, rule_file: str = "rules.csv"):
        self.categories = []
        categories_dict = defaultdict(list)
        with open(rule_file, 'r') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for i, row in enumerate(csv_reader):
                if i == 0:
                    continue
                categories_dict[row[1]].append((row[0], row[2]))
        for name, symptoms in categories_dict.items():
            self.categories.append(Category(name, symptoms))

    def classify(self, symptoms_scores: Dict[str, int]):
        scores = defaultdict(int)
        for s_idx, s_score in symptoms_scores.items():
            category = self.get_category_by_symptom_index(s_idx)
            if category is None:
                continue
            scores[category.name] += s_score
        max_score = -1
        max_name = ''
        for name, score in scores.items():
            if score > max_score and name != 'General':
                max_name = name
                max_score = score
        return max_name

    def get_classes(self) -> List[str]:
        return list(map(lambda c: c.name, self.categories))

    def get_all_symptoms(self) -> List[str]:
        return list(chain.from_iterable(map(lambda c: c.symptoms, self.categories)))

    def get_symptoms(self, category_name: str) -> Optional[List[str]]:
        category = next(filter(lambda c: c.name == category_name, self.categories), None)
        if category is None:
            return None
        return category.symptoms

    def get_category_by_symptom_index(self, s_idx: str):
        for category in self.categories:
            for symptom in category.symptoms:
                if s_idx == symptom[0]:
                    return category
        return None
