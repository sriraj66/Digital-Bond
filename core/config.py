from web3 import Web3

web3 = Web3(Web3.HTTPProvider('http://127.0.0.1:7545'))

def pay_eth(from_acc,to_acc,pv,amt):
    print(from_acc," to ",to_acc," : ",amt," ETH")
    context = {}
    if not web3.isConnected():
        context['err']= "Check Internet"
    
    balance = web3.eth.get_balance(from_acc)
    if balance <0:
        context['err']= "In suff blance"
    
   

    address1 = web3.toChecksumAddress(from_acc)
    address2 = web3.toChecksumAddress(to_acc)
    nonce = web3.eth.getTransactionCount(address1)
    tx = {
    'nonce':nonce,
    'to':address2,
    'value':web3.toWei(float(amt), 'ether'),
    'gas':200000,
    'gasPrice':web3.toWei('50', 'gwei')
    }
    signed_tx = web3.eth.account.signTransaction(tx,private_key=pv)
    try:
        tx_transation = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
        tx_script = web3.toHex(tx_transation)
        tx_recipt = web3.eth.wait_for_transaction_receipt(tx_script)
        context['hash'] = tx_script
        context['recipt'] = tx_recipt
        context['transction'] = True
    except ValueError as e:
        context['err'] = str(e)
        context['transction'] = False

    return context