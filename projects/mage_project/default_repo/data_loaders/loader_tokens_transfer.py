from mage_ai.data_preparation.repo_manager import get_repo_path
from mage_ai.io.bigquery import BigQuery
from mage_ai.io.config import ConfigFileLoader
from os import path
from datetime import datetime
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
    is_backfill = kwargs.get('is_backfill')
    # is_first_time_load = kwargs['is_token_transfers_first_run']
    # sDate = kwargs['tokens_transfers_start_date'] if is_first_time_load=='True' else kwargs['execution_date']
    
    # execution_date = kwargs['backfill_execution_date'] if is_backfill == True else get_previous_date(str(sDate), 1) 

    execution_date = kwargs['backfill_execution_date'] if is_backfill is not None else get_previous_date(str(kwargs['execution_date']), 1)

    print(f"Loading data token_transfers for '{execution_date}'")

    query = f"""SELECT * FROM `bigquery-public-data.crypto_ethereum.token_transfers` WHERE DATE(block_timestamp) = "{execution_date}" """
    # query = f"""SELECT * FROM `bigquery-public-data.crypto_ethereum.token_transfers` WHERE DATE(block_timestamp) = '2023-04-01' """
   
    config_path = path.join(get_repo_path(), 'io_config.yaml')
    config_profile = 'default'

    return BigQuery.with_config(ConfigFileLoader(config_path, config_profile)).load(query)


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.🍩🍩
    """
    assert output is not None, 'The output is undefined'
