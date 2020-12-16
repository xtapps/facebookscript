import datetime
import os
from shutil import copyfile

from bs4 import BeautifulSoup

SOURCE_MEDIA_FOLDER = "/Users/ajai/Downloads/fwdquickfixscriptneeded/"

SOURCE_FILES = [
    "/Users/ajai/Downloads/fwdquickfixscriptneeded/0.html",
    "/Users/ajai/Downloads/fwdquickfixscriptneeded/1.html",
    "/Users/ajai/Downloads/fwdquickfixscriptneeded/2.html",
]

DESTINATION_ROOT_FOLDER = "/Users/ajai/Desktop/FB"  # Files will be copied to this directory


class ImageExtract(object):

    def read_html(self):
        for item in SOURCE_FILES:
            with open(item, 'r') as f:
                html_content = f.read()
                self.find_image_tags(html_content)

    def find_image_tags(self, html_content):
        soup = BeautifulSoup(html_content, "html.parser")
        img_parent_divs = soup.find_all("div", attrs={"class": "pam _3-95 _2pi0 _2lej uiBoxWhite noborder"})
        for item in img_parent_divs:
            image = item.a.img
            date_div = item.find("div", attrs={"class": "_3-94 _2lem"})
            image_src = image.get('src')
            # self.create_dummy_files_for_testing(SOURCE_MEDIA_FOLDER, image_src)
            date_time_str = date_div.a.text
            date_time_str = ' '.join(date_time_str.split(", ")[:-1])
            formatted_date_str = datetime.datetime.strptime(date_time_str, '%b %d %Y').strftime('%Y %m %d')
            self.copy_image_to_target_directory(image_src, formatted_date_str)

    def copy_image_to_target_directory(self, image, date_folder):
        target_folder = '{}/{}'.format(DESTINATION_ROOT_FOLDER, date_folder)
        if not os.path.exists(target_folder):
            os.makedirs(target_folder)
        filename = image.split("/")[-1]
        copyfile(SOURCE_MEDIA_FOLDER+image, target_folder+'/'+filename)
        print("Copied {} to {}".format(image, date_folder))

    def create_dummy_files_for_testing(self, SOURCE_MEDIA_FOLDER, image):
        with open(SOURCE_MEDIA_FOLDER+image, 'w') as f:
            f.write('aaa')


if __name__ == '__main__':
    extractor = ImageExtract()
    extractor.read_html()
