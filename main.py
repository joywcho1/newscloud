# -*- coding: utf-8, utf-8-si, euc-kr -*-

# ================================================================================
# 모듈 추가
# ================================================================================

# GUI 관련 모듈
import tkinter as tk
from tkinter import ttk, scrolledtext

# 파일 관련 모듈
import json
import csv

# 온라인통신 관련 모듈
import requests
import re
from bs4 import BeautifulSoup
import webbrowser

# NewsCloud 관련 모듈
from articleparser import ArticleParser
from writer import Writer

# 시스템 관련 모듈
import os
import sys

# 시간 관련 모듈
from time import sleep
from datetime import datetime, date, timedelta

# 멀티프로세스 관련 모듈
from multiprocessing import Pool, current_process, Lock

# 워드클라우드 관련 모듈
from collections import Counter
from wordcloud import WordCloud


# 기타 로그, 예외처리
# import logging
class NewsCloud(object):

    def __init__(self, selected_categories, cloud_start_date, cloud_end_date):
        self.selected_categories = selected_categories
        self.start_date = cloud_start_date
        self.end_date = cloud_end_date

    @staticmethod
    def sentence_f(top_word, left_sentence):

        inc_sent = []
        exc_sent = []
        split_word = []
        for left_sentence_v, left_sentence_i in left_sentence:
            if top_word in left_sentence_v:
                inc_sent.append((left_sentence_v, left_sentence_i))
            else:
                exc_sent.append((left_sentence_v, left_sentence_i))

        if len(inc_sent) > 0:
            tu_word, tu_cnt = inc_sent[0]
            split_word = tu_word.split()
            # print('split_word : ', split_word)

        return exc_sent, inc_sent, split_word

    @staticmethod
    def read_file(file_name, col):
        if os.path.isfile(file_name):
            f = open(file_name, 'r', encoding='utf-8-sig')
            list_csv = csv.reader(f)

            all_split_sentence_list = []
            all_split_word_list = []

            for line in list_csv:
                split_sentence_list = []

                line_contents = str(line[col]).replace('”', '')

                split_sentence = line_contents.split('. ')
                for sentence_v in split_sentence:
                    split_sentence_list.append((sentence_v, len(sentence_v)))

                all_split_sentence_list.extend(split_sentence_list)

                line_contents = re.sub(r'\.', '', line_contents)
                split_word = line_contents.split()
                all_split_word_list.extend(split_word)

            f.close()
            return all_split_sentence_list, all_split_word_list
        else:
            raise Exception('파일이 존재하지 않습니다.')

    @staticmethod
    def divide_sentence(sentence, sentence_len, div_num):
        rst_sent = []
        sentence = re.sub(r'\(.+?\)', '', sentence)
        sentence = sentence.replace('(', '').replace(')', '')
        list_sentence = sentence.split()
        tot_num = len(list_sentence)

        dived_num = (tot_num // div_num) + 1

        for n in range(div_num):
            if len(list_sentence[n * dived_num:(n + 1) * dived_num]) < 1:
                break
            rst_sent.append((' '.join(list_sentence[n * dived_num:(n + 1) * dived_num]), sentence_len))
        return rst_sent

    def count_sentence_list(self, category_name, file_name, a_type, col):

        if a_type == 'A':
            stopwords = []
            max_word = 30
        elif a_type == 'S':
            stopwords = []
            max_word = 55
        elif a_type == 'N':
            stopwords = ['대해', '위한', '없다', '다시', '어떤', '것도', '것은', '있다', '있는', '것이다', '한다']
            max_word = 99
        else:
            stopwords = []
            max_word = 50

        sentence_list, list_word = self.read_file(file_name, col)

        rst_word_list = []
        rst_sent_list = []
        rst_sent = []

        for word_v in list_word:
            word_v = word_v.replace('.', '').strip()

            if len(word_v) > 1:
                rst_word_list.append(word_v)

        count_word_list = Counter(rst_word_list)
        top_words_tuple = count_word_list.most_common(200)

        if len(top_words_tuple) < 1:
            print(f"[Error] {category_name}의 기사가 적어 NewsCloud 를 생성할 수 없습니다.")
            return None

        if a_type != 'N':
            sel_word = []

            for top_word_v, top_word_i in top_words_tuple:
                sel_word.append(top_word_v)

            top_w = sel_word[0]

            sentence_list.sort(key=lambda element: element[1], reverse=True)
            re_sentence = sentence_list
            n = 0

            for sentence_i in range(len(sentence_list)):
                n += 1
                if len(re_sentence) < 1:
                    break
                exc_sent, long_sent, split_word = self.sentence_f(top_w, re_sentence)

                if len(long_sent) < 1 or len(exc_sent) < 1:
                    rst_sent.extend(exc_sent)
                    break

                rst_sent.extend(long_sent)

                if a_type == 'A':
                    m = 0
                    print(category_name)
                    for v, i in rst_sent:
                        m += 1
                        print(m, v)
                        if m > 20:
                            break

                re_sel_word = []

                for sel_word_v in sel_word:
                    if sel_word_v in split_word:
                        continue
                    else:
                        re_sel_word.append(sel_word_v)

                sel_word = re_sel_word
                top_w = sel_word[0]
                re_sentence = exc_sent

            if len(rst_sent) < 1:
                print(f"[Error] {category_name}의 기사 문장이 적어 NewsCloud 를 생성할 수 없습니다.")
                return None

            if a_type == 'S':
                div_num = 4

                for sent_v, sent_i in rst_sent:
                    rst_sent_v = self.divide_sentence(sent_v, sent_i, div_num)
                    rst_sent_list.extend(rst_sent_v)

        wc = WordCloud(
            font_path='C:\\Users\\JOY\\PycharmProjects\\newscloud\\NotoSansCJKkr-hinted\\NotoSansMonoCJKkr-Bold.otf',
            stopwords=stopwords,
            background_color='black',
            width=800,
            height=800,
            # contour_width =1,
            # contour_color= 'firebrick',
            # mask= test_mask3,
            max_words=max_word,
            max_font_size=200)

        # rst_sent top_words_tuple, rst_sent_list
        if a_type == 'A':
            wc.generate_from_frequencies(dict(rst_sent))
        elif a_type == 'S':
            wc.generate_from_frequencies(dict(rst_sent_list))
        elif a_type == 'N':
            wc.generate_from_frequencies(dict(top_words_tuple))

        file_name = category_name + '_' + self.start_date + '_' + self.end_date + '.jpg'
        wc.to_file(file_name)

        webbrowser.open(file_name)


class ArticleCrawler(object):

    def __init__(self, all_categories, selected_categories, crawler_start_date, crawler_end_date):
        self.all_categories = all_categories
        self.selected_categories = selected_categories
        self.start_date = crawler_start_date
        self.end_date = crawler_end_date

    @staticmethod
    def find_news_total_page(url):
        """당일 기사 목록 전체페이지수를 반환하기"""
        try:
            # print(url) # headers = 안쓰면 에러 발생
            request_content = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
            document_content = BeautifulSoup(request_content.content, 'html.parser')
            headline_tag = document_content.find('div', {'class': 'paging'}).find('strong')
            regex = re.compile(r'<strong>(?P<num>\d+)')
            match = regex.findall(str(headline_tag))
            return int(match[0])
        except Exception as e:
            print(f"{url}에서 에러가 발생했습니다.", e)
            return 0

    def make_news_page_url(self, category_url, make_start_date, make_end_date):
        """시작일 ~ 마지막일까지 가져올 수 있는 모든 페이지 주소 생성하기"""
        made_urls = []
        start_date_split = make_start_date.split(',')
        end_date_split = make_end_date.split(',')
        start_date_form = date(int(start_date_split[0]), int(start_date_split[1]), int(start_date_split[2]))
        end_date_form = date(int(end_date_split[0]), int(end_date_split[1]), int(end_date_split[2]))
        delta_day = end_date_form - start_date_form

        for i in range(delta_day.days + 1):
            day = start_date_form + timedelta(days=i)
            url = category_url + str(day).replace('-', '')
            # print(url)
            total_page = self.find_news_total_page(url + "&page=10000")

            for page in range(1, total_page + 1):
                made_urls.append(url + "&page=" + str(page))

        return made_urls

    @staticmethod
    def get_url_data(url, max_tries=5):
        """url 로부터 내용 가져오기"""
        remaining_tries = int(max_tries)
        while remaining_tries > 0:
            try:
                return requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
            except Exception as e:
                print(e)
                sleep(5)
            remaining_tries = remaining_tries - 1
        raise Exception("")

    def crawling(self, category_name):
        # 분산 처리 실행
        print(f"\r\n [{str(os.getpid())}] 프로세스에 {category_name} 프로세서가 활성화 됩니다.")

        # 주제별 일자별 CSV 화일 준비, 저장할 Instance 생성
        writer = Writer(category_name=category_name, start_date=self.start_date, end_date=self.end_date)

        proc_name = current_process().name

        if not self.all_categories.get(category_name) is None:
            # URL 기본
            url = "http://news.naver.com/main/list.nhn?mode=LSD&mid=sec&sid1=" + str(
                self.all_categories.get(category_name)) + "&date="

            # start_year 년 start_month 월 ~ end_year 의 end_month 날짜까지 주제별 url 만들기 함수 호출해서 뉴스 목록페이지의 url list 생성하기
            day_urls = self.make_news_page_url(url, self.start_date, self.end_date)
            print(f"\r\n [{category_name}] 뉴스의 URL 을 수집했습니다. 각 뉴스를 크롤링합니다. \n")

            # 목록에서 뉴스의 원본 url 을 추출하고 원본으로 접근하기
            for n, URL in enumerate(day_urls):
                sys.stdout.write(f"\r [ID:{proc_name}] / [주제:{category_name}] / "
                                 f"[진행률({n}/{len(day_urls)}):{100 * n / len(day_urls):3.2f}%]")
                sys.stdout.flush()

                regex = re.compile("date=(\d+)")
                news_date = regex.findall(URL)[0]
                request = self.get_url_data(URL)
                request.encoding = 'euc-kr'
                document = BeautifulSoup(request.content, 'html.parser')

                # html - newsflash_body - type06_headline, type06
                # 목록에서 원본이 있는 url 수집
                post_temp = document.select('.newsflash_body .type06_headline li dl')
                post_temp.extend(document.select('.newsflash_body .type06 li dl'))

                # 원본 url 저장
                post = []
                for line in post_temp:
                    detail_url = line.a.get('href')
                    post.append(detail_url)  # 해당되는 page 에서 모든 기사들의 URL 을 post 리스트에 넣음
                del post_temp

                post = list(set(post))
                # 원본 기사 수집
                for url_i, content_url in enumerate(post):  # 기사 URL
                    try:
                        sleep(0.01)
                        request_content = self.get_url_data(content_url)
                        document_content = BeautifulSoup(request_content.content, 'html.parser')
                    except Exception as error_docu:
                        print('')
                        print('any_error', category_name, error_docu, content_url, url_i)
                        del request_content, document_content

                    text_title = ''
                    try:
                        # 기사 제목 가져옴
                        if category_name == '스포츠':
                            tag_headline = document_content.select('h4.title')
                            if len(tag_headline) < 1:
                                tag_headline = document_content.select('h3.info_tit')
                        elif category_name == '연예':
                            tag_headline = document_content.select('h2.end_tit')
                        else:
                            tag_headline = document_content.find_all('h3', {'id': 'articleTitle'},
                                                                     {'class': 'tts_head'})
                            if len(tag_headline) < 1:
                                tag_headline = document_content.select('h4.title')
                                if len(tag_headline) < 1:
                                    tag_headline = document_content.select('h3.info_tit')
                                    if len(tag_headline) < 1:
                                        tag_headline = document_content.select('h2.end_tit')

                        text_headline = str(tag_headline[0].find_all(text=True))
                        text_title = ArticleParser.clear_headline(text_headline)
                    except Exception as error_headline:
                        print('error_headline', error_headline, category_name, content_url)

                    # 본문내용 초기화 및 기사 본문 가져옴
                    text_journalist = ''
                    text_email = ''
                    text_sentence = ''
                    try:
                        if category_name == '스포츠':
                            tag_content = document_content.find_all('div', {'id': 'newsEndContents'})
                        elif category_name == '연예':
                            tag_content = document_content.find_all('div', {'id': 'articeBody'})
                        else:
                            tag_content = document_content.find_all('div', {'id': 'articleBodyContents'})
                            if len(tag_content) < 1:
                                tag_content = document_content.find_all('div', {'id': 'newsEndContents'})
                                if len(tag_content) < 1:
                                    tag_content = document_content.find_all('div', {'id': 'articeBody'})
                        text_content = str(tag_content[0].find_all(text=True))
                        text_journalist, text_email, text_sentence = ArticleParser.clear_content(text_content)
                    except Exception as error_content:
                        print('error_content', error_content, category_name, content_url)

                    # 기사 언론사 가져옴
                    text_company = ''
                    try:

                        if category_name == '스포츠':
                            tag_company = document_content.find_all('meta', {'property': 'og:article:author'})
                        elif category_name == '연예':
                            tag_company = document_content.find_all('meta', {'property': 'og:article:author'})
                        else:
                            tag_company = document_content.find_all('meta', {'property': 'me2:category1'})
                            if len(tag_company) < 1:
                                tag_company = document_content.find_all('meta', {'property': 'og:article:author'})

                        text_company = text_company + str(tag_company[0].get('content'))
                        text_company.replace('네이버 스포츠 | ', '').replace(' | 네이버 TV연예', '')

                    except Exception as error_company:
                        print('error_company', error_company, category_name, content_url)

                    # CSV 작성
                    if text_company == '' or text_title == '' or text_sentence == '':
                        continue
                    else:
                        write_csv = writer.get_writer_csv()
                        write_csv.writerow(
                            [news_date, category_name, text_company, text_journalist, text_email,
                             text_title, text_sentence,
                             content_url])

                        del text_company, text_sentence, text_headline
                        del text_journalist, text_email
                        del tag_company
                        del tag_content, tag_headline
                        del request_content, document_content
            writer.close()


if __name__ == '__main__':

    def draw_word():
        selected_categories_file = "wanted_categories.txt"
        if os.path.isfile(selected_categories_file):
            with open(selected_categories_file, encoding='UTF-8') as f:
                contents_list = f.read()
            contents_list = contents_list.replace(" ", "")
            selected_categories = contents_list.split(',')
        else:
            selected_categories = []
            print(f"==> {selected_categories_file} 파일이 존재하지 않습니다.")
        print()

        from_day = start_date.get().replace('년', '').replace('월', '').replace('일', '')
        to_day = end_date.get().replace('년', '').replace('월', '').replace('일', '')
        cls_news_cloud = NewsCloud(selected_categories, from_day, to_day)

        a_type = 'N'
        col = 5

        for category_name in selected_categories:
            file_name = category_name + '_' + from_day + '_' + to_day + '.csv'
            if os.stat(file_name).st_size < 10:
                print(f"[{category_name}]은 생성하지 않습니다.")
            else:
                cls_news_cloud.count_sentence_list(category_name, file_name, a_type, col)
                log_text.insert(tk.END, f"[{category_name}] 기사의 NewsCloud 이미지를 저장했습니다. \n")


    def crawl_news():
        # 특정 폴더의 파일 존재 여부 확인
        all_categories_file = "all_categories.json"
        if os.path.isfile(all_categories_file):
            with open(all_categories_file, encoding='UTF-8') as j:
                all_categories = json.load(j)
        else:
            print(f"==> {all_categories_file} 파일이 존재하지 않습니다.")

        # 특정 폴더의 파일 존재 여부 확인
        selected_categories_file = "wanted_categories.txt"
        if os.path.isfile(selected_categories_file):
            with open(selected_categories_file, encoding='UTF-8') as f:
                contents_list = f.read()
            contents_list = contents_list.replace(" ", "")
            selected_categories = contents_list.split(',')
        else:
            print(f"==> {selected_categories_file} 파일이 존재하지 않습니다.")
            selected_categories = []

        # 분산 크롤링 시작
        now = datetime.now()
        print(f"{now} 에 수집을 시작합니다. {selected_categories}, {start_date.get()} ~ {end_date.get()}")
        from_day = start_date.get().replace('년', ',').replace('월', ',').replace('일', ',')
        to_day = end_date.get().replace('년', ',').replace('월', ',').replace('일', ',')
        # ArticleCrawler 인스턴스 생성하기
        crawler = ArticleCrawler(all_categories, selected_categories,
                                 from_day,
                                 to_day)

        proc = Pool(3)
        proc.map(crawler.crawling, selected_categories)
        proc.close()
        proc.join()
        dummy_now = datetime.now()
        speed_crawling = dummy_now - now
        print(speed_crawling)
        log_now = f"{now.strftime('%Y년%m월%d일 %H시%M분%S초'.encode('unicode-escape').decode()).encode().decode('unicode-escape')} " \
                  f"시작. {dummy_now.strftime('%Y년%m월%d일 %H시%M분%S초'.encode('unicode-escape').decode()).encode().decode('unicode-escape')}"
        sleep(3)
        main_label.configure(foreground='red', text=f"{speed_crawling}동안 뉴스를 수집했습니다.")
        dummy_label.configure(foreground='blue', text=f"{log_now} 완료")
        print(f"{log_now} 완료")


    # master GUI 인스턴스 생성
    new_cloud_gui = tk.Tk()
    new_cloud_gui.title("뉴스클라우드")

    # 오늘 날짜
    today = date.today()

    # 메인 Label
    main_label = tk.Label(new_cloud_gui, text=f"시작일자와 종료일자를 정하고 실행 버튼을 누르세요.")
    main_label.grid(column=0, row=0, sticky='W', columnspan=6)

    # 더미 Label
    dummy_label = ttk.Label(new_cloud_gui, text=f"")
    dummy_label.grid(column=0, row=1, sticky='W', columnspan=6)

    # 시작날짜 변수선언
    start_date = tk.StringVar()
    start_date_entered = tk.Entry(new_cloud_gui, width=15, textvariable=start_date)
    start_date_entered.grid(column=0, row=2)
    start_date_entered.insert(0, today.strftime('%Y년%m월%d일'.encode('unicode-escape').decode()).encode().decode(
        'unicode-escape'))

    # 시작날짜 Label
    start_date_label = tk.Label(new_cloud_gui, width=6, text=" 부터")
    start_date_label.grid(column=1, row=2)

    # 마지막날짜 변수선언
    end_date = tk.StringVar()
    end_date_entered = tk.Entry(new_cloud_gui, width=15, textvariable=end_date)
    end_date_entered.grid(column=2, row=2)
    end_date_entered.insert(0, today.strftime('%Y년%m월%d일'.encode('unicode-escape').decode()).encode().decode(
        'unicode-escape'))

    # 마지막날짜 Label
    end_date_label = tk.Label(new_cloud_gui, width=6, text=" 까지")
    end_date_label.grid(column=3, row=2)

    # 뉴스크롤링 시작 Button
    start_crawling = tk.Button(new_cloud_gui, text='크롤링시작', command=crawl_news)
    start_crawling.grid(column=4, row=2)

    # 뉴스클라우드 생성 시작 Button
    news_cloud = tk.Button(new_cloud_gui, text='NewsCloud', command=draw_word)
    news_cloud.grid(column=5, row=2)

    # 로그를 표시하기 위한 텍스트박스
    top_padding = 10
    scroll_w = 60
    scroll_h = 5
    log_text = scrolledtext.ScrolledText(new_cloud_gui, width=scroll_w, height=scroll_h, wrap=tk.WORD)
    log_text.grid(column=0, columnspan=6, row=3, sticky='WE', pady=(top_padding, 0))

    scroll_w = 60
    scroll_h = 5
    log1_text = scrolledtext.ScrolledText(new_cloud_gui, width=scroll_w, height=scroll_h, wrap=tk.WORD)
    log1_text.grid(column=0, columnspan=6, row=4, sticky='WE')

    # Place cursor into StringVar
    start_date_entered.focus()

    # ===========================================
    # Start GUI
    # ===========================================
    new_cloud_gui.mainloop()
