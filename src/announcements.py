

class Announcements(object):
    """
    Contains the meta-data for an ASX announcement.
    """
    download_prefix_link = "http://www.asx.com.au/asx/statistics/displayAnnouncement.do?display=pdf&idsId="
    download_prefix_pdf = "http://www.asx.com.au"

    def __init__(self):
        """
        Return a Announcement object.
        """
        self.company_id = company_id
        self.published_at = published_at
        self.price_sens = price_sens
        self.information = information
        self.link = self.download_prefix_link + link

    def __get_pdf_link(self):
        """
        Returns the pdf for this announcement
        """
        access_page = requests.get(self.link)
        souped_access_page = bs(access_page.text, "lxml")
        pdf_url_suffix = souped_access_page.find('input', {'name': 'pdfURL'}).get('value')
        pdf_link = self.download_prefix_pdf + pdf_url_suffix
        return pdf_link