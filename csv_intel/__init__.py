import csv
import sys
import os
import random

distexplore_enabled = False
try:
	import distexplore
	distexplore_enabled = True
except:
	pass


def process(path):
	f = open(path, 'rb')
	filename = os.path.basename(path)
	filename_pure = filename.rsplit('.', 1)[0]
	print(filename)

	reader = csv.reader(f)

	columns = [x.strip() for x in reader.next()]
	#print( 'Columns:', columns )

	total = 0
	distribs = {}
	for column in columns:
		distribs[column] = {'value': {}, 'empty': 0, 'numeric': 0, 'numeric_values': []}

	for cols in reader:
		total = total + 1
		populate_distribs_for_columns(cols, columns, distribs)

	print('%d entries' % total)
	for i,col in enumerate(columns):
		print_entry_distribs(i, col, distribs, total)

	print('Numerics:')
	for col in columns:
		process_numerics_column(col, distribs, total)

	f.close()

def average(seq):
	return sum(seq)*1.0/len(seq)

def populate_distribs_for_columns(cols, columns, distribs):
	for i, col in enumerate(cols):
		distribs[columns[i]]['value'][col] = distribs[columns[i]]['value'].get(col, 0) + 1
		if col.strip() == '':
			distribs[columns[i]]['empty'] += 1
			try:
				v = float(col)
				distribs[columns[i]]['numeric'] += 1
				distribs[columns[i]]['numeric_values'].append(v)
			except ValueError:
				pass

def process_numerics_column(col, distribs, total):
	numeric_values = distribs[col]['numeric_values']
	if (distribs[col]['numeric']*1.0) / total > 0.7:
		print_numeric_value_stats(numeric_values, distribs)
		if distexplore_enabled:
			distexplore.distribution_file('distributions/%s-%s.html' % (filename_pure, col),
				col,
				numeric_values,
				circular=False, freqrep=True)
			distexplore.distribution_file('distributions/%s-%s-no0.html' % (filename_pure, col),
				col,
				[x for x in numeric_values if x != 0],
				circular=False, freqrep=True)

def print_numeric_value_stats(numeric_values, distribs):
	print('\t%s: %f - %f (avg: %r, non-0 avg: %r, median: %f, mode: %r)' % (
		col,
		min(numeric_values),
		max(numeric_values),
		average(numeric_values),
		average([x for x in numeric_values if x != 0]),
		numeric_values[len(numeric_values)/2],
		max(distribs[col]['value'].items(), key=lambda x: x[1])[0]
		))


def print_entry_distribs(i, col, distribs, total):
	print('\t(%d) %s: %d unique (%.2f%%)\n\t\t%d empty (%.2f%%),\n\t\t%d numeric (%.2f%%)' % (
		i, col,
		len(distribs[col]['value']),
		(len(distribs[col]['value'])*100.0)/total,
		distribs[col]['empty'],
		(distribs[col]['empty']*100.0) / total,
		distribs[col]['numeric'],
		(distribs[col]['numeric']*100.0) / total
		))
	print('\t\te.g. %r' % [random.choice(distribs[col]['value'].keys()) for i in xrange(5)])

def run(args):
	if len(args) < 2 or (len(args) >= 2 and args[1] in ['help', '-h', '--help']):
		print('Usage:')
		print('\tcsv-intel data.csv')
	else:
		process(args[1])


if __name__ == '__main__':
	run(sys.argv)
