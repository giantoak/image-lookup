import random
from string import ascii_uppercase, digits
import os
class ImgSearch(object):
    img_exts = ['jpg', 'jpeg', 'png', 'gif', 'bmp']
    def get_filename(self, filename):
        """
        Generate 50-char long random filename
        """
        s = ''.join(random.choice(ascii_uppercase + digits) for _ in
                       range(50))

        name, ext = os.path.splitext(filename.lower())
        ext = ext.strip('.')
        if not ext in self.img_exts:
            raise TypeError('{} is not a valid image file\
                            extension'.format(ext))

        return '{name}.{ext}'.format(name=s, ext=ext)
    
    def query_google(self, img):
        """
        Queries Google's Reverse Image Search API with the URL in `img`

        Returns a response object like the following:
            {'query': `Google's best guess for a query`,
             'results': [img1, img2, img3...]
             }

             Where img* are urls of returned images
        """
        
        query = googbase.format(img)
        

