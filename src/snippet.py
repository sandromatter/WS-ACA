def save(url):
    response = requests.urlopen(url)
    html_doc = response.read()
    soup = BeautifulSoup(html_doc, 'html.parser')

    fields = {}

    fields['headline'] = soup.find("span", class_="lede-headline__highlighted").text
    fields['cover_data'] = ""
    fields['cover_url'] = ""
    fields['cover_credit'] = soup.find("div", class_="credit").text
    fields['author_name'] = soup.find("a", class_="author-link").text
    fields['author_url'] = soup.find("a", class_="author-link")['href']
    fields['timestamp_published'] = soup.find("time", itemprop="datePublished")['datetime']
    fields['timestamp_updated'] = soup.find("time", class_="updated-at__time")['datetime']
    fields['abstract'] = soup.findAll("li", class_="article-abstract__item")
    fields['content'] = soup.find("div", class_="article-body__content").text

    print fields['author_url']

    abstract_list = []

    for l in fields['abstract']:
        abstract_list.append(l.text)

    abstract_text = json.dumps(abstract_list, separators=(',',':'))

    #print fields

    final = [url, fields['headline'], fields['cover_data'], fields['cover_url'], fields['cover_credit'], fields['author_name'], fields['author_url'], fields['timestamp_published'], fields['timestamp_updated'], abstract_text, fields['content']]

    # database section
    conn = sqlite3.connect('blmbg.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS articles (id INTEGER PRIMARY KEY AUTOINCREMENT, url TEXT NOT NULL, headline TEXT NOT NULL, cover_data BLOB, cover_url TEXT, cover_credit TEXT, author_name TEXT NOT NULL, author_url TEXT NOT NULL, timestamp_published DATETIME NOT NULL, timestamp_updated DATETIME, abstract TEXT, content TEXT NOT NULL);''')
    c.execute('''INSERT INTO articles (url, headline, cover_data, cover_url, cover_credit, author_name, author_url, timestamp_published, timestamp_updated, abstract, content) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', final)
    conn.commit()
    conn.close()