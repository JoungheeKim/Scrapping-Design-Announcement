# Scrapping-Design-Announcement
'디자인' 관련 입찰공고 알림 시스템 으로써 입찰공고 사이트에서 입찰관련 정보를 스크래핑 하여,
1. 관련 정보를 정리한 Excel파일을 생성
2. 관련 입찰양식을 다운로드
3. 진행중인 입찰공고가 있을 때 사이트 팝업

Scrapping Sites
-------------
RIPC-사업수행 지원시스템-협력기관 POOL 공고
https://www.ripc.org/cont/notice.do?action=noticeList

RIPC-사업수행 지원시스템-입찰공고
https://www.ripc.org/agency/tenderNotice.do?action=getTenderNoticeList

RIPC-지원사업 신청시스템-지원사업 공고
https://biz.ripc.org/online/csNotice.do

RIPC-통합공지
https://www2.ripc.org/portal/notice/ripcNoticeList.do

나라장터-입찰공고-디자인(용역), 제품디자인(용역), 브랜딩(용역), rhino(용역)
http://www.g2b.go.kr

#### 실행방법
```python
python main.py 
```

#### 사용자 설정
1. path.txt 에 스크래핑한 정보를 저장하고 싶은 폴더의 path를 기입한다.
2. config.json 파일 설정을 수정한다.
