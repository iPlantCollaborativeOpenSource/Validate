# ValPy -- Validate.R in Python
# Author: Dustin Landers
# Contact: (770 289-8830 :: dustin.landers@gmail.com


"""Dependencies"""
from commandline import *
from fileimport import *
from checkhidden import *
from gwas import *
import numpy as np


"""Main function and execution"""
def main():
	initializeGraphics()
	folder, analysis, truth, snp, score, beta, filename, threshold, seper, kttype, kttypeseper = checkArgs()
	appOutputList = checkList(getList(folder))
	ktFile = loadKT(truth, kttypeseper)


	if kttype == "OTE":
		acquiredData = loadFile(folder, appOutputList[0], seper)
		snpColumnNo = acquiredData.header.index(snp)
		snpColumn = list()
		for each in acquiredData.data.iteritems():
			snpColumn.append(each[1][snpColumnNo])
		
		ktSnps = list()
		for each in ktFile.data.iteritems():
			ktSnps.append(each[1][0])
		ktBetas = list()
		for each in ktFile.data.iteritems():
			ktBetas.append(each[1][1])

		snpTrueFalse = list()
		for each in snpColumn:
			snpTrueFalse.append(trueFalse(each, ktSnps))
		
		if beta is not None:
			betaTrueFalse = list()
			count = 0
			for each in snpTrueFalse:
				if each is True:
					current = snpColumn[count]
					match = ktSnps.index(current)
					thisBeta = ktBetas[match]
					betaTrueFalse.append(float(thisBeta))
				else:
					betaTrueFalse.append(float(0))
				count += 1

	"""	if severity is None:
			severity = float(len(ktSnps))/float(len(snpTrueFalse) - len(ktSnps))"""

	firstForHeader = True
	for each in appOutputList:
		acquiredData = loadFile(folder, each, seper)
		snpColumnNo = acquiredData.header.index(snp)
		snpColumn = list()
		for each in acquiredData.data.iteritems():
			snpColumn.append(each[1][snpColumnNo])

		scoreColumnNo = acquiredData.header.index(score)
		scoreColumn = list()
		for each in acquiredData.data.iteritems():
			scoreColumn.append(float(each[1][scoreColumnNo]))

		if beta is not None:
			betaColumnNo = acquiredData.header.index(beta)
			betaColumn = list()
			for each in acquiredData.data.iteritems():
				betaColumn.append(float(each[1][betaColumnNo]))

		if analysis == "GWAS" and firstForHeader:
			if beta is not None:
				keepToWrite = gwasWithBeta(betaColumn, betaTrueFalse, snpTrueFalse, scoreColumn, threshold)
				writeCSV(filename, keepToWrite, "wb", "\t")
			if beta is None:
				keepToWrite = gwasWithoutBeta(snpTrueFalse, scoreColumn, threshold)
				writeCSV(filename, keepToWrite, "wb", "\t")
		else:
			if beta is not None:
				keepToWrite = gwasWithBeta(betaColumn, betaTrueFalse, snpTrueFalse, scoreColumn, threshold)
				writeCSV(filename, keepToWrite, "a", "\t")
			if beta is None:
				keepToWrite = gwasWithoutBeta(snpTrueFalse, scoreColumn, threshold)
				writeCSV(filename, keepToWrite, "a", "\t")
		firstForHeader = False


if __name__ == "__main__":
	main()
