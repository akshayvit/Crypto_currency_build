let Web3=require('web3');
let web3 = new Web3(new Web3.providers.HttpProvider("http://127.0.0.1:7545"));
web3.eth.getBalance("0xC64d2Ccd9432E2ffF5A8a084148f067D11e85032").then(data=>console.log(data)).catch(err=>console.log(err));
web3.eth.sendTransaction({from:"0xC64d2Ccd9432E2ffF5A8a084148f067D11e85032",
to:"0x55894d9c9cCc7Aa896028B1D69fb6393095620d3",value:web3.utils.toWei("5","ether")})
let contract=new web3.eth.Contract([
	{
		"constant": true,
		"inputs": [
			{
				"name": "investor",
				"type": "address"
			}
		],
		"name": "equity_in_usd",
		"outputs": [
			{
				"name": "",
				"type": "uint256"
			}
		],
		"payable": false,
		"stateMutability": "view",
		"type": "function"
	},
	{
		"constant": false,
		"inputs": [
			{
				"name": "investor",
				"type": "address"
			},
			{
				"name": "coins_sold",
				"type": "uint256"
			}
		],
		"name": "sell_akcoins",
		"outputs": [],
		"payable": false,
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"constant": true,
		"inputs": [],
		"name": "usd_to_akcoins",
		"outputs": [
			{
				"name": "",
				"type": "uint256"
			}
		],
		"payable": false,
		"stateMutability": "view",
		"type": "function"
	},
	{
		"constant": false,
		"inputs": [
			{
				"name": "investor",
				"type": "address"
			},
			{
				"name": "usd_invested",
				"type": "uint256"
			}
		],
		"name": "buy_akcoins",
		"outputs": [],
		"payable": false,
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"constant": true,
		"inputs": [],
		"name": "akcoins",
		"outputs": [
			{
				"name": "",
				"type": "uint256"
			}
		],
		"payable": false,
		"stateMutability": "view",
		"type": "function"
	},
	{
		"constant": true,
		"inputs": [
			{
				"name": "investor",
				"type": "address"
			}
		],
		"name": "equity_in_akcoins",
		"outputs": [
			{
				"name": "",
				"type": "uint256"
			}
		],
		"payable": false,
		"stateMutability": "view",
		"type": "function"
	},
	{
		"constant": true,
		"inputs": [],
		"name": "akcoins_bought",
		"outputs": [
			{
				"name": "",
				"type": "uint256"
			}
		],
		"payable": false,
		"stateMutability": "view",
		"type": "function"
	}
],"0xD7fFCB1291cd4a70883BA18Ec45d1dBAd611ed33");
contract.methods.sell_akcoins("0xC64d2Ccd9432E2ffF5A8a084148f067D11e85032",20).send({from:"0xC64d2Ccd9432E2ffF5A8a084148f067D11e85032"})
contract.methods.akcoins_bought().call().then(data=>console.log(data)).catch(err=>console.log(err));