from mage_ai.data_preparation.repo_manager import get_repo_path
from mage_ai.io.config import ConfigFileLoader
from mage_ai.io.postgres import Postgres
from os import path
from pandas import DataFrame

if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def transform_in_postgres(*args, **kwargs) -> DataFrame:
    """
    Performs a transformation in Postgres
    """
    config_path = path.join(get_repo_path(), 'io_config.yaml')
    config_profile = 'default'

    execution_datetime = datetime.strptime(str(kwargs['execution_date']), '%Y-%m-%d %H:%M:%S.%f')
    execution_date = execution_datetime.date().strftime('%Y-%m-%d')
    print(f'Loading data for {execution_date}')

    # Specify your SQL transformation query
    query = f"DELETE FROM ethereum.token_transfers where day(block_timestamp) = '{execution_datetime}' "

    # Specify table to sample data from. Use to visualize changes to table.
    sample_table = 'table_to_sample_data_from'
    sample_schema = 'schema_of_table_to_sample'
    sample_size = 10_000

    with Postgres.with_config(ConfigFileLoader(config_path, config_profile)) as loader:
        # Write queries to transform your dataset with
        loader.execute(query)
        loader.commit() # Permanently apply database changes
        return loader.sample(sample_schema, sample_size, sample_table)


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
