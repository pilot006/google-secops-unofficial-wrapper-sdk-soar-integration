from SiemplifyAction import SiemplifyAction
from SiemplifyUtils import unix_now, convert_unixtime_to_datetime, output_handler
from ScriptResult import EXECUTION_STATE_COMPLETED, EXECUTION_STATE_FAILED,EXECUTION_STATE_TIMEDOUT
from secops import SecOpsClient
from datetime import datetime, timedelta, timezone
import json
from dataclasses import dataclass, asdict


@output_handler
def main():
    siemplify = SiemplifyAction()

    sa_key = siemplify.extract_configuration_param('Integration',"JSON Service Account Key")
    instance_id = siemplify.extract_configuration_param('Integration',"SecOps Customer ID")
    project_id = siemplify.extract_configuration_param('Integration',"SecOps Project ID")
    secops_region = siemplify.extract_configuration_param('Integration',"SecOps Region")
    sa_key = json.loads(sa_key)

    entity_id = siemplify.extract_action_param("Entity", print_value=True)

    # Initialize with service account info
    client = SecOpsClient(service_account_info=sa_key)
    # Initialize Chronicle client
    chronicle = client.chronicle(
        customer_id=instance_id,
        project_id=project_id,
        region=secops_region
    )

    # Set time range for queries
    end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(days=90)
    ip_summary = chronicle.summarize_entity(
        value=entity_id,
        start_time=start_time,
        end_time=end_time
    )
    ent_obj = json.dumps(asdict(ip_summary), default=str)
    summary = json.loads(ent_obj)
    siemplify.result.add_result_json(summary)
    siemplify.LOGGER.info(ent_obj)    

    status = EXECUTION_STATE_COMPLETED
    output_message = "Enriched entity"
    result_value = True

    siemplify.end(output_message, result_value, status)

if __name__ == "__main__":
    main()
