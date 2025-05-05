from SiemplifyAction import SiemplifyAction
from SiemplifyUtils import unix_now, convert_unixtime_to_datetime, output_handler
from ScriptResult import EXECUTION_STATE_COMPLETED, EXECUTION_STATE_FAILED,EXECUTION_STATE_TIMEDOUT
from secops import SecOpsClient
from datetime import datetime, timedelta, timezone
import json

from tabulate import tabulate



@output_handler
def main():
    siemplify = SiemplifyAction()

    sa_key = siemplify.extract_configuration_param('Integration',"JSON Service Account Key")
    instance_id = siemplify.extract_configuration_param('Integration',"SecOps Customer ID")
    project_id = siemplify.extract_configuration_param('Integration',"SecOps Project ID")
    secops_region = siemplify.extract_configuration_param('Integration',"SecOps Region")
    sa_key = json.loads(sa_key)

    stats_query = siemplify.extract_action_param("Stats Query", print_value=True)
    hours_back = siemplify.extract_action_param("Hours Back", print_value=True)

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
    start_time = end_time - timedelta(hours=int(hours_back))

    stats = chronicle.get_stats(
        query=stats_query,
        start_time=start_time,
        end_time=end_time,
        max_events=1000,
        max_values=1000
    )

    column_headers = stats['columns']
    table_data_for_tabulate = stats['rows']
    formatted_rows = []
    for row_dict in stats['rows']:
        current_row = [row_dict.get(col, "") for col in column_headers] # Use .get for safety
        formatted_rows.append(current_row)
    ascii_table = tabulate(formatted_rows, headers=column_headers, tablefmt="grid")
    status = EXECUTION_STATE_COMPLETED
    wall_message = "<p style=\"font-family:'Courier New'\">" + stats_query + "<br><br>" + ascii_table + "</p>"
    siemplify.add_comment(comment=wall_message)
    siemplify.result.add_result_json(stats)
    output_message = "Stats results written to case wall"
    result_value = None

    siemplify.end(output_message, result_value, status)


if __name__ == "__main__":
    main()
