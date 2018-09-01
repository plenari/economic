#coding:utf-8
import msvcrt
import sys
import TradeX

class QA_Query():
    sHost = "101.227.77.254"
    nPort = 7709
    def login(self):
        try:
            self.clientHq = TradeX.TdxHq_Connect(self.sHost, self.nPort)
            return self.clientHq
        except TradeX.error as e:
            print ("error: " + e.message)
            sys.exit(-1)


    def query_k(self,client,stock,num):
        nCategory = 9
        
        
        nStart = 0
       
        if str(stock)[0]=='6':
            nMarket = 1
        else:
            nMarket = 0
        errinfo, count, result = client.GetSecurityBars(nCategory, nMarket, stock, nStart, num)
        if errinfo != "":
            print (errinfo)
        else:
            #print(stock)
            #print(nMarket)
            #print(result)
            temp=result.split('\n')
            res=[]
            for i in range(1,len(temp),1):
                res.append(temp[i].split('\t'))
            res.sort()
            #print(res)
            return res
if __name__=='__main__':
    qe=QA_Query()
    qc=qe.login()
    res=qe.query_k(qc,'000002',6)
    print(res)