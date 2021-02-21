import pandas as pd
from matching.games import StableRoommates

CATEGORICAL_QUESTIONS = []


def populate_categorical(question_df):
    global CATEGORICAL_QUESTIONS
    questions = list(question_df.columns.values)
    for question in questions[2:]:
        if(question[-1:] == '?'):
            CATEGORICAL_QUESTIONS.append(question)
    return


def convert_categorical(question_df):
    dummify = question_df[CATEGORICAL_QUESTIONS]
    q_prefix = ["q" + str(i) for i in range(1, len(CATEGORICAL_QUESTIONS) + 1)]
    dummified = pd.get_dummies(dummify, prefix=q_prefix, prefix_sep="_")
    dummified.set_index(question_df.iloc[:, 1], inplace=True)
    return dummified


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
