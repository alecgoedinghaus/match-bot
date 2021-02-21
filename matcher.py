import pandas as pd
from matching import Player
from matching.games import StableRoommates
import random
from math import floor

CATEGORICAL_QUESTIONS = ["What is your idea of a good night out?",
                         "Which of these would be your ideal holiday?",
                         "How would you best describe your character?",
                         "What are the most important characteristics in a partner?",
                         "Are you a fundamentally happy person?"
                         ]


def convert_categorical(question_df):
    dummify = question_df[CATEGORICAL_QUESTIONS]
    q_prefix = ["q" + str(i) for i in range(1, len(CATEGORICAL_QUESTIONS) + 1)]
    dummified = pd.get_dummies(dummify, prefix=q_prefix, prefix_sep="_")
    dummified.set_index(question_df["Discord Username:"], inplace=True)
    return dummified

# takes a matrix of scores, creates a correlation matrix, and returns pair array of matches
def pair(pair_matrix):
    corr_pair = pair_matrix.T.corr()
    named_rankings = {}
    for user_name, correlations in corr_pair.iteritems():
        dropped_self = correlations.drop(labels=[user_name])
        named_rankings[user_name] = dropped_self.sort_values()
    return named_rankings

def solve_stm(named_rankings):
    players = {name: prefs.index for name, prefs in named_rankings.items()}
    game = StableRoommates.create_from_dictionary(players)
    pairs = game.solve()
    return pairs.items()

        