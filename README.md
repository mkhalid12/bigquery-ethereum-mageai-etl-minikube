# BigQuery-Ethereum-Mageai-ETL-Minikube

In this project I created end-to-end pipeline to extract Ethereum `tokens` and `token-transfers` from public dataset available in Google [BigQuery Ethereum](https://cloud.google.com/blog/products/data-analytics/ethereum-bigquery-public-dataset-smart-contract-analytics]). This pipeline is completely developed in Mageai and deployed via locally installed minikube.


### Mage.ai

[Mage.ai](https://www.mage.ai/) is modern data integration with transformation and pipeline-orchestration features. It has integrated all features required for pipeline to developed, test, deploy and scheduling. That's why i give it a try to test and develop small pipeline integration.

##### NOTE: This whole project is developed and deployed while considering local resources 

### Architecture

The architecture comprised of many components as shown in following diagram:

![architecture.jpg](images%2Farchitecture.jpg)

Following tools I used and deployed it via Helm Charts to minikube 
- GoogleBiqQuery: Data Source
- MageAi: For Data Integration transformation and scheduling the pipeline
- Postgres: For Data Storage
- Serving Layer: The implementation of Serving layer is part of future todos. It is not yet available in this repo at the moment.


MageAi Pipelines reads data from Good BigQuery public dataset `bigquery-public-data.crypto_ethereum` and store data to Postgresql database of `ethereum` schema. 

### Pre-Requesities

1. To run this project, the expectation is your local system has `docker` and `make` installed.
2. Google BigQuery Setup: You need to have GCP (Google Cloud Platform) and you need to create a  Service Account with access to `BigQuery Data Viewer`, `BigQuery Job User` and `BigQuery Session User`. Once you created a service account you need to download the GCP BIgQuery authentication key in json format. 


### Setup Infrastructure

In order to start this project we need to install  `minikube`, `helm` and `kubectl` and ofcourse `docker`. As `minikube` will run as a docker container.
To begin with i have created make recipe for it `setup-k8`.
Before running this recipe you need to go to [Makefile](Makefile)
 and update the `PROJECT_DIRECTORY` variable with your Project Directory full path.

```
1. PROJECT_DIRECTORY={full/path/to/your/project/directory}/mage-ai/projects/
2. Replace Google BigQuery credentials secrets/gcp_bg_user.json with you created 
```

Now you are all set to run this following command.

```
3. make setup-k8
```


This will start your minikube docker conatiner which mount your projects 'projects/' directory and save Mageai Pipeline code.


Now start the `mageai` and `postgres` services via helm chart run this following command.

```
4. make kick-start
```
It is deployed inside the `mk-mageai` namespace inside the kubernetes. The namespace name is configurable in [Makefile](Makefile)

As soon as you see the kick-start the service and pods starts running via kubectl command we need to forward port to our local. You should see the pods status running as follows

```
5. kubectl get pods  -n mk-mageai

NAME                      READY   STATUS    RESTARTS   AGE
mageai-5f588d564c-7xqd9   1/1     Running   0          3h35m
postgresql-0              1/1     Running   0          3h33m
```
Now we need to `forward-port` from minikube pods to our local system.
```
6. make forward-port
```

Once your pods visible to your local system now you can browse mage.ai dashboard using this link http://localhost:6789/
You should see this Mage-Ai Dashboard with 3 pre-defined pipeline which we mount via our current `project/` directory to `mageai` helm chart container. 
Until now you should see this MageAi dashboard with pre-configured Pipelines. If not please feel free to drop a message, as it is important to move forward.

![mageai-dashbaord.png](images%2Fmageai-dashbaord.png)

### Mageai-ETL-Pipelines 
In this section, We discussed about each pipeline in details. By default, all pipeline are set to `inactive`. You can change it to `active` in pipeline's trigger.yaml file. For example for daily_ethereum_tokens pipeline it is in  [triggers.yaml](projects%2Fmage_project%2Fdefault_repo%2Fpipelines%2Fdaily_ethereum_tokens%2Ftriggers.yaml)
In Mageai dashboard there are 3 pipeline
1. **Backfill Tokens Transfers**: backfill_daily_ethereum_token_transfers 
2. **Token Transfers** : daily_ethereum_token_transfers
3. **Tokens**: daily_ethereum_tokens
 
The datasource extraction is developed using `Inceremental Loading`. Each pipeline use pre-define Global Variable  `execution_date` available in MageAI and extract the data from bigquery `tokens`  using where the condition is `execution_date-1`. In short always extract data from yesterday.

### Tokens Pipeline:

![pipeline-tokens.png](images%2Fpipeline-tokens.png)


#### Backfill:

As the data in `tokens` source table is not so big it only contains ~34MB of data until now with 214,759 number of records. The pipeline is easy to extract the whole table in one go. 
Using MageAI Global Variables `is_tokens_first_run` variable defined in  [metadata.yaml](projects%2Fmage_project%2Fdefault_repo%2Fpipelines%2Fdaily_ethereum_tokens%2Fmetadata.yaml) defined in  `pipelines/daily_ethereum_tokens`. 
This variable check make sure if the pipeline is running for the first time it load data since the beginning otherwise it uses `execution_date` for data extraction. 

#### Trigger:
The Tokens pipeline triggers automatically everyday. It's configuration defined in [triggers.yaml](projects%2Fmage_project%2Fdefault_repo%2Fpipelines%2Fdaily_ethereum_tokens%2Ftriggers.yaml)


### Token Transfers Pipeline:

This datasource has large amount of data. Daily ~1.3 million of recorded ingested to this BigQuery dataset. Considering local-resource, the complete data extract from this data-source is difficult to extract as a whole. That's why again Incremental approach is considered to load data for yesterday only for each execution. 

![pipeline-token-transfers.png](images%2Fpipeline-token-transfers.png)

#### Backfill:
The Backfill of token-transfer was one of the most challenging part to integrate it using limited local resources. In my current resources i have capacity of 4 CPU and 8GB RAM.   
First I try with MageAi Backfill feature, but this will run the backfill for each runs or execution_date in parallel and hence it crashes the minikube container because of out of resources. This approach is good for production backfill when we can scale dynamically on demand.
Hence, to extract data for each date from `token_transfers` took ~4-5 mins and utilize all available container resources. The backfill is only possible to run sequentially from state_date to end_date one by one.

This sequential execution is developed as a [MAGEAI Trigger Pipeline](https://docs.mage.ai/orchestration/triggers/trigger-pipeline) in [backfill_daily_ethereum_token_transfers](projects%2Fmage_project%2Fdefault_repo%2Fpipelines%2Fbackfill_daily_ethereum_token_transfers) 

#### Triggers:
The Tokens pipeline triggers automatically everyday. It's configuration defined in [triggers.yaml](projects%2Fmage_project%2Fdefault_repo%2Fpipelines%2Fdaily_ethereum_token_transfers%2Ftriggers.yaml)
![token-transfers-trigger.jpg](images%2Ftoken-transfers-trigger.jpg)


### Extras:

#### MageAi Helm-Chart Contribution:
I also made a small contribution to MageAi Helm chart https://github.com/mkhalid12/helm-charts to mount Google Secretes as Kubernetes Secrets to follow good practise to save secrets. That's why I used my own mageai helm-chart repo available here. 
The commit for this link is [here](https://github.com/mage-ai/helm-charts/commit/4dbbb6e78342c142991c3afa0aa887edeba3294d?diff=split)

#### Future Todos:
1. Add Serving Layer for data visualization
2. Add transformation block for token-transfers pipeline












