import pymongo

mongo_url = "127.0.0.1:27017"
client = pymongo.MongoClient(mongo_url)
db = client["quantaxis"]

def setMarket():
    db = client["quantaxis"]
    stock_list = db["stock_day"].find()
    guben = db["stock_xdxr"]
    i = 0
    errCodes = []
    for s in stock_list:
        code = s["code"]
        open = s["open"]
        date = s["date"]
        lastGuben = guben.find({"code": code, "date": {"$lte": str(date)}, "liquidity_before": {"$ne": None}})
        try:
            lastGuben = lastGuben[lastGuben.count()-1]
            liquidity_before = int(float(lastGuben["liquidity_before"])*10000)*float(open)
            liquidity_after = int(float(lastGuben["liquidity_after"])*10000)*float(open)
            shares_before = int(float(lastGuben["shares_before"])*10000)*float(open)
            shares_after = int(float(lastGuben["shares_after"])*10000)*float(open)
            data = {"date":date,"code":code,"liquidity_before":liquidity_before,"liquidity_after":liquidity_after,"shares_before":shares_before,"shares_after":shares_after}
            db["financeData"].insert(data)
        except:
            if code not in errCodes:
                errCodes.append(code)
        i+=1
    print(errCodes)

setMarket()
