from scrap.model import *
import json
import os
import datetime
import time

def load_config(debug_mode=False, download_mode=True):
    config_file_name = "config.json"
    currnet_path = str(os.getcwd())
    ##Config 파일 다운로드
    if os.path.isfile(config_file_name) and not debug_mode:
        with open(config_file_name, encoding='UTF-8-sig') as json_file:
            config = json.load(json_file)
    else:
        config = {}
        config['협력기관 POOL 공고'] = {
            'popup_url': 'https://www.ripc.org/cont/notice.do?action=noticeList',
            'path': currnet_path,
            'name': 'RIPC 협력기관 POOL 공고',
            'root_url': 'https://www.ripc.org',
            'notice_url': '/cont/notice.do?action=noticeList&currentPage=',
            'data_list_url': '/agencyNotice.do?method=getBoardList&board_type=PDS&board_id=FORMDATA&center_id=&search_field=&search_text=&classification_code_type=&class1=&class2=&class3=&cp=',
            'data_detail_url': '/agencyNotice.do?method=getBoardInfo&board_id=FORMDATA&board_type=PDS&board_seq=',
            'download_url': {
                'downloadAttachFile': '/agencyNotice.do?method=downloadAttachFile&attach_seq='
            },
            'hyperlink_column': '공고명',
            'data_hyperlink_column': '제목',
            'state_column': '공고상태',
            'state_false': '공고마감',
            'state_true': '공고중',
            'debug_mode': str(debug_mode),
            'download_mode': str(download_mode),
            'outformat': 'excel'
        }
        config['입찰공고'] = {
            'popup_url': 'https://www.ripc.org/agency/tenderNotice.do?action=getTenderNoticeList',
            'path': currnet_path,
            'name': 'RIPC 입찰공고',
            'root_url': 'https://www.ripc.org',

            ##실제
            'notice_url': '/agency/tenderNotice.do?action=getTenderNoticeList&noticeSeq=',
            ##테스트용
            #'notice_url': '/agency/tenderNotice.do?action=getTenderNoticeList&bizYear=2017&centerCode=&biz1Code=&biz2Code=&statusCode=&currentPage=',

            'data_list_url': '/agencyNotice.do?method=getBoardList&board_type=PDS&board_id=FORMDATA&center_id=&search_field=&search_text=&classification_code_type=&class1=&class2=&class3=&cp=',
            'data_detail_url': '/agencyNotice.do?method=getBoardInfo&board_id=FORMDATA&board_type=PDS&board_seq=',
            'download_url': {
                'downloadAttachFile': '/agencyNotice.do?method=downloadAttachFile&attach_seq='
            },
            'hyperlink_column': '공고명',
            'data_hyperlink_column': '제목',
            'state_column': '공고상태',
            'state_false': '공고마감',
            'state_true': '공고중',
            'debug_mode': str(debug_mode),
            'download_mode': str(download_mode),
            'outformat': 'excel'
        }
        config['지원사업 공고'] = {
            'popup_url': 'https://biz.ripc.org/online/csNotice.do',
            'path': currnet_path,
            'name': 'RIPC 지원사업 공고',
            'root_url': 'https://biz.ripc.org',
            'notice_url': '/online/csNotice.do&notice_seq=&biz_year=2019&notice_status_code=&notice_title=&pageNum=',
            'data_list_url': '/agencyNotice.do?method=getBoardList&board_type=PDS&board_id=FORMDATA&center_id=&search_field=&search_text=&classification_code_type=&class1=&class2=&class3=&cp=',
            'data_detail_url': '/online/csDetail.do&notice_seq=&notice_status_code=&biz_year=2019&notice_title=&pageNum=1&noticeTitle=',
            'download_url': {
                'attachDown': '/attach/noticeDown.do?cs_attach_seq='
            },
            'hyperlink_column': '공고명',
            'data_hyperlink_column': '제목',
            'state_column': '공고상태',
            'state_false': '공고마감',
            'state_true': '공고중',
            'debug_mode': str(debug_mode),
            'download_mode': str(download_mode),
            'outformat': 'excel'
        }
        config['공지사항'] = {
            'popup_url': 'https://www2.ripc.org/portal/notice/ripcNoticeList.do',
            'path': currnet_path,
            'name': 'RIPC 공지사항',
            'root_url': 'https://www2.ripc.org',
            'notice_url': '/portal/notice/ripcNoticeList.do?noticeType=ripcNotice&downloadFileSeq=&targetBoardNo=&searchType=&searchQuery=&inSearchType=title&inSearchQuery=&pagingModel.rowPerPage=100&pagingModel.rowSize=114&pagingModel.blockCount=10&pagingModel.orderByColumn=writeDate&pagingModel.orderByType=desc&pagingModel.pageNo=',
            'data_list_url': '/agencyNotice.do?method=getBoardList&board_type=PDS&board_id=FORMDATA&center_id=&search_field=&search_text=&classification_code_type=&class1=&class2=&class3=&cp=',
            'data_detail_url': '/portal/notice/ripcNoticeDetail.do?noticeType=ripcNotice&targetBoardNo=',
            'download_url': {
                '#': '/portal/attFile/download.do?noticeType=ripcNotice&searchType=&searchQuery=&pagingModel.pageNo=1&pagingModel.rowPerPage=20&downloadFileSeq='
            },
            'hyperlink_column': '제목',
            'data_hyperlink_column': '제목',
            'state_column': '공고상태',
            'state_false': '기존',
            'state_true': '신규',
            'debug_mode': str(debug_mode),
            'download_mode': str(download_mode),
            'outformat': 'excel'
        }
        config['나라장터'] = {}
        config['나라장터']['디자인'] = {
            'popup_url': 'http://www.g2b.go.kr:8340/search.do?category=TGONG&kwd=%B5%F0%C0%DA%C0%CE&&category=TGONG&subCategory=%BF%EB%BF%AA',
            'path': currnet_path,
            'name': '나라장터 디자인',
            'root_url': 'http://www.g2b.go.kr',
            'notice_url': ':8340/body.do?kwd=%B5%F0%C0%DA%C0%CE&&category=TGONG&subCategory=%BF%EB%BF%AA&detailSearch=false&sort=R&reSrchFlag=false&srchFd=ALL&orgType=balju&swFlag=Y&body=yes&pageNum=',
            'data_list_url': '',
            'data_detail_url': ':8340/link.do?target=%BF%EB%BF%AA&kwd=%B5%F0%C0%DA%C0%CE&&category=TGONG',
            'download_url': {
                'toFileDownload': ':8081/ep/co/fileDownload.do?fileTask=NOTIFY&fileSeq=',
                'eeOrderAttachFileDownload': ':8426/cmm/FileDownload.do?atchFileId='
            },
            'hyperlink_column': '제목',
            'data_hyperlink_column': '제목',
            'state_column': '상태',
            'state_false': '입찰마감',
            'state_true': '입찰중',
            'debug_mode': str(debug_mode),
            'download_mode': str(download_mode),
            'outformat': 'excel'
        }
        config['나라장터']['제품디자인'] = {
            'popup_url': 'http://www.g2b.go.kr:8340/search.do?category=TGONG&kwd=%C1%A6%C7%B0%B5%F0%C0%DA%C0%CE&category=TGONG&subCategory=%BF%EB%BF%AA',
            'path': currnet_path,
            'name': '나라장터 제품디자인',
            'root_url': 'http://www.g2b.go.kr',
            'notice_url': ':8340/body.do?kwd=%C1%A6%C7%B0%B5%F0%C0%DA%C0%CE&category=TGONG&subCategory=%BF%EB%BF%AA&detailSearch=false&sort=R&reSrchFlag=false&srchFd=ALL&orgType=balju&swFlag=Y&body=yes&pageNum=',
            'data_list_url': '',
            'data_detail_url': ':8340/link.do?target=%BF%EB%BF%AA&kwd=%C1%A6%C7%B0%B5%F0%C0%DA%C0%CE&category=TGONG',
            'download_url': {
                'toFileDownload': ':8081/ep/co/fileDownload.do?fileTask=NOTIFY&fileSeq=',
                'eeOrderAttachFileDownload': ':8426/cmm/FileDownload.do?atchFileId='
            },
            'hyperlink_column': '제목',
            'data_hyperlink_column': '제목',
            'state_column': '상태',
            'state_false': '입찰마감',
            'state_true': '입찰중',
            'debug_mode': str(debug_mode),
            'download_mode': str(download_mode),
            'outformat': 'excel'
        }
        config['나라장터']['브랜딩'] = {
            'popup_url': 'http://www.g2b.go.kr:8340/search.do?category=TGONG&kwd=%BA%EA%B7%A3%B5%F9&subCategory=%BF%EB%BF%AA',
            'path': currnet_path,
            'name': '나라장터 브랜딩',
            'root_url': 'http://www.g2b.go.kr',
            'notice_url': ':8340/body.do?kwd=%BA%EA%B7%A3%B5%F9&category=TGONG&subCategory=%BF%EB%BF%AA&detailSearch=false&sort=R&reSrchFlag=false&srchFd=ALL&orgType=balju&swFlag=Y&body=yes&pageNum=',
            'data_list_url': '',
            'data_detail_url': ':8340/link.do?target=%BF%EB%BF%AA&kwd=%BA%EA%B7%A3%B5%F9&category=TGONG',
            'download_url': {
                'toFileDownload': ':8081/ep/co/fileDownload.do?fileTask=NOTIFY&fileSeq=',
                'eeOrderAttachFileDownload': ':8426/cmm/FileDownload.do?atchFileId='
            },
            'hyperlink_column': '제목',
            'data_hyperlink_column': '제목',
            'state_column': '상태',
            'state_false': '입찰마감',
            'state_true': '입찰중',
            'debug_mode': str(debug_mode),
            'download_mode': str(download_mode),
            'outformat': 'excel'
        }
        config['나라장터']['rhino'] = {
            'popup_url': 'http://www.g2b.go.kr:8340/search.do?category=TGONG&kwd=rhino&subCategory=%BF%EB%BF%AA',
            'path': currnet_path,
            'name': '나라장터 rhino',
            'root_url': 'http://www.g2b.go.kr',
            'notice_url': ':8340/body.do?kwd=rhino&category=TGONG&subCategory=%BF%EB%BF%AA&detailSearch=false&sort=R&reSrchFlag=false&srchFd=ALL&orgType=balju&swFlag=Y&body=yes&pageNum=',
            'data_list_url': '',
            'data_detail_url': ':8340/link.do?target=%BF%EB%BF%AA&kwd=rhino&category=TGONG',
            'download_url': {
                'toFileDownload': ':8081/ep/co/fileDownload.do?fileTask=NOTIFY&fileSeq=',
                'eeOrderAttachFileDownload': ':8426/cmm/FileDownload.do?atchFileId='
            },
            'hyperlink_column': '제목',
            'data_hyperlink_column': '제목',
            'state_column': '상태',
            'state_false': '입찰마감',
            'state_true': '입찰중',
            'debug_mode': str(debug_mode),
            'download_mode': str(download_mode),
            'outformat': 'excel'
        }


        with open(config_file_name, 'w', encoding='UTF-8-sig') as outfile:
            json.dump(config, outfile, ensure_ascii=False)
    return config

def modified_config(config, debug_mode=False):
    if not debug_mode:
        config['지원사업 공고']['notice_url'] = '/online/csNotice.do&notice_seq=&biz_year=' + str(datetime.datetime.now().year) + '&notice_status_code=&notice_title=&pageNum='
        config['지원사업 공고']['data_detail_url'] = '/online/csDetail.do&notice_seq=&notice_status_code=&biz_year=' + str(datetime.datetime.now().year) + '&notice_title=&pageNum=1&noticeTitle='
    return config

def modified_path(config, debug_mode=False):
    ##path 설정
    path_file = 'path.txt'
    if os.path.isfile(path_file) and not debug_mode:
        with open(path_file, 'r') as f:
            currnet_path = f.read()
            print(os.path.isdir(currnet_path))
            if os.path.isdir(currnet_path):
                for key, value in config.items():
                    if key == '나라장터':
                        for key2, value2 in value.items():
                            config[key][key2]['path'] = str(currnet_path)
                    else:
                        config[key]['path'] = str(currnet_path)
            else:
                print("'path.txt'에 설정된 경로가 존재하지 않습니다. 다시한번 확인하시기 바랍니다.")
    return config

def run(config):
    print("SCRAPPING FILES....")
    for key, value in config.items():
        try:
            print("SCRAPPING ", key)
            if key == '협력기관 POOL 공고':
                noticeList_Model(value).execute()
            elif key == '입찰공고':
                tenderNoticeList_Model(value).execute()
            elif key == '지원사업 공고':
                csNoticeList_Model(value).execute()
            elif key == '공지사항':
                ripcNoticeList_Model(value).execute()
            elif key == '나라장터':
                for key2, value2 in value.items():
                    print("SCRAPPING ", key, key2)
                    g2b_Model(value2).execute()
        except Exception as ex:
            print('에러 발생......')
            print('잠시 후 다시 시도하시기 바랍니다.')
            time.sleep(10)
    print("SCRAPPING FINISHED....")


if __name__ == "__main__":
    debug_mode = False
    download_mode = True

    print("START TO READ 'config.json' file")
    config = load_config(debug_mode=debug_mode, download_mode=download_mode)
    config = modified_config(config, debug_mode=debug_mode)
    config = modified_path(config, debug_mode=debug_mode)
    
    ##실행
    run(config)


    #notice = noticeList_Model(config['협력기관 POOL 공고'])
    #notice.execute()

    #tenderNotice = tenderNoticeList_Model(config['입찰공고'])
    #tenderNotice.execute()

    #csNotice = csNoticeList_Model(config['지원사업 공고'])
    #csNotice.execute()

    #ripcNotice = ripcNoticeList_Model(config['공지사항'])
    #ripcNotice.execute()

    #g2bDesign = g2b_Model(config['나라장터']['디자인'])
    #g2bDesign.execute()

    #g2bDesign = g2b_Model(config['나라장터']['제품디자인'])
    #g2bDesign.execute()

    #g2bDesign = g2b_Model(config['나라장터']['브랜딩'])
    #g2bDesign.execute()

    #g2bDesign = g2b_Model(config['나라장터']['rhino'])
    #g2bDesign.execute()







