from mage_ai.orchestration.triggers.api import trigger_pipeline
if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
from datetime import date, datetime, timedelta

@data_loader
def trigger(*args, **kwargs):
    """
    Trigger another pipeline to run.

    Documentation: https://docs.mage.ai/orchestration/triggers/trigger-pipeline
    """
    
    DATE_FORMAT = '%Y-%m-%d'
    start_date = datetime.strptime(kwargs['start_date'], DATE_FORMAT)
    end_date = datetime.strptime(kwargs['end_date'], DATE_FORMAT)
    delta = timedelta(days=1)
    # end_date = datetime.now() - delta
  
    while start_date <= end_date:
        
        execution_date = start_date.strftime(DATE_FORMAT)
        print(f'Starting Backfill for {execution_date}')
        trigger_pipeline(
            'daily_ethereum_token_transfers',        # Required: enter the UUID of the pipeline to trigger
            variables={'is_backfill': True, 'backfill_execution_date':execution_date},           # Optional: runtime variables for the pipeline
            check_status=True,     # Optional: poll and check the status of the triggered pipeline
            error_on_failure=True, # Optional: if triggered pipeline fails, raise an exception
            poll_interval=20,       # Optional: check the status of triggered pipeline every N seconds
            poll_timeout=None,      # Optional: raise an exception after N seconds
            verbose=True,           # Optional: print status of triggered pipeline run
        )
        
        start_date += delta

