import requests
from subprocess import Popen, PIPE


def get_raw_text_from_link(pdf_link):
    """
    Runs pdftotext to extract all text from a pdf. Needs to run on a system where
    streams can be piped to pdftotext.

    Requires pdftotext from Poppler: sudo apt-get install poppler-utils
    """
    process = Popen(["pdftotext", "-", "-"], stdin=PIPE, stdout=PIPE, stderr=PIPE, bufsize=-1)
    process.stdin.write((requests.get(pdf_link)).content)
    process.stdin.close()

    result = str(process.stdout.read())
    error = process.stderr.read()

    return result

