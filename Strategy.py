



class Strategy:
	def results(self):
		return "results"


class RSIStrategy(Strategy):
	pass

class RSIExpStrategy(Strategy):
	pass









__STRATEGIES = []

def add_to_list(strategy):
	__STRATEGIES.append(strategy)

def results():
	res = ""
	for strategy in __STRATEGIES:
		res += strategy.results() + "\n"
	return res
