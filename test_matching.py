import from_sheets
import matcher

import pandas as pd


def test_sheet_to_df():
    returned_df = from_sheets.survey_to_df()
    assert all(
        [expected_q in returned_df.columns for expected_q in matcher.CATEGORICAL_QUESTIONS])


TEST_SURVEY_DATA = pd.DataFrame(data={"Timestamp": ["12/31/31", "12/31/31", "12/31/31", "12/31/31"], "ID": ["1", "2", "3", "4"], "Hello": ["not", "a", "valid", "question"], "To be or not to be?": [
                                "Y", "N", "N", "Y"], "Favorite number between 1 and 2?": ["1", "1", "2", "2"]})


def test_pop_categorical():
    global TEST_SURVEY_DATA
    matcher.populate_categorical(TEST_SURVEY_DATA)
    assert matcher.CATEGORICAL_QUESTIONS == [
        "To be or not to be?", "Favorite number between 1 and 2?"]


def test_convert_cat():
    global TEST_SURVEY_DATA
    dummies = matcher.convert_categorical(TEST_SURVEY_DATA)
    assert all([di == i for di, i in zip(dummies.index, ["1", "2", "3", "4"])])
