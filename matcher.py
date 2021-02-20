import pandas as pd

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
