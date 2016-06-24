import requests
import PyPDF2
from bs4 import BeautifulSoup as bs


class Announcement(object):
    """
    Contains the meta-data for an ASX announcement.
    """
    download_prefix_link = "http://www.asx.com.au/asx/statistics/displayAnnouncement.do?display=pdf&idsId="
    download_prefix_pdf = "http://www.asx.com.au"

    def __init__(self, company_id, published_at, price_sens, information, link):
        """Return a Announcement object."""
        self.company_id = company_id
        self.published_at = published_at
        self.price_sens = price_sens
        self.information = information
        self.link = link

    def get_link(self):
        """Returns the link string for an announcement."""
        return self.link

    def get_pdf(self):
        """Returns the pdf for this announcement"""
        access_page = requests.get(self.download_prefix_link + self.link)
        souped_access_page = bs(access_page.text)
        pdf_url_suffix = souped_access_page.find(name="pdfURL").attrs['value']
        pdf = requests.get(self.download_prefix_pdf + pdf_url_suffix)
        return pdf

    def get_text(self):
        """Returns the announcement as a text string"""
        pdf = self.get_pdf()
        pdf_reader = PyPDF2.PdfFileReader(pdf)
        return pdf_reader.flattenedPages.extractText()

