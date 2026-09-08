trades:([] 
  symbol:`AAPL`MSFT`NVDA;
  price:180.25 420.50 125.75;
  volume:1000 2500 1800
  );

select
  symbol,
  price,
  volume,
  value:price*volume
from trades
