from ibapi import wrapper
from ibapi.client import EClient
from ibapi.utils import iswrapper #just for decorator
from ibapi.common import *
from ibapi.contract import *
from ibapi.ticktype import *

class TestApp(wrapper.EWrapper, EClient):
    def __init__(self):
        wrapper.EWrapper.__init__(self)
        EClient.__init__(self, wrapper=self)
        self.reqIsFinished = True
        self.started = False
        self.nextValidOrderId = 0

    @iswrapper
    def nextValidId(self, orderId:int):
        print("setting nextValidOrderId: %d", orderId)
        self.nextValidOrderId = orderId
        # we can start now

    @iswrapper
    def error(self, reqId:TickerId, errorCode:int, errorString:str):
        print("Error. Id: " , reqId, " Code: " , errorCode , " Msg: " ,     errorString)

    @iswrapper
    # ! [contractdetails]
    def contractDetails(self, reqId: int, contractDetails: ContractDetails):
        super().contractDetails(reqId, contractDetails)
        print("ContractDetails. ReqId:", reqId, contractDetails.summary.symbol,
              contractDetails.summary.secType, "ConId:", contractDetails.summary.conId,
          "@", contractDetails.summary.exchange)
        # ! [contractdetails]

    @iswrapper
    # ! [contractdetailsend]
    def contractDetailsEnd(self, reqId: int):
        super().contractDetailsEnd(reqId)
        print("ContractDetailsEnd. ", reqId, "\n")
        self.done = True  # This ends the messages loop
        # ! [contractdetailsend]

def main():
    app = TestApp()
    app.connect("127.0.0.1", 7496, clientId=123)
    print("serverVersion:%s connectionTime:%s" % (app.serverVersion(),
                                            app.twsConnectionTime()))

    print('MSFT contract details:')
    contract = Contract()
    contract.symbol = "MSFT"
    contract.secType = "STK"
    contract.currency = "USD"
    contract.exchange = ""
    app.reqContractDetails(210, contract)
    app.run()

    print('IBM contract details:')
    contract.symbol = "IBM"
    app.done = False # must be set before next run
    app.reqContractDetails(210, contract)
    app.run()

    app.disconnect() 

if __name__ == "__main__":
    main()