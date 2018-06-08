import numpy as np
import pandas as pd
import talib


UNIVERSE = ['000300.XSHG']
BOARDS = ['MainBoard']
INDUSTRIES = ['*']
ST_OPTION = 'include'

SELECT_INTERVAL = 5
BUY_INTERVAL = 1
SELL_INTERVAL = 1

MAX_HOLDING_NUM = 10
MAX_WEIGHT = 0.2

SINGLE_PROFIT_TAKEN = 0.2
SINGLE_STOP_LOSS = -0.1
HOLDING_PROFIT_TAKEN = 0.3
HOLDING_STOP_LOSS = -0.1
STRATEGY_PROFIT_TAKEN = None
STRATEGY_STOP_LOSS = None

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
    
    {'lhs': {'name': 'MACD.macd', 'type': 'technical', 'parameters': [12, 26, 9]}, 'rhs': {'name': 'MACD.macdsignal', 'type': 'technical', 'parameters': [12, 26, 9]}, 'operator': 'long'},
    
]

SORTING_RULES = [
    
]

SELL_CONDITIONS = [
    
]

BUY_CONDITIONS = [
    
]


def get_turnover(stocks, count=1, fields=None):
    result = get_turnover_rate(stocks, count=count, fields=fields)
    if isinstance(result, pd.Series):
        name = stocks if isinstance(stocks, str) else stocks[0]
        return result.to_frame(name=name)

    return result


SIMPLE_OPERATOR = {
    "greater_than",
    "less_than",
    "in_range",
    "rank_in_range",
}


def apply_simple_operator(operator, data, rhs):
    if operator == "greater_than":
        return data.index[data > rhs].tolist()
    elif operator == "less_than":
        return data.index[data < rhs].tolist()
    elif operator == "in_range":
        vmin, vmax = rhs
        return data.index[(data > vmin) & (data < vmax)].tolist()
    else:
        assert operator == "rank_in_range"
        vmin, vmax = rhs[0] / 100.0, rhs[1] / 100.0
        rank = data.rank(pct=True)
        c = (rank > vmin) & (rank < vmax)
        return c[c].index.tolist()


KNOWN_FILTERS = {}


def register_filter(category, detail):
    def decorator(fun):
        global KNOWN_FILTERS
        KNOWN_FILTERS[category, detail] = fun
        return fun

    return decorator


@register_filter('fundamental', '*')
def fundamental_filter(stocks, rule, bar_dict):
    if rule["operator"] not in SIMPLE_OPERATOR:
        print('[WARNING] unknown operator in rule:', rule)
        return stocks

    data = get_factor(stocks, rule["lhs"]["name"])
    return apply_simple_operator(rule["operator"], data, rule["rhs"])


@register_filter('extra', 'listed_days')
def listed_days_filter(stocks, rule, bar_dict):
    data = pd.Series({
        s: instruments(s).days_from_listed() for s in stocks
    })
    return apply_simple_operator(rule["operator"], data, rule["rhs"])


@register_filter('extra', 'turnover_rate')
def turnover_rate_filter(stocks, rule, bar_dict):
    lhs = rule["lhs"]
    if rule["operator"] in SIMPLE_OPERATOR:
        data = get_turnover(stocks, fields=lhs["parameters"]).iloc[0]
        return apply_simple_operator(rule["operator"], data, rule["rhs"])

    if not rule['operator'] in {'greater_than_ma', 'less_than_ma', 'in_ma_range'}:
        print('unknown operator for rule:', rule)
        return stocks

    count = rule["rhs"][1] if isinstance(rule["rhs"], list) else rule["rhs"]
    data = get_turnover(stocks, count=count, fields=rule["parameters"])
    value = data.iloc[-1]
    if rule["operator"] == "greater_than_ma":
        return value.index[value > data.mean()].tolist()
    elif rule["operator"] == "less_than_ma":
        return value.index[value < data.mean()].tolist()
    else:
        l, r = rule["parameters"]
        ma1 = data.iloc[:l].mean()
        ma2 = data.mean()
        condition = (value > ma1) & (value < ma2)
        condition |= (value < ma1) & (value > ma2)
        return condition[condition].index.tolist()


@register_filter('pricing', '*')
def pricing_filter(stocks, rule, bar_dict):
    lhs, operator, rhs = rule['lhs'], rule['operator'], rule['rhs']
    if operator == 'rank_in_range':
        data = pd.Series({s: getattr(bar_dict[s], lhs['name']) for s in stocks})
        return apply_simple_operator(data, operator, rhs)

    filtered_stocks = []
    for s in stocks:
        lv = getattr(bar_dict[s], lhs["name"])
        if isinstance(rhs, dict):
            rv = get_factor_value(s, rhs, bar_dict)
        else:
            rv = rhs
        if operator == "greater_than":
            if lv > _to_scalar(rv):
                filtered_stocks.append(s)
        elif operator == "less_than":
            if lv < _to_scalar(rv):
                filtered_stocks.append(s)
        elif operator == "in_range":
            l, r = rv
            if l < lv < r:
                filtered_stocks.append(s)
        elif operator == "greater_than_ma":
            ma = history_bars(s, rv, "1d", fields=lhs["name"]).mean()
            if lv > ma:
                filtered_stocks.append(s)
        elif operator == "less_than_ma":
            ma = history_bars(s, rv, "1d", fields=lhs["name"]).mean()
            if lv < ma:
                filtered_stocks.append(s)
        elif operator == "in_ma_range":
            data = history_bars(s, rv[1], "1d", fields=lhs["name"])
            ma1 = data[:rv[0]].mean()
            ma2 = data.mean()
            if ma1 < lv < ma2 or ma2 < lv < ma1:
                filtered_stocks.append(s)
        else:
            raise RuntimeError("不支持的操作符: {}, 因子 {}".format(operator, lhs))
    return filtered_stocks


def n_day_gain_rate(stock, n):
    l = history_bars(stock, n, '1d', 'close')
    return (l[-1] - l[0]) / l[0]


@register_filter('pricing', 'n_day_gain_rate')
def n_day_gain_rate_filter(stocks, rule, bar_dict):
    n = rule['lhs']['parameters'][0]
    data = pd.Series({
        s: n_day_gain_rate(s, n)
        for s in stocks
    })
    return apply_simple_operator(rule['operator'], data, rule['rhs'])


@register_filter('pricing', 'n_day_loss_rate')
def n_day_loss_rate_filter(stocks, rule, bar_dict):
    n = rule['lhs']['parameters'][0]
    data = pd.Series({
        s: -n_day_gain_rate(s, n)
        for s in stocks
    })
    return apply_simple_operator(rule['operator'], data, rule['rhs'])


@register_filter('technical', '*')
def technical_filter(stocks, rule, bar_dict):
    operator = rule["operator"]
    lhs = rule["lhs"]
    rhs = rule["rhs"]
    filtered_stocks = []
    for s in stocks:
        lv = get_technical_series(s, lhs)
        rv = get_factor_value(s, rhs, bar_dict) if isinstance(rhs, dict) else rhs
        if operator == "greater_than" or operator == "long":
            if lv[-1] > _to_scalar(rv):
                filtered_stocks.append(s)
        elif operator == "less_than" or operator == "short":
            if lv[-1] < _to_scalar(rv):
                filtered_stocks.append(s)
        elif operator == "in_range":
            if rv[0] < lv[-1] < rv[1]:
                filtered_stocks.append(s)
        elif operator == "cross":
            if len(lv) < 2 or len(rv) < 2:
                continue
            if lv[-2] < rv[-2] and lv[-1] > rv[-1]:
                filtered_stocks.append(s)
        elif operator == "reverse_cross":
            if len(lv) < 2 or len(rv) < 2:
                continue
            if lv[-2] > rv[-2] and lv[-1] < rv[-1]:
                filtered_stocks.append(s)
        else:
            raise RuntimeError(
                "不支持的规则：{} {} {}".format(
                    lhs, operator, rhs))
    return filtered_stocks


@register_filter('CDL', '*')
def CDL_filter(stocks, rule, bar_dict):
    name = rule["lhs"]["name"]
    filtered_stocks = []
    for stock in stocks:
        function = getattr(talib, name)
        result = function(
            history_bars(stock, 5, '1d', 'open'),
            history_bars(stock, 5, '1d', 'high'),
            history_bars(stock, 5, '1d', 'low'),
            history_bars(stock, 5, '1d', 'close')
        )
        if len(result) > 0 and result[-1] != 0:
            filtered_stocks.append(stock)
    return filtered_stocks


def _to_scalar(v):
    return v[-1] if isinstance(v, np.ndarray) else v


def _extract_input_names(d):
    if "price" in d:
        return [d["price"]]
    elif "prices" in d:
        return d["prices"]
    return []


def get_technical_series(stock, factor):
    name = factor["name"]
    output = "real"
    if "." in name:
        name, output = name.split(".")
    func = getattr(talib.abstract, name)
    func.set_parameters(
        dict(zip(func.parameters.keys(),
                 factor["parameters"])))
    func.set_input_arrays({
        name: history_bars(stock, 100, "1d", fields=name)
        for name in _extract_input_names(func.input_names)
    })
    if output == "real":
        return func.outputs
    output_index = func.output_names.index(output)
    return func.outputs[output_index]


def get_factor_value(stock, factor, bar_dict):
    # 对于量价指标返回值
    if factor["type"] == "pricing":
        return getattr(bar_dict[stock], factor["name"])
    # 对于技术指标返回 series
    return get_technical_series(stock, factor)


RULE_SCORE = {
    'fundamental': 0,
    'extra': 1,
    'pricing': 2,
    'technical': 3,
    'CDL': 4,
}


def filter_for(rule):
    lhs = rule['lhs']
    try:
        return KNOWN_FILTERS[lhs['type'], lhs['name']]
    except KeyError:
        return KNOWN_FILTERS[lhs['type'], '*']


def apply_filters(stocks, filters, bar_dict):
    filters = sorted(filters, key=lambda r: RULE_SCORE[r['lhs']['type']])
    for rule in filters:
        if not stocks:
            return []

        f = filter_for(rule)
        stocks = f(stocks, rule, bar_dict)

    return stocks


def market_panic(rules, bar_dict):
    for r in rules:
        index, rule = r['index'], r['rule']
        f = filter_for(rule)
        result = f([index], rule, bar_dict)
        if result:
            return True

    return False


def market_enter(rules, bar_dict):
    for r in rules:
        index, rule = r['index'], r['rule']
        f = filter_for(rule)
        result = f([index], rule, bar_dict)
        if not result:
            return False

    return True


def sort_stocks(stocks, rules, bar_dict):
    if len(stocks) <= 1:
        return stocks
    if not rules:
        return sorted(stocks)

    result = pd.Series(data=0.0, index=stocks)
    for rule in rules:
        factor = rule["factor"]
        if factor["type"] == "fundamental":
            data = get_factor(stocks, factor["name"])
        elif factor["type"] == "pricing":
            data = pd.Series({s: getattr(bar_dict[s], factor["name"]) for s in stocks})
        elif factor["type"] == "extra":
            if factor["name"] == "listed_days":
                data = pd.Series({s: instruments(s).days_from_listed() for s in stocks})
            else:
                data = get_turnover(stocks, fields=factor["parameters"]).iloc[0]
        else:
            data = pd.Series({s: get_technical_series(s, factor)[-1] for s in stocks})
        na_option = "bottom" if rule["ascending"] else "top"
        result += data.rank(method="average", na_option=na_option, pct=True)
    stocks = result.sort_values().index.tolist()
    return stocks


def _ensure_list(v):
    return [] if v is None else v


def get_universe(universe, industries, boards, st_option):
    stocks = set()
    if universe != ["*"]:
        for index in universe:
            stocks.update(_ensure_list(index_components(index)))
    else:
        stocks.update(all_instruments("CS").order_book_id)

    if industries != ["*"]:
        stocks_of_industries = set()
        for ind in industries:
            stocks_of_industries.update(_ensure_list(shenwan_industry(ind)))
        stocks.intersection_update(stocks_of_industries)

    if boards != ["*"]:
        stocks = {s for s in stocks if instruments(s).board_type in boards}
    if st_option == "only":
        stocks = {s for s in stocks if is_st_stock(s)}
    elif st_option == "exclude":
        stocks = {s for s in stocks if not is_st_stock(s)}

    return list(stocks)


def sell_out_all(portfolio):
    for order_book_id, position in portfolio.positions.items():
        if position.quantity > 0:
            order_target_value(order_book_id, 0)



def init(context):
    context.count = -1
    context.strategy_stop = False
    context.day_stop = False
    context.market_panic = False
    context.pool = []

    scheduler.run_daily(rebalance_first_part, time_rule=market_open(minute=1))
    scheduler.run_daily(rebalance_second_part, time_rule=market_open(minute=2))


def before_trading(context):
    context.count += 1
    context.day_stop = False
    context.market_panic = False


def handle_bar(context, bar_dict):
    if context.strategy_stop or context.day_stop or context.market_panic:
        sell_out_all(context.portfolio)
        return

    if MARKET_PANIC_SIGNALS and market_panic(MARKET_PANIC_SIGNALS, bar_dict):
        print('大盘止损触发')
        context.market_panic = True
        sell_out_all(context.portfolio)
        return

    if (HOLDING_PROFIT_TAKEN is not None or HOLDING_STOP_LOSS is not None or
        STRATEGY_PROFIT_TAKEN is not None or STRATEGY_STOP_LOSS is not None):
        total_returns = context.portfolio.total_returns
        fired = False
        if ((STRATEGY_PROFIT_TAKEN is not None and STRATEGY_PROFIT_TAKEN < total_returns) or
            (STRATEGY_STOP_LOSS is not None and STRATEGY_STOP_LOSS > total_returns)):
            fired = True
            context.strategy_stop = True

        if ((HOLDING_PROFIT_TAKEN is not None and HOLDING_PROFIT_TAKEN < total_returns) or
            (HOLDING_STOP_LOSS is not None and HOLDING_STOP_LOSS > total_returns)):
            fired = True
            context.day_stop = True

        if fired:
            sell_out_all(context.portfolio)
            return

    if SINGLE_STOP_LOSS is None and SINGLE_PROFIT_TAKEN is None:
        return

    for order_book_id, position in context.portfolio.positions.items():
        if position.quantity == 0:
            continue

        profit = bar_dict[order_book_id].last / position.avg_price - 1
        if SINGLE_PROFIT_TAKEN is not None and SINGLE_PROFIT_TAKEN < profit:
            print('止盈卖出：', order_book_id, position.quantity)
            order_target_value(order_book_id, 0)
        elif SINGLE_STOP_LOSS is not None and SINGLE_STOP_LOSS > profit:
            print('止损卖出：', order_book_id, position.quantity)
            order_target_value(order_book_id, 0)


def rebalance_first_part(context, bar_dict):
    if context.strategy_stop:
        return

    if context.count % SELECT_INTERVAL == 0:
        stocks = get_universe(UNIVERSE, INDUSTRIES, BOARDS, ST_OPTION)
        filtered = apply_filters(stocks, FILTERS, bar_dict)
        context.pool = filtered

    if MARKET_PANIC_SIGNALS and market_panic(MARKET_PANIC_SIGNALS, bar_dict):
        context.market_panic = True
        sell_out_all(context.portfolio)
        return

    if context.count % SELL_INTERVAL == 0:
        need_adjust = []
        max_position_value = None
        if MAX_WEIGHT is not None:
            max_position_value = context.portfolio.total_value * MAX_WEIGHT
            need_adjust = [s for s, position in context.portfolio.positions.items()
                           if position.market_value > max_position_value]

        if SELL_CONDITIONS:
            stocks = [s for s, position in context.portfolio.positions.items() if position.quantity > 0]
            sell_list = apply_filters(stocks, SELL_CONDITIONS, bar_dict)
            for s in sell_list:
                order_target_value(s, 0)
                if s in need_adjust:
                    need_adjust.remove(s)

        for s in need_adjust:
            order_target_value(s, max_position_value)


def rebalance_second_part(context, bar_dict):
    if (context.count % BUY_INTERVAL != 0 or
        context.strategy_stop or context.day_stop or
        context.market_panic):
        return

    holdings = [s for s, position in context.portfolio.positions.items() if position.quantity > 0]
    if len(holdings) >= MAX_HOLDING_NUM:
        print('持仓数已达到限制，不再买入')
        return

    stocks = [s for s in context.pool if not is_suspended(s)]
    filtered = apply_filters(stocks, BUY_CONDITIONS, bar_dict)
    if not filtered:
        return

    sorted_stocks = sort_stocks(filtered, SORTING_RULES, bar_dict)
    buy_list = sorted_stocks[:MAX_HOLDING_NUM-len(holdings)]
    target_value = context.stock_account.cash / len(buy_list)
    for s in buy_list:
        order_value(s, target_value)
