import sys 
import re 

with open(sys.argv[1]) as in_file:
	with open(sys.argv[2], 'w') as out_file:
		for l in in_file:
			if l == '\n' or l[0] == '[': 
				continue 

			f = re.findall(r'\{\s([0-9a-zA-Z\/\s\-\.]+)\s\}', l)
			
			for i in f:
				ls = i.split(' ')[: 2]
				print(ls)
				out_file.write('{}\n'.format(' '.join(ls)))
