# url = "https://api.cryptocloud.plus/v2/invoice/create"
# headers = {
#     "Authorization": f"Token {CRYPTO_API}",
#     "Content-Type": "application/json"
# }

import aiohttp

class CryptoCloudAPI:
    def __init__(self, token) -> None:
        self.token = token
        self.headers = {"Authorization": f"Token {self.token}", "Content-Type": "application/json"}
        self.urls = {"create_invoice": "https://api.cryptocloud.plus/v2/invoice/create",
                    "cancel_invoice": "https://api.cryptocloud.plus/v2/invoice/merchant/canceled",
                    "invoice_list": "https://api.cryptocloud.plus/v2/invoice/merchant/list",
                    "invoice_information": "https://api.cryptocloud.plus/v2/invoice/merchant/info",
                    "balace": "https://api.cryptocloud.plus/v2/merchant/wallet/balance/all"}
    
    async def createInvoice(self, shop_id, amount, currency):
        data = {
            "amount": amount,
            "shop_id": shop_id,
            "currency": currency
        }

        async with aiohttp.ClientSession() as session:
             async with aiohttp.ClientSession() as session:
                async with session.post(self.urls['create_invoice'], headers=self.headers, json=data) as response:
                    if response.status == 200:
                        r = await response.json()
                        result = r['result']

                        return [f"{result['link']}?lang=ru", result['uuid']]
                    else:
                        return response.status, await response.text()
        

    async def cancelInvoice(self, uuid):
        data = {
            "uuid": uuid
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(self.urls['cancel_invoice'], headers=self.headers, json=data) as response:
                if response.status == 200:
                    r = await response.json()

                    if r['result'] == ['ok']:
                        return 'success'

    
    async def invoiceList(self, start, end):
        data = {
            "start": start,
            "end": end
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(self.urls['invoice_list'], headers=self.headers, data=data) as response:
                if response.status == 200:
                    return await response.json()
                

    async def invoiceInfo(self, uuids = list | str):
        if isinstance(uuids, list):
            data = {
                "uuids": uuids
            }
            async with aiohttp.ClientSession() as session:
                async with session.post(self.urls['invoice_info'], headers=self.headers, data=data) as response:
                    if response.status == 200:
                        return await response.json()
                    
        elif isinstance(uuids, str):
            data = {
                "uuids": [uuids]
            }
            async with aiohttp.ClientSession() as session:
                async with session.post(self.urls['invoice_info'], headers=self.headers, data=data) as response:
                    if response.status == 200:
                        return await response.json()

             
    async def getBalance(self):
        async with aiohttp.ClientSession() as session:
            async with session.post(self.urls['balance'], headers=self.headers) as response:
                if response.status == 200:
                    return await response.json()
                