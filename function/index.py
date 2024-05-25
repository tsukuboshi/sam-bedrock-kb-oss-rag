import logging
import time
from typing import Any, Dict

import boto3
import cfnresponse
from opensearchpy import AWSV4SignerAuth, OpenSearch, RequestsHttpConnection

logger = logging.getLogger()


def lambda_handler(event: Dict[str, Any], context: Any) -> None:
    request_type = event["RequestType"]
    logger.info(f"RequestType: {request_type}")

    try:
        if request_type == "Create":
            # Get the parameters from the event
            region = event["ResourceProperties"]["Region"]
            dimension = event["ResourceProperties"]["Dimension"]
            colection_id = event["ResourceProperties"]["CollectionId"]
            index_name = event["ResourceProperties"]["IndexName"]
            vector_field = event["ResourceProperties"]["VectorField"]
            mapping_text = event["ResourceProperties"]["MappingText"]
            mapping_metadata = event["ResourceProperties"]["MappingMetadata"]

            # Create OpenSearch client
            service = "aoss"
            host = colection_id + "." + region + "." + service + "." + "amazonaws.com"
            credentials = boto3.Session().get_credentials()
            auth = AWSV4SignerAuth(credentials, region, service)

            client = OpenSearch(
                hosts=[{"host": host, "port": 443}],
                http_auth=auth,
                use_ssl=True,
                verify_certs=True,
                connection_class=RequestsHttpConnection,
                pool_maxsize=20,
            )

            # Create OpenSearch Index (Wait for 30 seconds for index creation)
            index_body = {
                "settings": {
                    "index": {
                        "number_of_shards": "2",
                        "number_of_replicas": "0",
                        "knn": "true",
                    }
                },
                "mappings": {
                    "properties": {
                        vector_field: {
                            "type": "knn_vector",
                            "dimension": dimension,
                            "method": {
                                "name": "hnsw",
                                "space_type": "l2",
                                "engine": "faiss",
                                "parameters": {},
                            },
                        },
                        mapping_text: {
                            "type": "text",
                        },
                        mapping_metadata: {"type": "text", "index": "false"},
                    }
                },
            }

            response = client.indices.create(
                index_name,
                body=index_body,
            )

            logger.info(f"Index creating: {response}")
            time.sleep(30)

            cfnresponse.send(event, context, cfnresponse.SUCCESS, {})
        if request_type == "Update":
            cfnresponse.send(event, context, cfnresponse.SUCCESS, {})
        if request_type == "Delete":
            cfnresponse.send(event, context, cfnresponse.SUCCESS, {})
    except Exception as e:
        cfnresponse.send(event, context, cfnresponse.FAILED, {"Message": str(e)})
