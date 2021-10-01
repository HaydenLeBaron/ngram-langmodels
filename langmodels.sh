rm langmodels-output.txt
echo "TRAIN/TEST 1:\n" >> langmodels-output.txt
python3 langmodels.py train1.txt -test test1.txt >> langmodels-output.txt
echo "TRAIN/TEST 2:\n" >> langmodels-output.txt
python3 langmodels.py train2.txt -test test2.txt >> langmodels-output.txt
