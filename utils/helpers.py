def getHtml(pageName):
    with open(f"templates/{pageName}.html") as htmlPage:
        return htmlPage.read()