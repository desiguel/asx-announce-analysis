#!/usr/bin/python3

import requests
import io
from bs4 import BeautifulSoup as bs
from pdf_utilities import *
from text_utilities import *

class Announcement(object):
    """
    Contains the meta-data for an ASX announcement.
    """
    download_prefix_link = "http://www.asx.com.au/asx/statistics/displayAnnouncement.do?display=pdf&idsId="
    download_prefix_pdf = "http://www.asx.com.au"

    def __init__(self, company_id, published_at, price_sens, information, link):
        """
        Return a Announcement object.
        """
        self.company_id = company_id
        self.published_at = published_at
        self.price_sens = price_sens
        self.information = information
        self.link = link
        self.pre_price_sens = 0  # Unknown at object construction time

    def __get_pdf_link(self):
        """
        Returns the pdf for this announcement
        """
        access_page = requests.get(self.download_prefix_link + self.link)
        souped_access_page = bs(access_page.text, "lxml")
        pdf_url_suffix = souped_access_page.find('input', {'name': 'pdfURL'}).get('value')
        pdf_link = self.download_prefix_pdf + pdf_url_suffix
        return pdf_link

    def __get_pdf(self):
        """
        Returns the pdf for this announcement.
        """
        pdf_link = self.__get_pdf_link()
        pdf = io.BytesIO((requests.get(pdf_link)).content)
        return pdf

    def get_text(self, source="html"):
        """
        Returns the pdf of an announcement processed into a word list.
        """
        if source == "html":
            raw = get_raw_text_from_html_link(self.__get_pdf_link())
        else:
            raw = get_raw_text_from_fs_link(self.link)

        return raw

    def get_price_result(self):
        # TODO
        return 1

    def is_sensitive(self):
        """Returns true of false depending on whether or not this announcement is price sensitive or not"""
        return True if self.price_sens == 1 else False


