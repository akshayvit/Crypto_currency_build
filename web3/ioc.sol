pragma solidity >=0.4.0;

contract ioc {
    uint public akcoins=1000000;
    uint public usd_to_akcoins=1000;
    uint public akcoins_bought=0;
    mapping(address=>uint) equity_akcoins;
    mapping(address=>uint) equity_usd;
    modifier can_buy_akcoins(uint  usd_invested) {
        require(usd_invested*usd_to_akcoins+akcoins<=akcoins);
        _;
    }
    function equity_in_akcoins(address investor) external  returns (uint){
        return equity_akcoins[investor];
    }

    function equity_in_usd(address investor) external  returns (uint){
        return equity_usd[investor];
    }

    function buy_akcoins(address investor,uint usd_invested) external can_buy_akcoins(usd_invested) {
        uint investor_hascoins=usd_invested*usd_to_akcoins;
        equity_akcoins[investor]+=investor_hascoins;
        equity_akcoins[investor]/=usd_to_akcoins;
        akcoins_bought+=investor_hascoins;
    }

    function sell_akcoins(address investor,uint coins_sold) external {
        equity_akcoins[investor]-=coins_sold/usd_to_akcoins;
        akcoins_bought-=coins_sold;
    }
}