from SiemplifyAction import SiemplifyAction
from SiemplifyUtils import unix_now, convert_unixtime_to_datetime, output_handler
from ScriptResult import EXECUTION_STATE_COMPLETED, EXECUTION_STATE_FAILED,EXECUTION_STATE_TIMEDOUT
from secops import SecOpsClient
import json


@output_handler
def main():
    siemplify = SiemplifyAction()

    sa_key = siemplify.extract_configuration_param('Integration',"JSON Service Account Key")
    instance_id = siemplify.extract_configuration_param('Integration',"SecOps Customer ID")
    project_id = siemplify.extract_configuration_param('Integration',"SecOps Project ID")
    secops_region = siemplify.extract_configuration_param('Integration',"SecOps Region")
    sa_key = json.loads(sa_key)

    # Initialize with service account info
    client = SecOpsClient(service_account_info=sa_key)
    # Initialize Chronicle client
    chronicle = client.chronicle(
        customer_id=instance_id,
        project_id=project_id,
        region=secops_region
    )
    log_types = chronicle.get_all_log_types()
    if 'WINEVTLOG' in str(log_types):
        status = EXECUTION_STATE_COMPLETED
        output_message = "OK"
        result_value = True
    else:
        status = EXECUTION_STATE_FAILED
        output_message = "Failed"
        result_value = False

    siemplify.end(output_message, result_value, status)


if __name__ == "__main__":
    main()
