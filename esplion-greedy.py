from stats import stats
from stocks import *
from random import shuffle, choice, uniform


def epsilonBandit(numActions, reward,epsilon,bestAction):
   t = 0
   if(uniform(0, 1) <= epsilon):

      while True:
         i = choice(range(numActions))
         yield i, reward(i, t)
         t += 1
   else:

       while True:
           i=bestAction
           yield i, reward(i,t)
           t += 1


def epsilonBanditStocks(stockTable):
   tickers = list(stockTable.keys())
   shuffle(tickers) # note that this makes the algorithm SO unstable
   numRounds = len(stockTable[tickers[0]])
   numActions = len(tickers)

   reward = lambda choice, t: payoff(stockTable, t, tickers[choice])
   singleActionReward = lambda j: sum([reward(j,t) for t in range(numRounds)])

   bestAction = max(range(numActions), key=singleActionReward)
   bestActionCumulativeReward = singleActionReward(bestAction)

   cumulativeReward = 0
   t = 0
   epsilonGenerator = epsilonBandit(numActions, reward, 0.001, bestAction)
   for (chosenAction, reward) in epsilonGenerator:
      cumulativeReward += reward
      t += 1
      if t == numRounds:
         break

   return cumulativeReward, bestActionCumulativeReward, tickers[bestAction]


prettyList = lambda L: ', '.join(['%.3f' % x for x in L])
payoffStats = lambda data: stats(epsilonBanditStocks(data)[0] for _ in range(1000))


def runExperiment(table):
   print("(Expected payoff, variance) over 1000 trials is %r" % (payoffStats(table),))
   reward, bestActionReward, bestStock = epsilonBanditStocks(table)
   print("For a single run: ")
   print("Payoff was %.2f" % reward)
   print("Regret was %.2f" % (bestActionReward - reward))
   print("Best stock was %s at %.2f" % (bestStock, bestActionReward))


if __name__ == "__main__":
   table = readInStockTable('stocks/new-stocks.csv')
   runExperiment(table)
   payoffGraph(table, list(sorted(table.keys())), cumulative=False)
   print()
