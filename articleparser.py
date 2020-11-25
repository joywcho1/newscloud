# -*- coding: utf-8, utf-8-si, euc-kr -*-
import re


class ArticleParser(object):
    unvailiable_text = re.compile(r"""[\'\-\=\#\/\?\:\$\[\{\}\,\‘\"\]]""")
    email_pattern = re.compile(r'([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+(\.[a-zA-Z]{2,4}))')
    ex_pattern = re.compile(r'[\'\"\,\/\{\}]|\\(n)?\\(t)?\\(r)?]')
    content_pattern = re.compile(r'동영상 뉴스|파이낸셜뉴스.|파이낸셜 뉴스|파이낸셜뉴스|앵커 멘트|'
                                 r'본문 내용|TV플레이어|function \_flash\_removeCallback|'
                                 r'flash 오류를 우회하기 위한 함수 추가|저작권자\(c\) YTN \& YTN PLUS 무단전재 및 재배포 금지|'
                                 r'현재 코스닥은|기관 코스닥에서|외국인 코스닥에서|거래소 외국인 순매도에서|본문 내용|'
                                 r'거래소 외국인 순매도 상위에|거래소 외국인 순매도상위에|거래소 외국인 순매수 상위에|'
                                 r'거래소 외국인 순매수상위에|기관 거래소에서|거래소 기관 순매도상위에|'
                                 r'코스닥 외국인 순매도 상위 종목|거래소 기관 순매도 상위 종목|등 순매도|등 순매수|마감시황|마감 시황|'
                                 r'endif|supportEmptyPara|재판매 및 DB 금지|오후 주식시장은'
                                 r'네이버에서 구독하기|뉴시스통신사|[가-힣]\=뉴시스|그래픽|머니투데이|'
                                 r'st&인터뷰|엠스플 이슈|SC핫포커스|엑\'s 셔터스토리|MD포토|똑똑SNS|M\+|SNS|e글중심|세상읽기|'
                                 r'SHOT|권혁주의 직격|기자 칼럼 신호등|36.5℃|김재호의 생명이야기|테마진단분수대|'
                                 r'매경데스크|글로벌 아이|문화단상|신용호 논설위원이 간다|안혜리의 시선|전성인의 경제노트|'
                                 r'[가-힣]+ [가-힣]+\/[가-힣]+|'
                                 r'세상만사|촌철댓글|동서남북|데스크에서|아침을 열며|데스크 시각|슬기로운 국회생활|오후여담|서울광장|'
                                 r'연합시론|일본 바로보기|살며 생각하며|문화논단|여론마당|뉴스와 시각|東語西話|기고|한겨레|여론마당|'
                                 r'오동희의 思見|그림과 詩가 있는 아침|김유진의 어린이처럼|[가-힣]+\/[가-힣]+|벗드갈의 한국 블로그|'
                                 r'/재송|시사캐리커쳐|아트만두의 인간대백과사전|파이낸셜뉴스|머니S리포트\【편집자주\】|'
                                 r'경동인베스트 외국인|기관 매매동향|한경로보뉴스|'
                                 r'한국경제신문과 금융|오류를 우회하기 위한 함수 추가|\'\"\/\\|\,|아시아경제'
                                 r'/\[[가-힣]+칼럼\]|\[[가-힣]+ 칼럼\]|국회보 \d+년 \d+월호|'
                                 r'\d+일 오전 서울 여의도|마이데일리 = [가-힣]+ |\d+.\d+.\d+|'
                                 r'\d+일 오전|\d+일 오후 서울 여의도|\d+일 오후|했다고 \d+일 밝혔다|'
                                 r'\d+일 밝혔다|코스닥 기관 순매도 상위 종목|'
                                 r'서울경제 편집자註 이 기사는 '
                                 r'\d+년 \d+월 \d+일 \d+ \d+ 프리미엄 컨버전스 미디어 시그널 Signal 에 표출된 기사입니다.|'
                                 r'이 기사는 \d+월\d+일 \d+ \d+ 자본시장의 혜안|\d+월 \d+일 \d+ \d+ 모바일한경에'
                                 r' 게재된 기사입니다 모바일한경 기사 더보기|'
                                 r'이 기사는 \d+월\d+일 \d+ \d+|지티지웰니스 219750 가 VI가 발동했다|'
                                 r'오후 \d+ \d+|오후 \d+\:\d+|오전 \d+\:\d+|현재 코스피는|\d+ \d+으로 매도우위 매도강세 업종은|'
                                 r'\d+\:\d+으로 매도우위 매도강세 업종은|\d+\:\d+으로 매도우위\, 매도강세 업종은|\\n|\\t|\\r|xa0'
                                 )

    @classmethod
    def clear_content(cls, text):
        # 기사 본문에서 필요없는 특수문자 및 본문 양식 등을 다 지움
        match_email = re.search(cls.email_pattern, text)
        email = 'No'
        if match_email:
            email = match_email.group()

        text = text.replace(email, '')
        text = re.sub(r'(http(s)?\://)?[a-zA-Z0-9](\.[a-zA-Z0-9])+\/[a-zA-Z0-9]|[a-zA-Z0-9]\.[a-zA-Z0-9]', '', text)
        text = re.sub(r'[\[(*?)\=(*?)\]|\((*?)\=(*?)\)]', '', text)
        text = re.sub(r'[\※|\★|\❤|\♥\◀|\▶|\■|\#|\$|\◇|\○|종합]', ' ', text)
        text = re.sub(r'[(*?)\(무단전재 및 재배포 금지\)]', ' ', text)
        text = re.sub(cls.content_pattern, '', text)

        ex_symbol_removed_content = re.sub(cls.ex_pattern, ' ', text)
        ex_symbol_removed_content = re.sub(' +', ' ', ex_symbol_removed_content)
        unvailiable_text_removed_content = re.sub(cls.unvailiable_text, ' ', ex_symbol_removed_content)
        end_phrase_removed_content = re.sub(cls.content_pattern, ' ', unvailiable_text_removed_content)

        blank_removed_content = re.sub(' +', ' ', end_phrase_removed_content).lstrip()  # 공백 에러 삭제
        # print('blank_removed_content [] : ', unvailiable_text_removed_content)
        reversed_content = ''.join(reversed(blank_removed_content))  # 기사 내용을 reverse 한다.
        content = ''
        journalist_pattern = re.compile(r'자기 [가-힣]+|원파특 [가-힣]+|트스니럼칼 [가-힣]+|자기[가-힣]+')
        match_journalist = journalist_pattern.search(reversed_content)
        journalist = 'No'
        if match_journalist:
            journalist = ''.join(reversed(match_journalist.group()))

        r_j = journalist.replace('기자', '').replace('특파원', '').strip()
        # print('blank_removed : ', reversed_content)
        for i in range(0, len(reversed_content)):
            if reversed_content[i:i + 2] == r' .' and reversed_content[i:i + 3] != r' . ':
                content = ''.join(reversed(reversed_content[i:]))
                break
        # print('content      : ', content)
        content = content.replace(
            journalist, '').replace(r_j, '').replace('“', '')

        content = content.replace(
            '뉴스 가치나 화제성이 있다고 판단되는 사진 또는 영상을 사진영상부',
            '').replace('매도우위 매도강세 업종은',
                        '').replace('로 보내주시면 적극 반영하겠습니다',
                                    '').replace('한경로보 이 기사는 신문과 금융 AI 전문기업 씽크풀이 공동 개발한 기사 자동생성 알고리즘에 의해 실시간으로 작성된 것입니다',
                                                '').replace('사진 영상 제보받습니다 공감언론 가 독자 여러분의 소중한 제보를 기다립니다',
                                                            '').replace('연합뉴스',
                                                                        '').replace('뉴스 가치나 화제성이 있다고 판단되는 사진 또는 영상을',
                                                                                    '').replace('사진영상부',
                                                                                                '').replace(
            '가 독자 여러분의 소중한 제보를 기다립니다.',
            '').replace('사진 영상 제보받습니다',
                        '').replace('이 기사는 조선비즈와 아티웰스가 공동으로 개발해 서비스하는 로봇 기사입니다.',
                                    '').replace('flash 오류를 우회하기 함수 추가 function flashremoveCallback',
                                                '').replace('이 기사는 증권플러스 두나무 가 자체 개발한 인 C Biz봇 이 실시간으로 작성했습니다.',
                                                            '').replace(
            '저작권자 c MBC hps imnews.imbc.com 무단복제 재배포 금지 네이버 홈에서 MBC뉴스 채널 구독하기 새로움을 탐험하다.',
            '').replace('이 기사는 아시아경제와 금융 AI 전문기업 씽크풀이 공동 개발한 기사 자동생성 알고리즘에 의해 실시간으로 작성된 것입니다.',
                        '').replace('사진 영상 제보받습니다',
                                    '').replace('사진 영상 제보받습니다',
                                                '').replace('이데일리',
                                                            '').replace('지디넷코리아',
                                                                        '').replace('재판매 DB',
                                                                                    '').replace('이 기사는 한국경제신문과',
                                                                                                '').replace(
            '창원 연예현장 진짜 논설위원의 뉴스 스타들의 아찔한 순간 나의 아이돌을 픽♥ 해주세요.',
            '').replace('이 기사는 아시아경제와',
                        '').replace('한경로보뉴스',
                                    '').replace('www.mydaily.co.kr',
                                                '').replace('마켓인사이트',
                                                            '').replace('에 게재된 기사입니다',
                                                                        '').replace(
            '이 기사는 증시분석  서경뉴스봇 newsbot sedaily.com 이 실시간으로 작성했습니다.',
            '').replace('지속적인 업그레이드를 통해 더욱 풍부하고 정확한 내용을 담아 가겠습니다.',
                        '').replace('저작권자 c YTN YTN PLUS', '').replace('이 시각 코로나19 확진자 현황을 확인하세요.',
                                                                       '').replace(
            '저작권자 SPOTV NEWS 무단전재 및 재배포 금지 기사제공 스포티비뉴스 현장에서 작성된 기사입니다.',
            '').replace('이 금융감독원 전자공시시스템 DART 과 한국거래소 KRX 데이터를 토대로 작성한 것입니다.',
                        '').replace('이 기사는 국민일보와 엠로보가 개발한 증권뉴스 전용 인공지능 로봇',
                                    '').replace('본 기사는 한국경제TV와 금융 AI 전문기업 씽크풀 이 실시간으로 작성한 기사입니다.',
                                                '').replace('금융 AI 전문기업 씽크풀이 공동 개발한 기사 자동생성 알고리즘에 의해 실시간으로 작성된 것입니다.',
                                                            '').replace('기자 한국경제TV', '').replace('한국경제TV  기자',
                                                                                                 '').replace(
            '그래프 올리패스 외국인 기관 매매동향',
            '').replace('는 금융 AI 전문기업 씽크풀과 파이낸셜뉴스의 협업으로 가 실시간으로 생산하는 기사입니다.',
                        '').replace('‘', '').replace('newsis.com',
                                                     '').replace('newsis', '').replace(
            '잠실 연예현장 진짜 논설위원의 뉴스 스타들의 아찔한 순간 나의 아이돌을 픽♥ 해주세요.',
            '').replace('사직 연예현장 진짜 논설위원의 뉴스 스타들의 아찔한 순간 나의 아이돌을 픽♥ 해주세요.', '').replace('photo',
                                                                                        '').replace(
            '네이버 메인에서  구독하기  11기  모집 © 코리아 news1.', '').replace('n  .com .',
                                                                '').replace('dadazon', '').replace('서울 뉴스1',
                                                                                                   '').replace(
            '연예현장 진짜 논설위원의 뉴스 스타들의 아찔한 순간 나의 아이돌을 픽♥ 해주세요.',
            '').replace('Copyrights 스포츠조선 h p sports.chosun.com',
                        '').replace('저작권자(c) YTN & YTN PLUS 무단전재 및 재배포 금지', '').replace('뉴스1',
                                                                                        '').replace(
            '대구 스포츠경향 인기 무료만화 보기 지금 옆사람이 보고 뉴스 스포츠경향 sports.khan.co.kr 무단전재 및 재배포 금지 기사제공 스포츠경향 현장에서 작성된 기사입니다.',
            '').replace('©', '').replace('© News1', '').replace('뉴시스', '').replace('공감언론', '').replace('apos',
                                                                                                       '').replace(
            'News1', '').replace('in .com ', '').replace('네이버 메인에서', '').replace('구독하기 11기',
                                                                                 '').replace('모집', '').replace('news1',
                                                                                                               '').replace(
            '현장에서 작성된 기사입니다.', '').replace('추천',
                                           '').replace('금융 AI 전문기업 씽크풀이 공동 개발한 기사', '').replace(
            '그래프 지티지웰니스 외국인 기관 매매동향',
            '').replace('그래프 지티지웰니스 차트 분석 주체별 매매동향', '').replace('그래프 지티지웰니스 차트 분석',
                                                                 '').replace('…', '. ').replace('jtbc', '').replace(
            '화면캡쳐', '').replace('end block',
                                '').replace('start block', '').replace('데스크 시각', '').replace('서울연합뉴스', '').replace(
            '글로벌 포커스',
            '').replace('전문기자 칼럼', '').replace('열린세상', '').replace('이동구 수석논설위원', '').replace('시사만평',
                                                                                             '').replace('선데이 칼럼',
                                                                                                         '').replace(
            '데스크칼럼', '').replace('논설위원의 뉴스', '').replace('강천석 칼럼',
                                                         '').replace('정기수 칼럼', '').replace('칼럼', '').replace('월요논단',
                                                                                                             '').replace(
            '만물상',
            '').replace('특파원 리포트', '').replace('김지연의', '').replace('2030 세상보기',
                                                                   '').replace('배영대 曰', '').replace('세상사는 이야기',
                                                                                                    '').replace(
            '사람과 법 이야기', '').replace('매경춘추',
                                     '').replace('특파원 칼럼', '').replace('MK이슈', '').replace('오태식의', '').replace('오늘의 운세',
                                                                                                               '').replace(
            'MK이슈', '').replace('오태식의 알바트로스', '').replace('오태식의', '').replace('이슈포커스',
                                                                              '').replace('apos', '').replace('집코노미 TV',
                                                                                                              '').replace(
            'MK 시황', '').replace('사설', '').replace('이평선',
                                                   '').replace('이상', '').replace('중기', '').replace('단기', '').replace(
            '기고', '').replace('서소문 포럼',
                              '').replace('포럼', '').replace('홍태경의 지구', '').replace('Column', '').replace('최준호의 사이언스',
                                                                                                         '').replace(
            '경제시평', '').replace('시선', '').replace('시평', '').replace('시론', '').replace('오늘의 날씨',
                                                                                      '').replace('fnRASSI',
                                                                                                  '').replace('fn',
                                                                                                              '').replace(
            '오류를 우회하기 위한 함수 추가', '').replace('차트 분석',
                                             '').replace('매매 동향', '').replace('속보', '').replace('아시아 경제',
                                                                                                '').replace('머니 투데이',
                                                                                                            '').replace(
            '”', '').replace('’',
                             '').replace('.. .', '. ').replace('...', '. ').replace('..', '. ').replace('서울 경제',
                                                                                                        '').replace(
            '매일경제',
            '').replace('스타투데이', '').replace('서울경제', '').replace('헤럴드 경제', '').replace('뉴스 기자',
                                                                                       '').replace('기자', '').replace(
            'MD 리뷰', '').replace('<>', '').replace(', ,', '').replace('()',
                                                                      '').replace(' · ', '').replace('/', '').replace(
            '≪≫', '').replace('{}', '').replace('[]',
                                                '').replace('【】', '').replace('ⓒ', '').replace('xa0', '').replace('\\',
                                                                                                                  '')
        result_content = re.sub(' +', ' ', content).strip()  # 공백 에러 삭제
        return journalist, email, result_content

    @classmethod
    def clear_headline(cls, text):
        # 기사 제목에서 필요없는 특수문자들을 지움
        text = re.sub(r'http(s)?\://[a-zA-Z0-9](\.[a-zA-Z0-9])+\/[a-zA-Z0-9]', '', text)
        text = re.sub(r'[\[(*?)\]]', ' ', text)
        text = re.sub(r'[\((*?)\)]', ' ', text)
        text = re.sub(r'지디넷코리아|재판매 DB|M\+[가-힣]|\\n|\\t|\\r|xa0', ' ', text)
        text = re.sub(r'[a-zA-Z]+[가-힣]+\=[a-zA-Z]+[가-힣]+', ' ', text)
        text = re.sub(r'[\※|\★|\❤|\♥\◀|\▶|\■|\#|\$|\◇|\○|종합]', ' ', text)

        ex_symbol_removed_headline = re.sub(cls.ex_pattern, ' ', text)
        ex_symbol_removed_headline = re.sub(' +', ' ', ex_symbol_removed_headline)
        # print('ex_symbol_removed_content [] : ', ex_symbol_removed_content)
        unvailiable_text_removed_headline = re.sub(cls.unvailiable_text, ' ', ex_symbol_removed_headline)

        result_headline = unvailiable_text_removed_headline.replace('뉴스포커스', '').replace('“', '').replace("‘",
                                                                                                          '').replace(
            '저작권자(c) YTN & YTN PLUS 무단전재 및 재배포 금지', '').replace('취재파일',
                                                                '').replace('…', '. ').replace('박기자의 스맛폰', '').replace(
            '이정재의 퍼스펙티브', '').replace('장세정의 시선',
                                      '').replace('기자칼럼', '').replace('주성하 기자의 서울과 평양 사이', '').replace('BOOK',
                                                                                                       '').replace(
            '강성주의 홑눈겹눈', '').replace('에세이 오늘', '').replace('천병혁의 야구세상', '').replace('금요칼럼',
                                                                                    '').replace('→', '').replace('X',
                                                                                                                 '').replace(
            'Pick', '').replace('옴부즈만', '').replace('오늘의 건강',
                                                    '').replace('S1 포커스', '').replace('SC핫이슈', '').replace('SS창간특집',
                                                                                                           '').replace(
            'S트리밍',
            '').replace('스토리S', '').replace('이성주의 건강편지', '').replace('뉴스A 클로징', '').replace('광화문에서 이헌재',
                                                                                            '').replace('독자 마당',
                                                                                                        '').replace(
            '역사와 현실', '').replace('몸으로 말하기', '').replace('D 인터뷰',
                                                         '').replace('TF씨네리뷰', '').replace('N컷', '').replace('Y리뷰',
                                                                                                             '').replace(
            '핫클릭', '').replace('경향의 눈',
                               '').replace('김홍표의 과학 한 귀퉁이', '').replace('미술 세상 졸보기', '').replace('이은화의 미술시간',
                                                                                                 '').replace('SC리뷰',
                                                                                                             '').replace(
            'Nbox', '').replace('여적', '').replace('미술 세상 졸보기',
                                                  '').replace('여의도포럼', '').replace('광화문', '').replace('양상훈 칼럼',
                                                                                                      '').replace(
            '기자의 시각',
            '').replace('내일을 열며', '').replace('경제포커스', '').replace('MT시평', '').replace('샛강에서',
                                                                                       '').replace('한마당', '').replace(
            '기자의 눈', '').replace('기억할 오늘', '').replace('해외',
                                                       '').replace('박상현의 디지털 미디어', '').replace('똑똑 우리말', '').replace(
            '삶과 문화', '').replace('문화마당',
                                 '').replace('장준우의 푸드 오디세이', '').replace('김유민의 노견일기', '').replace('내 생각은 이성규',
                                                                                                  '').replace('씨줄날줄',
                                                                                                              '').replace(
            '난세의 사자후', '').replace('하재근의 이슈분석', '').replace('관풍루',
                                                            '').replace('기자수첩', '').replace('뉴스해설', '').replace(
            '정윤하의 러브월드', '').replace('야고부',
                                     '').replace('이종락 논설위원', '').replace('임병식의 창과 방패', '').replace('이동구 칼럼',
                                                                                                   '').replace(
            '글로벌 포커스', '').replace('WWDC20', '').replace('논설위원의 뉴스',
                                                         '').replace('전문기자 칼럼', '').replace('선데이 칼럼', '').replace(
            '강천석 칼럼',
            '').replace('정기수 칼럼', '').replace('월요논단', '').replace('만물상',
                                                                  '').replace('특파원 리포트', '').replace('김지연의',
                                                                                                     '').replace(
            '2030 세상보기',
            '').replace('배영대 曰', '').replace('세상사는 이야기', '').replace('사람과 법 이야기', '').replace('매경춘추',
                                                                                              '').replace('특파원 칼럼',
                                                                                                          '').replace(
            'MK이슈', '').replace('전문기자 칼럼', '').replace('열린세상',
                                                       '').replace('이동구 수석논설위원', '').replace('시사만평', '').replace(
            '선데이 칼럼',
            '').replace('데스크칼럼', '').replace('논설위원의 뉴스', '').replace('오태식의', '').replace('오늘의 운세',
                                                                                         '').replace('MK이슈',
                                                                                                     '').replace(
            '오태식의 알바트로스', '').replace('오태식의', '').replace('이슈포커스',
                                                          '').replace('apos', '').replace('집코노미 TV', '').replace(
            'MK 시황', '').replace('사설', '').replace('뉴스',
                                                   '').replace('포토엔HD', '').replace('TV', '').replace('상승', '').replace(
            '이상',
            '').replace('MD 리뷰', '').replace('SNS 컷', '').replace('중기', '').replace('칼럼',
                                                                                    '').replace('단기', '').replace(
            '바이블시론', '').replace('Mk포토', '').replace('MK포토', '').replace('MD인터뷰',
                                                                         '').replace('N인터뷰', '').replace('서소문 포럼',
                                                                                                         '').replace(
            '포럼', '').replace('홍태경의 지구',
                              '').replace('Column', '').replace('최준호의 사이언스', '').replace('”', '').replace('인터뷰',
                                                                                                          '').replace(
            '경제시평', '').replace('DA 이슈', '').replace('시선', '').replace('시평', '').replace('D 피플라운지',
                                                                                         '').replace('김영필의 3분 월스트리트',
                                                                                                     '').replace(
            'epaselect', '').replace('시론', '').replace('오늘의 날씨',
                                                       '').replace('fnRASSI', '').replace('우리말 톺아보기', '').replace(
            '살며 사랑하며', '').replace('여의춘추',
                                   '').replace('혜윰노트', '').replace('김귀남의 기업가정신 바로보기', '').replace('포토', '').replace(
            '한경에세이',
            '').replace('SC이슈', '').replace('직설', '').replace('임수지의 글로벌 CEO 인사이트', '').replace('인 잇',
                                                                                               '').replace('DA 리뷰',
                                                                                                           '').replace(
            'DAY컷', '').replace('fn', '').replace('해시태그',
                                                  '').replace('오류를 우회하기 위한 함수 추가', '').replace('속보', '').replace(
            'PRNewswire',
            '').replace('분양 포커스', '').replace('투데이 연예', '').replace('스타@스타일', '').replace('엑 s PICK',
                                                                                          '').replace('엑 s',
                                                                                                      '').replace(
            'SHOT', '')

        result_headline = result_headline.replace('”', '').replace(', ,', '').replace('엑 s HD',
                                                                                      '').replace('···', ' ').replace(
            '··', ' ').replace('’', '').replace('...', '. ').replace('..',
                                                                     '. ').replace('<>', '').replace('()', '').replace(
            ' · ', '').replace('/', '').replace('≪≫',
                                                '').replace('{}', '').replace('[]', '').replace('【】', '').replace('xa0',
                                                                                                                  '').replace(
            '\\', '')
        result_headline = re.sub(' +', ' ', result_headline)  # 공백 에러 삭제 MD
        result_headline = re.sub(cls.unvailiable_text, ' ', result_headline)
        result_headline = result_headline.strip()
        if result_headline[-1] != '.':
            result_headline = result_headline + '.'
        return result_headline
