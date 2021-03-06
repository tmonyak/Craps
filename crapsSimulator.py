import math
import sys
import statistics

from crapsGame import CrapsGame
from math import log10, floor


money = int(sys.argv[1])
iterations = int(sys.argv[2])
debug = bool(sys.argv[3] == 'True')

if (debug == True):
	returns = [money*1.5]
	minimums = [10]
else:
	#returns = [int(money * 1.2), int(money * 1.5), int(money * 1.7), money * 2]
	returns = [int(money * 1.5)]
	#minimums = [5, 10, 15, 25]
	minimums = [5]
	

resultFile = open('results.txt', 'w')
lowFile = open('low.txt', 'w')
highFile = open('high.txt', 'w')
resultFile.write("Start: ${}, Iterations: {}\n\n".format(sys.argv[1], sys.argv[2]))
lowFile.write("Start: ${}, Iterations: {}\n\n".format(sys.argv[1], sys.argv[2]))
highFile.write("Start: ${}, Iterations: {}\n\n".format(sys.argv[1], sys.argv[2]))

probTemplate = "{0:^20}|{1:^20}|{2:^20}|{3:^20}|{4:^20}|{5:^20}|{6:^20}|{7:^20}"
resultTemplate = "{0:^15}|{1:^15}|{2:^15}|{3:^15}|{4:^15}"
resultFile.write(resultTemplate.format("MINIMUM", "RETURN", "SUCCESS", "AVG ROLLS", "AVG POINTS"))
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
		for iteration in range(0, iterations):
			game = CrapsGame(int(sys.argv[1]), minBet, False, False, debug)

			#don't terminate until all money off table
			while (game.getMoney() >= minBet and game.getAvailableMoney() < desiredReturn):

				game.startRound()

				#bet
				if (game.isOn() == False):
					game.betPass(1)

					if(game.getCameLastRoll() == True and game.getNumBetsOnTable() < 3 and game.getMoney() < desiredReturn):
						if (game.getLastCome() == 6 or game.getLastCome() == 8):
							multiple = 3
						elif (game.getLastCome() == 5 or game.getLastCome() == 9):
							multiple = 2
						else: #point == 4 or point == 10
							multiple = 1
						game.betComeOdds(game.getLastCome(), multiple)

				else:
					if(game.getCameLastRoll() == True):
						if (game.getLastCome() == 6 or game.getLastCome() == 8):
							multiple = 2
						elif (game.getLastCome() == 5 or game.getLastCome() == 9):
							multiple = 2
						else: #point == 4 or point == 10
							multiple = 2
						game.betComeOdds(game.getLastCome(), multiple)
						

					if (game.getLastRollComeOut() == True):
						lastRollComeOut = False
						if (game.getPoint() == 6 or game.getPoint() == 8):
							multiple = 2
						elif (game.getPoint() == 5 or game.getPoint() == 9):
							multiple = 2
						else: #point == 4 or point == 10
							multiple = 2
						game.betPassOdds(multiple)

						if (game.getNumBetsOnTable() < 3 and game.getMoney() < desiredReturn):
							game.betCome(1)
						

					elif (game.getNumBetsOnTable() < 3 and game.getMoney() < desiredReturn):
						if (game.getNumBetsOnTable() == 1):
							game.betCome(1)
							
						elif (game.sixAndEightNotTaken() == True):
							game.betCome(1)
							#game.betPlace(6, 1)
							#game.betPlace(8, 1)

						else:
							game.betCome(1)

				#roll
				rollValue = game.roll()
				
				#update earnings
				game.updateEarnings(rollValue)
				
			totalRolls = totalRolls + game.getNumRolls()
			totalPoints = totalPoints + game.getNumPoints()
			if (game.getAvailableMoney() >= desiredReturn):
				winLows.insert(success, game.getLow())
				success = success + 1
			else:
				loseHighs.insert(iteration-success, game.getHigh())
			allHighs.insert(iteration, game.getHigh())
			allLows.insert(iteration, game.getLow())

		successRate = success/iterations * 100
		roundedSuccessRate = round(successRate, -int(math.floor(math.log10(abs(successRate))) - (4)))
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
		resultFile.write(resultTemplate.format("${}".format(minBet), "${}".format(desiredReturn), "{}%".format(roundedSuccessRate), "{}".format(meanRolls), "{}".format(meanPoints)));
		resultFile.write("\n")
		lowFile.write(probTemplate.format("${}".format(desiredReturn), "${}".format(medianWinLow), "${}".format(medianAllLow), "${}".format(meanWinLow), "${}".format(meanAllLow), "${}".format(stddevWinLow), "${}".format(stddevAllLow), "${}".format(minLow)))
		lowFile.write("\n")
		highFile.write(probTemplate.format("${}".format(desiredReturn), "${}".format(medianLoseHigh), "${}".format(medianAllHigh), "${}".format(meanLoseHigh), "${}".format(meanAllHigh), "${}".format(stddevLoseHigh), "${}".format(stddevAllHigh), "${}".format(maxHigh)))
		highFile.write("\n")


resultFile.close()
lowFile.close()
highFile.close()