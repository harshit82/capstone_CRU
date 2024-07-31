import re


def ends_with_pdf(url):
    """
    Checks if the given URL ends with '.pdf' and returns the URL if it matches the pattern.

    Args:
        url (str): The URL to check.

    Returns:
        str: The URL if it ends with '.pdf', otherwise None.

    Example:
        >>> ends_with_pdf('https://example.com/report.pdf')
        'https://example.com/report.pdf'

        >>> ends_with_pdf('https://example.com/report.docx')
        None
    """
    pattern = r'http[s]?:\/\/.*\/[^\/]*\.pdf'
    pdf_link = re.search(pattern, url)
    if pdf_link:
        return pdf_link.group()


def get_filename(url):
    """
    Extracts the filename from the URL, assuming the filename is followed by '.pdf'.

    Args:
        url (str): The URL from which to extract the filename.

    Returns:
        str: The filename without the extension if it matches the pattern, otherwise None.

    Example:
        >>> get_filename('https://example.com/files/report-2023.pdf')
        'report-2023'

        >>> get_filename('https://example.com/files/report-2023.docx')
        None
    """
    pattern = r'(?<=/)[^/]*(?=\.pdf)'
    match = re.search(pattern, url)
    if match:
        return match.group()
