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
        self.link = self.download_prefix_link + link
        self.pre_price_sens = 0  # Unknown at object construction time

    def __get_pdf_link(self):
        """
        Returns the pdf for this announcement
        """
        access_page = requests.get(self.link)
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

    def get_text_list(self):
        """Returns the pdf of an announcement processed into a word list."""
        pdf_link = self.__get_pdf_link()
        raw = get_raw_text_from_link(self.__get_pdf_link())
        text = clean_text(raw)
        text = remove_stop_words(text)
        word_list = tokenised(text)
        word_list = stem_list(word_list)
        text = remove_repeats(word_list)
        return text

    def get_price_result(self):
        return 1

    def is_sensitive(self):
        """Returns true of false depending on whether or not this announcement is price sensitive or not"""
        return True if self.price_sens == 1 else False


