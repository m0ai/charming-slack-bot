# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import unicode_literals
from rtmbot.core import Plugin
import os
import re
import random
import sqlite3
import requests
from datetime import datetime
from bs4 import BeautifulSoup
# Token is required to use slack api
prob_db = "prob.sqlite"
score_db = "score.sqlite"
score = 3

class ChosungGame(Plugin):
    def create_prob_db(self):
        if os.path.exists(prob_db):
            return
        conn = sqlite3.connect(prob_db)
        c = conn.cursor()
        c.execute("CREATE TABLE prob (subject text, anwser text, hint text, examiner text)")
        conn.commit()
        conn.close()

    def is_exists_subject_in_db(self, subject):
        conn = sqlite3.connect(prob_db)
        c = conn.cursor()
        for row in c.execute(u"SELECT COUNT(*) from prob where subject='{}'".format(subject)):
            count, = row
            if count > 0:
                return True
            elif count == 0:
                return False
            else:
                raise Exception("Unexcepted Error is_exists_subject_in_db")
        conn.close()

    def select_contents_by_random(self):
        conn = sqlite3.connect(prob_db)
        c = conn.cursor()
        data = None
        for row in c.execute(u"SELECT * from prob order by random() limit 1"):
            data = row #subject, anwser, hint, examiner
        conn.close()
        return data

    def insert_content(self, subject, anwser, hint="Handmade", examiner=""):
        conn = sqlite3.connect(prob_db)
        c = conn.cursor()
        payload = u"INSERT INTO {} VALUES ('{subject}', '{anwser}', '{hint}', '{exa}')".format("prob", subject=subject, anwser=anwser, hint=hint, exa=examiner)
        c.execute(payload)
        conn.commit()
        conn.close()

    # 기초 사자성어
    def create_saja_list(self):
        subject = u"사자성어"
        if self.is_exists_subject_in_db(subject) is True:
            return
        return
        url = "https://ko.wiktionary.org/wiki/%EB%B6%80%EB%A1%9D:%EC%82%AC%EC%9E%90%EC%84%B1%EC%96%B4"
        html_code = requests.get(url).text
        soup = BeautifulSoup(html_code, 'html.parser')
        table = soup.find('table', {'class' : 'datatable'})
        for row in table.find_all('tr')[1:]:
            hanja, anwser, mean = [td.text for td in row.find_all('td')]
            hint = [hanja, mean]
            hint = "&".join(hint)
            self.insert_content(subject, anwser, h)
        return

    # 게임 차트 순위
    def create_game_list(self):
        url = "http://www.gamemeca.com/ranking.php?rid=1360"
        game_list = list()
        html_code = requests.get(url).text
        soup = BeautifulSoup(html_code, "html.parser")
        for div in  soup.find_all("div", {'class' : 'game-name'}):
            game_list.append(div.text.encode('utf-8'))

	for page in range(12):
	    url = "http://gamechart100.com/bbs/board.php?bo_table=B11&page={}".format(page)
	    html_code = requests.get(url).text
	    soup = BeautifulSoup(html_code, "html.parser")
	    for div in  soup.find_all("div", {'class' : 'mw_basic_list_subject_desc'}):
		game_list.append(div.a.span.text.encode('utf-8'))

        return u"게임 ", game_list

    # 벅스 앨범 크롤링 2014
    def create_memory_song_list(self):
        song_list = list()
        url = "https://music.bugs.co.kr/musicpd/albumview/11152"
        r = requests.get(url)
        html_code = r.text
        soup = BeautifulSoup(html_code, 'html.parser')
        songs = soup.find_all('p', {'class': 'title'})
        for song in songs:
            song_name = song.a.text
            index = song_name.find(" (")
            if index is not -1:
                song_list.append(song_name[:index].encode('utf-8'))
            else:
                song_list.append(song_name.encode('utf-8'))
        return u"노래", song_list

    # 영화 제목 크롤링 (네이버 영화 평점 순위 크롤링 === 1 ~ 50위)
    def create_movie_list(self):
        keywordList = []
        # 오늘 날짜 계산
        year = str(datetime.today().year)
        if datetime.today().month < 10:
            month = '0' + str(datetime.today().month)
        else:
            month = str(datetime.today().month)
        if datetime.today().day < 10:
            day = '0' + str(datetime.today().day)
        else:
            day = str(datetime.today().day)
        today = year + month + day
        # 제목 크롤링
        url = "http://movie.naver.com/movie/sdb/rank/rmovie.nhn?sel=pnt&date=" + today
        def crawling(url):
            soup = BeautifulSoup(requests.get(url).text, 'html.parser')
            moveList = soup.find_all('div', 'tit5')
            for m in moveList:
                title= m.find('a')
                a = re.search('title=".+"', str(title)).group()[7:-1]
                keywordList.append(str(a))
            return keywordList
        urls = list()
        urls.extend(["http://movie.naver.com/movie/sdb/rank/rmovie.nhn?sel=cur&date=" + today])
        urls.extend(["http://movie.naver.com/movie/sdb/rank/rmovie.nhn?sel=pnt&date=" + today])
        urls.extend(["http://movie.naver.com/movie/sdb/rank/rmovie.nhn?sel=cnt&date=" + today])
        keywordList.extend(map(crawling, urls))
        return u"영화", keywordList

    def paly(self):
        return

    # 초성 생성기
    def create_chosung(self, word):
	BASECODE, END, CHOSUNG = 44032, 55199, 588
	CHOSUNG_LIST = ['ㄱ', 'ㄲ', 'ㄴ', 'ㄷ', \
                        'ㄸ', 'ㄹ', 'ㅁ', 'ㅂ', \
                        'ㅃ', 'ㅅ', 'ㅆ', 'ㅇ', \
                        'ㅈ', 'ㅉ', 'ㅊ', 'ㅋ', \
                        'ㅌ', 'ㅍ', 'ㅎ']
        splitKeywordList = list(word)
        if list(set(CHOSUNG_LIST)&set(splitKeywordList)) != list():
            return None
        result = []
        for keyword in splitKeywordList:
            if ord(keyword) >= BASECODE and ord(keyword) <= END:
                charCode = ord(keyword) - BASECODE
                ch = int(charCode / CHOSUNG)
                result.append(CHOSUNG_LIST[ch])
            else:
                result.append(keyword)
        return result

    # Anwser format is subject:awnser:hint
    def read_anwser_format(self, _str):
        return _str.split("|")

    def write_anwser_format(self, score, subject, anwser, hint="no hint"):
        return "{}|{}|{}|{}".format(score, subject, anwser, hint)

    def write_anwser(self, score, subject, anwser, hint="no hint"):
        with open("anwser", 'w') as f:
            f.write(self.write_anwser_format(score, subject, anwser, hint).encode('utf8')) # save successful

    def read_anwser(self):
        with open("anwser", 'r') as f:
            anwser = f.readline().decode('utf8')
            return self.read_anwser_format(anwser)

    def is_correct(self, keyword):
        with open("anwser", 'r') as f:
            _, _, anwser, _ = self.read_anwser()
            return keyword == anwser
        return False

    def get_userinfo(self, name):
        url = "https://slack.com/api/users.info?token={}&&user={}"\
                .format(os.environ['SLACK_BOT_TOKEN'], name)
        import json
        data = requests.get(url).text
        return json.loads(data)['user']

    def process_message(self, data):
        self.create_prob_db()
        self.run_rank_system()
        # Only Vaild DM
        if data['channel'].startswith("D"):
            text = data['text']
            if text == "help":
                self.outputs.append([data['channel'], u"초성 문제 등록 방법"])
                self.outputs.append([data['channel'], u"> 정답:모아이 석상:세계미스테리 중 하나"])
                self.outputs.append([data['channel'], u"> 정답:{정답}:{주제}"])
                self.outputs.append([data['channel'], u"요렇게 말하면 됩니다."])
            elif text.startswith(u"정답:") and text.find(u":") == 2:
                text = text.split(":")
                anwser = text[1]
                subject = text[2]
                general = "C5FJ1SN1X"
                userinfo = self.get_userinfo(data['user'])
		cs = self.create_chosung(anwser)
                if cs is None:
                    self.outputs.append([data['channel'], u"엇.. 정답이 이상한 것 같습니다."])
                    return
                self.insert_content(subject, anwser, examiner=userinfo['name'])
                self.write_anwser(3, subject, anwser)

                self.outputs.append([general,  u"@{}님이 문제를 출제하였습니다.\n> {} (3점) : {}"\
                        .format(userinfo['name'], subject, "".join(cs))])
                self.outputs.append([data['channel'],"Okay checkout <#C5FJ1SN1X>"])
            elif text.startswith(u"정답:"):
                self.outputs.append([data['channel'], u"> 정답:{정답}:{주제}"])
                self.outputs.append([data['channel'], u"요렇게 하라고!!!"])

        if data['channel'].startswith("C"):
            text = data['text']
            if  text == "hint":
                score, subject, anwser, hint = self.read_anwser()
                hint = random.choice(hint.split(u"&"))
                if hint[0] == "no hint":
                    self.outputs.append([data['channel'], u"this prob has no hint."])
                else:
                    self.outputs.append([data['channel'], u"score 3 to 1 :(, {}".format(hint)])
                    self.write_anwser(1, subject, anwser, hint)
            elif text == "prob":
                self.create_saja_list()
                subject, anwser, hint, _ = self.select_contents_by_random()
                self.write_anwser(3, subject, anwser, hint)
		cs = self.create_chosung(anwser)
                self.outputs.append([data['channel'], u"{} (3점) : {}".format(subject, "".join(cs))])
            elif text == "re":
                score, subject, keyword, hint = self.read_anwser()
		cs = self.create_chosung(keyword)
                self.outputs.append([data['channel'], u"{subject} : {anwser}".format(subject=subject, anwser="".join(cs))])

            elif text.startswith("!"):
                word = text[1:]
                userinfo = self.get_userinfo(data['user'])
                if self.is_correct(word):
                    self.outputs.append([data['channel'],\
                                "anwser is {}, @{} is correct! currently score {}"\
                                .format(word, userinfo['name'], self.get_score(userinfo['name']))])
                    os.remove("anwser")
                else:
                    self.outputs.append([data['channel'],\
                                u"응 아니야"])
            elif text == "rank":
                    self.outputs.append([data['channel'],\
                                "{}".format(self.print_rank_score())])

    def run_rank_system(self):
        if os.path.exists(score_db):
            return
        conn = sqlite3.connect(score_db)
        c = conn.cursor()
        c.execute("CREATE TABLE chosung (name text, score integer)")
        conn.commit()
        conn.close()


    def get_best_examiner(self):
        conn = sqlite3.connect(prob_db)
        c = conn.cursor()
        best_examiner = ""
        for row in c.execute("select examiner, COUNT(*) FROM prob GROUP BY examiner ORDER BY COUNT(*) DESC"):
            user, total = row
            if user == None:
                continue
            else:
                best_examiner = user
                break
        conn.commit()
        conn.close()
        return best_examiner

    def print_rank_score(self):
        conn = sqlite3.connect(score_db)
        c = conn.cursor()
        best_examiner = self.get_best_examiner()
        output = u""
        for i, row in enumerate(c.execute("SELECT * from chosung order by score DESC")):
            db_username, score = row
            rank = i+1
            special_emoji = ""
            if rank == 1:
                special_emoji += ":crown:"
            elif rank == 2:
                special_emoji += ":kejang4:"
            if best_examiner == db_username:
                special_emoji += ":dollar:"

            output += u">{}위 @{} {} : {}\n".format(rank, db_username, special_emoji, score).lstrip()

        output += u":crown: 1등, :kejang4: 2등, :dollar: 명예 출제자, :gun: 최고 마피아"
        conn.commit()
        conn.close()
        return output

    def get_score(self, user):
        score = None
        db_username = None
        conn = sqlite3.connect(score_db)
        c = conn.cursor()
        for row in c.execute("SELECT * FROM chosung WHERE name='{}'".format(user)):
            db_username, score = row

        if db_username is None:
            c.execute("INSERT INTO chosung VALUES ('{}', {})".format(user, 0))
            conn.commit()
            score = 0
        prob_score, _, _, _= self.read_anwser()
        c.execute("UPDATE chosung SET score='{}' WHERE name='{}'".format(score+int(prob_score), user))
        conn.commit()
        conn.close()
        return score+1
