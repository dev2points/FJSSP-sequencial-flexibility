TO=10800
MO=14000


DATA_DIR=datasets/dafjs
RESULT_DIR=results/vm/test/test_precedence

mkdir -p $RESULT_DIR

# ./runlim -r $TO -s $MO  python3 -u temp.py 0 $DATA_DIR/DAFJS29 2>&1 | tee $RESULT_DIR/DAFJS29_0.log
# ./runlim -r $TO -s $MO  python3 -u temp.py 1 $DATA_DIR/DAFJS09 2>&1 | tee $RESULT_DIR/DAFJS09_1.log
# ./runlim -r $TO -s $MO  python3 -u temp.py 0 $DATA_DIR/DAFJS09 2>&1 | tee $RESULT_DIR/DAFJS09_0.log
# ./runlim -r $TO -s $MO  python3 -u temp.py $DATA_DIR/DAFJS10 2>&1 | tee $RESULT_DIR/DAFJS10.log
# ./runlim -r $TO -s $MO  python3 -u temp.py $DATA_DIR/DAFJS12 2>&1 | tee $RESULT_DIR/DAFJS12.log
./runlim -r $TO -s $MO  python3 -u temp.py 1 $DATA_DIR/DAFJS16 2>&1 | tee $RESULT_DIR/DAFJS16_1.log
./runlim -r $TO -s $MO  python3 -u temp.py 1 $DATA_DIR/DAFJS23 2>&1 | tee $RESULT_DIR/DAFJS23_1.log
# ./runlim -r $TO -s $MO  python3 -u temp.py 1 0 0 $DATA_DIR/DAFJS09 2>&1 | tee $RESULT_DIR/DAFJS09_1_0_0.log
# ./runlim -r $TO -s $MO  python3 -u temp.py 1 0 0 $DATA_DIR/DAFJS29 2>&1 | tee $RESULT_DIR/DAFJS29_1_0_0.log
# ./runlim -r $TO -s $MO  python3 -u temp.py 1 1 0 $DATA_DIR/DAFJS29 2>&1 | tee $RESULT_DIR/DAFJS29_1_1_0.log