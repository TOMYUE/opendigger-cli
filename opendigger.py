import os
import json
import argparse

import numpy as np
import plotext as plt
import matplotlib.pyplot as matplot
from datetime import datetime

import urllib.request

prefix = "https://oss.x-lab.info/open_digger/github/"
pwd = "./"
suffix_assets_folder = ".assets"
suffix_png = ".png"
delim_folder = "/"


def get_url_json(url):
    try:
        response = urllib.request.urlopen(url)
        data = response.read()
        json_data = json.loads(data)
        return json_data
    except urllib.error.HTTPError as e:
        print(f"HTTPError: {e.code} - {e.reason}")
    except urllib.error.URLError as e:
        print(f"URLError: {e.reason}")
    except json.JSONDecodeError as e:
        print(f"JSONDecodeError: {e.msg}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    return None


def get_json_data(url, month):
    json_data = get_url_json(url)
    return json_data if month is None else json_data.get(month)


def plotext_plot(dates, metrics, repo_name: str, metrics_name:str, f=None, download=False, color='red'):
    plt.clear_figure()
    plt.date_form('m/Y')
    plt.plotsize(50, 15)
    plt.plot(dates, metrics, color='red')
    plt.xlabel("Date")
    plt.ylabel(metrics_name)
    plt.show()
    if download and f is not None:
        file_path = pwd + repo_name + delim_folder + metrics_name + suffix_png
        x = np.linspace(0, len(dates) - 1, 5, dtype=int)
        x_labels = [dates[i] for i in x]
        matplot.clf()
        matplot.xticks(x, x_labels)
        matplot.title(f"{metrics_name} and dates line plot")
        matplot.xlabel('Dates')
        matplot.ylabel(f'{metrics_name}')
        matplot.plot(dates, metrics, color=color, label=metrics_name)
        matplot.legend()
        matplot.savefig(file_path)
        f.write(f"### {metrics_name} trend fig\n")
        f.write(f"> {repo_name} **{metrics_name}** trend is as follow:\n\n")
        f.write(f"![image-{str(datetime.now().time())}](./{metrics_name + suffix_png})\n")


class OpenDigger:
    def __init__(self):
        self.metrics = {
            "openrank": self.display_openrank,
            "activity": self.display_activity,
            "attention": self.display_attention,
            "all": self.display_all,
        }

    # OpenRank data manipulation
    def display_openrank(self, repo_name: str, month=None, f= None, download=False):
        suffix = "/openrank.json"
        openrank_data = get_json_data(prefix + repo_name + suffix, month)
        print("OpenRank: ")
        if openrank_data is None:
            print("\tOpen Rank data not found or not updated here, try other month or metrics")
            return
        if month is None:
            openrank_data.popitem()
            openrank_data_formatted = {datetime.strptime(d, '%Y-%m').strftime('%m/%Y'): v for d, v in openrank_data.items()}
            openrank = list(openrank_data_formatted.values())
            dates = list(openrank_data_formatted.keys())
            plotext_plot(dates, openrank, repo_name, "OpenRank", f, download)
            print("\nSpecific OpenRank data: ")
            count = 0
            if f is not None and download:
                f.write(f"###  OpenRank data table\n")
                f.write(f'|Dates and OpenRank||||\n')
                f.write('| --- | --- | --- | --- |\n')
                # Write the table rows
                count = 0
                for key, value in openrank_data.items():
                    print(f"\t{key}:{value}\t", end="")
                    # Check if four items have been written to the row
                    if count % 4 == 0:
                        print()
                        f.write('|')  # Start a new row
                    # Write the current item to the row
                    f.write(f' {key}: {value} |')
                    # Check if this is the last item in the row
                    if count % 4 == 3:
                        f.write('\n')  # End the row
                    count += 1
                # If the last row is not complete, add empty cells to fill it
                if count % 4 != 0:
                    empty_cells = 4 - (count % 4)
                    f.write('|' + ' | '.join([''] * empty_cells) + '\n')
                print()
            else:
                for key, value in openrank_data.items():
                    print(f"\t{key}: {value}", end="\t")
                    count += 1
                    if count % 4 == 0:
                        print()
                print()
        else:
            print("\t" + month, end=" ")
            print(openrank_data)

    # activity data manipulation
    def display_activity(self, repo_name: str, month=None, f=None, download=False):
        suffix = "/activity.json"
        activity_data = get_json_data(prefix + repo_name + suffix, month)
        if activity_data is None:
            return
        print("Activity: ")
        if month is None:
            activity_data.popitem()
            meta_data_formatted = {datetime.strptime(d, '%Y-%m').strftime('%m/%Y'): v for d, v in activity_data.items()}
            activities = list(meta_data_formatted.values())
            dates = list(meta_data_formatted.keys())
            plotext_plot(dates, activities, repo_name, "Activity", f, download)
            print("\nSpecific activities data: ")
            count = 0
            if f is not None and download:
                f.write(f"###  Activity data table\n")
                f.write(f'|Dates and Activities||||\n')
                f.write('| --- | --- | --- | --- |\n')
                # Write the table rows
                count = 0
                for key, value in activity_data.items():
                    print(f"\t{key}:{value}\t", end="")
                    # Check if four items have been written to the row
                    if count % 4 == 0:
                        print()
                        f.write('|')  # Start a new row
                    # Write the current item to the row
                    f.write(f' {key}: {value} |')
                    # Check if this is the last item in the row
                    if count % 4 == 3:
                        f.write('\n')  # End the row
                    count += 1
                # If the last row is not complete, add empty cells to fill it
                if count % 4 != 0:
                    empty_cells = 4 - (count % 4)
                    f.write('|' + ' | '.join([''] * empty_cells) + '\n')
                print()
            else:
                for key, value in activity_data.items():
                    print(f"\t{key}:{value}\t")
                    count += 1
                    if count % 4 == 0:
                        print()
                print()
        else:
            print("\t" + month, end=" ")
            print(activity_data)

    # attention data manipulation
    def display_attention(self, repo_name: str, month=None, f=None, download=False):
        suffix = "/attention.json"
        attention_data = get_json_data(prefix + repo_name + suffix, month)
        if attention_data is None:
            return
        print("Attention: ")
        if month is None:
            attention_data.popitem()
            attention_data_formatted = {datetime.strptime(d, '%Y-%m').strftime('%m/%Y'): v for d, v in attention_data.items()}
            attention = list(attention_data_formatted.values())
            dates = list(attention_data_formatted.keys())
            plotext_plot(dates, attention, repo_name, "Attention", f, download)
            print("\nSpecific attention data: ")
            count = 0
            if f is not None and download:
                f.write(f"###  Attention data table\n")
                f.write(f'|Dates and Attention||||\n')
                f.write('| --- | --- | --- | --- |\n')
                # Write the table rows
                count = 0
                for key, value in attention_data.items():
                    print(f"\t{key}: {value}", end="\t")
                    # Check if four items have been written to the row
                    if count % 4 == 0:
                        print()
                        f.write('|')  # Start a new row
                    # Write the current item to the row
                    f.write(f' {key}: {value} |')
                    # Check if this is the last item in the row
                    if count % 4 == 3:
                        f.write('\n')  # End the row
                    count += 1
                # If the last row is not complete, add empty cells to fill it
                if count % 4 != 0:
                    empty_cells = 4 - (count % 4)
                    f.write('|' + ' | '.join([''] * empty_cells) + '\n')
                print()
            else:
                for key, value in attention_data.items():
                    print(f"\t{key}: {value}", end="\t")
                    count += 1
                    if count % 4 == 0:
                        print()
                print()
        else:
            print("\t" + month, end=" ")
            print(attention_data)

    # all metrics data manipulation
    def display_all(self, repo_name: str, month=None, f=None, download=False):
        self.display_openrank(repo_name, month, f, download)
        self.display_activity(repo_name, month, f, download)
        self.display_attention(repo_name, month, f, download)

    # command line arguments parser
    def run(self, args):
        repo_name = args.repo
        month = args.month if args.month else None
        metric = args.metric
        download = True if args.d else False
        download_type = args.d

        if repo_name and download and metric in self.metrics:
            print("repo.name: " + repo_name)
            print("repo.url: " + "https://github.com/" + repo_name)
            dir_path = pwd + repo_name + '/'
            file_path = dir_path + "OpenDiggerInfo." + download_type
            directory = os.path.dirname(dir_path)
            if not os.path.exists(directory):
                os.makedirs(directory)
            with open(f"{file_path}", "w") as f:
                f.write(f"# OpenDigger Data Analysis - {repo_name}\n\n")
                f.write(f"### Repo\n")
                f.write(f"- repo name: {repo_name}\n")
                f.write(f"- repo url: https://github.com/{repo_name}\n")
                if month:
                    f.write(f"- month: {month}\n")
                self.metrics[metric](repo_name, month, f, download)
                if os.path.exists(file_path):
                    print(f"The download file write successfully in {file_path}.")
                else:
                    print("The download file failed to write.")
            f.close()
        elif repo_name and metric in self.metrics:
            print("repo.name: " + repo_name)
            print("repo.url: " + "https://github.com/" + repo_name)
            self.metrics[metric](repo_name, month)
        else:
            print("Please provide a repository name and a valid metric.")


def main():
    parser = argparse.ArgumentParser(description="Get OpenRank data for a GitHub repository.")
    parser.add_argument("-repo", help="GitHub repository name in the format <owner>/<repo>.")
    parser.add_argument("-metric", choices=["openrank", "activity", "attention", "all"], help="Metric to retrieve."
                                                                                              "See each metrics specification on: https://github.com/X-lab2017/open-digger/")

    parser.add_argument("-month", help="Month to retrieve OpenRank data for in the format YYYY-MM.")
    parser.add_argument("-d", choices=["md"], help="Download OpenRank info in Markdown or text format.")
    args = parser.parse_args()

    open_digger = OpenDigger()
    open_digger.run(args)


# if __name__ == '__main__':
#     main()
