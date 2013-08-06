# -*- coding:utf-8 -*-

alias = []
handler = []

import urllib
import urllib2
import re
import HTMLParser


def cmd_gg(bot, line, args):
    if not args:
        bot.con.query(
            'PRIVMSG',
            line.target,
            u'구글 검색 명령어입니다. | usage: ?gg 검색어'
        )
        return

    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.52 Safari/537.17')]
    try:
        data = opener.open('http://www.google.co.kr/search?%s' % urllib.urlencode({'q': args.encode('utf8')}), None, 3).read()
    except:
        bot.con.query(
            'PRIVMSG',
            line.target,
            u'멍멍! 접속에 실패하였습니다.'
        )
        return

    data = data.decode('utf8', 'replace')
    data = data.replace('\n', ' ').replace('\r', '')
    f = data.find('<li class="g')
    if f == -1:
        bot.con.query('PRIVMSG', line.target, u'검색 실패')
    else:
        website = r'<li class="g"><div[^>]*>\s*<div[^>]*>\s*<div[^>]*>\s*</div>\s*</div>\s*'+\
        r'<h3 class="r"><a href="([^"]+)"[^>]+>(.+?)</a></h3>'+\
        r'<div class="s"><div class="f kv"><cite>.*?</cite>(?:.*?</div>)?'+\
        r'(?:<span class="gl">.+?</span>)?(?:<span class="vshid">.+?</span>)?(?:<span class="std">(?:&nbsp;<span class=gl>-</span>)?.+?</span>)?(?:<a[^>]+><span class="pplsrsl">.+?</span></a>)?'+\
        r'(?:<div data-ved[^>]+>.+?</div>)?'+\
        r'</div>(?:<div class="esc slp"[^>]+>.+?</div>)?(?:<span class="f">.+?</span>)?'+\
        r'(?:<table class="ts">(?<!<span class="st">))?'+\
        r'<span class="st">(.+?)</span>'+\
        r'(?:<div class=osl>.+?</div>)?(?:<table[^>]*>.+?</table>)?'+\
        r'(?:</td></tr></table>)?'+\
        r'</div>(?:<h3[^>]+>.+?</h3>)?<!--n--></div>(?:<table class="nrgt" cellpadding="0" cellspacing="0">.+?</table>)?</li>'
        """
<li class="g"><div data-hveid="72" class="vsc" sig="lkW">  <div data-ved="0CEkQkgowAg">  <div data-ved="0CEoQkQowAg"> </div>   </div>
<h3 class="r"><a href="https://twitter.com/bufferapp"><em>Buffer</em> (bufferapp) on <em>Twitter</em></a></h3>
<div class="s"><div class="f kv"><cite>https://<b>twitter</b>.com/<b>buffer</b>app</cite
><span class="gl">&nbsp;-&nbsp;</span><a ><span class="pplsrsl">공유</span></a>
<div data-ved="0CE4Q5xkw></div>
</div><div class="esc slp"></div>
<span class="st">The latest from Buffer (@bufferapp). Hi guys, the official <em>Buffer Twitter</em> account is over at @buffer. Come join us there! Oh and feel free to email us any questions&nbsp;<b>...</b><br></span>
</div><!--n--></div></li>

<li class="g"><div data-hveid="46" class="vsc" sig="9fR">  <div data-ved="0CC8QkgowAA">  <div data-ved="0CDAQkQowAA"> </div>   </div>
<h3 class="r"><a href="http://bufferapp.com/"><em>Buffer</em> - A Smarter Way to Share on Social Media</a></h3>
<div class="s"><div class="f kv"><cite><b>buffer</b>app.com/</cite>
<span class="gl">&nbsp;-&nbsp;</span><span class="vshid"></span><span class="std">&nbsp;<span class=gl>-</span></a></span><a href="javascript:void(0)" ><span class="pplsrsl">공유</span></a>
<div data-ved="0CDcQ5xkwAA" class="pplsrslc" id="srslc_0"></div>
</div><div class="esc slp"></div>
<span class="st">Easily add great articles, pictures and videos to your <em>Buffer</em> and we automagically share them for you through the day! Sign in or Sign up! Sign In with <em>Twitter</em>&nbsp;<b>...</b><br></span>
<div class=osl></div>
</div><!--n--></div></li>


<li class="g"><div class="vsc" sig="Wth">  <div data-ved="0CDkQkgowAA">  <div data-ved="0CDoQkQowAA"> </div>   </div>   <h3 class="r">
<a href="http://flask.pocoo.org/">Welcome | <em>Flask</em> (A <em>Python</em> Microframework)</a></h3>
<div class="s"><div class="f kv"><cite><b>flask</b>.pocoo.org/</cite>
<span class="gl"> - <a >저장된&nbsp;페이지</a></span><span class="vshid"><a>유사한 페이지</a></span><span class="std">&nbsp;<span class=gl>-</span> <a>이 페이지 번역하기</a></span></div>
<div class="esc slp" id="poS0" style="display:none">공개적으로 +1했습니다.&nbsp;<a href="#" class="fl">실행취소</a></div>
<table class="ts"><span class="st">A lightweight <em>Python</em> web framework based on Werkzeug and Jinja 2. Code, documentation, and community links are provided.<br></span>
<div class=osl></div></td></tr></table></div></div><!--n--></li><!--m--><li class="g"><div class="vsc" sig="6Fx">  <div data-ved="0CEoQkgowAQ">  <div data-ved="0CEsQkQowAQ"> </div>   </div>   <h3 class="r"><a href="http://flask-script.readthedocs.org/" target=_blank class=l onmousedown="return rwt(this,'','','','2','AFQjCNGcqGuT-SoP1Vlm-SRGrZ7uHw2GGg','','0CEwQFjAB','','',event)"><em>Flask</em>-Script — <em>Flask</em>-Script 0.4.0 documentation</a></h3><div class="s"><div class="f kv"><cite><b>flask</b>-script.readthedocs.org/</cite><span class="gl"> - <a href="http://webcache.googleusercontent.com/search?q=cache:k6qEErq9OqAJ:flask-script.readthedocs.org/+&amp;cd=2&amp;hl=ko&amp;ct=clnk&amp;gl=kr&amp;client=firefox-a" onmousedown="return rwt(this,'','','','2','AFQjCNGEN52splsnYtonRiW0uJ1PSi2Xog','','0CE0QIDAB','','',event)" target="_blank" target="_blank">저장된&nbsp;페이지</a></span><span class="std">&nbsp;<span class=gl>-</span> <a href="http://translate.google.co.kr/translate?hl=ko&amp;sl=en&amp;u=http://flask-script.readthedocs.org/&amp;prev=/search%3Fq%3Dpython%2Bflask%26hl%3Dko%26newwindow%3D1%26client%3Dfirefox-a%26hs%3DHus%26rls%3Dorg.mozilla:ko:official%26channel%3Dfflb&amp;sa=X&amp;ei=KGEnUcfLGtCViQeRyYCQAg&amp;ved=0CE4Q7gEwAQ" class=fl target=_blank>이 페이지 번역하기</a></span></div><div class="esc slp" id="poS1" style="display:none">공개적으로 +1했습니다.&nbsp;<a href="#" class="fl">실행취소</a></div><span class="st">The <em>Flask</em>-Script extension provides support for writing external scripts in <em>Flask</em>. This includes running a development server, a customised <em>Python</em> shell, scripts <b>...</b><br></span></div></div><!--n--></li>

<li class="g"><div class="vsc" sig="18q">  <div data-ved="0CDUQkgowAA">  <div data-ved="0CDYQkQowAA"> </div>   </div>   <h3 class="r">
<a href="http://isohunt.com/torrent_details/434772113/Shows.torrent"><em>무한도전</em>.E306.121201.HDTV.H264.720p-WITH.mp4 › Shows <b>...</b></a></h3>
<div class="s"><div class="f kv"><cite>isohunt.com/.../Shows.torre...</cite>
<span class="gl"> - <a  target="_blank" target="_blank">저장된&nbsp;페이지</a></span>
<span class="std">&nbsp;<span class=gl>-</span> <a target=_blank>이 페이지 번역하기</a></span>
<a ><span class="pplsrsl">공유</span></a>
<div data-ved">+페이지에서 확인하세요.</a></div>
</div><div class="esc slp" id="poS0" style="display:none">공개적으로 +1했습니다.&nbsp;<a href="#" class="fl">실행취소</a></div>
<span class="st">bttrack.9you.com:80/:8080/announce: 1 seeds. Uploader&#39;s Comments: Category: TV shows. Seeds: 232Leechers: 4Size: 1.33 GBMore @ Limetorrents.com <b>...</b><br></span>
</div></div><!--n--></li>

<li class="g"><div class="vsc" sig="3u9">  <div data-ved="0CEAQkgowAg">  <div data-ved="0CEEQkQowAg"> </div>   </div>   <h3 class="r">
<a href="http://westhooksandandgravel.com/BlueClayPondSiltCrushedItem4.html">Westhook Sand&amp;Gravel: Blue Clay, Pond Silt Crushed <em>Item4</em></a></h3>
<div class="s"><div class="f kv"><cite>westhooksandandgravel.co...</cite>
<span class="gl"> - <a>저장된&nbsp;페이지</a></span>
<span class="vshid"><a LUYn5E9CviQf93YGgCQ&amp;ved=0CEQQHzAC">유사한 페이지</a></span>
<span class="std">search%3Fq%3Ditem4%26hl%3Dko%26newwindow%3D1%26tbo%3Dd&amp;sa=X&amp;ei=i4YLUYn5E9CviQf93YGgCQ&amp;ved=0CEUQ7gEwAg" class=fl target=_blank>이 페이지 번역하기</a></span>
<a href="javascript:void(0)" data-ved="0CEcQ5hkwAg" class="pplsrsla" data-url="http://westhooksandandgravel.com/BlueClayPondSiltCrushedItem4.html" data-title="Westhook Sand&amp;Gravel: Blue Clay, Pond Silt Crushed Item4" data-desc="Suggested Uses*: This material is used in much the same way that blue clay is, but it is of a different coarseness, and it may also contain tailings. Be sure to ..." data-sli="srsl_2" data-ci="srslc_2" data-vli="srslcl_2" id="srsl_2" data-slg="webres" jsaction="srl.s" role="button" tabindex="0"><span class="pplsrsl">공유</span></a><div data-ved="0CEgQ5xkwAg" class="pplsrslc" id="srslc_2">Google+에서 공유했습니다.&nbsp;<a href="javascript:void(0)" class="pplsrslcl" id="srslcl_2" data-ved="">+페이지에서 확인하세요.</a></div></div><div class="esc slp" id="poS2" style="display:none">공개적으로 +1했습니다.&nbsp;<a href="#" class="fl">실행취소</a></div><span class="st">Suggested Uses*: This material is used in much the same way that blue clay is, but it is of a different coarseness, and it may also contain tailings. Be sure to <b>...</b><br></span></div></div><!--n--></li>


<li class="g"><div class="vsc" sig="L-B">  <div data-ved="0CEwQkgowAg">  <div data-ved="0CE0QkQowAg"> </div>   </div>   <h3 class="r">
<a href="http://me2day.net/i_u0516" target=_blank class=l onmousedown="return rwt(this,'','','','3','AFQjCNF25a0QXw_s-nyDpQrrCwxiMXnQyA','','0CE4QFjAC','','',event)">아이유님의 <em>미투데이</em></a></h3>
<div class="s"><div class="f kv"><cite>me2day.net/i_u0516</cite>
<span class="vshid"><a href="/search?hl=ko&amp;newwindow=1&amp;tbo=1&amp;q=related:me2day.net/i_u0516+%EB%AF%B8%ED%88%AC%EB%8D%B0%EC%9D%B4&amp;sa=X&amp;ei=In4LUcHIKoiuiQeOtIGwCQ&amp;ved=0CE8QHzAC">유사한 페이지</a></span>
<a href="javascript:void(0)" data-ved="0CFAQ5hkwAg" class="pplsrsla" data-url="http://me2day.net/i_u0516" data-title="아이유님의 미투데이" data-desc="오늘 채팅 함께 하신 분들 재미있으셨어요 ? 전 좋았는데…^^ 인증샷 올려드리고 ..." data-sli="srsl_2" data-ci="srslc_2" data-vli="srslcl_2" id="srsl_2" data-slg="webres" jsaction="srl.s" role="button" tabindex="0"><span class="pplsrsl">공유</span></a>
<div data-ved="0CFEQ5xkwAg" class="pplsrslc" id="srslc_2">Google+에서 공유했습니다.&nbsp;<a href="javascript:void(0)" class="pplsrslcl" id="srslcl_2" data-ved="">+페이지에서 확인하세요.</a></div>
</div><div class="esc slp" id="poS2" style="display:none">공개적으로 +1했습니다.&nbsp;<a href="#" class="fl">실행취소</a></div>
<span class="st">오늘 채팅 함께 하신 분들 재미있으셨어요? 전 좋았는데…^^ 인증샷 올려드리고 <b>...</b><br></span></div></div><!--n--></li>

<li class="g"><div class="vsc" sig="_TT">  <div data-ved="0CFMQkgowAw">  <div data-ved="0CFQQkQowAw"> </div>   </div>   <h3 class="r">
<a href="http://me2day.net/me2/welcome"><em>미투데이</em>란 - Me2day</a></h3>
<div class="s"><div class="f kv"><cite>me2day.net/me2/welcome</cite>
<span class="gl"></span><a><span class="pplsrsl">공유</span></a>
<div data-ved="0CFgQ5xkwAw" class="pplsrslc" id="srslc_3">Google+에서 공유했습니다.&nbsp;<a href="javascript:void(0)" class="pplsrslcl" id="srslcl_3" data-ved="">+페이지에서 확인하세요.</a></div>
</div><div class="esc slp" id="poS3" style="display:none">공개적으로 +1했습니다.&nbsp;<a href="#" class="fl">실행취소</a></div>
<span class="st">미투모바일 &middot; 미투 플러그인 &middot; 미투앱스 &middot; 미투데이란 &middot; 미투데이 소개 &middot; 미투데이 <b>...</b><br></span></div></div>

<li class="g"><div class="vsc" sig="UV5">  <div data-ved="0CDkQkgowAA">  <div data-ved="0CDoQkQowAA"> </div>   </div>   <h3 class="r">
<a href="https://minecraft.net/" target=_blank class=l onmousedown="return rwt(this,'','','','1','AFQjCNFrDD6WaaabZPpq6gPLTuhKWwpJrw','','0CDsQFjAA','','',event)"><em>Minecraft</em></a></h3><div class="s"><div class="f kv"><cite>https://<b>minecraft</b>.net/</cite>
<span class="gl"> - <a href="http://webcache.googleusercontent.com/search?q=cache:rzlwQPgdcWAJ:https://minecraft.net/+&amp;cd=1&amp;hl=ko&amp;ct=clnk&amp;gl=kr" onmousedown="return rwt(this,'','','','1','AFQjCNGkaSbT3Zj_RgTATk4aIhJBmQl75w','','0CDwQIDAA','','',event)" target="_blank" target="_blank">저장된&nbsp;페이지</a></span><a href="javascript:void(0)" data-ved="0CD0Q5hkwAA" class="pplsrsla" data-url="https://minecraft.net/" data-title="Minecraft" data-desc="Minecraft is a game about placing blocks to build anything you can imagine. At night monsters come out, make sure to build a shelter before that happens." data-sli="srsl_0" data-ci="srslc_0" data-vli="srslcl_0" id="srsl_0" data-slg="webres" jsaction="srl.s" role="button" tabindex="0"><span class="pplsrsl">공유</span></a><div data-ved="0CD4Q5xkwAA" class="pplsrslc" id="srslc_0">Google+에서 공유했습니다.&nbsp;<a href="javascript:void(0)" class="pplsrslcl" id="srslcl_0" data-ved="">+페이지에서 확인하세요.</a></div></div><div class="esc slp" id="poS0" style="display:none">공개적으로 +1했습니다.&nbsp;<a href="#" class="fl">실행취소</a></div>
<span class="st"><em>Minecraft</em> is a game about placing blocks to build anything you can imagine. At night monsters come out, make sure to build a shelter before that happens.<br></span>
<div class=osl></div></div></div><!--n--></li>


<li class="g"><div class="vsc" sig="Xb7">  <div data-ved="0CFwQkgowCg">  <div data-ved="0CF0QkQowCg"> </div>   </div>   <h3 class="r">
<a href="http://answers.microsoft.com/message/2793f6e3-596a-e011-8dfc-68b599b31bf5?threadId=046a4447-6969-e011-8dfc-68b599b31bf5">windows 7 에서 <em>cmd</em>.exe를 <em>복사</em>하여 사용하기 - Microsoft Community</a></h3>
<div class="s"><div class="f kv"><cite>answers.microsoft.com/.../2793f6e3-596a-e011-...</cite>
<span class="gl"> - <a >저장된&nbsp;페이지</a></span><a ><span class="pplsrsl">공유</span></a>
<div data-ved="0CGEQ5xkwCg" class="pplsrslc" id="srslc_10">Google+에서 공유했습니다.&nbsp;<a href="javascript:void(0)" class="pplsrslcl" id="srslcl_10" data-ved="">+페이지에서 확인하세요.</a></div>
</div><div class="esc slp" id="poS10" style="display:none">공개적으로 +1했습니다.&nbsp;<a href="#" class="fl">실행취소</a></div>
<span class="st">32 bit 응용프로그램에서 64bit의 <em>cmd</em> 창을 사용하기 위하여 아래 명령으로 <em>복사</em>를 하였습니다. copy %windir%\system32\<em>cmd</em>.exe %windir%\cmd64.exe 이후 <b>...</b><br></span></div></div><!--n--></li>

<li class="g"><div class="vsc" sig="8Xv">  <div data-ved="0CGMQkgowCw">  <div data-ved="0CGQQkQowCw"> </div>   </div>   <h3 class="r">
<a href="http://weezzle.net/3097">[Windows XP][도스 창] <em>Command</em> (<em>CMD</em>) 명령어 모음!!</a></h3>
<div class="s"><div class="f kv"><cite><span class=bc>weezzle.net &rsaquo; <a >컴퓨터</a> &rsaquo; <a>운영체제(OS)</a></span></cite>
<span class="gl"> - <a >저장된&nbsp;페이지</a></span><a ><span class="pplsrsl">공유</span></a>
<div data-ved="0CGsQ5xkwCw" class="pplsrslc" id="srslc_11">Google+에서 공유했습니다.&nbsp;<a href="javascript:void(0)" class="pplsrslcl" id="srslcl_11" data-ved="">+페이지에서 확인하세요.</a></div>
</div><div class="esc slp" id="poS11" style="display:none">공개적으로 +1했습니다.&nbsp;<a href="#" class="fl">실행취소</a></div>
<span class="st"><span class="f">2012. 6. 23. &ndash; </span><em>CMD</em> Windows 명령 인터프리터의 새 인스턴스를 시작합니다. COLOR 콘솔의 <b>...</b> COPY 하나 이상의 파일을 다른 위치로 <em>복사</em>합니다. DATE 날짜를 <b>...</b><br></span></div></div><!--n--></li>

li class="g"><div class="vsc" sig="t9t">  <div data-ved="0CG4QkgowDA">  <div data-ved="0CG8QkQowDA"> </div>   </div>   <h3 class="r">
<a href="http://www.google.com/support/adwordseditor/bin/bin/answer.py?answer=57767&amp;hl=ko">애드워즈 에디터 빠른 참조(Mac용) - 애드워즈 에디터 도움말</a></h3>
<div class="s"><div class="f kv"><cite>www.google.com/support/.../answer.py?...hl...</cite>
<span class="gl"> - <a >저장된&nbsp;페이지</a></span><a ><span class="pplsrsl">공유</span></a>
<div data-ved="0CHMQ5xkwDA" class="pplsrslc" id="srslc_12">Google+에서 공유했습니다.&nbsp;<a href="javascript:void(0)" class="pplsrslcl" id="srslcl_12" data-ved="">+페이지에서 확인하세요.</a></div>
</div><div class="esc slp" id="poS12" style="display:none">공개적으로 +1했습니다.&nbsp;<a href="#" class="fl">실행취소</a></div>
<span class="f">50개 항목 &ndash; </span>
<span class="st">변경사항 다운로드, 게시 또는 확인, 계정 열기, <em>Cmd</em>+O.<br></span><table class="tsnip"><tbody><tr><td>최근 변경사항 가져오기 - 기본 옵션(빠름)<td><em>Cmd</em>+R<tr><td>최근 변경사항 가져오기 - 추가 데이터(느림)<td><em>Cmd</em>+Alt+R</table></div></div><!--n--></li> <li class="foot s"><a class="fl" href="/search?q=cmd+%EB%B3%B5%EC%82%AC&amp;hl=ko&amp;newwindow=1&amp;tbo=d&amp;ei=21ALUbKyOMnpiAeV5oH4BA&amp;start=10&amp;sa=N&amp;ved=0CHUQqx8">웹문서 더보기</a></li><li class="head"><b>Q&amp;A</b></li>

        """

        blog = r'<li class="g "><div[^>]+><span[^>]+><h3 class=r><a class=l href="([^"]+)"[^>]+>(.+?)</a></h3>.?'+\
        r'<nobr>.+?</nobr></span>'+\
        r'<div class=s><cite>.+?</cite>'+\
        r'<br>(.+?)</div></div><!--n-->'
        """
<li class="g "><div class=vsc sig=3OH><span class=tl><h3 class=r><a class=l href="http://mwultong.blogspot.com/2007/06/cmd-copy.html" target=_blank class=l onmousedown="return rwt(this,'','','','1','AFQjCNGH0cavnpudMubZzMUbPbDRLCW5Ew','','0CDEQmAEwAA','','',event)">도스창 내용 <em>복사</em> 방법; 도스창 출력 글자 카피; <em>Cmd</em> Copy</a></h3>‎
<nobr> - <span class=f>2007년 6월 20일</span></nobr></span>
<div class=s><cite><span class=a>mwultong.blogspot.com/&nbsp;-&nbsp;mwultong Blog ... 디카 / IT</span></cite><br>도스창 내용 <em>복사</em> 방법; 도스창 출력 글자 카피; <em>Cmd</em> Copy. Thursday, June 21, 2007. 윈도우 도스창에서, 어떤 명령을 실행했을 때 출력된 글자들을 <em>복사</em>하여 다른 <b>...</b></div></div><!--n--><!--m-->

<li class="g "><div class=vsc sig=YtB><span class=tl><h3 class=r><a class=l href="http://coolpunch.tistory.com/315" target=_blank class=l onmousedown="return rwt(this,'','','','2','AFQjCNElxmbXOh8au44IKU-3GO0CSt3Q0A','','0CDUQmAEwAQ','','',event)"><em>CMD</em> 에서 마우스 이용 방법 :: 쿨펀치의 세상리뷰</a></h3>‎
<nobr> - <span class=f>2012년 1월 31일</span></nobr></span>
<div class=s><cite><span class=a>coolpunch.tistory.com/&nbsp;-&nbsp;쿨펀치의 세상리뷰</span></cite><br>장점 1. <em>CMD</em> 창에서 사용한 명령어 드래그 <em>복사</em>가 가능하다. 2. 마우스 드래그 <em>복사</em> 명령어 메모장이나 기타 텍스트 편집 유틸에 <em>복사</em>가 가능 단점 1.</div></div><!--n--><!--m-->"""

        data = data[f:]
        blog_pos = data.find('<li class="g ">')
        web_pos = data.find('<li class="g">')
        if blog_pos == -1 and web_pos == -1:
            bot.con.query(
                'PRIVMSG',
                line.target,
                u'알 수 없는 에러'
            )
            return
        elif blog_pos == -1:
            pattern = website
        elif web_pos == -1:
            pattern = blog
        elif blog_pos < web_pos:
            pattern = blog
        else:
            pattern = website
        pattern = re.compile(pattern)

        iterator = pattern.finditer(data)

        c = 1
        for x in iterator:
            res = u'[ %s - %s ] %s' % (x.group(2), x.group(1), x.group(3))
            res = res.replace('<br>', '').replace('<wbr>', '')
            res = res.replace('<b>', '').replace('</b>', '')
            res = res.replace('<em>', '\x02').replace('</em>', '\x02')
            res = res.replace('<span class="f">', '').replace('</span>', '')
            res = re.sub('<a [^>]+>(.+?)</a>', r'\1', res)

            res = HTMLParser.HTMLParser().unescape(res)
            bot.con.query(
                'PRIVMSG',
                line.target,
                res
            )
            c += 1
            if c > 3:
                break

        if c == 1:
            bot.con.query(
                'PRIVMSG',
                line.target,
                u'파싱 실패' + str(data.find('<li class="g">'))
            )


def main():
    pass

if __name__ == '__main__':
    main()
