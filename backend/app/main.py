from fastapi import FastAPI
import os
from adobe.pdfservices.operation.auth.service_principal_credentials import ServicePrincipalCredentials
from adobe.pdfservices.operation.pdf_services import PDFServices
from adobe.pdfservices.operation.pdfjobs.jobs.export_pdf_job import ExportPDFJob
from adobe.pdfservices.operation.pdfjobs.params.export_pdf.export_pdf_params import ExportPDFParams
from adobe.pdfservices.operation.pdfjobs.params.export_pdf.export_pdf_target_format import ExportPDFTargetFormat
from adobe.pdfservices.operation.io.stream_asset import StreamAsset

app = FastAPI()


@app.post("/convert/{filename}")
async def convert_pdf(filename: str):
    input_path = os.path.join("uploads", filename)
    if not os.path.exists(input_path):
        return {"error": "File not found"}

    output_path = os.path.splitext(input_path)[0] + ".docx"

    # Setup Adobe client
    credentials = ServicePrincipalCredentials(
        client_id=os.getenv("PDF_SERVICES_CLIENT_ID"),
        client_secret=os.getenv("PDF_SERVICES_CLIENT_SECRET")
    )
    pdf_services = PDFServices(credentials=credentials)

    # Upload file
    with open(input_path, "rb") as f:
        input_stream = StreamAsset(input_stream=f, mime_type="application/pdf")

    # Export job setup
    params = ExportPDFParams(target_format=ExportPDFTargetFormat.DOCX)
    job = ExportPDFJob(input_asset=pdf_services.upload(input_stream=input_stream), export_pdf_params=params)

    # Execute and save
    result = pdf_services.submit(job)
    pdf_services_response = pdf_services.get_job_result(result, ExportPDFJob)
    resource = pdf_services_response.get_result().get_resource()
    stream_asset = pdf_services.get_content(resource)
    with open(output_path, "wb") as f:
        f.write(stream_asset.get_input_stream().read())

    return {"message": "Converted successfully", "output": output_path}




