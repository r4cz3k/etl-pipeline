import pandas as pd
from src.transform import create_one_column_dataframe, transform_reviews_dataframe

def test_explode_in_transform():
    df = pd.DataFrame({'id': [1], 'images':[['a', 'b', 'c']]})
    result = create_one_column_dataframe(df, 'images') # column_name images or tags

    assert len(result) == 3

def test_rename_and_reorder_in_transform():
    df = pd.DataFrame({'review_message': ['good'], 'id': [1]})
    result = transform_reviews_dataframe(df)

    assert 'product_id' in result.columns
    assert result.columns[0] == 'product_id'