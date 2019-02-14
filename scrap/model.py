from urllib.parse import urlencode
from urllib.request import Request
from selenium import webdriver
from scrap.tools import *
from scrap.writer import *
from scrap.downloader import *

class BasicModel:
    def debug_print(self, name):
        if self.debug_mode == 'True':
            print('BasicModel ---- ', name)

    def __init__(self, config):
        self.config_init(path=config['path'], name=config['name'], popup_url=config['popup_url'], root_url=config['root_url'], notice_url=config['notice_url'], data_list_url=config['data_list_url'],
                      data_detail_url=config['data_detail_url'], download_url=config['download_url'], hyperlink_column=config['hyperlink_column'], state_column=config['state_column'],
                      state_false=config['state_false'], state_true=config['state_true'], debug_mode=config['debug_mode'], download_mode=config['download_mode'], outformat=config['outformat'])
        return

    def config_init(self, path, name, popup_url, root_url, notice_url, data_list_url, data_detail_url, download_url, hyperlink_column="공고명", data_hyperlink_column='제목', state_column="공고상태", state_false="공고마감",
                 state_true = "공고중", debug_mode='False', download_mode='False', outformat='excel'):
        self.path = os.path.join(path, name)
        self.name = name
        self.popup_url = popup_url
        self.root_url = root_url
        self.notice_url = notice_url
        self.data_list_url = data_list_url
        self.data_detail_url = data_detail_url
        self.download_url = download_url

        ## TRUE/FALSE 값
        self.debug_mode = debug_mode
        self.download_mode = download_mode

        self.hyperlink_column = hyperlink_column
        self.data_hyperlink_column = data_hyperlink_column
        self.state_column = state_column
        self.state_true = state_true
        self.state_false = state_false
        self.outformat = outformat

        self.debug_print('config_init')
        return


    def execute(self):
        self.debug_print('execute')

        ##폴더 생성
        make_dir(self.path)

        ##데이터 분석 (overwrite가 필요함.
        self.make_noticeList()

        ##다운로드
        self.download_file_list()

        ##엑셀프로그램 저장.
        self.export_file()

        ##팝업
        self.check_Popup()
        return

    def check_Popup(self):
        self.debug_print('check_Popup')
        check_Popup_State(df=self.notice_df, url=self.popup_url, state_column=self.state_column, state_false=self.state_false, debug_mode=self.debug_mode)
        return

    def export_file(self):
        self.debug_print('export_file')
        save_file(df=self.notice_df, root_url=self.root_url, path=self.path, name=self.name, outformat=self.outformat)
        return

    def download_file_list(self):
        self.debug_print('download_file_list')
        for idx, row in self.notice_df.iterrows():
            path = os.path.join(self.path, re.sub('[?.!/;:,<>]', '', row[self.hyperlink_column]).strip())
            if self.download_mode == 'True':
                if not row[self.state_column] == self.state_false:
                    download_file(path=path, root_url=self.root_url, data_url=row['입찰서류URL'],download_url=self.download_url)
            else:
                download_file(path=path, root_url=self.root_url, data_url=row['입찰서류URL'], download_url=self.download_url)
        return


    def get_data_document(self, url):
        totalURL = self.root_url + str(url)
        with urlopen(totalURL) as response:
            html = response.read()
            soup = BeautifulSoup(html, 'html5lib')
            ps = soup.find_all("p")
            divs = soup.find_all("div")

            resultStr = ''
            for idx, p in enumerate(ps):
                tempStr = str(p.get_text())
                if "번호" in tempStr and "제목" in tempStr:
                    resultStr = tempStr

            for idx, div in enumerate(divs):
                tempStr = str(div.get_text())
                if "번호" in tempStr and "제목" in tempStr:
                    resultStr = tempStr
            resultNum = re.sub("[^0-9]", "", resultStr.split("번호")[1].split("제목")[0])
        return resultNum


    ##입찰서류URL과 URL을 만들어야 한다.
    def make_noticeList(self):
        self.debug_print('make_noticeList')

        ##['공고번호', '공고명', '공고분야', '공고기간', '공고상태', "URL', '입찰서류번호', '입찰서류URL']
        page = 1
        notice_df = self.get_notice_dataframe(self.notice_url, self.hyperlink_column, page)
        while (True):
            page = page + 1
            next_notice_df = self.get_notice_dataframe(self.notice_url, self.hyperlink_column, page)
            if len(next_notice_df.index) == 0:
                break
            else:
                notice_df = pd.merge(notice_df, next_notice_df, how='outer')

        ###종료조건
        if len(notice_df.index) == 0:
            self.notice_df = notice_df
            return

        notice_df['입찰서류번호'] = notice_df['URL'].apply(self.get_data_document)
        notice_df['입찰서류URL'] = self.data_detail_url + notice_df['입찰서류번호']
        self.notice_df = notice_df
        return



    def get_notice_dataframe(self, url, hyperlink_column, page, drive_option='urlopen'):
        total_url = self.root_url + url + str(page)
        if drive_option == 'urlopen':
            with urlopen(total_url) as response:
                html = response.read()
                soup = BeautifulSoup(html, 'html5lib')
        elif drive_option == 'driver':
            with webdriver.PhantomJS(
                    executable_path=os.path.join(os.getcwd(), 'phantomjs-2.1.1-windows', 'phantomjs-2.1.1-windows',
                                                 'bin', 'phantomjs.exe')) as browser:
                browser.get(total_url)
                html = browser.execute_script('return document.documentElement.outerHTML')
                soup = BeautifulSoup(html, "html5lib")
                browser.quit()
        elif drive_option == 'post':
            total_url, post_fields = parse_url_to_postForm(total_url)
            request = Request(total_url, urlencode(post_fields).encode())
            json = urlopen(request).read().decode()
            soup = BeautifulSoup(json, 'html5lib')

        trs = soup.find_all("tr")
        columns = []
        data = []
        for idx, tr in enumerate(trs):
            if idx == 0:
                ths = tr.find_all("th")
                for idx2, th in enumerate(ths):
                    columns.append(str(th.get_text()).strip())

                ##URL 추가코딩
                columns.append('URL')
            else:
                content = []
                tds = tr.find_all("td")
                URL = ''
                for idx2, td in enumerate(tds):
                    if columns[idx2] == hyperlink_column:
                        title = td.get('title')
                        if title == None or title == 'None':
                            title = str(td.find('a').get('title')).strip()
                        if title == None or title == 'None':
                            title = str(td.find('a').get_text().strip())
                        content.append(title)
                        URL = td.find('a')['href']
                    else:
                        content.append(str(td.get_text()).strip())
                content.append(URL)
                data.append(content)
        if len(data[0]) == len(columns):
            df = pd.DataFrame(columns=columns, data=data)
        else:
            df = pd.DataFrame(columns=columns)
        return df

######################################################################################################################################################################

class noticeList_Model(BasicModel):
    def debug_print(self, name):
        if self.debug_mode == 'True':
            print('noticeList_Model ---- ', name)


########################################################################################################################################################################

class tenderNoticeList_Model(BasicModel):
    def debug_print(self, name):
        if self.debug_mode == 'True':
            print('tenderNoticeList_Model ---- ', name)

    ##입찰서류URL과 URL을 만들어야 한다.
    def make_noticeList(self):
        self.debug_print('make_noticeList')

        ##데이터 가져오기
        ##['번호', '제목', '작성자', '날짜', '첨부파일', '조회', 'URL']
        page = 1
        data_df = self.get_notice_dataframe(self.data_list_url, self.data_hyperlink_column, page, 'urlopen')
        while (True):
            page = page + 1
            next_data_df = self.get_notice_dataframe(self.data_list_url, self.data_hyperlink_column, page, 'urlopen')
            if len(next_data_df.index) == 0:
                break
            else:
                data_df = pd.merge(data_df, next_data_df, how='outer')

        ##['공고번호', '공고명', '공고분야', '공고기간', '공고상태', "URL', '입찰서류번호', '입찰서류URL']
        self.debug_print(self.notice_url)
        page = 1
        notice_df = self.get_notice_dataframe(self.notice_url, self.hyperlink_column, page, drive_option='driver')
        while (True):
            page = page + 1
            next_notice_df = self.get_notice_dataframe(self.notice_url, self.hyperlink_column, page, drive_option='driver')
            if len(next_notice_df.index) == 0:
                break
            else:
                notice_df = pd.merge(notice_df, next_notice_df, how='outer')

        self.debug_print(len(notice_df.index))
        self.debug_print(notice_df.columns)
        ###종료조건
        if len(notice_df.index) == 0:
            self.notice_df = notice_df
            return

        data_df[self.data_hyperlink_column] = data_df[self.data_hyperlink_column].apply(removeExtra)
        matching_list = find_matching_tender2(notice_df, data_df, 2)
        notice_df['입찰서류번호'] = matching_list
        notice_df['입찰서류URL'] = self.data_detail_url + notice_df['입찰서류번호']
        self.notice_df = notice_df
        return

#####################################################################################################################################################################

class csNoticeList_Model(BasicModel):
    def debug_print(self, name):
        if self.debug_mode == 'True':
            print('csNoticeList_Model ---- ', name)

    def get_notice_dataframe(self, url, hyperlink_column, page, drive_option='urlopen'):
        total_url = self.root_url + url + str(page)
        if drive_option == 'urlopen':
            with urlopen(total_url) as response:
                html = response.read()
                soup = BeautifulSoup(html, 'html5lib')
        elif drive_option == 'driver':
            with webdriver.PhantomJS(
                    executable_path=os.path.join(os.getcwd(), 'phantomjs-2.1.1-windows', 'phantomjs-2.1.1-windows',
                                                 'bin', 'phantomjs.exe')) as browser:
                browser.get(total_url)
                html = browser.execute_script('return document.documentElement.outerHTML')
                soup = BeautifulSoup(html, "html5lib")
                browser.quit()
        elif drive_option == 'post':
            total_url, post_fields = parse_url_to_postForm(total_url)
            request = Request(total_url, urlencode(post_fields).encode())
            json = urlopen(request).read().decode()
            soup = BeautifulSoup(json, 'html5lib')

        trs = soup.find_all("tr")
        columns = []
        data = []
        for idx, tr in enumerate(trs):
            if idx == 0:
                ths = tr.find_all("th")
                for idx2, th in enumerate(ths):
                    columns.append(str(th.get_text()).strip())

                ##URL 추가코딩
                columns.append('URL')
            else:
                content = []
                tds = tr.find_all("td")
                URL = ''
                for idx2, td in enumerate(tds):
                    if columns[idx2] == hyperlink_column:
                        title = td.get('title')
                        if title == None or title == 'None':
                            title = str(td.find('a').get('title')).strip()
                        if title == None or title == 'None':
                            title = str(td.find('a').get_text().strip())
                        content.append(title)
                        URL = td.find('a')['href']
                    else:
                        content.append(str(td.get_text()).strip())
                content.append(URL)
                data.append(content)
        if len(data[0]) == len(columns):
            df = pd.DataFrame(columns=columns, data=data)
        else:
            df = pd.DataFrame(columns=columns)

        page_flag = False
        page_list = []
        ul = soup.find('ul', class_=['pagination'])
        if len(ul) > 0 :
            lis = ul.find_all('li', class_=lambda x: x != 'disabled')
            if len(lis) > 0 :
                for li in lis:
                    page_list.append(int(li.get_text()))

        if len(page_list) > 0:
            if max(page_list) > page :
                page_flag = True
        return df, page_flag

    ##입찰서류URL과 URL을 만들어야 한다.
    def make_noticeList(self):
        self.debug_print('make_noticeList')

        ##['공고번호', '공고명', '공고분야', '공고기간', '공고상태', "URL', '입찰서류번호', '입찰서류URL']
        self.debug_print(self.notice_url)
        page = 1
        notice_df, page_flag = self.get_notice_dataframe(self.notice_url, self.hyperlink_column, page, drive_option='post')
        while (page_flag):
            page = page + 1
            next_notice_df, page_flag = self.get_notice_dataframe(self.notice_url, self.hyperlink_column, page,
                                                       drive_option='post')
            if len(next_notice_df.index) == 0:
                break
            else:
                next_notice_df = next_notice_df[~next_notice_df[self.hyperlink_column].str.contains('테스트')]
                next_notice_df = next_notice_df[~next_notice_df[self.hyperlink_column].str.contains('test')]
                if len(next_notice_df.index) == 0:
                    break
                notice_df = pd.merge(notice_df, next_notice_df, how='outer')

        ###종료조건
        if len(notice_df.index) == 0:
            self.notice_df = notice_df
            return
        else:
            notice_df = notice_df[~notice_df[self.hyperlink_column].str.contains('테스트')]
            notice_df = notice_df[~notice_df[self.hyperlink_column].str.contains('test')]
            if len(notice_df.index) == 0:
                self.notice_df = notice_df
                return

        notice_df['입찰서류URL'] = notice_df['URL'].apply(self.get_csDetail_url)
        self.notice_df = notice_df
        return

    def get_csDetail_url(self, javascript):
        url = self.data_detail_url
        candidates = javascript.split('csDetail')
        if len(candidates) == 2:
            candidates = candidates[1].split('\'')
            if len(candidates) == 5:
                custom_option = {}
                custom_option['notice_seq'] = candidates[1]
                custom_option['notice_status_code'] = candidates[3]
                url, post_fields = parse_url_to_postForm(url)
                url = merge_postForm_to_url(url, post_fields=post_fields, custom_option=custom_option)
        return url

    def export_file(self):
        self.debug_print('export_file')
        notice_url, post_fields = parse_url_to_postForm(self.notice_url)
        self.notice_df['URL'] = notice_url
        self.notice_df = self.notice_df.drop(columns=['입찰서류URL'])
        save_file(df=self.notice_df, root_url=self.root_url, path=self.path, name=self.name, outformat=self.outformat)
        return

##########################################################################################################################################################################################################################
class ripcNoticeList_Model(BasicModel):
    def debug_print(self, name):
        if self.debug_mode == 'True':
            print('ripcNoticeList_Model ---- ', name)

    ##입찰서류URL과 URL을 만들어야 한다.
    def make_noticeList(self):
        self.debug_print('make_noticeList')

        ##['공고번호', '공고명', '공고분야', '공고기간', '공고상태', "URL', '입찰서류번호', '입찰서류URL']
        self.debug_print(self.notice_url)
        page = 1
        notice_df, page_flag = self.get_notice_dataframe(self.notice_url, self.hyperlink_column, page,
                                                         drive_option='urlopen')
        while (page_flag):
            page = page + 1
            next_notice_df, page_flag = self.get_notice_dataframe(self.notice_url, self.hyperlink_column, page,
                                                                  drive_option='urlopen')
            if len(next_notice_df.index) == 0:
                break
            else:
                next_notice_df = next_notice_df[~next_notice_df[self.hyperlink_column].str.contains('테스트')]
                next_notice_df = next_notice_df[~next_notice_df[self.hyperlink_column].str.contains('test')]
                if len(next_notice_df.index) == 0:
                    break
                notice_df = pd.merge(notice_df, next_notice_df, how='outer')

        self.debug_print(len(notice_df.index))
        self.debug_print(notice_df.columns)

        ###종료조건
        if len(notice_df.index) == 0:
            self.notice_df = notice_df
            return

        notice_df['입찰서류번호'] = notice_df['URL']
        notice_df['입찰서류URL'] = self.data_detail_url + notice_df['입찰서류번호']
        notice_df['URL'] = notice_df['입찰서류URL']
        self.notice_df = notice_df
        return


    def get_notice_dataframe(self, url, hyperlink_column, page, drive_option='urlopen'):
        total_url = self.root_url + url + str(page)
        if drive_option == 'urlopen':
            with urlopen(total_url) as response:
                html = response.read()
                soup = BeautifulSoup(html, 'html5lib')
        elif drive_option == 'driver':
            with webdriver.PhantomJS(
                    executable_path=os.path.join(os.getcwd(), 'phantomjs-2.1.1-windows', 'phantomjs-2.1.1-windows',
                                                 'bin', 'phantomjs.exe')) as browser:
                browser.get(total_url)
                html = browser.execute_script('return document.documentElement.outerHTML')
                soup = BeautifulSoup(html, "html5lib")
                browser.quit()
        elif drive_option == 'post':
            total_url, post_fields = parse_url_to_postForm(total_url)
            request = Request(total_url, urlencode(post_fields).encode())
            json = urlopen(request).read().decode()
            soup = BeautifulSoup(json, 'html5lib')

        trs = soup.find_all("tr")
        columns = []
        data = []
        for idx, tr in enumerate(trs):
            if idx == 0:
                ths = tr.find_all("th")
                for idx2, th in enumerate(ths):
                    columns.append(str(th.get_text()).strip())

                ##URL 추가코딩
                columns.append('URL')
                ##STATE 추가코딩
                columns.append(self.state_column)
            else:
                content = []
                tds = tr.find_all("td")
                URL = ''
                temp_state = self.state_false
                for idx2, td in enumerate(tds):
                    if columns[idx2] == hyperlink_column:
                        title = td.get('title')
                        if title == None or title == 'None':
                            title = str(td.find('a').get('title')).strip()
                        if title == None or title == 'None':
                            title = str(td.find('a').get_text().strip())
                        content.append(title)
                        URL = td.find('a').get('boardno')
                        imgs = td.find_all('img')
                        src_name = 'table-icon_note-new'
                        for img in imgs:
                            if src_name in img.get('src'):
                                temp_state = self.state_true
                    else:
                        content.append(str(td.get_text()).strip())
                content.append(URL)
                content.append(temp_state)
                data.append(content)
        if len(data[0]) == len(columns):
            df = pd.DataFrame(columns=columns, data=data)
        else:
            df = pd.DataFrame(columns=columns)

        page_flag = self.pageExist(soup, page)
        return df, page_flag

    def pageExist(self, soup, page):
        self.debug_print('pageExist')
        page_flag = False
        page_list = []
        div = soup.find('div', class_=['paginate_complex'])
        if len(div) > 0:
            a_list = div.find_all('a')
            for a_item in a_list:
                if 'goPaging' in a_item['href']:
                    page_list.append(int(re.sub("[^0-9]", "", a_item['href'])))
        if len(page_list) > 0:
            if max(page_list) > page:
                page_flag = True
        return page_flag

    def export_file(self):
        self.debug_print('export_file')
        self.notice_df = self.notice_df.drop(columns=['입찰서류URL','첨부파일','입찰서류번호','입찰서류URL'])
        columns = list(self.notice_df.columns)
        size = len(columns)
        columns[size-1], columns[size-2] = columns[size-2], columns[size-1]
        self.notice_df = self.notice_df[columns]
        save_file(df=self.notice_df, root_url=self.root_url, path=self.path, name=self.name, outformat=self.outformat)
        return


############################################################################################################################################

class g2b_Model(BasicModel):
    def debug_print(self, name):
        if self.debug_mode == 'True':
            print('g2b_Model ---- ', name)

    ##입찰서류URL과 URL을 만들어야 한다.
    def make_noticeList(self):
        self.debug_print('make_noticeList')
        self.debug_print(self.notice_url)

        page = 1
        notice_df = self.get_notice_dataframe(self.notice_url, page, drive_option='urlopen')
        self.debug_print(len(notice_df.index))
        self.debug_print(notice_df.columns)

        ###종료조건
        if len(notice_df.index) == 0:
            self.notice_df = notice_df
            return

        notice_df['입찰서류URL'] = notice_df['URL']
        self.notice_df = notice_df
        return

    def get_notice_dataframe(self, url, page, drive_option='urlopen'):
        total_url = self.root_url + url + str(page)
        with urlopen(total_url) as response:
            html = response.read().decode('CP949', errors='ignore')
            soup = BeautifulSoup(html, 'html5lib')

        ul = soup.find("ul", class_=['search_list'])
        lis = ul.findChildren("li", recursive=False)
        columns = []
        data = []
        columns.append('제목')  ##title
        columns.append('상태')  ##state_column
        columns.append('공고')  ##notice_date
        columns.append('개찰')  ##examination
        columns.append('수요기관')  ##supplier
        columns.append('URL')  ##title

        for idx, li in enumerate(lis):
            content = []

            ###제목
            title = li.find('strong', class_=['tit']).get_text().strip()
            content.append(title)

            ###상태
            state_column = li.find('ul', class_=['info2']).find('li', class_=['m1']).find('strong').get_text().strip()
            content.append(state_column)

            ###공고
            notice_date = li.find('ul', class_=['info2']).find('li', class_=['m2']).find('span').get_text().strip()
            content.append(notice_date)

            ###개찰
            examination = li.find('ul', class_=['info2']).find('li', class_=['m3']).find('span').get_text().strip()
            content.append(examination)

            ###수요기관
            supplier = li.find('ul', class_=['info2']).find('li', class_=['m4']).find('span').get_text().strip()
            content.append(supplier)

            ###URL
            url = li.find('strong', class_=['tit']).find('a')['href'].split("('")[1].split(")")[0].split("','")
            url = script_to_g2bUrl(url, self.data_detail_url)
            content.append(url)

            data.append(content)
        if len(data[0]) == len(columns):
            df = pd.DataFrame(columns=columns, data=data)
        else:
            df = pd.DataFrame(columns=columns)
        return df

    def download_file_list(self):
        self.debug_print('download_file_list')
        for idx, row in self.notice_df.iterrows():
            path = os.path.join(self.path, re.sub('[?.!/;:<>]', '', row[self.hyperlink_column]).strip())
            if self.download_mode == 'True':
                if not row[self.state_column] == self.state_false:
                    download_file_g2bDetail(path=path, root_url=self.root_url, data_url=row['입찰서류URL'],download_url=self.download_url)
            else:
                download_file_g2bDetail(path=path, root_url=self.root_url, data_url=row['입찰서류URL'], download_url=self.download_url)















