import os
import re
from urllib.request import urlopen
from bs4 import BeautifulSoup
import webbrowser

DEBUG_MODE = True
def debug_print(name, content):
    if DEBUG_MODE:
        print(name + " : ", content)
    return

def make_dir(path):
    if not os.path.exists(path):
        os.mkdir(path)
    return

def getDataDocument(root_url, url):
    totalURL = root_url + str(url)
    with urlopen(totalURL) as response:
        html = response.read()
        soup = BeautifulSoup(html, 'html5lib')
        ps = soup.find_all("p")
        divs = soup.find_all("div")

        resultStr = ''
        for idx, p in enumerate(ps) :
            tempStr = str(p.get_text())
            if "번호" in tempStr and "제목" in tempStr:
                resultStr = tempStr

        for idx, div in enumerate(divs):
            tempStr = str(div.get_text())
            if "번호" in tempStr and "제목" in tempStr:
                resultStr = tempStr
        resultNum = re.sub("[^0-9]", "", resultStr.split("번호")[1].split("제목")[0])
    return resultNum

def find_matching_tender(tender_df, data_df):
    tender_list = tender_df['공고명'].values.tolist()
    data_list = data_df[['제목', '번호']].values.tolist()
    result_list = []
    for tender in tender_list:
        temp_score = []
        for data in data_list:
            score_list = []
            ##1. levenshtein LIST점수(MIN), 2.LIST 길이 차이(MAX) 3.levenshtein String점수(MIN) 4.String 길이 차이(MAX)
            score_list.append(levenshtein(tender.split(), data[0].split()))
            score_list.append(get_len_diff(tender.split(), data[0].split()))
            score_list.append(levenshtein(tender, data[0]))
            score_list.append(get_len_diff(tender, data[0]))
            temp_score.append(score_list)
        result_list.append(data_list[find_index_from_score(temp_score)][1])
    return result_list

def find_matching_tender2(tender_df, data_df, option=2):
    tender_title_list = tender_df['공고명'].values.tolist()
    tender_region_list = tender_df['센터명'].values.tolist()
    data_title_list = data_df['제목'].values.tolist()
    data_region_list = data_df['작성자'].values.tolist()
    data_number_list = data_df['번호'].values.tolist()

    result_list = []
    for idx_tender, tender in enumerate(tender_title_list):
        temp_max = 0
        temp_result = data_number_list[0]
        for idx_data, data in enumerate(data_title_list):
            score = matched_lenght(tender, data, option)

            ##같은 지역 Advantage Point
            if tender_region_list[idx_tender] == data_region_list[idx_data]:
                score = score + 5
            if score > temp_max:
                temp_max = score
                temp_result = data_number_list[idx_data]

        result_list.append(temp_result)
    return result_list

def find_index_from_score(score_list):
    result_index = 0
    ##1. levenshtein LIST점수(MIN), 2.LIST 길이 차이(MAX) 3.levenshtein String점수(MIN) 4.String 길이 차이(MAX)
    result_item = score_list[result_index]
    for temp_idx, temp_item in enumerate(score_list):
        if temp_item[0] < result_item[0] :
            result_index = temp_idx
            result_item = temp_item
        elif temp_item[0] == result_item[0] :
            if temp_item[1] > result_item[1]:
                result_index = temp_idx
                result_item = temp_item
            elif temp_item[1] == result_item[1]:
                if temp_item[2] < result_item[2]:
                    result_index = temp_idx
                    result_item = temp_item
                elif temp_item[2] == result_item[2]:
                    if temp_item[3] > result_item[3]:
                        result_index = temp_idx
                        result_item = temp_item
    return result_index

def levenshtein(s1, s2, cost=None, debug=False):
    if len(s1) < len(s2):
        return levenshtein(s2, s1, debug=debug)

    if len(s2) == 0:
        return len(s1)

    if cost is None:
        cost = {}

    # changed
    def substitution_cost(c1, c2):
        if c1 == c2:
            return 0
        return cost.get((c1, c2), 1)

    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            # Changed
            substitutions = previous_row[j] + substitution_cost(c1, c2)
            current_row.append(min(insertions, deletions, substitutions))

        if debug:
            print(current_row[1:])

        previous_row = current_row

    return previous_row[-1]

def get_len_diff(s1, s2):
    if len(s1) > len(s2):
        return len(s1) - len(s2)
    else:
        return len(s2) - len(s1)

def matched_lenght(target_str, test_str, option = 2):
    array_target = array_from_string(target_str, option)
    array_test = array_from_string((test_str), option)
    count = 0
    for tempStr in array_target:
        if tempStr in array_test:
            count = count + 1
    return count

def array_from_string(s1, distance = 2):
    result_list = []
    array_s1 = s1.split()
    for temp_str in array_s1:
        result_list = result_list + [temp_str[0 + index :distance + index] for index, i in enumerate(temp_str[:-(distance-1)])]
    return result_list

def removeExtra(str):
    return re.sub("[\W\d_]", "", str)

def check_Popup_State(df, url, state_column="공고상태", state_false = "공고마감", debug_mode='False'):
    webbrowser_flag = False
    if len(df.index) > 0:
        for item in df[state_column].unique():
            if not state_false == item:
                webbrowser_flag = True
                webbrowser.open_new(url)
                return

    if debug_mode == 'True':
        print("debug_mode : ", debug_mode)
        print("webbrowser.open_new(url) : ", url)
        webbrowser_flag = True

    if webbrowser_flag:
        webbrowser.open_new(url)
    return


def parse_url_to_postForm(url):
    array_url = url.split('&')
    post_fields = {}
    if len(array_url) < 0:
        return array_url[0], post_fields
    else :
        for idx, item in enumerate(array_url):
            if not idx == 0:
                item = item.split('=')
                if len(item) >1:
                    post_fields[item[0]] = item[1]
                else:
                    post_fields[item[0]] = ''
        return array_url[0], post_fields

def merge_postForm_to_url(url, post_fields={}, custom_option={}):
    for key, val in custom_option.items():
        post_fields[key] = val
    url = url + "?"
    str_list = []
    for key, val in post_fields.items():
        str_list.append(str(key) + "=" + str(val))
    return url + '&'.join(str_list)

def script_to_g2bUrl(items, detail_url):
    url = detail_url + "&val1=" + items[0]
    url = url + "&val2=" + items[1]
    url = url + "&type=" + items[2]
    return url