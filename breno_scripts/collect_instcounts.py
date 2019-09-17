import sys

def parse_results():
	if (len(sys.argv) < 2):
		print("Not enough import arguments!")
		print("Usage: python {} <opt_output_file>".format(sys.argv[0]))
		print("opt_output_file -> a file containing the output of opt -stats")
		return

	infile = sys.argv[1]
	currfile = str()

	print("bench,total,basicblock,ret,br,switch,unreachable,add,fadd,sub,fsub,mul,fmul,udiv,sdiv,fdiv,urem,srem,frem,shl,lshr,ashr,and,or,xor,alloca,load,store,getelementptr,icmp,fcmp,phi,select,call")

	with open(infile) as fd:
		line = fd.readline()

		while line:
			#Newfile
			if "file: " in line:
				if currfile:
					print("{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}".format(currfile,numTotal,numBB,numRet,numBr,numSwitch,numUnreachable,numAdd,numFAdd,numSub,numFSub,numMul,numFMul,numUDiv,numSDiv,numFDiv,numURem,numSRem,numFRem,numShl,numLShr,numAShr,numAnd,numOr,numXor,numAlloca,numLoad,numStore,numGetElementPtr,numICmp,numFCmp,numPHI,numSelect,numCall))

				#Terminators
				numRet = 0
				numBr = 0
				numSwitch = 0
				numUnreachable = 0

				#Binary
				numAdd = 0
				numFAdd = 0
				numSub = 0
				numFSub = 0
				numMul = 0
				numFMul = 0
				numUDiv = 0
				numSDiv = 0
				numFDiv = 0
				numURem = 0
				numSRem = 0
				numFRem = 0

				#Bitwise
				numShl = 0
				numLShr = 0
				numAShr = 0
				numAnd = 0
				numOr = 0
				numXor = 0

				#Memory
				numAlloca = 0
				numLoad = 0
				numStore = 0
				numGetElementPtr = 0

				#Other
				numICmp = 0
				numFCmp = 0
				numPHI = 0
				numSelect = 0
				numCall = 0

				#Basic Blocks
				numBB = 0

				#Total
				numTotal = 0

				#Update current file
				currfile = line[len("file:"):len(line)-4] + ".c"

			#Terminators
			elif "Number of Ret insts" in line:
				numRet = int(line.split()[0])
			elif "Number of Br insts" in line:
				numBr = int(line.split()[0])
			elif "Number of Switch insts" in line:
				numSwitch = int(line.split()[0])
			elif "Number of Unreachable insts" in line:
				numUnreachable = int(line.split()[0])

			#Binary
			elif "Number of Add insts" in line:
				numAdd = int(line.split()[0])
			elif "Number of Sub insts" in line:
				numSub = int(line.split()[0])
			elif "Number of FSub insts" in line:
				numFSub = int(line.split()[0])
			elif "Number of Mul insts" in line:
				nuMul = int(line.split()[0])
			elif "Number of FMul insts" in line:
				numFMul = int(line.split()[0])
			elif "Number of UDiv insts" in line:
				numUDiv = int(line.split()[0])
			elif "Number of SDiv insts" in line:
				numSDiv = int(line.split()[0])
			elif "Number of FDiv insts" in line:
				numFDiv = int(line.split()[0])
			elif "Number of URem insts" in line:
				numURem = int(line.split()[0])
			elif "Number of SRem insts" in line:
				numSRem = int(line.split()[0])
			elif "Number of FRem insts" in line:
				numFRem = int(line.split()[0])

			#Bitwise
			elif "Number of Shl insts" in line:
				numShl = int(line.split()[0])
			elif "Number of LShr insts" in line:
				numLShr = int(line.split()[0])
			elif "Number of AShr insts" in line:
				numAShr = int(line.split()[0])
			elif "Number of And insts" in line:
				numAnd = int(line.split()[0])
			elif "Number of Or insts" in line:
				numOr = int(line.split()[0])
			elif "Number of Xor insts" in line:
				numXor = int(line.split()[0])

			#Memory
			elif "Number of Alloca insts" in line:
				numAlloca = int(line.split()[0])
			elif "Number of Load insts" in line:
				numLoad = int(line.split()[0])
			elif "Number of Store insts" in line:
				numStore = int(line.split()[0])
			elif "Number of GetElementPtr insts" in line:
				numGetElementPtr = int(line.split()[0])

			#Other
			elif "Number of ICmp insts" in line:
				numICmp = int(line.split()[0])
			elif "Number of FCmp insts" in line:
				numFCmp = int(line.split()[0])
			elif "Number of PHI insts" in line:
				numPHI = int(line.split()[0])
			elif "Number of Select insts" in line:
				numSelect = int(line.split()[0])
			elif "Number of Call insts" in line:
				numCall = int(line.split()[0])

			#Basic blocks
			elif "Number of basic blocks" in line:
				numBB = int(line.split()[0])
			
			elif "(of all types)" in line:
				numTotal = int(line.split()[0])

			line = fd.readline()

	print("{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}".format(currfile,numTotal,numBB,numRet,numBr,numSwitch,numUnreachable,numAdd,numFAdd,numSub,numFSub,numMul,numFMul,numUDiv,numSDiv,numFDiv,numURem,numSRem,numFRem,numShl,numLShr,numAShr,numAnd,numOr,numXor,numAlloca,numLoad,numStore,numGetElementPtr,numICmp,numFCmp,numPHI,numSelect,numCall))

if __name__ == "__main__":
	parse_results()
