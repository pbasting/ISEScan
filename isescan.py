#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ISEScan version
version = '1.7.1'

import argparse
import os
import sys


def isPredictSingle(args):
	import isPredict
	seqfile = args.seqfile.strip()
	path2proteome = args.path2proteome
	path2hmm = args.path2hmm
	seqfilename = os.path.basename(seqfile)
	org = os.path.basename(os.path.dirname(seqfile))
	filelist = org + '_' + seqfilename + '.list'
	with open(filelist, 'w') as fp:
		fp.write(seqfile+'\n')

	isPredict.isPredict(filelist, path2proteome, path2hmm)
	os.remove(filelist)

if __name__ == "__main__":
	# import textwrap

	# # Parse command line arguments
	## required ##
	parser = argparse.ArgumentParser(prog='isescan', description='''Search IS Profile HMMs against gene database. A typical invocation would be:\
																	\npython3 isescan.py -i seqfile -p proteome -hmm hmm\n\
																	- If you want isescan to report both complete and incomplete (partial) IS elements, you can change the output options (section "Option switch to report partial IS element") in constants.py.''')
	
	## required ##
	parser.add_argument("-i", "--seqfile", type=str, help="sequence file in fasta format", required=True)
	parser.add_argument("-p", "--path2proteome", type=str, help="directory where proteome (each line corresponds to a protein sequence database translated from a genome) files will be placed", required=True)
	parser.add_argument("-hmm", "--path2hmm", type=str, help="directory where the results of hmmsearch will be placed", required=True)

    ## optional ##
	parser.add_argument('--version', action='version', version='%(prog)s' + ' ' + version)
	parser.add_argument("-t", "--nthread", type=int, help="number of threads to use in calculation (default = '4') ", required=False)
	parser.add_argument("-n", "--nproc", type=int, help="number of processes to use in calculation (default = '2') ", required=False)
	parser.add_argument("-r", "--removeShortIS", action="store_true", help="ISEScan will remove partial IS elements which include: IS element with length < 400 or single copy IS element without perfect TIR (default = 'False') ", required=False)
	parser.add_argument("-d", "--maxDistBetweenOrfs", type=int, help="maximum distance (bp) between two neighboring orfs (including +/- strand) within one IS element (default = '100') ", required=False)
	parser.add_argument("-m", "--train_model", type=str, help="train_model used by FragGeneScan (default = 'illumina_5') options:'complete', 'sanger_5', 'sanger_10', '454_10', '454_30', 'illumina_5', 'illumina_10'; see FragGeneScan documentation for more details", required=False)

	args = parser.parse_args()


	isescan_path = os.path.dirname(os.path.abspath(__file__))
	config = isescan_path+"/config.py"
	if os.path.isfile(config):
		os.remove(config)
	with open(config,"w") as conf:
		conf.write("#!/usr/bin/env python3\n\n\n")
		if args.nthread is not None:
			conf.write("nthread="+str(args.nthread)+"\n")

		if args.nproc is not None:
			conf.write("nproc="+str(args.nproc)+"\n")

		if args.removeShortIS == True:
			conf.write("removeShortIS=True"+"\n")
		else:
			conf.write("removeShortIS=False\n")

		if args.maxDistBetweenOrfs is not None:
			conf.write("maxDistBetweenOrfs="+str(args.maxDistBetweenOrfs)+"\n")
		
		valid_train_models = ['complete', 'sanger_5', 'sanger_10', '454_10', '454_30', 'illumina_5', 'illumina_10']
		if args.train_model is None:
			args.train_model = 'illumina_5'
		elif args.train_model not in valid_train_models:
			sys.exit("train_model: '"+args.train_model+"' not valid, please use one of: "+", ".join(valid_train_models)+"\n")
			
		conf.write("train_model='"+args.train_model+"'\n")

	print(isescan_path)
	# sys.exit(0)

	isPredictSingle(args)
