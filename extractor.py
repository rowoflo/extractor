"""Extract relevant information from PDF files, text files, and strings"""
import datetime
import os
import re
import subprocess

import dateparser


def extract_date_from_pdf(input_pdf: str) -> datetime.date:
    """Extract the date from a PDF file

    Args:
        input_pdf: Path to PDF file

    Returns:
        Date found in file
    """
    input_pdf = os.path.expanduser(input_pdf)
    if not os.path.exists(input_pdf):
        raise FileNotFoundError('Not a valid file: {}'.format(input_pdf))
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

    Note:
        If multiple dates are found, returns the newest date
    """
    with open(input_file) as opened_file:
        return extract_date_from_string(opened_file.read())


def extract_date_from_string(input_str: str) -> datetime.date:
    """Extract the date from a string

    Args:
        input_str: Input string with date

    Returns:
        Date found in string

    Note:
        If multiple dates are found, returns the oldest date
    """
    months = ['january', 'february', 'march', 'april', 'may', 'june',
              'july', 'august', 'september', 'october', 'november' 'december']
    months_rex_strs = []
    for month in months:
        month_rex_str = r''
        for letter in month[0:3]:
            month_rex_str += (r'[' + letter.upper() + letter + ']')
        for letter in month[3:]:
            month_rex_str += (r'[' + letter.upper() + letter + ']?')
        months_rex_strs.append(month_rex_str)

    date_patterns = []
    # Format: m/d/yy to mm/dd/yyyy with / or -
    date_patterns.append(('MDY', r'((?<!\d)\d\d?)(-|/)((?<!\d)\d\d?)(-|/)(\d\d\d\d|\d\d)'))
    # Format: yyyy/mm/dd with / or -
    date_patterns.append(('YMD', r'(\d\d\d\d)(-|/)((?<!\d)\d\d?)(-|/)((?<!\d)\d\d?)'))
    # Format: MMM dd, yyyy
    date_patterns.append(('MDY',
                          r'(' + r'|'.join(months_rex_strs) + \
                          r")[\D|^,]*?(\d\d?)[,|\s|1|']+?(\d\d\d\d|\d\d)"))
    # Format: dd MMM, yyyy
    date_patterns.append(('DMY',
                          r'(\d\d?)\s*(' + \
                          r'|'.join(months_rex_strs) + r')[,|\s]+?(\d\d\d\d|\d\d)'))

    dates_found = []
    for order, date_regex_str in date_patterns:
        these_dates = []
        for this_date in re.findall(date_regex_str, input_str):
            if '' not in this_date:
                these_dates.append((order, this_date))
        dates_found.extend(these_dates)


    oldest_date = None
    for order, date_found in dates_found:
        this_date = dateparser.parse('/'.join(date_found), settings={'DATE_ORDER': order})
        if this_date is not None and (oldest_date is None or this_date < oldest_date):
            oldest_date = this_date
    return oldest_date
