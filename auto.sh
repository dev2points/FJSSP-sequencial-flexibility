TO=10800
MO=14000

YDATA_DIR=datasets/yfjs
DADATA_DIR=datasets/dafjs
FMJDATA_DIR=datasets/fmj
MKDATA_DIR=datasets/brandimarte
YRESULT_DIR=results/vm/yfjs
DARESULT_DIR=results/vm/only_xm+no_sb/dafjs
FMJRESULT_DIR=results/vm/only_xm+no_sb/fmj
MKRESULT_DIR=results/vm/only_xm+no_sb/brandimarte

mkdir -p $YRESULT_DIR
mkdir -p $DARESULT_DIR
mkdir -p $FMJRESULT_DIR
mkdir -p $MKRESULT_DIR

# ./runlim -r $TO -s $MO  python3 -u temp.py $YDATA_DIR/YFJS01 2>&1 | tee $YRESULT_DIR/YFJS01.log
# ./runlim -r $TO -s $MO  python3 -u temp.py $YDATA_DIR/YFJS02 2>&1 | tee $YRESULT_DIR/YFJS02.log
# ./runlim -r $TO -s $MO  python3 -u temp.py $YDATA_DIR/YFJS03 2>&1 | tee $YRESULT_DIR/YFJS03.log
# ./runlim -r $TO -s $MO  python3 -u temp.py $YDATA_DIR/YFJS04 2>&1 | tee $YRESULT_DIR/YFJS04.log 
# ./runlim -r $TO -s $MO  python3 -u temp.py $YDATA_DIR/YFJS05 2>&1 | tee $YRESULT_DIR/YFJS05.log
# ./runlim -r $TO -s $MO  python3 -u temp.py $YDATA_DIR/YFJS06 2>&1 | tee $YRESULT_DIR/YFJS06.log 
# ./runlim -r $TO -s $MO  python3 -u temp.py $YDATA_DIR/YFJS07 2>&1 | tee $YRESULT_DIR/YFJS07.log
# ./runlim -r $TO -s $MO  python3 -u temp.py $YDATA_DIR/YFJS08 2>&1 | tee $YRESULT_DIR/YFJS08.log
# ./runlim -r $TO -s $MO  python3 -u temp.py $YDATA_DIR/YFJS09 2>&1 | tee $YRESULT_DIR/YFJS09.log
# ./runlim -r $TO -s $MO  python3 -u temp.py $YDATA_DIR/YFJS10 2>&1 | tee $YRESULT_DIR/YFJS10.log
# ./runlim -r $TO -s $MO  python3 -u temp.py $YDATA_DIR/YFJS11 2>&1 | tee $YRESULT_DIR/YFJS11.log
# ./runlim -r $TO -s $MO  python3 -u temp.py $YDATA_DIR/YFJS12 2>&1 | tee $YRESULT_DIR/YFJS12.log
# ./runlim -r $TO -s $MO  python3 -u temp.py $YDATA_DIR/YFJS13 2>&1 | tee $YRESULT_DIR/YFJS13.log
# ./runlim -r $TO -s $MO  python3 -u temp.py $YDATA_DIR/YFJS14 2>&1 | tee $YRESULT_DIR/YFJS14.log
# ./runlim -r $TO -s $MO  python3 -u temp.py $YDATA_DIR/YFJS15 2>&1 | tee $YRESULT_DIR/YFJS15.log
# ./runlim -r $TO -s $MO  python3 -u temp.py $YDATA_DIR/YFJS16 2>&1 | tee $YRESULT_DIR/YFJS16.log
# ./runlim -r $TO -s $MO  python3 -u temp.py $YDATA_DIR/YFJS17 2>&1 | tee $YRESULT_DIR/YFJS17.log
# ./runlim -r $TO -s $MO  python3 -u temp.py $YDATA_DIR/YFJS18 2>&1 | tee $YRESULT_DIR/YFJS18.log
# ./runlim -r $TO -s $MO  python3 -u temp.py $YDATA_DIR/YFJS19 2>&1 | tee $YRESULT_DIR/YFJS19.log
# ./runlim -r $TO -s $MO  python3 -u temp.py $YDATA_DIR/YFJS20 2>&1 | tee $YRESULT_DIR/YFJS20.log

# ./runlim -r $TO -s $MO  python3 -u temp.py $DADATA_DIR/DAFJS01 2>&1 | tee $DARESULT_DIR/DAFJS01.log
# ./runlim -r $TO -s $MO  python3 -u temp.py $DADATA_DIR/DAFJS02 2>&1 | tee $DARESULT_DIR/DAFJS02.log
# ./runlim -r $TO -s $MO  python3 -u temp.py $DADATA_DIR/DAFJS03 2>&1 | tee $DARESULT_DIR/DAFJS03.log
# ./runlim -r $TO -s $MO  python3 -u temp.py $DADATA_DIR/DAFJS04 2>&1 | tee $DARESULT_DIR/DAFJS04.log
# ./runlim -r $TO -s $MO  python3 -u temp.py $DADATA_DIR/DAFJS05 2>&1 | tee $DARESULT_DIR/DAFJS05.log
# ./runlim -r $TO -s $MO  python3 -u temp.py $DADATA_DIR/DAFJS06 2>&1 | tee $DARESULT_DIR/DAFJS06.log
# ./runlim -r $TO -s $MO  python3 -u temp.py $DADATA_DIR/DAFJS07 2>&1 | tee $DARESULT_DIR/DAFJS07.log
# ./runlim -r $TO -s $MO  python3 -u temp.py $DADATA_DIR/DAFJS08 2>&1 | tee $DARESULT_DIR/DAFJS08.log
# ./runlim -r $TO -s $MO  python3 -u temp.py $DADATA_DIR/DAFJS09 2>&1 | tee $DARESULT_DIR/DAFJS09.log
# ./runlim -r $TO -s $MO  python3 -u temp.py $DADATA_DIR/DAFJS09 2>&1 | tee $DARESULT_DIR/DAFJS09.log
# ./runlim -r $TO -s $MO  python3 -u temp.py $DADATA_DIR/DAFJS10 2>&1 | tee $DARESULT_DIR/DAFJS10.log
# ./runlim -r $TO -s $MO  python3 -u temp.py $DADATA_DIR/DAFJS11 2>&1 | tee $DARESULT_DIR/DAFJS11.log
# ./runlim -r $TO -s $MO  python3 -u temp.py $DADATA_DIR/DAFJS12 2>&1 | tee $DARESULT_DIR/DAFJS12.log
# ./runlim -r $TO -s $MO  python3 -u temp.py $DADATA_DIR/DAFJS13 2>&1 | tee $DARESULT_DIR/DAFJS13.log
# ./runlim -r $TO -s $MO  python3 -u temp.py $DADATA_DIR/DAFJS14 2>&1 | tee $DARESULT_DIR/DAFJS14.log
# ./runlim -r $TO -s $MO  python3 -u temp.py $DADATA_DIR/DAFJS15 2>&1 | tee $DARESULT_DIR/DAFJS15.log
# ./runlim -r $TO -s $MO  python3 -u temp.py $DADATA_DIR/DAFJS16 2>&1 | tee $DARESULT_DIR/DAFJS16.log
# ./runlim -r $TO -s $MO  python3 -u temp.py $DADATA_DIR/DAFJS17 2>&1 | tee $DARESULT_DIR/DAFJS17.log
# ./runlim -r $TO -s $MO  python3 -u temp.py $DADATA_DIR/DAFJS18 2>&1 | tee $DARESULT_DIR/DAFJS18.log
# ./runlim -r $TO -s $MO  python3 -u temp.py $DADATA_DIR/DAFJS19 2>&1 | tee $DARESULT_DIR/DAFJS19.log
# ./runlim -r $TO -s $MO  python3 -u temp.py $DADATA_DIR/DAFJS20 2>&1 | tee $DARESULT_DIR/DAFJS20.log
# ./runlim -r $TO -s $MO  python3 -u temp.py $DADATA_DIR/DAFJS21 2>&1 | tee $DARESULT_DIR/DAFJS21.log
# ./runlim -r $TO -s $MO  python3 -u temp.py $DADATA_DIR/DAFJS22 2>&1 | tee $DARESULT_DIR/DAFJS22.log
# ./runlim -r $TO -s $MO  python3 -u temp.py $DADATA_DIR/DAFJS23 2>&1 | tee $DARESULT_DIR/DAFJS23.log
# ./runlim -r $TO -s $MO  python3 -u temp.py $DADATA_DIR/DAFJS24 2>&1 | tee $DARESULT_DIR/DAFJS24.log
# ./runlim -r $TO -s $MO  python3 -u temp.py $DADATA_DIR/DAFJS25 2>&1 | tee $DARESULT_DIR/DAFJS25.log
# ./runlim -r $TO -s $MO  python3 -u temp.py $DADATA_DIR/DAFJS26 2>&1 | tee $DARESULT_DIR/DAFJS26.log
# ./runlim -r $TO -s $MO  python3 -u temp.py $DADATA_DIR/DAFJS27 2>&1 | tee $DARESULT_DIR/DAFJS27.log
# ./runlim -r $TO -s $MO  python3 -u temp.py $DADATA_DIR/DAFJS28 2>&1 | tee $DARESULT_DIR/DAFJS28.log
# ./runlim -r $TO -s $MO  python3 -u temp.py $DADATA_DIR/DAFJS29 2>&1 | tee $DARESULT_DIR/DAFJS29.log
# ./runlim -r $TO -s $MO  python3 -u temp.py $DADATA_DIR/DAFJS29 2>&1 | tee $DARESULT_DIR/DAFJS29.log
# ./runlim -r $TO -s $MO  python3 -u temp.py $DADATA_DIR/DAFJS30 2>&1 | tee $DARESULT_DIR/DAFJS30.log

# ./runlim -r $TO -s $MO  python3 -u temp.py $FMJDATA_DIR/sfjs01 2>&1 | tee $FMJRESULT_DIR/sfjs01.log
# ./runlim -r $TO -s $MO  python3 -u temp.py $FMJDATA_DIR/sfjs02 2>&1 | tee $FMJRESULT_DIR/sfjs02.log
# ./runlim -r $TO -s $MO  python3 -u temp.py $FMJDATA_DIR/sfjs03 2>&1 | tee $FMJRESULT_DIR/sfjs03.log
# ./runlim -r $TO -s $MO  python3 -u temp.py $FMJDATA_DIR/sfjs04 2>&1 | tee $FMJRESULT_DIR/sfjs04.log
# ./runlim -r $TO -s $MO  python3 -u temp.py $FMJDATA_DIR/sfjs05 2>&1 | tee $FMJRESULT_DIR/sfjs05.log
# ./runlim -r $TO -s $MO  python3 -u temp.py $FMJDATA_DIR/sfjs06 2>&1 | tee $FMJRESULT_DIR/sfjs06.log
# ./runlim -r $TO -s $MO  python3 -u temp.py $FMJDATA_DIR/sfjs07 2>&1 | tee $FMJRESULT_DIR/sfjs07.log
# ./runlim -r $TO -s $MO  python3 -u temp.py $FMJDATA_DIR/sfjs08 2>&1 | tee $FMJRESULT_DIR/sfjs08.log
# ./runlim -r $TO -s $MO  python3 -u temp.py $FMJDATA_DIR/sfjs09 2>&1 | tee $FMJRESULT_DIR/sfjs09.log
# ./runlim -r $TO -s $MO  python3 -u temp.py $FMJDATA_DIR/sfjs10 2>&1 | tee $FMJRESULT_DIR/sfjs10.log
# ./runlim -r $TO -s $MO  python3 -u temp.py $FMJDATA_DIR/mfjs01 2>&1 | tee $FMJRESULT_DIR/mfjs01.log
# ./runlim -r $TO -s $MO  python3 -u temp.py $FMJDATA_DIR/mfjs02 2>&1 | tee $FMJRESULT_DIR/mfjs02.log
# ./runlim -r $TO -s $MO  python3 -u temp.py $FMJDATA_DIR/mfjs03 2>&1 | tee $FMJRESULT_DIR/mfjs03.log
# ./runlim -r $TO -s $MO  python3 -u temp.py $FMJDATA_DIR/mfjs04 2>&1 | tee $FMJRESULT_DIR/mfjs04.log
# ./runlim -r $TO -s $MO  python3 -u temp.py $FMJDATA_DIR/mfjs05 2>&1 | tee $FMJRESULT_DIR/mfjs05.log
# ./runlim -r $TO -s $MO  python3 -u temp.py $FMJDATA_DIR/mfjs06 2>&1 | tee $FMJRESULT_DIR/mfjs06.log
# ./runlim -r $TO -s $MO  python3 -u temp.py $FMJDATA_DIR/mfjs07 2>&1 | tee $FMJRESULT_DIR/mfjs07.log
# ./runlim -r $TO -s $MO  python3 -u temp.py $FMJDATA_DIR/mfjs08 2>&1 | tee $FMJRESULT_DIR/mfjs08.log
# ./runlim -r $TO -s $MO  python3 -u temp.py $FMJDATA_DIR/mfjs09 2>&1 | tee $FMJRESULT_DIR/mfjs09.log
# ./runlim -r $TO -s $MO  python3 -u temp.py $FMJDATA_DIR/mfjs10 2>&1 | tee $FMJRESULT_DIR/mfjs10.log

# ./runlim -r $TO -s $MO  python3 -u temp.py $MKDATA_DIR/MK01 2>&1 | tee $MKRESULT_DIR/MK01.log
# ./runlim -r $TO -s $MO  python3 -u temp.py $MKDATA_DIR/MK02 2>&1 | tee $MKRESULT_DIR/MK02.log
# ./runlim -r $TO -s $MO  python3 -u temp.py $MKDATA_DIR/MK03 2>&1 | tee $MKRESULT_DIR/MK03.log
# ./runlim -r $TO -s $MO  python3 -u temp.py $MKDATA_DIR/MK04 2>&1 | tee $MKRESULT_DIR/MK04.log
# ./runlim -r $TO -s $MO  python3 -u temp.py $MKDATA_DIR/MK05 2>&1 | tee $MKRESULT_DIR/MK05.log
# ./runlim -r $TO -s $MO  python3 -u temp.py $MKDATA_DIR/MK06 2>&1 | tee $MKRESULT_DIR/MK06.log
# ./runlim -r $TO -s $MO  python3 -u temp.py $MKDATA_DIR/MK07 2>&1 | tee $MKRESULT_DIR/MK07.log
# ./runlim -r $TO -s $MO  python3 -u temp.py $MKDATA_DIR/MK08 2>&1 | tee $MKRESULT_DIR/MK08.log
# ./runlim -r $TO -s $MO  python3 -u temp.py $MKDATA_DIR/MK09 2>&1 | tee $MKRESULT_DIR/MK09.log
# ./runlim -r $TO -s $MO  python3 -u temp.py $MKDATA_DIR/MK10 2>&1 | tee $MKRESULT_DIR/MK10.log
# ./runlim -r $TO -s $MO  python3 -u temp.py $MKDATA_DIR/MK11 2>&1 | tee $MKRESULT_DIR/MK11.log
./runlim -r $TO -s $MO  python3 -u temp.py $MKDATA_DIR/MK12 2>&1 | tee $MKRESULT_DIR/MK12.log
./runlim -r $TO -s $MO  python3 -u temp.py $MKDATA_DIR/MK13 2>&1 | tee $MKRESULT_DIR/MK13.log
./runlim -r $TO -s $MO  python3 -u temp.py $MKDATA_DIR/MK14 2>&1 | tee $MKRESULT_DIR/MK14.log
./runlim -r $TO -s $MO  python3 -u temp.py $MKDATA_DIR/MK15 2>&1 | tee $MKRESULT_DIR/MK15.log