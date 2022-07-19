# class to scrape and unzip data archives and present them with sockets to use in main app
# may need admin privileges for /opt/ directory

import json
import requests
import socket
import subprocess
import os
import pandas
import urllib3

# we get it
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class ArchiveTrawler(object):

    target = "https://mtarchive.geol.iastate.edu/"
    headers = {"Connection": "keep-alive"}
    target_folder = "ProbSevere/"

    # data targets
    # validTime, features[properties:{}]

    # directories SET BEFORE RUNNING
    working_directory = "/opt/ArchiveTrawler/"
    save_directory = working_directory + "saves/"

    urls = []
    output = []

    # output data, accessible to parent
    output_data = []  # list of dicts containing weather data from probsevere

    def __init__(self, target=None, save_to: str = None):

        # if save_to:
        #     self.working_directory = save_to
        if target:
            self.target = target

        # initialize directory
        if not os.path.exists(self.working_directory):
            os.mkdir(self.working_directory)
        if not os.path.exists(self.save_directory):
            os.mkdir(self.save_directory)

    # return 1 once data is collected and parsed
    def main(self):
        print("[*] Disabled ssl verification. Consider adding certs in future updates")
        print("Building urls...")
        self.build_urls(self.target)  # recurse build
        print("Fetched and parsed json data")
        return 1

    # get zip, dump to directory and unzip
    def get(self, url=None):
        try:
            if self.target:
                if not url:
                    print("Fetching target data: {}".format(self.target))
                    jsonresp = requests.get(
                        self.target, headers=self.headers, verify=False
                    )
                    jsonresp = jsonresp.text
                    self.parse_json(jsonresp)

                else:
                    print("Fetching url: {}".format(url))
                    jsonresp = requests.get(
                        self.target, headers=self.headers, verify=False
                    )
                    jsonresp = jsonresp.text
                    name = url.split("/")[-1]  # get filename
                    f = open(self.save_directory + name, "w+")
                    f.write(jsonresp)
                    f.close()

            return 1

        except Exception as e:
            print("get: " + str(e))
            return 0

    # recursively build urls
    def build_urls(self, url: str):
        try:
            print("Fetching: {}".format(url))
            r = requests.get(url, headers=self.headers, verify=False)
            p = pandas.read_html(r.text)
            # print("Pandas munching")
            links = list(
                p[0]["Name"]
            )  # invert folder to search root directory most recent -> past
            links.reverse()
            for l in links:
                l = str(l)
                # if subdir, recurse
                # print(l + " : " + str(self.target_folder))
                if l[-1] == "/" and not self.target_folder in l:
                    print("Found directory: {}".format(url + l))
                    self.build_urls(url + l)
                # if Probsevere in dir name, grab files and return
                elif self.target_folder in l:
                    print("Found Probsevere folder at: {}".format(url + l))
                    rx = requests.get(url + l, verify=False)
                    px = pandas.read_html(rx.text)
                    for name in px[0]["Name"]:
                        name = str(name)
                        print("Adding: " + str(url + l + name))
                        self.get(url + l + name)
            return 1

        except Exception as e:
            print("build_urls: " + str(e))
            return 0

    def get_data(self):
        return self.output


if __name__ == "__main__":
    x = ArchiveTrawler()
    x.main()
