"""Extract relevant information from PDF files, text files, and strings"""
import datetime
import os
import re
import subprocess


def extract_date_from_pdf(input_pdf: str) -> datetime.date:
    """Extract the date from a PDF file

    Args:
        input_pdf: Path to PDF file

    Returns:
        Date found in file
    """
    process_err = subprocess.call(['pdftotext', input_pdf])
    if process_err:
        raise RuntimeError('Unable to convert PDF to text')
    input_file = os.path.splitext(input_pdf)[0] + '.txt'
    try:
        date = extract_date_from_file(input_file)
    except:  # pylint: disable=try-except-raise
        raise
    finally:
        os.remove(input_file)
    return date


def extract_date_from_file(input_file: str) -> datetime.date:
    """Extract the date from a text file

    Args:
        input_file: Path to text file

    Returns:
        Date found in file
    """
    with open(input_file) as opened_file:
        return extract_date_from_string(opened_file.read())


def extract_date_from_string(input_str: str) -> datetime.date:
    """Extract the date from a string

    Args:
        input_str: Input string with date

    Returns:
        Date found in string
    """
    # mm/dd/yyyy format
    date_pattern = r'(?P<month>\d\d)/(?P<day>\d\d)/(?P<year>\d\d\d\d)'
    result = re.search(date_pattern, input_str)
    datedict = {key: int(val) for key, val in  result.groupdict().items()}
    return datetime.date(**datedict)
