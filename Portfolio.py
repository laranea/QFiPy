import numpy as np
import pandas as pd

class Portfolio:
	def __init__(self, stocks):
		self.stocks = stocks

	def getStocks(self):
		return self.stocks

	def addStock(self, stock):
		self.getStocks().append(stock)

	def calcCovMatrix(self):
		ret = {}

		for stock in self.getStocks():
			ret[stock.getQuote()] = stock.calcLogReturns()

		ret = pd.DataFrame(ret)
		cov_matrix = ret.cov()

		return ret, cov_matrix

	def calcPortfolioPerformance(self):
		ret, cov_matrix = self.calcCovMatrix()
		weights = []
		days = len(ret)

		for stock in self.getStocks():
			weights.append(stock.getWeight())

		portfolio_return = np.dot(ret.mean(), weights) * days
		portfolio_std = np.sqrt(np.dot(weights, np.dot(cov_matrix, weights))) * np.sqrt(days)

		return portfolio_return, portfolio_std

	def calcMinVarPortfolio(self):
		ret, cov_matrix = self.calcCovMatrix()

		e = np.ones(len(self.getStocks()))
		C_inv = np.linalg.inv(cov_matrix.values)

		weights = np.dot(e, C_inv) / np.dot(e, np.dot(C_inv, e))
		i = 0

		for stock in self.getStocks():
			stock.setWeight(weights[i])
			i += 1

	def calcPortfolioSharpeRatio(self):
		n = len(self.getStocks())
		w = np.ones(n) / n
		rf = 0.01

		ret, cov_matrix = self.calcCovMatrix()
		var = np.dot(w, np.dot(cov_matrix, w)) * 252