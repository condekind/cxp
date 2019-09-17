#!/bin/bash

ORIG_FOLDER=$1
OUT_FILE=$2

CC="/home/condekind/stuff/llvm/build/bin/clang"
OPT="/home/condekind/stuff/llvm/build/bin/opt"

if [ -z "$1" ] || [ -z "$2" ]
then
	echo "Usage: $0 <source_dir> <out_file>"
	echo "source_dir -> folder containing programs to be compiled."
	echo "out_file -> file to output opt results"
	exit 1
fi

if [ ! -d "$ORIG_FOLDER" ]
then
	echo "Source directory does not exist!"
	exit 1
fi

CFILES=$(find $ORIG_FOLDER -name "*.c")
FILES=$(find $ORIG_FOLDER -name "*.bc")

for f in $CFILES; do
	rm ${f/.c/.bc}
	$CC -Xclang -disable-O0-optnone -c -emit-llvm $f -o ${f/.c/.bc}
done

for f in $FILES; do
	base=$(basename $f)
	no_ext=${base%.*}

	echo "Processing file: $base"
	echo "file: $base" >>$OUT_FILE

	$OPT $f -O3 -loops -demanded-bits -dfsan -module-summary-analysis -aa-eval -aa -basicaa -canonicalize-aliases -cfl-anders-aa -cfl-steens-aa -external-aa -globals-aa -objc-arc-aa -scev-aa -scoped-noalias -tbaa -instcount -stats -disable-output 2>>$OUT_FILE
done
