import csv

def Save_OutPut_csv(filename, list_to_save) :
	with open(filename, 'w', newline='') as ff:
		writer = csv.writer(ff, lineterminator='\n')
		for nnn in list_to_save : 
			writer.writerow(nnn)

def Save_OutPut_txt(filename, list_to_save) :
	with open(filename, 'w', newline='') as ff: 
		for nnn in list_to_save : 
			#ff.write(str(line)) 
			res = str(nnn)[1:-1]
			ff.write("%s\n" % res)
