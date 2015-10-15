import random
from string import ascii_uppercase, digits
import os


class ImgSearch(object):
    img_exts = ['jpg', 'jpeg', 'png', 'gif', 'bmp']

    def get_filename(self, filename):
        """
        Generate 50-char long random filename
        """
        s = ''.join(random.choice(ascii_uppercase + digits) for _ in range(50))

        name, ext = os.path.splitext(filename.lower())
        ext = ext.strip('.')
        if not ext in self.img_exts:
            raise TypeError('{} is not a valid image file extension'.format(ext))

        return '{name}.{ext}'.format(name=s, ext=ext)

    def parse_google_query(self, html):
        """
        Parses the html from the Google reverse image search

        :param html:
        :return dict:
            {'query': `Google's best guess for a query`,
             'results': [link1, link2, link3...]
             }
        """
        from bs4 import BeautifulSoup
        import json

        soup = BeautifulSoup(html)
        text = soup.find("a", class_="qb-b")
        if text:
            text = text.find(text=True)
        
        matches = soup.find_all("h3", class_="r")
        if (matches):
            output_matches = []
            for match in matches:
                output_matches.append(match.find(href=True)['href'])
            matches = output_matches

        output = { 
            "query" : str(text), 
            "results" : matches }
        return output 

