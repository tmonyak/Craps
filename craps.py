import math
import sys
import statistics

from random import randint

class Number:
	def __init__(self, value, payoff, placePayoff):
		self.value = value
		self.payoff = payoff
		self.placePayoff = placePayoff
		self.passBet = 0
		self.passOdds = 0
		self.comeBet = 0
		self.comeOdds = 0
		self.placeBet = 0

def roll():
	di1 = randint(1,6)
	di2 = randint(1,6)
	return di1 + di2


def sixAndEightNotTaken(bets, betsArray):
	return (bets[6].passBet == 0 and
		bets[6].comeBet == 0 and
		bets[6].placeBet == 0 and
		bets[8].passBet == 0 and
		bets[8].comeBet == 0 and
		bets[8].placeBet == 0)


money = int(sys.argv[1])
iterations = int(sys.argv[2])
debug = bool(sys.argv[3] == 'True')

betsArray = [6, 8, 5, 9, 4, 10]

bets = {}
bets[4] = Number(4, 2/1, 9/5)
bets[5] = Number(5, 3/2, 7/5)
bets[6] = Number(6, 6/5, 7/6)
bets[8] = Number(8, 6/5, 7/6)
bets[9] = Number(9, 3/2, 7/5)
bets[10] = Number(10, 2/1, 9/5)

if (debug == True):
	returns = [money*1.5]
	minimums = [10]
else:
	returns = [int(money * 1.2), int(money * 1.5), int(money * 1.7), money * 2]
	#minimums = [5, 10, 15, 25]
	minimums = [10]
	

resultFile = open('results.txt', 'w')
lowFile = open('low.txt', 'w')
highFile = open('high.txt', 'w')
resultFile.write("Start: ${}, Iterations: {}\n\n".format(sys.argv[1], sys.argv[2]))
lowFile.write("Start: ${}, Iterations: {}\n\n".format(sys.argv[1], sys.argv[2]))
highFile.write("Start: ${}, Iterations: {}\n\n".format(sys.argv[1], sys.argv[2]))

probTemplate = "{0:^20}|{1:^20}|{2:^20}|{3:^20}|{4:^20}|{5:^20}|{6:^20}|{7:^20}"
resultTemplate = "{0:^15}|{1:^15}|{2:^15}|{3:^15}|{4:^15}"
resultFile.write(resultTemplate.format("MINIMUM", "RETURN", "SUCCESS", "AVG TURNS", "AVG POINTS"))
lowFile.write(probTemplate.format("RETURN", "MEDIAN LOW (WIN)", "MEDIAN LOW (ALL)", "MEAN LOW (WIN)", "MEAN LOW (ALL)", "STDDEV LOW (WIN)", "STDDEV LOW (ALL)", "MIN LOW (WIN)"))
highFile.write(probTemplate.format("RETURN", "MEDIAN HIGH (LOSE)", "MEDIAN HIGH (ALL)", "MEAN HIGH (LOSE)", "MEAN HIGH (ALL)", "STDDEV HIGH (LOSE)", "STDDEV HIGH (ALL)", "MAX HIGH (LOSE)"))
resultFile.write("\n");
lowFile.write("\n");
highFile.write("\n");
resultFile.write("-------------------------------------------------------------------------------\n");
highFile.write("----------------------------------------------------------------------------------------------------------------------------------------------------------------------\n");
lowFile.write("----------------------------------------------------------------------------------------------------------------------------------------------------------------------\n");


for desiredReturn in returns:
	for minBet in minimums:
		success = 0
		totalRolls = 0
		totalPoints = 0
		allLows = []
		winLows = []
		allHighs = []
		loseHighs = []
		for x in range(0, iterations):
			money = int(sys.argv[1])
			lastRollComeOut = False
			cameLastRoll = False
			passBet = 0
			comeBet = 0
			point = 0
			on = False
			numRolls = 0
			numPoints = 0
			numBetsOnTable = 0
			availableMoney = money
			low = money
			high = money

			while (availableMoney >= minBet and availableMoney < desiredReturn):
				if (availableMoney < low):
					low = availableMoney
				if (availableMoney > high):
					high = availableMoney
				numRolls = numRolls + 1
				if(debug == True):
					print("\nRoll: {}, Money: ${}, Available Money: ${}".format(numRolls, money, availableMoney))
					print("{} bets on the table:".format(numBetsOnTable))
					if (comeBet != 0):
						print("${} on come".format(comeBet))
					for num in betsArray:
						if (bets[num].passBet != 0):
							print("${} on point ({})".format(bets[num].passBet, point))
						if (bets[num].passOdds != 0):
							print("${} on point odds ({})".format(bets[num].passOdds, point))
						if (bets[num].comeBet != 0):
							print("${} on come ({})".format(bets[num].comeBet, num))
						if (bets[num].comeOdds != 0):
							print("${} on come odds ({})".format(bets[num].comeOdds, num))
						if (bets[num].placeBet != 0):
							print("${} on place ({})".format(bets[num].placeBet, num))

					if(on == True):
						print("Point is: {}".format(point))
					else:
						print("Come out roll")
				#bet
				# add checks for having enough money
				if (on == False):
					if (minBet <= availableMoney):
						passBet = minBet
						availableMoney = availableMoney - passBet
						if (debug == True):
							print("Betting ${} on pass".format(passBet))

					if(cameLastRoll == True):
						cameLastRoll = False
						if (lastCome == 6 or lastCome == 8):
							comeOdds = minBet * 3
						elif (lastCome == 5 or lastCome == 9):
							comeOdds = minBet * 2
						else: #point == 4 or point == 10
							comeOdds = minBet
						while (comeOdds > availableMoney and comeOdds > 0):
							comeOdds = comeOdds - minBet
						if (comeOdds > 0):
							bets[lastCome].comeOdds = bets[lastCome].comeOdds + comeOdds
							availableMoney = availableMoney - comeOdds
							if (debug == True):
								print("Bet ${} on come odds ({})".format(comeOdds, lastCome))
				else:
					if(cameLastRoll == True):
						cameLastRoll = False
						if (lastCome == 6 or lastCome == 8):
							comeOdds = minBet * 3
						elif (lastCome == 5 or lastCome == 9):
							comeOdds = minBet * 2
						else: #point == 4 or point == 10
							comeOdds = minBet
						while (comeOdds > availableMoney and comeOdds > 0):
							comeOdds = comeOdds - minBet
						if (comeOdds > 0):
							bets[lastCome].comeOdds = bets[lastCome].comeOdds + comeOdds
							availableMoney = availableMoney - comeOdds
							if (debug == True):
								print("Bet ${} on come odds ({})".format(comeOdds, lastCome))

					if (lastRollComeOut == True):
						lastRollComeOut = False
						if (point == 6 or point == 8):
							passOdds = minBet * 3
						elif (point == 5 or point == 9):
							passOdds = minBet * 2
						else: #point == 4 or point == 10
							passOdds = minBet

						while (passOdds > availableMoney and passOdds > 0):
							passOdds = passOdds - minBet
						if (passOdds > 0):
							bets[point].passOdds = passOdds
							availableMoney = availableMoney - passOdds
							if (debug == True):
								print("Bet ${} on pass odds ({})".format(passOdds, point))

						#bet come
						if (minBet <= availableMoney):
							comeBet = minBet
							availableMoney = availableMoney - comeBet
							if (debug == True):
								print("Bet ${} on come".format(comeBet))

					elif (numBetsOnTable < 3):
						if (numBetsOnTable == 1):
							if (minBet <= availableMoney):
								comeBet = minBet
								availableMoney = availableMoney - comeBet
								if (debug == True):
									print("Bet ${} on come".format(comeBet))
						elif (sixAndEightNotTaken(bets, betsArray) == True):
							numBetsOnTable = numBetsOnTable + 1
							placeBet = int(minBet * 6 / 5)
							if (placeBet <= availableMoney):
								bets[6].placeBet = placeBet
								availableMoney = availableMoney - placeBet
								if (debug == True):
									print("Place ${} on 6".format(placeBet))
							if (placeBet <= availableMoney):
								bets[8].placeBet = placeBet
								availableMoney = availableMoney - placeBet
								if (debug == True):
									print("Place ${} on 8".format(placeBet))
						else:
							if (minBet * 2 <= availableMoney):
								comeBet = minBet * 2
							else:
								comeBet = minBet
							if (comeBet <= availableMoney):
								availableMoney = availableMoney - comeBet
								if (debug == True):
									print("Bet ${} on come (Less than 3)".format(comeBet))

				#roll
				rollValue = roll()
				if(debug == True):
					print("ROLL: {}".format(rollValue))
				
				#update earnings
				if (on == False):
					if (rollValue == 7 or rollValue == 11):
						if (debug == True):
							print("Won ${} on pass".format(passBet))
						if(debug == True):
								print("Available money: ${}".format(availableMoney))
						money = money + passBet
						availableMoney = availableMoney + passBet * 2
						if(debug == True):
								print("Available money: ${}".format(availableMoney))
						passBet = 0
						if (rollValue == 7): #comeBet is on, comeOdds and placeBet off
							for num in betsArray:
								if(debug == True):
									if (bets[num].comeBet != 0):
										print("Lost ${} on come bet, giving back comeOdds".format(bets[num].comeBet))
								money = money - bets[num].comeBet
								bets[num].comeBet = 0
								availableMoney = availableMoney + bets[num].comeOdds
								bets[num].comeOdds = 0
					elif (rollValue == 2 or rollValue == 3 or rollValue == 12):
						if (debug == True):
							print("Lost ${} on pass bet".format(passBet))
						money = money - passBet
						passBet = 0
					else:
						point = rollValue
						numPoints = numPoints + 1
						if (debug == True):
							print("Point is set at {}".format(point))
						if (bets[point].comeBet != 0):
							money = money + bets[point].comeBet
							availableMoney = availableMoney + bets[point].comeBet * 2
							if (debug == True):
								print("Won ${} on come bet".format(bets[point].comeBet))
							bets[point].comeBet = 0

							numBetsOnTable = numBetsOnTable - 1
						on = True
						bets[point].passBet = passBet
						numBetsOnTable = numBetsOnTable + 1
						lastRollComeOut = True

				else:
					if (rollValue == 7):
						if (debug == True):
							print("ROLLED A SEVEN")
						on = False
						if (comeBet != 0):
							if(debug == True):
								print("Won ${} on come".format(comeBet))
							money = money + comeBet
							availableMoney = availableMoney + comeBet * 2
							comeBet = 0
						#update earnings
						for num in betsArray:
							money = money - bets[num].passBet
							if(debug == True):
								if (bets[num].passBet != 0):
									print("Lost ${} on pass bet".format(bets[num].passBet))
							money = money - bets[num].passOdds
							if(debug == True):
								if (bets[num].passOdds != 0):
									print("Lost ${} on pass odds".format(bets[num].passOdds))
							money = money - bets[num].comeBet
							if(debug == True):
								if (bets[num].comeBet != 0):
									print("Lost ${} on come bet".format(bets[num].comeBet))
							money = money - bets[num].comeOdds
							if(debug == True):
								if (bets[num].comeOdds != 0):
									print("Lost ${} on comeOdds".format(bets[num].comeOdds))
							money = money - bets[num].placeBet
							if(debug == True):
								if (bets[num].placeBet != 0):
									print("Lost ${} on place bet".format(bets[num].placeBet))

						if (debug == True):
							print("Resetting all bets to zero")
						for num in betsArray:
							bets[num].passBet = 0
							bets[num].comeBet = 0
							bets[num].placeBet = 0
							bets[num].passOdds = 0
							bets[num].comeOdds = 0
						numBetsOnTable = 0
						lastRollComeOut = False
						cameLastRoll = False
						passBet = 0
						comeBet = 0
						point = 0
						on = False


					elif (rollValue == 11):
						if (comeBet != 0):
							if (debug == True):
								print("Won ${} on come".format(comeBet))
							money = money + comeBet
							if(debug == True):
								print("Available money: ${}".format(availableMoney))
							availableMoney = availableMoney + comeBet * 2
							if(debug == True):
								print("Available money: ${}".format(availableMoney))
							comeBet = 0

					elif (rollValue == 2 or rollValue == 3 or rollValue == 12):
						if (comeBet != 0):
							if (debug == True):
								print("Lost ${} on come".format(comeBet))
							money = money - comeBet
							comeBet = 0
					else:
						
						#update earnings
						money = money + bets[rollValue].passBet
						availableMoney = availableMoney + bets[rollValue].passBet
						if (debug == True):
							if (bets[rollValue].passBet != 0):
								print("Won ${} on pass bet".format(bets[rollValue].passBet))
						money = money + bets[rollValue].passOdds * bets[rollValue].payoff
						availableMoney = availableMoney + bets[rollValue].passOdds * bets[rollValue].payoff
						if (debug == True):
							if (bets[rollValue].passOdds != 0):
								print("Won ${} on pass odds".format(bets[rollValue].passOdds * bets[rollValue].payoff))
						if (bets[rollValue].comeBet != 0):
							money = money + bets[rollValue].comeBet
							availableMoney = availableMoney + bets[rollValue].comeBet*2
							numBetsOnTable = numBetsOnTable - 1
							if (debug == True):
								print("Won ${} on come bet".format(bets[rollValue].comeBet))
							bets[rollValue].comeBet = 0
						if (bets[rollValue].comeOdds != 0):
							money = money + bets[rollValue].comeOdds * bets[rollValue].payoff
							availableMoney = availableMoney + bets[rollValue].comeOdds + bets[rollValue].comeOdds * bets[rollValue].payoff
							if (debug == True):
								print("Won ${} on come odds".format(bets[rollValue].comeOdds * bets[rollValue].payoff))
							bets[rollValue].comeOdds = 0
						money = money + bets[rollValue].placeBet * bets[rollValue].placePayoff
						availableMoney = availableMoney + bets[rollValue].placeBet * bets[rollValue].placePayoff
						if (debug == True):
							if (bets[rollValue].placeBet != 0):
								print("Won ${} on place bet".format(bets[rollValue].placeBet * bets[rollValue].placePayoff))
						if (comeBet != 0):
							if(debug == True):
								print("Come point set")
							numBetsOnTable = numBetsOnTable + 1
							cameLastRoll = True
							lastCome = rollValue
							bets[lastCome].comeBet = bets[lastCome].comeBet + comeBet
							comeBet = 0
					if (rollValue == point):
						if (debug == True):
							print("Resetting pass bets to zero")

						availableMoney = availableMoney + bets[point].passBet
						availableMoney = availableMoney + bets[point].passOdds
						for num in betsArray:
							bets[num].passBet = 0
							bets[num].passOdds = 0
						numBetsOnTable = numBetsOnTable - 1
						on = False
			totalRolls = totalRolls + numRolls
			totalPoints = totalPoints + numPoints
			if (availableMoney >= desiredReturn):
				winLows.insert(success, low)
				success = success + 1
			else:
				loseHighs.insert(x-success, high)
			allHighs.insert(x, high)
			allLows.insert(x, low)
		successRate = int(success/iterations * 100)
		meanRolls = int(totalRolls/iterations)
		meanPoints = int(totalPoints/iterations)
		meanWinLow = int(statistics.mean(winLows))
		medianWinLow = int(statistics.median(winLows))
		stddevWinLow = int(statistics.stdev(winLows))
		meanAllLow = int(statistics.mean(allLows))
		medianAllLow = int(statistics.median(allLows))
		stddevAllLow = int(statistics.stdev(allLows))
		meanLoseHigh = int(statistics.mean(loseHighs))
		medianLoseHigh = int(statistics.median(loseHighs))
		stddevLoseHigh = int(statistics.stdev(loseHighs))
		meanAllHigh = int(statistics.mean(allHighs))
		medianAllHigh = int(statistics.median(allHighs))
		stddevAllHigh = int(statistics.stdev(allHighs))
		minLow = int(min(winLows))
		maxHigh = int(max(loseHighs))
		resultFile.write(resultTemplate.format("${}".format(minBet), "${}".format(desiredReturn), "{}%".format(successRate), "{}".format(meanRolls), "{}".format(meanPoints)));
		resultFile.write("\n")
		lowFile.write(probTemplate.format("${}".format(desiredReturn), "${}".format(medianWinLow), "${}".format(medianAllLow), "${}".format(meanWinLow), "${}".format(meanAllLow), "${}".format(stddevWinLow), "${}".format(stddevAllLow), "${}".format(minLow)))
		lowFile.write("\n")
		highFile.write(probTemplate.format("${}".format(desiredReturn), "${}".format(medianLoseHigh), "${}".format(medianAllHigh), "${}".format(meanLoseHigh), "${}".format(meanAllHigh), "${}".format(stddevLoseHigh), "${}".format(stddevAllHigh), "${}".format(maxHigh)))
		highFile.write("\n")


resultFile.close()
lowFile.close()
highFile.close()