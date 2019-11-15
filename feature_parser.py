import sys
import csv

suitedelim = '>>> SUITE: '
benchdelim = '>>> BENCHMARK: '
statsdelim = \
'===-------------------------------------------------------------------------===\n' + \
'                          ... Statistics Collected ...\n' + \
'===-------------------------------------------------------------------------===\n\n'


if __name__ == '__main__':

	if len(sys.argv) < 2:
		print('Usage: {}, "/path/to/stats/file" "output"'.format(sys.argv[0]))

	infile = sys.argv[1]
	outfile = sys.argv[2]

	featurenames = {'suitename': 1, 'benchname': 2}
	filefeatures = {}

	with open(infile, 'r') as finput, open(outfile, 'w') as foutput:
		
		rawstatlist = finput.read().split(suitedelim)
		data = [x for x in rawstatlist if statsdelim in x]
		#data = [ln(x) for x in data if statsdelim in x]
		
		for f in data:

			suitename, buff = f.split('\n', 1)
			benchname, buff = buff.replace(benchdelim, '', 1).split(statsdelim, 1)
			benchname = benchname.strip()

			print('Reading {}/{}'.format(suitename, benchname))

			if suitename + '/' + benchname in filefeatures:
				print('Benchmark: {}/{} already visited, skipping.'.format(suitename, benchname))
				continue
			else:
				filefeatures[suitename + '/' + benchname] = {
				'suitename': suitename,
				'benchname': benchname}

			currfeatures = [x.strip() for x in buff.splitlines() if x and not x.isspace()]

			for line in currfeatures:
				stat, pname, _ , desc = line.split(None, 3)
				if pname + '::' + desc not in featurenames:
					featurenames[pname + '::' + desc] = len(featurenames) + 1

				if pname + '::' + desc not in filefeatures[suitename + '/' + benchname]:
					filefeatures[suitename + '/' + benchname][pname + '::' + desc] = int(stat)
				
				else:
					filefeatures[suitename + '/' + benchname][pname + '::' + desc] += int(stat)

		writer = csv.DictWriter(foutput, fieldnames=featurenames, restval='0')
		writer.writeheader()

		for k, v in filefeatures.items():
			writer.writerow(v)

		print('File entries parsed: {}'.format(len(rawstatlist)))
		if len(rawstatlist) - len(filefeatures) > 0:
			print('File entries not parsed: {}'.format(len(rawstatlist) - len(filefeatures)))










