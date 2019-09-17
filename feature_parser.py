import sys
import csv

delim = \
'===-------------------------------------------------------------------------===\n' + \
'                          ... Statistics Collected ...\n' + \
'===-------------------------------------------------------------------------===\n\n'

if __name__ == '__main__':

	if len(sys.argv) < 2:
		print('Usage: {}, "/path/to/stats/file" "output"'.format(sys.argv[0]))

	infile = sys.argv[1]
	outfile = sys.argv[2]
	featurenames = ['filename']	# ['feature1', 'feature2', ... ]
	filefeatures = {}			# {'file1': {'feature1': value, ... }, ... }
	cnt = 0						# number of files parsed

	with open(infile, 'r') as finput, open(outfile, 'w') as foutput:
		
		filedata = [x for x in finput.read().split('file: ') if len(x) > 0]
		
		for f in filedata:

			cnt += 1
			
			if delim not in f:  # probably an error on that file
				continue

			filename = f.split()[0]

			if filename in filefeatures:
				print('File: {} already visited, skipping.'.format(filename))
				continue

			else:
				filefeatures[filename] = {'filename': filename}

			currfeatures = f.split(delim)[-1]

			for ftline in currfeatures.split('\n'):
				ft = ''

				if not len(ftline):  # blank line, skip
					continue
				else:
					ft = ftline

				line = ft.split(None, 2)

				if line[-2] + ' ' + line[-1] not in featurenames:
					featurenames.append(line[-2] + ' ' + line[-1])

				if line[-2] + ' ' + line[-1] not in filefeatures[filename]:
					filefeatures[filename][line[-2] + ' ' + line[-1]] = int(line[0])
				
				else:
					filefeatures[filename][line[-2] + ' ' + line[-1]] += int(line[0])

		writer = csv.DictWriter(foutput, fieldnames=featurenames, restval='0')
		writer.writeheader()

		for k, v in filefeatures.items():
			writer.writerow(v)

		print('File entries parsed: {}'.format(len(filefeatures)))
		if cnt - len(filefeatures) > 0:
			print('File entries not parsed: {}'.format(cnt - len(filefeatures)))











