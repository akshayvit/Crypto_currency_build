let solc=require("solc");
let fs=require("fs")
let Web3=require("web3")
let path=require("path")

let web3 = new Web3(new Web3.providers.HttpProvider("http://127.0.0.1:7545"));
let fileContent=fs.readFileSync("ioc.sol").toString();

const dpath=path.join(__dirname+process.cwd())

console.log(fileContent);

var input = {
    language: "Solidity",
    sources: {
      "ioc.sol": {
        content: fileContent,
      },
    },
  
    settings: {
      outputSelection: {
        "*": {
          "*": ["*"],
        },
      },
    },
  };

var output=JSON.parse(solc.compile(JSON.stringify(input)));
console.log(JSON.stringify(output));
ABI = output.contracts["ioc.sol"]["ioc"].abi;
bytecode = output.contracts["ioc.sol"]["ioc"].evm.bytecode.object;
console.log("Bytecode: ", bytecode);
console.log("ABI: ", ABI);
