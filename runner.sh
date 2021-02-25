#!/usr/bin/env bash

set -euo pipefail
IFS=$'\n\t'

if [[ $# -eq 0 ]];
then
	echo "Usage:   $0 <command to run ...>"
	echo "Example: $0 python my_solution.py"
	exit 1
fi


DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

time (
cd "$DIR"
for in_file in *.in; do
	echo "Running $in_file"
	out_file="${in_file}.out"
	time (
		"$@" < $in_file > $out_file
		echo
		echo -n "Finished $in_file in"
	) &
done

wait
echo
echo -n "Total time"
)
