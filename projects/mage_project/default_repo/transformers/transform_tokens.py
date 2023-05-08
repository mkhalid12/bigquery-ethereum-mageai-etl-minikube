from mage_ai.data_cleaner.transformer_actions.base import BaseAction
from mage_ai.data_cleaner.transformer_actions.constants import ActionType, Axis
from mage_ai.data_cleaner.transformer_actions.utils import build_transformer_action
from pandas import DataFrame
from typing import List
if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


def fill_missing_values(df: DataFrame, cols:List[str]) -> DataFrame:
    for col in cols:
        df[col] = df[col].replace('None', 'NULL', inplace=True)

    return df


@transformer
def execute_transformer_action(df: DataFrame, *args, **kwargs) -> DataFrame:
    """
    Execute Transformer Action: ActionType.FILTER

    Docs: https://docs.mage.ai/guides/transformer-blocks#filter
    """
    
    schema = {
        'address'   : 'str',
        'symbol'    : 'str',
        'name'      : 'str',
        'decimals'  : 'str',          
        'total_supply': 'str',
        'block_number': 'int',
        'block_hash':'str'
    }

    df = df.astype(schema)
    action = build_transformer_action(
        df,
        action_type=ActionType.FILTER,
        axis=Axis.ROW,
        action_code="(name != null)",  # Specify your filtering code here
    )

    df_transformed = fill_missing_values(df, ['decimals','total_supply'])
    return  BaseAction(action).execute(df_transformed) 



@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
