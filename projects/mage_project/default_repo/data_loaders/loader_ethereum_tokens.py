from mage_ai.data_preparation.repo_manager import get_repo_path
from mage_ai.io.bigquery import BigQuery
from mage_ai.io.config import ConfigFileLoader
from mage_ai.data_preparation.variable_manager import set_global_variable
from os import path



if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

from default_repo.utils.helpers.date_utils import get_previous_date

@data_loader
def load_data_from_big_query(*args, **kwargs):
    """
    Template for loading data from a BigQuery warehouse.
    Specify your configuration settings in 'io_config.yaml'.

    Docs: https://docs.mage.ai/design/data-loading#bigquery
    """

    is_first_time_load = kwargs['is_tokens_first_run']
    sDate = kwargs['tokens_start_date'] if is_first_time_load=='True' else kwargs['execution_date']
    execution_date = get_previous_date(str(sDate), 1) 
    print(f"Loading data from  '{execution_date}'")
    
    query = f"SELECT* FROM `bigquery-public-data.crypto_ethereum.tokens` where date(block_timestamp) >= '{execution_date}' "
    config_path = path.join(get_repo_path(), 'io_config.yaml')
    config_profile = 'default'
    return BigQuery.with_config(ConfigFileLoader(config_path, config_profile)).load(query)


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
