import from_sheets
import matcher

import pandas as pd


def test_sheet_to_df():
    returned_df = from_sheets.survey_to_df()
    assert all(
        [expected_q in returned_df.columns for expected_q in matcher.CATEGORICAL_QUESTIONS])
