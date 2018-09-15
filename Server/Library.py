from lxml import html
import requests
import re
import time


class Library(object):
    def __init__(self):
        self.library_visit = {}
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 "
                          "(KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36"
        }

    # 爬取进馆统计页面
    def get_visit(self):
        login_url = "http://lib.gzhu.edu.cn:8080/bookle/goLibTotal/index"
        view_response = requests.get(login_url, headers=self.headers)
        html_text = html.fromstring(view_response.text)
        total_view = html_text.xpath('//*[@id="total"]')[0].text

        total = re.findall("\d+", total_view)[0]

        college = html_text.xpath('//*[@id="view"]/table/tr/td[1]')
        amount = html_text.xpath('//*[@id="view"]/table/tr/td[2]')
        visit = html_text.xpath('//*[@id="view"]/table/tr/td[3]')
        average = html_text.xpath('//*[@id="view"]/table/tr/td[4]')

        college_list = []
        for i, item in enumerate(college):
            temp = []
            temp.append(college[i].text)
            temp.append(amount[i].text)
            temp.append(visit[i].text)
            temp.append(average[i].text)

            college_list.append(temp)

        self.library_visit = {"total": total, "update_time": time.strftime("%Y-%m-%d %H:%M:%S"), "college_list": college_list}

        # 存入本地文件
        with open("record_file/visit_data.txt", "w") as visit:
            visit.write(str(self.library_visit))

    # 设置定时器，15min更新一次
    def timer(self):
        hour = int(time.strftime("%H"))
        min = int(time.strftime("%M"))
        self.get_visit()
        if (hour > 0 and min < 30) and hour < 6:
            pass
        else:
            while hour >= 6:
                time.sleep(900)      # 15min执行一次
                self.get_visit()
                print(time.strftime("%Y-%m-%d %H:%M:%S"))


print("启动")
run = Library()
run.timer()