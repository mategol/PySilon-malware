import requests

websites = ['google.com', 'youtube.com', 'facebook.com', 'twitter.com', 'instagram.com', 'baidu.com', 'wikipedia.org', 'yandex.ru', 'yahoo.com', 'xvideos.com', 'whatsapp.com', 'pornhub.com', 'amazon.com', 'xnxx.com', 'yahoo.co.jp', 'live.com', 'netflix.com', 'docomo.ne.jp', 'tiktok.com', 'reddit.com', 'office.com', 'linkedin.com', 'dzen.ru', 'vk.com', 'xhamster.com', 'samsung.com', 'turbopages.org', 'mail.ru', 'bing.com', 'naver.com', 'microsoftonline.com', 'twitch.tv', 'discord.com', 'bilibili.com', 'pinterest.com', 'zoom.us', 'weather.com', 'qq.com', 'microsoft.com', 'globo.com', 'roblox.com', 'duckduckgo.com', 'news.yahoo.co.jp', 'quora.com', 'msn.com', 'realsrv.com', 'fandom.com', 'ebay.com', 'aajtak.in', 'ok.ru', 't.me', 'sharepoint.com', 'bbc.co.uk', 'nytimes.com', 'espn.com', 'uol.com.br', 'google.com.br', 'amazon.co.jp', 'bbc.com', 'stripchat.com', 'zhihu.com', 'cnn.com', 'indeed.com', 'imdb.com', 'spankbang.com', 'instructure.com', 'rakuten.co.jp', 'booking.com', 'paypal.com', 'apple.com', 'accuweather.com', 'amazon.de', 'etsy.com', 'chaturbate.com', 'news.google.com', 'cricbuzz.com', 'spotify.com', 'google.de', 'ya.ru', 'walmart.com', 'github.com', 'aliexpress.com', 'theguardian.com', 'messenger.com', 'yiyouliao.com', 'amazon.co.uk', 'dailymail.co.uk', 'canva.com', 'hotstar.com', 'amazon.in', 'avito.ru', 'disneyplus.com', 'archiveofourown.org', 'xhamster18.desi', 'line.me', 'pixiv.net', 'google.co.uk', 'marca.com', 'taobao.com', 'xvideos2.com']

def grab_cookies():
    total, done = len(websites), 0
    with open('cookies.txt', 'w') as cookies_save:
        for website in websites:
            for prefix in ['http://', 'https://']:
                cookies_save.write('\n\n' + prefix + website + '\n')
                try:
                    session = requests.Session()
                    website = website.replace('\n', '')
                    response = session.get(prefix + website.replace('\n', ''))

                    cookies = session.cookies.get_dict()
                    for cookie_name in cookies.keys():
                        cookies_save.write(cookie_name + ' -> ' + cookies[cookie_name] + '\n')
                    
                    request = requests.get(prefix + website.replace('\n', ''))
                    for cookie in request.cookies:
                        cookies_save.write(cookie.name + ' -> ' + cookie.value + '\n')
                except: cookies_save.write('Error\n')
            done += 1
    return True
