from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from msrest.authentication import CognitiveServicesCredentials
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
import time
import logging

# Configurar logging
logging.basicConfig(level=logging.DEBUG)

endpoint = "https://visionlabsychay.cognitiveservices.azure.com/"
key = "9ZwEn34Zb5O1ET52W1w2D9HmILDf16Vt7yTtePT4s6SPBDCXbClfJQQJ99BCACYeBjFXJ3w3AAAFACOGLz1N"

credentials = CognitiveServicesCredentials(key)

client = ComputerVisionClient(
    endpoint=endpoint,
    credentials=credentials
)

def read_image(image_file):
    numberOfCharsInOperationId = 36
    maxRetries = 10

    # SDK call
    rawHttpResponse = client.read_in_stream(image_file, language="en", raw=True)
    logging.debug(f"rawHttpResponse: {rawHttpResponse}")

    # Get ID from returned headers
    operationLocation = rawHttpResponse.headers["Operation-Location"]
    idLocation = len(operationLocation) - numberOfCharsInOperationId
    operationId = operationLocation[idLocation:]
    logging.debug(f"operationId: {operationId}")

    # SDK call
    result = client.get_read_result(operationId)
    logging.debug(f"Initial result: {result}")
    
    # Try API
    retry = 0
    
    while retry < maxRetries:
        if result.status.lower() not in ['notstarted', 'running']:
            break
        time.sleep(1)
        result = client.get_read_result(operationId)
        logging.debug(f"Retry {retry}: {result}")
        
        retry += 1
    
    if retry == maxRetries:
        logging.debug("Max retries reached")
        return "max retries reached"

    if result.status == OperationStatusCodes.succeeded:
        res_text = " ".join([line.text for line in result.analyze_result.read_results[0].lines])
        logging.debug(f"Extracted text: {res_text}")
        return res_text
    else:
        logging.debug("Operation did not succeed")
        return "error"