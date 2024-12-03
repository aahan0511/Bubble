# imports
from customtkinter import *
from pywinstyles import change_border_color, change_header_color, change_title_color
from hPyT import maximize_button
from os import getlogin, makedirs
from shutil import rmtree
import json
import requests
import urllib.request
import os
from PIL import Image

USER = getlogin()
DIR = f"C:\\Users\\{USER}\\AppData\\Local\\Bubble"
rmtree(DIR)
makedirs(DIR)

PATHS = {
    "favicon.ico" : DIR+f"\\assets\\icons\\favicon.ico",
    "logo.png" : DIR+f"\\assets\\blob\\logo.png"
}

class Downloader:

    def __init__(self, url="https://github.com/aahan0511/Bubble", branch="main"):
        tmp_url = url.replace('https://github.com/', 'https://api.github.com/repos/')
        tmp_url += '/git/trees/main?recursive=1'
        api = requests.get(tmp_url).text
        files = json.loads(api)
        output = []
        location = dict()
        for (k, i) in enumerate(files['tree']):
            if i['type'] == 'blob':
                tmp = [i['path']]
                tmp += [self.__get_raw_url(tmp[0], i['url'], branch)]
                output.append(tmp)
            else:
                location[i['path']] = k
        self.files = output
        self.location = location
        self.repo_url = url

    @classmethod
    def __get_raw_url(self, file_path, url, branch=''):
        tmp_url = url.replace(
            'https://api.github.com/repos/',
            'https://raw.githubusercontent.com/')
        tmp_url = tmp_url.split('/git/blobs/')[0]
        tmp_url = tmp_url + '/' + branch + '/' + file_path
        return tmp_url

    def __mkdirs(self, path):
        if not os.path.isdir(path):
            os.makedirs(path)

    def download(
        self,
        destination,
        target_folder='*',
        recursive=True,):
        self.__mkdirs(destination)
        if target_folder == '*':
            start = 0
        else:
            tmp_target = target_folder.replace('./', '')
            tmp_target = tmp_target.replace('../', '')
            tmp_target = (tmp_target if tmp_target[-1] != '/'
                          else tmp_target[:-1])
            start = self.location[target_folder]
        for i in self.files[start:]:
            if recursive or i[0].split(target_folder)[1].count('/') \
                    <= 1:
                self.__mkdirs(destination + '/' + os.path.dirname(i[0]))
                urllib.request.urlretrieve(i[1], destination + '/' + i[0])

github = Downloader()
github.download(DIR, "assets")

class App(CTk):

    def __init__(root) -> None:
        super().__init__(fg_color="#aac8e6")

        root.title("Bubble | SETUP")
        root.geometry("600x400")
        root.iconbitmap(PATHS["favicon.ico"])

        change_header_color(root, "#aac8e6")
        change_border_color(root, "#aac8e6")
        change_title_color(root, "#ffffff")
        maximize_button.disable(root)

        root.columnconfigure(0, weight=2, uniform="a")
        root.columnconfigure(1, weight=1, uniform="a")
        root.rowconfigure((0, 1), weight=1, uniform="a")

        root.normal = CTkButton(
            root,
            fg_color="#bccaff",
            hover_color="#bfbcff",
            text="Normal Installation",
            font=("JetBrains Mono Medium", 25),
            image=CTkImage(Image.open(PATHS['logo.png']), Image.open(PATHS['logo.png']))
        )
        root.normal.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        root.mainloop()

if __name__ == "__main__":
    app = App()