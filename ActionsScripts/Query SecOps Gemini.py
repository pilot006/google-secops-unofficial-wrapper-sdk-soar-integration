from SiemplifyAction import SiemplifyAction
from SiemplifyUtils import unix_now, convert_unixtime_to_datetime, output_handler
from ScriptResult import EXECUTION_STATE_COMPLETED, EXECUTION_STATE_FAILED,EXECUTION_STATE_TIMEDOUT
from secops import SecOpsClient
import json



@output_handler
def main():
    siemplify = SiemplifyAction()
    llm_prompt = siemplify.extract_action_param("Prompt", print_value=True)

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
    # Query Gemini with a security question
    response = chronicle.gemini(llm_prompt)

    # Get text content (combines TEXT blocks and stripped HTML content)
    text_explanation = response.get_text_content()
    siemplify.LOGGER.info("get_text_content(): " + text_explanation)

    raw_response = response.get_raw_response()
    # Work with different content blocks
    for block in response.blocks:
        print(f"Block type: {block.block_type}")
        if block.block_type == "TEXT":
            print("Text content:", block.content)
        elif block.block_type == "CODE":
            print(f"Code ({block.title}):", block.content)
        elif block.block_type == "HTML":
            print("HTML content (with tags):", block.content)

    status = EXECUTION_STATE_COMPLETED
    output_message = text_explanation
    result_value = text_explanation
    siemplify.end(output_message, result_value, status)


if __name__ == "__main__":
    main()
