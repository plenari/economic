您的策略异常终止: Traceback (most recent call last):
  File /tmp/strategy/user_strategy.py, line 496 in rebalance_first_part
    if MARKET_PANIC_SIGNALS and market_panic(MARKET_PANIC_SIGNALS, bar_dict):
    --> context = Context({pool = [], strategy_stop = False, day_stop = False, count = 0, market_panic = False})
    --> stocks = ['600648.XSHG', '601877.XSHG', '601628.XSHG', '600886.XSHG', '601099.XSHG', '600104.XSHG', '600485.XSHG', '000876.XSHE', '000938.XSHE', '601872.XSHG', '600031.X ...
    --> filtered = []
    --> bar_dict = BarMap()

  File /tmp/strategy/user_strategy.py, line 346 in market_panic
    result = f([index], rule, bar_dict)
    --> index = '000300.XSHG'
    --> rule = {'lhs': {'name': 'MACD', 'parameters': [12, 26, 9], 'type': 'technical'}, 'operator': 'short', 'rhs': [10, 20]}
    --> bar_dict = BarMap()
    --> f = <function technical_filter at 0x7f6144146c80>
    --> rules = [{'index': '000300.XSHG', 'rule': {'lhs': {'name': 'n_day_loss_rate', 'parameters': [10], 'type': 'pricing'}, 'operator': 'greater_than', 'rhs': 3}}, {'index':  ...
    --> r = {'index': '000300.XSHG', 'rule': {'lhs': {'name': 'MACD', 'parameters': [12, 26, 9], 'type': 'technical'}, 'operator': 'short', 'rhs': [10, 20]}}
    --> result = []

  File /tmp/strategy/user_strategy.py, line 235 in technical_filter
    if lv[-1] < _to_scalar(rv):
    --> lhs = {'name': 'MACD', 'parameters': [12, 26, 9], 'type': 'technical'}
    --> s = '000300.XSHG'
    --> lv = [array([         nan,          nan,          nan,          nan,
                nan,          nan,          nan,          nan,
                nan,          nan ...
    --> filtered_stocks = []
    --> operator = 'short'
    --> stocks = ['000300.XSHG']
    --> rule = {'lhs': {'name': 'MACD', 'parameters': [12, 26, 9], 'type': 'technical'}, 'operator': 'short', 'rhs': [10, 20]}
    --> rhs = [10, 20]
    --> rv = [10, 20]
    --> bar_dict = BarMap()

ValueError: operands could not be broadcast together with shapes (100,) (2,) 


MARKET_ENTER_SIGNALS = [
    
    {'index': '000300.XSHG', 'rule': {'lhs': {'name': 'n_day_loss_rate', 'type': 'pricing', 'parameters': [10]}, 'rhs': 3, 'operator': 'greater_than'}},
    
    {'index': '000300.XSHG', 'rule': {'lhs': {'name': 'n_day_gain_rate', 'type': 'pricing', 'parameters': [10]}, 'rhs': 15, 'operator': 'greater_than'}},
    
    {'index': '000300.XSHG', 'rule': {'lhs': {'name': 'MACD', 'type': 'technical', 'parameters': [12, 26, 9]}, 'rhs': [10, 20], 'operator': 'long'}},
    
]

MARKET_PANIC_SIGNALS = [
    
    {'index': '000300.XSHG', 'rule': {'lhs': {'name': 'n_day_loss_rate', 'type': 'pricing', 'parameters': [10]}, 'rhs': 3, 'operator': 'greater_than'}},
    
    {'index': '000300.XSHG', 'rule': {'lhs': {'name': 'MACD', 'type': 'technical', 'parameters': [12, 26, 9]}, 'rhs': [10, 20], 'operator': 'short'}},
    
]

FILTERS = [
    
    {'lhs': {'name': 'turnover_rate', 'type': 'extra', 'parameters': ['week']}, 'rhs': 1500, 'operator': 'greater_than'},