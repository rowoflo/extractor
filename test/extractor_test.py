'''Extrator package tests'''
import datetime
import os

from .. import extractor


def test_extract_date_from_string():
    '''Test the extract_date_from_string function'''
    test_cases = [
        'January 2, 2003',
        'Jan 2, 2003',
        'Jan 2 2003',
        '01/02/2003',
        '01/02/03',
        '1/2/03',
        '2003/01/02',
        '01-02-2003',
        '01-02-03',
        '1-2-03',
        '2003-01-02',
        '2 January, 2003',
    ]
    expected_date = datetime.datetime(2003, 1, 2)
    for case in test_cases:
        actual_date = extractor.extract_date_from_string(case)
        assert expected_date == actual_date, '{}'.format(case)

    test_cases = [
        'October 23, 2045',
        'Oct 23, 2045',
        'Oct 23 2045',
        '10/23/2045',
        '10/23/45',
        '10/23/45',
        '2045/10/23',
        '10-23-2045',
        '10-23-45',
        '2045-10-23',
        '23 October, 2045',
    ]
    expected_date = datetime.datetime(2045, 10, 23)
    for case in test_cases:
        actual_date = extractor.extract_date_from_string(case)
        assert expected_date == actual_date, '{}'.format(case)


def test_extract_date_from_pdf():
    '''Test the extract_date_from_pdf function'''
    test_data_folder = 'test/data'
    for root, _, files in os.walk(test_data_folder):
        for test_file in files:
            if test_file[0] == '.' or os.path.splitext(test_file)[1] != '.pdf':
                continue
            expected_date = datetime.datetime.strptime(
                test_file[0:10], '%Y-%m-%d')
            try:
                actual_date = extractor.extract_date_from_pdf(os.path.join(root, test_file))
            except Exception as err:
                print(test_file)
                raise err
            assert expected_date == actual_date, '{}'.format(test_file)
