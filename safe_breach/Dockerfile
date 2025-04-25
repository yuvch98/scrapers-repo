# aws integration:
FROM public.ecr.aws/lambda/python:3.12
# Copy function code
COPY app.py ${LAMBDA_TASK_ROOT}
# copy needed files for the execution
COPY safe_breach.py ${LAMBDA_TASK_ROOT}
#copy requirements
COPY requirements.txt ${LAMBDA_TASK_ROOT}

# Install the specified packages
RUN pip install -r requirements.txt


# Set the CMD the lambda handler
CMD [ "app.lambda_handler" ]