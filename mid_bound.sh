TO=1800
MO=14000


YRESULT_DIR=results/mid_bound/yfjs
DARESULT_DIR=results/mid_bound/dafjs
MKRESULT_DIR=results/mid_bound/mk


mkdir -p $YRESULT_DIR
mkdir -p $DARESULT_DIR
mkdir -p $MKRESULT_DIR

# ./runlim -r $TO  python3 -u top_down.py YFJS01 2>&1 | tee $YRESULT_DIR/YFJS01.log
# ./runlim -r $TO  python3 -u top_down.py YFJS02 2>&1 | tee $YRESULT_DIR/YFJS02.log
# ./runlim -r $TO  python3 -u top_down.py YFJS03 2>&1 | tee $YRESULT_DIR/YFJS03.log
# ./runlim -r $TO  python3 -u top_down.py YFJS04 2>&1 | tee $YRESULT_DIR/YFJS04.log 
# ./runlim -r $TO  python3 -u top_down.py YFJS05 2>&1 | tee $YRESULT_DIR/YFJS05.log
# ./runlim -r $TO  python3 -u top_down.py YFJS06 2>&1 | tee $YRESULT_DIR/YFJS06.log 
# ./runlim -r $TO  python3 -u top_down.py YFJS07 2>&1 | tee $YRESULT_DIR/YFJS07.log
# ./runlim -r $TO  python3 -u top_down.py YFJS08 2>&1 | tee $YRESULT_DIR/YFJS08.log
# ./runlim -r $TO  python3 -u top_down.py YFJS09 2>&1 | tee $YRESULT_DIR/YFJS09.log
# ./runlim -r $TO  python3 -u top_down.py YFJS10 2>&1 | tee $YRESULT_DIR/YFJS10.log
# ./runlim -r $TO  python3 -u top_down.py YFJS11 2>&1 | tee $YRESULT_DIR/YFJS11.log
# ./runlim -r $TO  python3 -u top_down.py YFJS12 2>&1 | tee $YRESULT_DIR/YFJS12.log
# ./runlim -r $TO  python3 -u top_down.py YFJS13 2>&1 | tee $YRESULT_DIR/YFJS13.log
# ./runlim -r $TO  python3 -u top_down.py YFJS14 2>&1 | tee $YRESULT_DIR/YFJS14.log
# ./runlim -r $TO  python3 -u top_down.py YFJS15 2>&1 | tee $YRESULT_DIR/YFJS15.log
# ./runlim -r $TO  python3 -u top_down.py YFJS16 2>&1 | tee $YRESULT_DIR/YFJS16.log
# ./runlim -r $TO  python3 -u top_down.py YFJS17 2>&1 | tee $YRESULT_DIR/YFJS17.log
# ./runlim -r $TO  python3 -u top_down.py YFJS18 2>&1 | tee $YRESULT_DIR/YFJS18.log
# ./runlim -r $TO  python3 -u top_down.py YFJS19 2>&1 | tee $YRESULT_DIR/YFJS19.log
# ./runlim -r $TO  python3 -u top_down.py YFJS20 2>&1 | tee $YRESULT_DIR/YFJS20.log

# ./runlim -r $TO  python3 -u top_down.py DAFJS01 2>&1 | tee $DARESULT_DIR/DAFJS01.log
# ./runlim -r $TO  python3 -u top_down.py DAFJS02 2>&1 | tee $DARESULT_DIR/DAFJS02.log
# ./runlim -r $TO  python3 -u top_down.py DAFJS03 2>&1 | tee $DARESULT_DIR/DAFJS03.log
# ./runlim -r $TO  python3 -u top_down.py DAFJS04 2>&1 | tee $DARESULT_DIR/DAFJS04.log
# ./runlim -r $TO  python3 -u top_down.py DAFJS05 2>&1 | tee $DARESULT_DIR/DAFJS05.log
# ./runlim -r $TO  python3 -u top_down.py DAFJS06 2>&1 | tee $DARESULT_DIR/DAFJS06.log
# ./runlim -r $TO  python3 -u top_down.py DAFJS07 2>&1 | tee $DARESULT_DIR/DAFJS07.log
# ./runlim -r $TO  python3 -u top_down.py DAFJS08 2>&1 | tee $DARESULT_DIR/DAFJS08.log
./runlim -r $TO  python3 -u top_down.py DAFJS09 2>&1 | tee $DARESULT_DIR/DAFJS09.log
./runlim -r $TO  python3 -u top_down.py DAFJS10 2>&1 | tee $DARESULT_DIR/DAFJS10.log
./runlim -r $TO  python3 -u top_down.py DAFJS11 2>&1 | tee $DARESULT_DIR/DAFJS11.log
./runlim -r $TO  python3 -u top_down.py DAFJS12 2>&1 | tee $DARESULT_DIR/DAFJS12.log
./runlim -r $TO  python3 -u top_down.py DAFJS13 2>&1 | tee $DARESULT_DIR/DAFJS13.log
./runlim -r $TO  python3 -u top_down.py DAFJS14 2>&1 | tee $DARESULT_DIR/DAFJS14.log
./runlim -r $TO  python3 -u top_down.py DAFJS15 2>&1 | tee $DARESULT_DIR/DAFJS15.log
./runlim -r $TO  python3 -u top_down.py DAFJS16 2>&1 | tee $DARESULT_DIR/DAFJS16.log
./runlim -r $TO  python3 -u top_down.py DAFJS17 2>&1 | tee $DARESULT_DIR/DAFJS17.log
./runlim -r $TO  python3 -u top_down.py DAFJS18 2>&1 | tee $DARESULT_DIR/DAFJS18.log
./runlim -r $TO  python3 -u top_down.py DAFJS19 2>&1 | tee $DARESULT_DIR/DAFJS19.log
./runlim -r $TO  python3 -u top_down.py DAFJS20 2>&1 | tee $DARESULT_DIR/DAFJS20.log
./runlim -r $TO  python3 -u top_down.py DAFJS21 2>&1 | tee $DARESULT_DIR/DAFJS21.log
./runlim -r $TO  python3 -u top_down.py DAFJS22 2>&1 | tee $DARESULT_DIR/DAFJS22.log
./runlim -r $TO  python3 -u top_down.py DAFJS23 2>&1 | tee $DARESULT_DIR/DAFJS23.log
./runlim -r $TO  python3 -u top_down.py DAFJS24 2>&1 | tee $DARESULT_DIR/DAFJS24.log
./runlim -r $TO  python3 -u top_down.py DAFJS25 2>&1 | tee $DARESULT_DIR/DAFJS25.log
./runlim -r $TO  python3 -u top_down.py DAFJS26 2>&1 | tee $DARESULT_DIR/DAFJS26.log
./runlim -r $TO  python3 -u top_down.py DAFJS27 2>&1 | tee $DARESULT_DIR/DAFJS27.log
./runlim -r $TO  python3 -u top_down.py DAFJS28 2>&1 | tee $DARESULT_DIR/DAFJS28.log
./runlim -r $TO  python3 -u top_down.py DAFJS29 2>&1 | tee $DARESULT_DIR/DAFJS29.log
./runlim -r $TO  python3 -u top_down.py DAFJS30 2>&1 | tee $DARESULT_DIR/DAFJS30.log

# ./runlim -r $TO  python3 -u top_down.py $MKDATA_DIR/MK01 2>&1 | tee $MKRESULT_DIR/MK01.log
# ./runlim -r $TO  python3 -u top_down.py $MKDATA_DIR/MK02 2>&1 | tee $MKRESULT_DIR/MK02.log
# ./runlim -r $TO  python3 -u top_down.py $MKDATA_DIR/MK03 2>&1 | tee $MKRESULT_DIR/MK03.log
# ./runlim -r $TO  python3 -u top_down.py $MKDATA_DIR/MK04 2>&1 | tee $MKRESULT_DIR/MK04.log
# ./runlim -r $TO  python3 -u top_down.py $MKDATA_DIR/MK05 2>&1 | tee $MKRESULT_DIR/MK05.log
# ./runlim -r $TO  python3 -u top_down.py $MKDATA_DIR/MK06 2>&1 | tee $MKRESULT_DIR/MK06.log
# ./runlim -r $TO  python3 -u top_down.py $MKDATA_DIR/MK07 2>&1 | tee $MKRESULT_DIR/MK07.log
# ./runlim -r $TO  python3 -u top_down.py $MKDATA_DIR/MK08 2>&1 | tee $MKRESULT_DIR/MK08.log
# ./runlim -r $TO  python3 -u top_down.py $MKDATA_DIR/MK09 2>&1 | tee $MKRESULT_DIR/MK09.log
# ./runlim -r $TO  python3 -u top_down.py $MKDATA_DIR/MK10 2>&1 | tee $MKRESULT_DIR/MK10.log
# ./runlim -r $TO  python3 -u top_down.py $MKDATA_DIR/MK11 2>&1 | tee $MKRESULT_DIR/MK11.log
# ./runlim -r $TO  python3 -u top_down.py $MKDATA_DIR/MK12 2>&1 | tee $MKRESULT_DIR/MK12.log
# ./runlim -r $TO  python3 -u top_down.py $MKDATA_DIR/MK13 2>&1 | tee $MKRESULT_DIR/MK13.log
# ./runlim -r $TO  python3 -u top_down.py $MKDATA_DIR/MK14 2>&1 | tee $MKRESULT_DIR/MK14.log
# ./runlim -r $TO  python3 -u top_down.py $MKDATA_DIR/MK15 2>&1 | tee $MKRESULT_DIR/MK15.log