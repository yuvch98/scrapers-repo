import time
import logging
from mobile_eye import MobileEye


def lambda_handler(event, context):
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    start_time = time.time()
    # moon_active job data
    mobile_eye = MobileEye()
    mobile_eye.extract_data_from_job()
    mobile_eye.move_to_mongo()
    mobile_eye.update_mongo()
    end_time = time.time()
    elapsed_time = round(end_time - start_time, 2)
    # Log the time taken to run the Lambda function
    logger.info(f"The time it took to run: {elapsed_time} seconds")

    return {
        'statusCode': 200,
        'body': f"The process completed in {elapsed_time} seconds."
    }
