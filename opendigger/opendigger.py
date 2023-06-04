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


def format_date_data(data):
    return {datetime.strptime(d, '%Y-%m').strftime('%m/%Y'): v for d, v in data.items()}


def plotext_plot(dates, metrics, repo_name: str, metrics_name: str, f=None, download=False, color='red', style="line"):
    plt.clear_figure()
    plt.date_form('m/Y')
    plt.plotsize(50, 15)
    if style == "line":
        plt.plot(dates, metrics, color=color)
    elif style == "bar":
        plt.bar(dates, metrics, color=color)
    plt.xlabel("Date")
    plt.ylabel(metrics_name)
    print(f"{repo_name} {metrics_name} figure:")
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
        f.write(f"#### {metrics_name} trend fig\n")
        f.write(f"> {repo_name} **{metrics_name}** trend is as follow:\n\n")
        f.write(f"![image-{str(datetime.now().time())}](./{metrics_name + suffix_png})\n")


class OpenDigger:
    def __init__(self):
        self.indexes = {
            "openrank": self.display_openrank,
            "activity": self.display_activity,
            "attention": self.display_attention,
            "all": self.display_all,
        }
        self.metrics = {
            "active-dates-times": self.display_active_dates_times,
            "stars": self.display_stars,
            "technical_fork": self.display_technical_fork,
            "participants": self.display_participants,
            "contributors": self.display_contributors,
            "bus_factor": self.display_bus_factor,
            "issues": self.display_issues,
            "code_change_line": self.display_code_change_line,
            "pr": self.display_pr,
            "all": self.diaplay_metrics_all
        }
        self.network = {
            "develop-net": self.display_develop_networks,
            "repo-net": self.display_repo_networks,
        }

    ##########################################
    #             Indexes                    #
    ##########################################
    # OpenRank data manipulation
    def display_openrank(self, repo_name: str, month=None, f=None, download=False):
        suffix = "/openrank.json"
        openrank_data = get_json_data(prefix + repo_name + suffix, month)
        print("OpenRank: ")
        if openrank_data is None:
            print("\tOpen Rank data not found or not updated here, try other month or metrics")
            return
        if month is None:
            openrank_data.popitem()
            openrank_data_formatted = {datetime.strptime(d, '%Y-%m').strftime('%m/%Y'): v for d, v in
                                       openrank_data.items()}
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
                    print(f"\t{key}:{value}\t", end="")
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
            attention_data_formatted = {datetime.strptime(d, '%Y-%m').strftime('%m/%Y'): v for d, v in
                                        attention_data.items()}
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

    ##########################################
    #               Metrics                  #
    ##########################################
    def display_active_dates_times(self, repo_name: str, month, f=None, download=False):
        if month is None:
            print("please specify the month")
            return
        data = get_json_data(prefix + repo_name + "/active_dates_times.json", month)
        if f is not None and download:
            f.write(f"#### Active dates and times for {repo_name}:\n")
            f.write(f"{data}\n")
        else:
            print(f"Active dates and times for {repo_name}:\n")
            print(f"{data}\n")

    def display_stars(self, repo_name: str, month, f=None, download=False):
        data = get_json_data(prefix + repo_name + "/stars.json", month)
        if f is not None and download:
            if month is None:
                f.write(f"#### Stars⭐️per month for {repo_name}:\n")
                f.write(f"{data} ⭐️\n")
                data.popitem()
                data_formateted = {datetime.strptime(d, '%Y-%m').strftime('%m/%Y'): v for d, v in data.items()}
                data_values = list(data.values())
                dates = list(data_formateted.keys())
                plotext_plot(dates, data_values, repo_name, "Stars", f, download)
            else:
                f.write(f"- Stars⭐ in {month} for {repo_name}:\n")
                f.write(f"{data} \n")
        else:
            print(f"Stars⭐per month for {repo_name}:\n", end="")
            count = 0
            for k, v in data.items():
                count += 1
                print(f"\t{k}: {v}", end="")
                if count % 4 == 0:
                    print()

    def display_technical_fork(self, repo_name: str, month=None, f=None, download=False):
        if month is None:
            print("please specify the month")
            return
        data = get_json_data(prefix + repo_name + "/technical_fork.json", month)
        if f is not None and download:
            f.write(f"#### Technical fork for {repo_name}:\n")
            f.write(f"{data}\n")
        else:
            print(f"Technical fork for {repo_name}:\n")
            print(f"{data}\n")

    def display_participants(self, repo_name: str, month=None, f=None, download=False):
        if month is None:
            print("please specify the month")
            return
        data = get_json_data(prefix + repo_name + "/participants.json", month)
        if f is not None and download:
            f.write(f"#### Participants number for {repo_name} in {month}:\n")
            f.write(f"{data}\n")
        else:
            print(f"Participants number for {repo_name} in {month}:\n")
            print(f"{data}\n")

    def display_contributors(self, repo_name: str, month=None, f=None, download=False):
        if month is None:
            return
        new_contributors = get_json_data(prefix + repo_name + "/new_contributors.json", month)  # int
        contributors_detail = get_json_data(prefix + repo_name + "/new_contributors_detail.json", month)  # list
        inactive_contributors = get_json_data(prefix + repo_name + "/inactive_contributors.json", month)  # int
        if f is not None and download:
            f.write(f"#### Contributors info for {repo_name} in {month}:\n")
            f.write(f"1. new contributors: {new_contributors}\n")
            f.write(f"2. contributors names:\n")
            for name in contributors_detail:
                f.write(f"- {name}\n")
            f.write(f"3. inactive contributors: {inactive_contributors}\n")
        else:
            print(f"Contributors for {repo_name} in {month}:\n")
            print(f"1. new contributors: {new_contributors}\n")
            print(f"2. contributors names:\n")
            for name in contributors_detail:
                print(f"- {name}\n")
            print(f"3. inactive contributors: {inactive_contributors}\n")

    def display_bus_factor(self, repo_name: str, month=None, f=None, download=False):
        if month is None:
            print("month not specified, please specify the month and retry this")
            return
        data = get_json_data(prefix + repo_name + "/bus_factor.json", month)  # TODO: change .json file name
        detail_data = get_json_data(prefix + repo_name + "/bus_factor_detail.json", month)
        if f is not None and download:
            f.write(f"#### Bus factor for {repo_name}:\n")
            f.write(f"bus factor: {month}: {data}\n")
            count = 0
            for _ in detail_data:
                f.write(f"{_} ")
                count += 1
                if count % 4 == 0:
                    f.write("\n")
        else:
            print(f"Bus factor for {repo_name}:\n", end="")
            print(f"{month}: {data}\t\n", end="")
            count = 0
            for _ in detail_data:
                print(f"{_} ", end="")
                count += 1
                if count % 4 == 0:
                    print()

    def draw_issues_response(self, data, repo_name, month, f, download):
        avg_data = data['avg']
        levels_data = data['levels']
        fig, (ax1, ax2) = matplot.subplots(2, 1, figsize=(10, 10))
        x_avg = list(avg_data.keys())
        y_avg = list(avg_data.values())

        ax1.plot(x_avg, y_avg)
        ax1.set_xlabel('Date')
        ax1.set_ylabel('Average')
        ax1.set_title('Average Values')
        ax1.tick_params(axis='x', rotation=45)
        x_levels = list(levels_data.keys())
        y_levels = list(levels_data.values())

        y1 = [level[0] for level in y_levels]
        y2 = [level[1] for level in y_levels]
        y3 = [level[2] for level in y_levels]
        y4 = [level[3] for level in y_levels]

        ax2.bar(x_levels, y1, label='Level 1')
        ax2.bar(x_levels, y2, bottom=y1, label='Level 2')
        ax2.bar(x_levels, y3, bottom=[sum(x) for x in zip(y1, y2)], label='Level 3')
        ax2.bar(x_levels, y4, bottom=[sum(x) for x in zip(y1, y2, y3)], label='Level 4')

        ax2.set_xlabel('Date')
        ax2.set_ylabel('Levels')
        ax2.set_title('Levels Stacked Bar Plot')
        ax2.tick_params(axis='x', rotation=45)
        ax2.legend()
        matplot.tight_layout()
        file_path = pwd + repo_name + delim_folder + "issues" + suffix_png
        matplot.savefig(file_path)
        f.write(f"> {repo_name} **issues** info is as follow:\n\n")
        f.write(f"![image-{str(datetime.now().time())}](./issues{suffix_png})\n")

    def display_issues(self, repo_name: str, month=None, f=None, download=False):
        issue_new = get_json_data(prefix + repo_name + "/issue_new.json", month)  # TODO: change .json file name, 3 types
        issue_closed = get_json_data(prefix + repo_name + "/issue_closed.json", month)
        issue_comments = get_json_data(prefix + repo_name + "/issue_comments.json", month)
        issue_response_time = get_url_json(prefix + repo_name + "/issue_response_time.json")
        issue_resolution_duration = get_url_json(prefix + repo_name + "/issue_resolution_duration.json")
        issue_age = get_url_json(prefix + repo_name + "/issue_age.json")
        if f is not None and download:
            f.write(f"- Issues for {repo_name}:\n")
            if month is not None:
                f.write(f"  - issue new: {issue_new}\n")
                f.write(f"  - issue closed: {issue_closed}\n")
                f.write(f"  - issue comments: {issue_comments}\n")
                f.write(f"  - issue response time fig:\n")
                self.draw_issues_response(issue_response_time, repo_name, month, f, download)
                self.draw_issues_response(issue_resolution_duration, repo_name, month, f, download)
                self.draw_issues_response(issue_age, repo_name, month, f, download)
            else:
                f.write(f"  - issue new: {issue_new}\n")
                f.write(f"  - issue closed: {issue_closed}\n")
                f.write(f"  - issue comments: {issue_comments}\n")
        else:
            print(f"Issues for {repo_name}:\n")
            print(f"\tissue new: {issue_new}\n")
            print(f"\tissue closed: {issue_closed}\n")
            print(f"\tissue comments: {issue_comments}\n")

    def display_code_change_line(self, repo_name: str, month=None, f=None, download=False):
        code_add = format_date_data(get_json_data(prefix + repo_name + "/code_change_lines_add.json", month))
        code_remove = format_date_data(get_json_data(prefix + repo_name + "/code_change_lines_remove.json", month))
        code_sum = format_date_data(get_json_data(prefix + repo_name + "/code_change_lines_sum.json", month))
        if f is not None:
            f.write(f"#### Code change line info for {repo_name}:\n")
        print(f"Code change line for {repo_name}:\n")
        plotext_plot(list(code_add.keys()), list(code_add.values()), repo_name, "code_chang_lines_add", f, download, color="green")
        plotext_plot(list(code_remove.keys()), list(code_remove.values()), repo_name, "code_chang_lines_remove", f, download, color="green")
        plotext_plot(list(code_sum.keys()), list(code_sum.values()), repo_name, "code_chang_lines_sum", f, download, color="green")


    def display_pr(self, repo_name: str, month=None, f=None, download=False):
        open_pr = get_json_data(prefix + repo_name + "/change_requests.json", month)
        accepted_pr = get_json_data(prefix + repo_name + "/change_requests_accepted.json", month)
        review_pr = get_json_data(prefix + repo_name + "/change_requests_reviews.json", month)
        pr_rr_time = get_json_data(prefix + repo_name + "/change_request_response_time.json", month)
        pr_resol_duration = get_json_data(prefix + repo_name + "/change_request_resolution_duration.json", month)
        if f is not None and download:
            f.write(f"#### PR for {repo_name}:\n")
        print(f"PR for {repo_name}:\n")
        if month is None:
            open_pr.popitem()
            open_pr = format_date_data(open_pr)
            accepted_pr.popitem()
            accepted_pr = format_date_data(accepted_pr)
            review_pr.popitem()
            review_pr = format_date_data(review_pr)
            if len(open_pr) > 0:
                plotext_plot(list(open_pr.keys()), list(open_pr.values()), repo_name, "open_pr", f, download, color="blue")
            if len(accepted_pr) > 0:
                plotext_plot(list(accepted_pr.keys()), list(accepted_pr.values()), repo_name, "accepted_pr", f, download, color="blue")
            if len(review_pr) > 0:
                plotext_plot(list(review_pr.keys()), list(review_pr.values()), repo_name, "review_pr", f, download, color="blue")
        else:
            print(f"\topen pr: {open_pr}\n")
            print(f"\taccepted pr: {accepted_pr}\n")
            print(f"\treview pr: {review_pr}\n")
    def diaplay_metrics_all(self, repo_name: str, month=None, f=None, download=False):
        self.display_stars(repo_name, month, f, download)
        self.display_active_dates_times(repo_name, month, f, download)
        self.display_technical_fork(repo_name, month, f, download)
        self.display_issues(repo_name, month, f, download)
        self.display_participants(repo_name, month, f, download)
        self.display_contributors(repo_name, month, f, download)
        self.display_code_change_line(repo_name, month, f, download)
        self.display_pr(repo_name, month, f, download)


    ##########################################
    #               NetWorks                 #
    ##########################################
    def display_develop_networks(self, repo_name: str, month=None, f=None, download=False):
        pass

    def display_repo_networks(self, repo_name: str, month=None, f=None, download=False):
        pass

    # command line arguments parser
    def run(self, args):
        repo_name = args.repo
        month = args.month if args.month else None
        index = args.index
        metric = args.metric
        download = True if args.d else False
        download_type = args.d

        if repo_name and download and (index in self.indexes or metric in self.metrics):
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
                if index is not None:
                    self.indexes[index](repo_name, month, f, download)
                if metric is not None:
                    f.write("### Repo Metrics\n")
                    self.metrics[metric](repo_name, month, f, download)
                if os.path.exists(file_path):
                    print(f"The download file write successfully in {file_path}.")
                else:
                    print("The download file failed to write.")
            f.close()
        elif repo_name and (index in self.indexes or metric in self.metrics):
            print("repo.name: " + repo_name)
            print("repo.url: " + "https://github.com/" + repo_name)
            if index is not None:
                print("repo indexes: ")
                self.indexes[index](repo_name, month)
            if metric is not None:
                print("repo metrics: ")
                self.metrics[metric](repo_name, month)
        else:
            print("Please provide a repository name and a valid metric.")


def main():
    parser = argparse.ArgumentParser(description="Get OpenRank data for a GitHub repository.")
    parser.add_argument("-repo", help="GitHub repository name in the format <owner>/<repo>.")
    parser.add_argument("-index", choices=["openrank", "activity", "attention", "all"], help="Metric to retrieve."
                                                                                             "See each metrics specification on: https://github.com/X-lab2017/open-digger/")
    parser.add_argument("-metric", choices=["active-dates-times", "stars", "technical_fork", "participants",
                                            "contributors", "bus_factor", "issues", "code_change_line",
                                            "pr", "network", "all"])
    parser.add_argument("-month", help="Month to retrieve OpenRank data for in the format YYYY-MM.")
    parser.add_argument("-d", choices=["md"], help="Download OpenRank info in Markdown or text format.")
    args = parser.parse_args()

    open_digger = OpenDigger()
    open_digger.run(args)
