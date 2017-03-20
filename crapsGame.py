from random import randint

class Number:
	def __init__(self, value, payoff, placePayoff, oddsMultiple, placeMultiple):
		self.value = value
		self.payoff = payoff
		self.placePayoff = placePayoff
		self.placeMultiple = placeMultiple
		self.passBet = 0
		self.passOdds = 0
		self.comeBet = 0
		self.comeOdds = 0
		self.placeBet = 0

class CrapsGame:
	def __init__(self, availableMoney, minBet, placeBetsWorking, comeOddsWorking, debug):
		self.availableMoney = availableMoney
		self.money = availableMoney
		self.placeBetsWorking = placeBetsWorking
		self.comeOddsWorking = comeOddsWorking
		self.minBet = minBet
		self.debug = debug
		self.betsArray = [6, 8, 5, 9, 4, 10]
		self.bets = {}
		self.bets[4] = Number(4, 2/1, 9/5, 1, 1)
		self.bets[5] = Number(5, 3/2, 7/5, 1, 1)
		self.bets[6] = Number(6, 6/5, 7/6, 1, 6/5)
		self.bets[8] = Number(8, 6/5, 7/6, 1, 6/5)
		self.bets[9] = Number(9, 3/2, 7/5, 1, 1)
		self.bets[10] = Number(10, 2/1, 9/5, 1, 1)
		self.lastRollComeOut = False
		self.cameLastRoll = False
		self.passBet = 0
		self.comeBet = 0
		self.point = 0
		self.lastCome = 0
		self.on = False
		self.numRolls = 0
		self.numPoints = 0
		self.numBetsOnTable = 0
		self.low = availableMoney
		self.high = availableMoney
		self.snakeEyes = 0


	def getMoney(self):
		return self.money

	def getAvailableMoney(self):
		return self.availableMoney

	def isOn(self):
		return self.on

	def getNumRolls(self):
		return self.numRolls

	def getNumPoints(self):
		return self.numPoints

	def getPoint(self):
		return self.point

	def getLastCome(self):
		return self.lastCome

	def getCameLastRoll(self):
		return self.cameLastRoll

	def getLastRollComeOut(self):
		return self.lastRollComeOut

	def getNumBetsOnTable(self):
		return self.numBetsOnTable

	def getLow(self):
		return self.low

	def getHigh(self):
		return self.high

	def getSnakeEyes(self):
		return self.snakeEyes

	def startRound(self):
		if (self.availableMoney < self.low):
			self.low = self.availableMoney
		if (self.availableMoney > self.high):
			self.high = self.availableMoney
		if (self.debug == True):
			print("\nRoll: {}, Money: ${}, Available Money: ${}".format(self.numRolls, self.money, self.availableMoney))
			print("{} bets on the table:".format(self.numBetsOnTable))
			if (self.comeBet != 0):
				print("${} on come".format(self.comeBet))
			for num in self.betsArray:
				if (self.bets[num].passBet != 0):
					print("${} on pass ({})".format(self.bets[num].passBet, self.point))
				if (self.bets[num].passOdds != 0):
					print("${} on pass odds ({})".format(self.bets[num].passOdds, self.point))
				if (self.bets[num].comeBet != 0):
					print("${} on come ({})".format(self.bets[num].comeBet, num))
				if (self.bets[num].comeOdds != 0):
					print("${} on come odds ({})".format(self.bets[num].comeOdds, num))
				if (self.bets[num].placeBet != 0):
					print("${} on place ({})".format(self.bets[num].placeBet, num))

		if (self.debug == True):
			if(self.on == True):
				print("Point is: {}".format(self.point))
			else:
				print("Come out roll")


	def roll(self):
		if (self.cameLastRoll == True):
			self.cameLastRoll = False
		if (self.lastRollComeOut == True):
			self.lastRollComeOut = False
		self.numRolls = self.numRolls + 1
		di1 = randint(1,6)
		di2 = randint(1,6)
		rollValue = di1 + di2
		if(self.debug == True):
			print("ROLL: {}".format(rollValue))
		return rollValue

	def sixAndEightNotTaken(self):
		return (self.bets[6].passBet == 0 and
		self.bets[6].comeBet == 0 and
		self.bets[6].placeBet == 0 and
		self.bets[8].passBet == 0 and
		self.bets[8].comeBet == 0 and
		self.bets[8].placeBet == 0)

	def betPass(self, multiple):
		self.passBet = self.minBet * multiple
		while (self.passBet > self.availableMoney and self.passBet > 0):
			self.passBet = self.passBet - self.minBet
		if (self.passBet > 0):
			self.availableMoney = self.availableMoney - self.passBet
			if (self.debug == True):
				print("Bet ${} on pass".format(self.passBet))

	def betPassOdds(self, multiple):
		self.passOdds = self.minBet * multiple
		while (self.passOdds > self.availableMoney and self.passOdds > 0):
			self.passOdds = self.passOdds - self.minBet
		if (self.passOdds > 0):
			self.bets[self.point].passOdds = self.passOdds
			self.availableMoney = self.availableMoney - self.passOdds
			if (self.debug == True):
				print("Bet ${} on pass odds ({})".format(self.passOdds, self.point))

	def betCome(self, multiple):
		self.comeBet = self.minBet * multiple
		while (self.comeBet > self.availableMoney and self.comeBet > 0):
			self.comeBet = self.comeBet - self.minBet
		if (self.comeBet > 0):
			self.availableMoney = self.availableMoney - self.comeBet
			if (self.debug == True):
				print("Bet ${} on come".format(self.comeBet))
			

	def betComeOdds(self, number, multiple):
		self.comeOdds = self.minBet * multiple
		while (self.comeOdds > self.availableMoney and self.comeOdds > 0):
			self.comeOdds = self.comeOdds - self.minBet
		if (self.comeOdds > 0):
			self.bets[number].comeOdds = self.bets[number].comeOdds + self.comeOdds
			self.availableMoney = self.availableMoney - self.comeOdds
			if (self.debug == True):
				print("Bet ${} on come odds ({})".format(self.comeOdds, self.lastCome))


	def betPlace(self, number, multiple):
		odds = self.bets[number].placeMultiple
		self.placeBet = int(self.minBet * multiple * odds)
		while (self.placeBet > self.availableMoney and self.placeBet > 0):
			self.placeBet = self.placeBet - int(self.minBet * odds)

		if (self.placeBet > 0):
			self.numBetsOnTable = self.numBetsOnTable + 1
			self.bets[number].placeBet = self.placeBet
			self.availableMoney = self.availableMoney - self.placeBet
			if (self.debug == True):
				print("Place ${} on {}".format(self.placeBet, number))

	def betSnakeEyes(self, multiple):
		self.snakeEyes = self.minBet * multiple
		self.availableMoney = self.availableMoney - self.snakeEyes
		self.numBetsOnTable = self.numBetsOnTable + 1

	def updateEarnings(self, rollValue):
		if (self.snakeEyes > 0):
			if (rollValue == 2):
				self.money = self.money + self.snakeEyes * 30
				self.availableMoney = self.availableMoney + self.snakeEyes * 31
			self.numBetsOnTable = self.numBetsOnTable - 1
			self.snakeEyes = 0

		if (self.on == False):
			if (rollValue == 7 or rollValue == 11):
				if (self.debug == True):
					print("Won ${} on pass".format(self.passBet))
				self.money = self.money + self.passBet
				self.availableMoney = self.availableMoney + self.passBet * 2
				self.passBet = 0
				if (rollValue == 7): #comeBet is on, comeOdds and placeBet off
					for num in self.betsArray:
						if(self.debug == True):
							if (self.bets[num].comeBet != 0):
								print("Lost ${} on come bet, giving back comeOdds".format(self.bets[num].comeBet))
						self.money = self.money - self.bets[num].comeBet
						self.bets[num].comeBet = 0
						self.availableMoney = self.availableMoney + self.bets[num].comeOdds
						self.bets[num].comeOdds = 0
			elif (rollValue == 2 or rollValue == 3 or rollValue == 12):
				if (self.debug == True):
					print("Lost ${} on pass bet".format(self.passBet))
				self.money = self.money - self.passBet
				self.passBet = 0
			else:
				self.point = rollValue
				self.numPoints = self.numPoints + 1
				if (self.debug == True):
					print("Point is set at {}".format(self.point))
				if (self.bets[self.point].comeBet != 0):
					self.money = self.money + self.bets[self.point].comeBet
					self.availableMoney = self.availableMoney + self.bets[self.point].comeBet * 2
					if (self.debug == True):
						print("Won ${} on come bet".format(self.bets[self.point].comeBet))
					self.bets[self.point].comeBet = 0

					self.numBetsOnTable = self.numBetsOnTable - 1
				self.on = True
				self.bets[self.point].passBet = self.passBet
				self.numBetsOnTable = self.numBetsOnTable + 1
				self.lastRollComeOut = True

		else:
			if (rollValue == 7):
				if (self.debug == True):
					print("ROLLED A SEVEN")
				self.on = False
				if (self.comeBet != 0):
					if(self.debug == True):
						print("Won ${} on come".format(self.comeBet))
					self.money = self.money + self.comeBet
					self.availableMoney = self.availableMoney + self.comeBet * 2
					self.comeBet = 0

				for num in self.betsArray:
					self.money = self.money - self.bets[num].passBet
					if(self.debug == True):
						if (self.bets[num].passBet != 0):
							print("Lost ${} on pass bet".format(self.bets[num].passBet))
					self.money = self.money - self.bets[num].passOdds
					if(self.debug == True):
						if (self.bets[num].passOdds != 0):
							print("Lost ${} on pass odds".format(self.bets[num].passOdds))
					self.money = self.money - self.bets[num].comeBet
					if(self.debug == True):
						if (self.bets[num].comeBet != 0):
							print("Lost ${} on come bet".format(self.bets[num].comeBet))
					self.money = self.money - self.bets[num].comeOdds
					if(self.debug == True):
						if (self.bets[num].comeOdds != 0):
							print("Lost ${} on come odds".format(self.bets[num].comeOdds))
					self.money = self.money - self.bets[num].placeBet
					if(self.debug == True):
						if (self.bets[num].placeBet != 0):
							print("Lost ${} on place bet".format(self.bets[num].placeBet))

				if (self.debug == True):
					print("Resetting all bets to zero")
				for num in self.betsArray:
					self.bets[num].passBet = 0
					self.bets[num].comeBet = 0
					self.bets[num].placeBet = 0
					self.bets[num].passOdds = 0
					self.bets[num].comeOdds = 0
				self.numBetsOnTable = 0
				self.lastRollComeOut = False
				self.cameLastRoll = False
				self.passBet = 0
				self.comeBet = 0
				self.point = 0
				self.on = False

			elif (rollValue == 11):
				if (self.comeBet != 0):
					if (self.debug == True):
						print("Won ${} on come".format(self.comeBet))
					self.money = self.money + self.comeBet
					self.availableMoney = self.availableMoney + self.comeBet * 2
					self.comeBet = 0

			elif (rollValue == 2 or rollValue == 3 or rollValue == 12):
				if (self.comeBet != 0):
					if (self.debug == True):
						print("Lost ${} on come".format(self.comeBet))
					self.money = self.money - self.comeBet
					self.comeBet = 0
			else:
				self.money = self.money + self.bets[rollValue].passBet
				self.availableMoney = self.availableMoney + self.bets[rollValue].passBet
				if (self.debug == True):
					if (self.bets[rollValue].passBet != 0):
						print("Won ${} on pass bet".format(self.bets[rollValue].passBet))
				self.money = self.money + int(self.bets[rollValue].passOdds * self.bets[rollValue].payoff)
				self.availableMoney = self.availableMoney + int(self.bets[rollValue].passOdds * self.bets[rollValue].payoff)
				if (self.debug == True):
					if (self.bets[rollValue].passOdds != 0):
						print("Won ${} on pass odds".format(int(self.bets[rollValue].passOdds * self.bets[rollValue].payoff)))
				if (self.bets[rollValue].comeBet != 0):
					self.money = self.money + self.bets[rollValue].comeBet
					self.availableMoney = self.availableMoney + self.bets[rollValue].comeBet*2
					self.numBetsOnTable = self.numBetsOnTable - 1
					if (self.debug == True):
						print("Won ${} on come bet".format(self.bets[rollValue].comeBet))
					self.bets[rollValue].comeBet = 0
				if (self.bets[rollValue].comeOdds != 0):
					self.money = self.money + int(self.bets[rollValue].comeOdds * self.bets[rollValue].payoff)
					self.availableMoney = self.availableMoney + self.bets[rollValue].comeOdds + int(self.bets[rollValue].comeOdds * self.bets[rollValue].payoff)
					if (self.debug == True):
						print("Won ${} on come odds".format(int(self.bets[rollValue].comeOdds * self.bets[rollValue].payoff)))
					self.bets[rollValue].comeOdds = 0
				self.money = self.money + int(self.bets[rollValue].placeBet * self.bets[rollValue].placePayoff)
				self.availableMoney = self.availableMoney + int(self.bets[rollValue].placeBet * self.bets[rollValue].placePayoff)
				if (self.debug == True):
					if (self.bets[rollValue].placeBet != 0):
						print("Won ${} on place bet".format(int(self.bets[rollValue].placeBet * self.bets[rollValue].placePayoff)))
				if (self.comeBet != 0):
					if(self.debug == True):
						print("Come point set at {}".format(rollValue))
					self.numBetsOnTable = self.numBetsOnTable + 1
					self.cameLastRoll = True
					self.lastCome = rollValue
					self.bets[self.lastCome].comeBet = self.bets[self.lastCome].comeBet + self.comeBet
					self.comeBet = 0
			if (rollValue == self.point):
				if (self.debug == True):
					print("Resetting pass bets to zero")

				self.availableMoney = self.availableMoney + self.bets[self.point].passBet
				self.availableMoney = self.availableMoney + self.bets[self.point].passOdds
				for num in self.betsArray:
					self.bets[num].passBet = 0
					self.bets[num].passOdds = 0
				self.numBetsOnTable = self.numBetsOnTable - 1
				self.on = False