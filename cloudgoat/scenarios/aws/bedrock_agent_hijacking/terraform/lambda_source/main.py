import json
import boto3

MAX_ITEMS = 100

iam_client = boto3.client('iam')
s3_client = boto3.client('s3')
ec2_client = boto3.client('ec2')












# Map operation values → implementation functions
OPERATION_HANDLERS = {
    "LIST_IAM_ROLES": inventory_iam_roles,
    "LIST_IAM_USERS": inventory_iam_users,
    "LIST_EC2_INSTANCES": inventory_ec2_instances,
    "LIST_S3_BUCKETS": inventory_s3_buckets,
    "LIST_ALL": inventory_all,
}


def handler(event, context):
    """
    Expected event:
    {
      "operation": "LIST_IAM_ROLES"
        | "LIST_S3_BUCKETS"
        | "LIST_IAM_USERS"
        | "LIST_EC2_INSTANCES"
        | "LIST_ALL"
    }
    """
    operation = event['function']

    # Handle invalid operation
    target_function = OPERATION_HANDLERS.get(operation)
    if target_function is None:
        return format_response(
            event,
            json.dumps({
                'error': f'Unsupported function "{operation}"',
                'allowedFunctions': list(OPERATION_HANDLERS.keys())
            }),
            'REPROMPT'
        )

    # Process and return results
    try:
        result = target_function()
        return format_response(
            event,
            json.dumps(result)
        )
    except Exception as e:
        format_response(
            event,
            json.dumps({
                'error': 'Internal error while processing operation',
                'details': str(e)
            }),
            'FAILURE'
        )


def format_response(event, message, error=None):
    response = {
        'actionGroup': event['actionGroup'],
        'function': event['function'],
        'functionResponse': {
            'responseBody': {
                'TEXT': {
                    'body': message
                }
            }
        }
    }
    if error:
        response['functionResponse']['responseState'] = error
    return {
        "messageVersion": "1.0",
        "response": response
    }
