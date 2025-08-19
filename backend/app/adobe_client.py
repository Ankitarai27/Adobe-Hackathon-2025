from adobe.pdfservices.operation.auth.credentials import Credentials
from adobe.pdfservices.operation.execution_context import ExecutionContext

def get_execution_context():
    credentials = Credentials.service_account_credentials_builder() \
        .from_file("pdfservices-api-credentials.json") \
        .build()
    return ExecutionContext.create(credentials)
