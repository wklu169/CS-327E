def main():
    # Test 1: "Hello World" program
    print("Test 1")
    print("Hello World")
    print()

    # Test 2: Beautiful Soup
    from urllib.request import urlopen
    from bs4 import BeautifulSoup
    import re

    html = urlopen("http://www.pythonscraping.com/pages/page3.html")
    bsObj = BeautifulSoup(html, "html.parser")

    print("Test 2")
    """
    for child in bsObj.find("table", {"id":"giftList"}).children:
        print (child)
    print()
    """
    images = bsObj.findAll("img", {"src":re.compile("\.\.\/img\/gifts/img.*\.jpg")})
    for image in images:
        print (image["src"])
    print()

    # Test 3: PyMySQL
    import pymysql
    
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='idkyle', passwd='Ymi1693328169!', db='mysql')
    cur = conn.cursor()

    print("Test 3")
    cur.execute("USE bank")
    cur.execute("SELECT * FROM employee WHERE title = 'Head Teller';")
    print(cur.fetchall())
    cur.close()
    conn.close()
    print()
    
    import datetime
    import random

    conn = pymysql.connect(host='127.0.0.1', port=3306, user='idkyle', passwd='Ymi1693328169!', db='mysql', charset='utf8')
    cur = conn.cursor()
    cur.execute("USE scraping")
    
    random.seed(datetime.datetime.now())

    def store(title, content):
        cur.execute("INSERT INTO pages (title, content) VALUES (\"%s\", \"%s\")", (title, content))
        cur.connection.commit()

    def getLinks(articleUrl):
        html = urlopen("http://en.wikipedia.org" + articleUrl)
        bsObj = BeautifulSoup(html, "html.parser")
        title = bsObj.find("h1").get_text()
        content = bsObj.find("div", {"id":"mw-content-text"}).find("p").get_text()
        store(title, content)
        return bsObj.find("div", {"id":"bodyContent"}).findAll("a", href=re.compile("^(/wiki/)((?!:).)*$"))

    try:
        cur.execute("DROP TABLE pages")
    except:
        None
    cur.execute("CREATE TABLE pages (id BIGINT(7) NOT NULL AUTO_INCREMENT, title VARCHAR(200), content VARCHAR(10000), created TIMESTAMP DEFAULT CURRENT_TIMESTAMP, PRIMARY KEY(id));")

    links = getLinks("/wiki/Super_Smash_Bros.")
    counter = 0
    try:
        while len(links) > 0 and counter < 3:
            newArticle = links[random.randint(0, len(links)-1)].attrs["href"]
            print(newArticle)
            links = getLinks(newArticle)
            counter += 1
    finally:
        cur.close()
        conn.close()

main()
