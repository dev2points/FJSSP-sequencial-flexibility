TO=10800
MO=14000
YDATA_DIR=datasets/yfjs
DADATA_DIR=datasets/dafjs
MKDATA_DIR=datasets/brandimarte
DPDATA_DIR=datasets/dauzere
HUEDATA_DIR=datasets/hurink/edata
HURDATA_DIR=datasets/hurink/rdata
HUVDATA_DIR=datasets/hurink/vdata
YRESULT_DIR=results/main/yfjs
DARESULT_DIR=results/test/dafjs
MKRESULT_DIR=results/main/mk
DPRESULT_DIR=results/main/dauzere
HUERESULT_DIR=results/vm/test/edata
HURRESULT_DIR=results/vm/test/rdata
HUVRESULT_DIR=results/vm/test/vdata


# mkdir -p $YRESULT_DIR
mkdir -p $DARESULT_DIR
# mkdir -p $MKRESULT_DIR
# mkdir -p $DPRESULT_DIR
# mkdir -p $HUERESULT_DIR
# mkdir -p $HURRESULT_DIR
# mkdir -p $HUVRESULT_DIR

./runlim -r $TO -s $MO  python3 -u main.py 1 $DADATA_DIR/DAFJS09 2>&1 | tee $DARESULT_DIR/DAFJS09_1.log
./runlim -r $TO -s $MO  python3 -u main.py 0 $DADATA_DIR/DAFJS09 2>&1 | tee $DARESULT_DIR/DAFJS09_0.log
./runlim -r $TO -s $MO  python3 -u main.py 1 $DADATA_DIR/DAFJS29 2>&1 | tee $DARESULT_DIR/DAFJS29_1.log
./runlim -r $TO -s $MO  python3 -u main.py 0 $DADATA_DIR/DAFJS29 2>&1 | tee $DARESULT_DIR/DAFJS29_0.log

# ./runlim -r $TO -s $MO  python3 -u main.py $YDATA_DIR/YFJS01 2>&1 | tee $YRESULT_DIR/YFJS01.log
# ./runlim -r $TO -s $MO  python3 -u main.py $YDATA_DIR/YFJS02 2>&1 | tee $YRESULT_DIR/YFJS02.log
# ./runlim -r $TO -s $MO  python3 -u main.py $YDATA_DIR/YFJS03 2>&1 | tee $YRESULT_DIR/YFJS03.log
# ./runlim -r $TO -s $MO  python3 -u main.py $YDATA_DIR/YFJS04 2>&1 | tee $YRESULT_DIR/YFJS04.log 
# ./runlim -r $TO -s $MO  python3 -u main.py $YDATA_DIR/YFJS05 2>&1 | tee $YRESULT_DIR/YFJS05.log
# ./runlim -r $TO -s $MO  python3 -u main.py $YDATA_DIR/YFJS06 2>&1 | tee $YRESULT_DIR/YFJS06.log 
# ./runlim -r $TO -s $MO  python3 -u main.py $YDATA_DIR/YFJS07 2>&1 | tee $YRESULT_DIR/YFJS07.log
# ./runlim -r $TO -s $MO  python3 -u main.py $YDATA_DIR/YFJS08 2>&1 | tee $YRESULT_DIR/YFJS08.log
# ./runlim -r $TO -s $MO  python3 -u main.py $YDATA_DIR/YFJS09 2>&1 | tee $YRESULT_DIR/YFJS09.log
# ./runlim -r $TO -s $MO  python3 -u main.py $YDATA_DIR/YFJS10 2>&1 | tee $YRESULT_DIR/YFJS10.log
# ./runlim -r $TO -s $MO  python3 -u main.py $YDATA_DIR/YFJS11 2>&1 | tee $YRESULT_DIR/YFJS11.log
# ./runlim -r $TO -s $MO  python3 -u main.py $YDATA_DIR/YFJS12 2>&1 | tee $YRESULT_DIR/YFJS12.log
# ./runlim -r $TO -s $MO  python3 -u main.py $YDATA_DIR/YFJS13 2>&1 | tee $YRESULT_DIR/YFJS13.log
# ./runlim -r $TO -s $MO  python3 -u main.py $YDATA_DIR/YFJS14 2>&1 | tee $YRESULT_DIR/YFJS14.log
# ./runlim -r $TO -s $MO  python3 -u main.py $YDATA_DIR/YFJS15 2>&1 | tee $YRESULT_DIR/YFJS15.log
# ./runlim -r $TO -s $MO  python3 -u main.py $YDATA_DIR/YFJS16 2>&1 | tee $YRESULT_DIR/YFJS16.log
# ./runlim -r $TO -s $MO  python3 -u main.py $YDATA_DIR/YFJS17 2>&1 | tee $YRESULT_DIR/YFJS17.log
# ./runlim -r $TO -s $MO  python3 -u main.py $YDATA_DIR/YFJS18 2>&1 | tee $YRESULT_DIR/YFJS18.log
# ./runlim -r $TO -s $MO  python3 -u main.py $YDATA_DIR/YFJS19 2>&1 | tee $YRESULT_DIR/YFJS19.log
# ./runlim -r $TO -s $MO  python3 -u main.py $YDATA_DIR/YFJS20 2>&1 | tee $YRESULT_DIR/YFJS20.log

# ./runlim -r $TO -s $MO  python3 -u main.py $DADATA_DIR/DAFJS01 2>&1 | tee $DARESULT_DIR/DAFJS01.log
# ./runlim -r $TO -s $MO  python3 -u main.py $DADATA_DIR/DAFJS02 2>&1 | tee $DARESULT_DIR/DAFJS02.log
# ./runlim -r $TO -s $MO  python3 -u main.py $DADATA_DIR/DAFJS03 2>&1 | tee $DARESULT_DIR/DAFJS03.log
# ./runlim -r $TO -s $MO  python3 -u main.py $DADATA_DIR/DAFJS04 2>&1 | tee $DARESULT_DIR/DAFJS04.log
# ./runlim -r $TO -s $MO  python3 -u main.py $DADATA_DIR/DAFJS05 2>&1 | tee $DARESULT_DIR/DAFJS05.log
# ./runlim -r $TO -s $MO  python3 -u main.py $DADATA_DIR/DAFJS06 2>&1 | tee $DARESULT_DIR/DAFJS06.log
# ./runlim -r $TO -s $MO  python3 -u main.py $DADATA_DIR/DAFJS07 2>&1 | tee $DARESULT_DIR/DAFJS07.log
# ./runlim -r $TO -s $MO  python3 -u main.py $DADATA_DIR/DAFJS08 2>&1 | tee $DARESULT_DIR/DAFJS08.log
# ./runlim -r $TO -s $MO  python3 -u main.py $DADATA_DIR/DAFJS09 2>&1 | tee $DARESULT_DIR/DAFJS09.log
# ./runlim -r $TO -s $MO  python3 -u main.py $DADATA_DIR/DAFJS10 2>&1 | tee $DARESULT_DIR/DAFJS10.log
# ./runlim -r $TO -s $MO  python3 -u main.py $DADATA_DIR/DAFJS11 2>&1 | tee $DARESULT_DIR/DAFJS11.log
# ./runlim -r $TO -s $MO  python3 -u main.py $DADATA_DIR/DAFJS12 2>&1 | tee $DARESULT_DIR/DAFJS12.log
# ./runlim -r $TO -s $MO  python3 -u main.py $DADATA_DIR/DAFJS13 2>&1 | tee $DARESULT_DIR/DAFJS13.log
# ./runlim -r $TO -s $MO  python3 -u main.py $DADATA_DIR/DAFJS14 2>&1 | tee $DARESULT_DIR/DAFJS14.log
# ./runlim -r $TO -s $MO  python3 -u main.py $DADATA_DIR/DAFJS15 2>&1 | tee $DARESULT_DIR/DAFJS15.log
# ./runlim -r $TO -s $MO  python3 -u main.py $DADATA_DIR/DAFJS16 2>&1 | tee $DARESULT_DIR/DAFJS16.log
# ./runlim -r $TO -s $MO  python3 -u main.py $DADATA_DIR/DAFJS17 2>&1 | tee $DARESULT_DIR/DAFJS17.log
# ./runlim -r $TO -s $MO  python3 -u main.py $DADATA_DIR/DAFJS18 2>&1 | tee $DARESULT_DIR/DAFJS18.log
# ./runlim -r $TO -s $MO  python3 -u main.py $DADATA_DIR/DAFJS19 2>&1 | tee $DARESULT_DIR/DAFJS19.log
# ./runlim -r $TO -s $MO  python3 -u main.py $DADATA_DIR/DAFJS20 2>&1 | tee $DARESULT_DIR/DAFJS20.log
# ./runlim -r $TO -s $MO  python3 -u main.py $DADATA_DIR/DAFJS21 2>&1 | tee $DARESULT_DIR/DAFJS21.log
# ./runlim -r $TO -s $MO  python3 -u main.py $DADATA_DIR/DAFJS22 2>&1 | tee $DARESULT_DIR/DAFJS22.log
# ./runlim -r $TO -s $MO  python3 -u main.py $DADATA_DIR/DAFJS23 2>&1 | tee $DARESULT_DIR/DAFJS23.log
# ./runlim -r $TO -s $MO  python3 -u main.py $DADATA_DIR/DAFJS24 2>&1 | tee $DARESULT_DIR/DAFJS24.log
# ./runlim -r $TO -s $MO  python3 -u main.py $DADATA_DIR/DAFJS25 2>&1 | tee $DARESULT_DIR/DAFJS25.log
# ./runlim -r $TO -s $MO  python3 -u main.py $DADATA_DIR/DAFJS26 2>&1 | tee $DARESULT_DIR/DAFJS26.log
# ./runlim -r $TO -s $MO  python3 -u main.py $DADATA_DIR/DAFJS27 2>&1 | tee $DARESULT_DIR/DAFJS27.log
# ./runlim -r $TO -s $MO  python3 -u main.py $DADATA_DIR/DAFJS28 2>&1 | tee $DARESULT_DIR/DAFJS28.log
# ./runlim -r $TO -s $MO  python3 -u main.py $DADATA_DIR/DAFJS29 2>&1 | tee $DARESULT_DIR/DAFJS29.log
# ./runlim -r $TO -s $MO  python3 -u main.py $DADATA_DIR/DAFJS30 2>&1 | tee $DARESULT_DIR/DAFJS30.log

# ./runlim -r $TO -s $MO  python3 -u main.py $MKDATA_DIR/MK01 2>&1 | tee $MKRESULT_DIR/MK01.log
# ./runlim -r $TO -s $MO  python3 -u main.py $MKDATA_DIR/MK02 2>&1 | tee $MKRESULT_DIR/MK02.log
# ./runlim -r $TO -s $MO  python3 -u main.py $MKDATA_DIR/MK03 2>&1 | tee $MKRESULT_DIR/MK03.log
# ./runlim -r $TO -s $MO  python3 -u main.py $MKDATA_DIR/MK04 2>&1 | tee $MKRESULT_DIR/MK04.log
# ./runlim -r $TO -s $MO  python3 -u main.py $MKDATA_DIR/MK05 2>&1 | tee $MKRESULT_DIR/MK05.log
# ./runlim -r $TO -s $MO  python3 -u main.py $MKDATA_DIR/MK06 2>&1 | tee $MKRESULT_DIR/MK06.log
# ./runlim -r $TO -s $MO  python3 -u main.py $MKDATA_DIR/MK07 2>&1 | tee $MKRESULT_DIR/MK07.log
# ./runlim -r $TO -s $MO  python3 -u main.py $MKDATA_DIR/MK08 2>&1 | tee $MKRESULT_DIR/MK08.log
# ./runlim -r $TO -s $MO  python3 -u main.py $MKDATA_DIR/MK09 2>&1 | tee $MKRESULT_DIR/MK09.log
# ./runlim -r $TO -s $MO  python3 -u main.py $MKDATA_DIR/MK10 2>&1 | tee $MKRESULT_DIR/MK10.log
# ./runlim -r $TO -s $MO  python3 -u main.py $MKDATA_DIR/MK11 2>&1 | tee $MKRESULT_DIR/MK11.log
# ./runlim -r $TO -s $MO  python3 -u main.py $MKDATA_DIR/MK12 2>&1 | tee $MKRESULT_DIR/MK12.log
# ./runlim -r $TO -s $MO  python3 -u main.py $MKDATA_DIR/MK13 2>&1 | tee $MKRESULT_DIR/MK13.log
# ./runlim -r $TO -s $MO  python3 -u main.py $MKDATA_DIR/MK14 2>&1 | tee $MKRESULT_DIR/MK14.log
# ./runlim -r $TO -s $MO  python3 -u main.py $MKDATA_DIR/MK15 2>&1 | tee $MKRESULT_DIR/MK15.log


# ./runlim -r $TO -s $MO  python3 -u main.py $DPDATA_DIR/01a.txt 2>&1 | tee $DPRESULT_DIR/01a.log
# ./runlim -r $TO -s $MO  python3 -u main.py $DPDATA_DIR/02a.txt 2>&1 | tee $DPRESULT_DIR/02a.log
# ./runlim -r $TO -s $MO  python3 -u main.py $DPDATA_DIR/03a.txt 2>&1 | tee $DPRESULT_DIR/03a.log
# ./runlim -r $TO -s $MO  python3 -u main.py $DPDATA_DIR/04a.txt 2>&1 | tee $DPRESULT_DIR/04a.log
# ./runlim -r $TO -s $MO  python3 -u main.py $DPDATA_DIR/05a.txt 2>&1 | tee $DPRESULT_DIR/05a.log
# ./runlim -r $TO -s $MO  python3 -u main.py $DPDATA_DIR/06a.txt 2>&1 | tee $DPRESULT_DIR/06a.log
# ./runlim -r $TO -s $MO  python3 -u main.py $DPDATA_DIR/07a.txt 2>&1 | tee $DPRESULT_DIR/07a.log
# ./runlim -r $TO -s $MO  python3 -u main.py $DPDATA_DIR/08a.txt 2>&1 | tee $DPRESULT_DIR/08a.log
# ./runlim -r $TO -s $MO  python3 -u main.py $DPDATA_DIR/09a.txt 2>&1 | tee $DPRESULT_DIR/09a.log
# ./runlim -r $TO -s $MO  python3 -u main.py $DPDATA_DIR/10a.txt 2>&1 | tee $DPRESULT_DIR/10a.log
# ./runlim -r $TO -s $MO  python3 -u main.py $DPDATA_DIR/11a.txt 2>&1 | tee $DPRESULT_DIR/11a.log
# ./runlim -r $TO -s $MO  python3 -u main.py $DPDATA_DIR/12a.txt 2>&1 | tee $DPRESULT_DIR/12a.log
# ./runlim -r $TO -s $MO  python3 -u main.py $DPDATA_DIR/13a.txt 2>&1 | tee $DPRESULT_DIR/13a.log
# ./runlim -r $TO -s $MO  python3 -u main.py $DPDATA_DIR/14a.txt 2>&1 | tee $DPRESULT_DIR/14a.log
# ./runlim -r $TO -s $MO  python3 -u main.py $DPDATA_DIR/15a.txt 2>&1 | tee $DPRESULT_DIR/15a.log
# ./runlim -r $TO -s $MO  python3 -u main.py $DPDATA_DIR/16a.txt 2>&1 | tee $DPRESULT_DIR/16a.log
# ./runlim -r $TO -s $MO  python3 -u main.py $DPDATA_DIR/17a.txt 2>&1 | tee $DPRESULT_DIR/17a.log
# ./runlim -r $TO -s $MO  python3 -u main.py $DPDATA_DIR/18a.txt 2>&1 | tee $DPRESULT_DIR/18a.log


# ./runlim -r $TO -s $MO  python3 -u main.py $HUEDATA_DIR/abz5.txt 2>&1 | tee $HUERESULT_DIR/abz5.log
# ./runlim -r $TO -s $MO  python3 -u main.py $HUEDATA_DIR/abz6.txt 2>&1 | tee $HUERESULT_DIR/abz6.log
# ./runlim -r $TO -s $MO  python3 -u main.py $HUEDATA_DIR/abz7.txt 2>&1 | tee $HUERESULT_DIR/abz7.log
# ./runlim -r $TO -s $MO  python3 -u main.py $HUEDATA_DIR/abz8.txt 2>&1 | tee $HUERESULT_DIR/abz8.log
# ./runlim -r $TO -s $MO  python3 -u main.py $HUEDATA_DIR/abz9.txt 2>&1 | tee $HUERESULT_DIR/abz9.log
# ./runlim -r $TO -s $MO  python3 -u main.py $HUEDATA_DIR/car1.txt 2>&1 | tee $HUERESULT_DIR/car1.log
# ./runlim -r $TO -s $MO  python3 -u main.py $HUEDATA_DIR/car2.txt 2>&1 | tee $HUERESULT_DIR/car2.log
# ./runlim -r $TO -s $MO  python3 -u main.py $HUEDATA_DIR/car3.txt 2>&1 | tee $HUERESULT_DIR/car3.log
# ./runlim -r $TO -s $MO  python3 -u main.py $HUEDATA_DIR/car4.txt 2>&1 | tee $HUERESULT_DIR/car4.log
# ./runlim -r $TO -s $MO  python3 -u main.py $HUEDATA_DIR/car5.txt 2>&1 | tee $HUERESULT_DIR/car5.log
# ./runlim -r $TO -s $MO  python3 -u main.py $HUEDATA_DIR/car6.txt 2>&1 | tee $HUERESULT_DIR/car6.log
# ./runlim -r $TO -s $MO  python3 -u main.py $HUEDATA_DIR/car7.txt 2>&1 | tee $HUERESULT_DIR/car7.log
# ./runlim -r $TO -s $MO  python3 -u main.py $HUEDATA_DIR/car8.txt 2>&1 | tee $HUERESULT_DIR/car8.log
# ./runlim -r $TO -s $MO  python3 -u main.py $HUEDATA_DIR/la01.txt 2>&1 | tee $HUERESULT_DIR/la01.log
# ./runlim -r $TO -s $MO  python3 -u main.py $HUEDATA_DIR/la02.txt 2>&1 | tee $HUERESULT_DIR/la02.log
# ./runlim -r $TO -s $MO  python3 -u main.py $HUEDATA_DIR/la03.txt 2>&1 | tee $HUERESULT_DIR/la03.log
# ./runlim -r $TO -s $MO  python3 -u main.py $HUEDATA_DIR/la04.txt 2>&1 | tee $HUERESULT_DIR/la04.log
# ./runlim -r $TO -s $MO  python3 -u main.py $HUEDATA_DIR/la05.txt 2>&1 | tee $HUERESULT_DIR/la05.log
# ./runlim -r $TO -s $MO  python3 -u main.py $HUEDATA_DIR/la06.txt 2>&1 | tee $HUERESULT_DIR/la06.log
# ./runlim -r $TO -s $MO  python3 -u main.py $HUEDATA_DIR/la07.txt 2>&1 | tee $HUERESULT_DIR/la07.log
# ./runlim -r $TO -s $MO  python3 -u main.py $HUEDATA_DIR/la08.txt 2>&1 | tee $HUERESULT_DIR/la08.log
# ./runlim -r $TO -s $MO  python3 -u main.py $HUEDATA_DIR/la09.txt 2>&1 | tee $HUERESULT_DIR/la09.log
# ./runlim -r $TO -s $MO  python3 -u main.py $HUEDATA_DIR/la10.txt 2>&1 | tee $HUERESULT_DIR/la10.log
# ./runlim -r $TO -s $MO  python3 -u main.py $HUEDATA_DIR/la11.txt 2>&1 | tee $HUERESULT_DIR/la11.log
# ./runlim -r $TO -s $MO  python3 -u main.py $HUEDATA_DIR/la12.txt 2>&1 | tee $HUERESULT_DIR/la12.log
# ./runlim -r $TO -s $MO  python3 -u main.py $HUEDATA_DIR/la13.txt 2>&1 | tee $HUERESULT_DIR/la13.log
# ./runlim -r $TO -s $MO  python3 -u main.py $HUEDATA_DIR/la14.txt 2>&1 | tee $HUERESULT_DIR/la14.log
# ./runlim -r $TO -s $MO  python3 -u main.py $HUEDATA_DIR/la15.txt 2>&1 | tee $HUERESULT_DIR/la15.log
# ./runlim -r $TO -s $MO  python3 -u main.py $HUEDATA_DIR/la16.txt 2>&1 | tee $HUERESULT_DIR/la16.log
# ./runlim -r $TO -s $MO  python3 -u main.py $HUEDATA_DIR/la17.txt 2>&1 | tee $HUERESULT_DIR/la17.log
# ./runlim -r $TO -s $MO  python3 -u main.py $HUEDATA_DIR/la18.txt 2>&1 | tee $HUERESULT_DIR/la18.log
# ./runlim -r $TO -s $MO  python3 -u main.py $HUEDATA_DIR/la19.txt 2>&1 | tee $HUERESULT_DIR/la19.log
# ./runlim -r $TO -s $MO  python3 -u main.py $HUEDATA_DIR/la20.txt 2>&1 | tee $HUERESULT_DIR/la20.log   
# ./runlim -r $TO -s $MO  python3 -u main.py $HUEDATA_DIR/la21.txt 2>&1 | tee $HUERESULT_DIR/la21.log
# ./runlim -r $TO -s $MO  python3 -u main.py $HUEDATA_DIR/la22.txt 2>&1 | tee $HUERESULT_DIR/la22.log
# ./runlim -r $TO -s $MO  python3 -u main.py $HUEDATA_DIR/la23.txt 2>&1 | tee $HUERESULT_DIR/la23.log
# ./runlim -r $TO -s $MO  python3 -u main.py $HUEDATA_DIR/la24.txt 2>&1 | tee $HUERESULT_DIR/la24.log
# ./runlim -r $TO -s $MO  python3 -u main.py $HUEDATA_DIR/la25.txt 2>&1 | tee $HUERESULT_DIR/la25.log
# ./runlim -r $TO -s $MO  python3 -u main.py $HUEDATA_DIR/la26.txt 2>&1 | tee $HUERESULT_DIR/la26.log
# ./runlim -r $TO -s $MO  python3 -u main.py $HUEDATA_DIR/la27.txt 2>&1 | tee $HUERESULT_DIR/la27.log
# ./runlim -r $TO -s $MO  python3 -u main.py $HUEDATA_DIR/la28.txt 2>&1 | tee $HUERESULT_DIR/la28.log   
# ./runlim -r $TO -s $MO  python3 -u main.py $HUEDATA_DIR/la29.txt 2>&1 | tee $HUERESULT_DIR/la29.log
# ./runlim -r $TO -s $MO  python3 -u main.py $HUEDATA_DIR/la30.txt 2>&1 | tee $HUERESULT_DIR/la30.log
# ./runlim -r $TO -s $MO  python3 -u main.py $HUEDATA_DIR/la31.txt 2>&1 | tee $HUERESULT_DIR/la31.log
# ./runlim -r $TO -s $MO  python3 -u main.py $HUEDATA_DIR/la32.txt 2>&1 | tee $HUERESULT_DIR/la32.log
# ./runlim -r $TO -s $MO  python3 -u main.py $HUEDATA_DIR/la33.txt 2>&1 | tee $HUERESULT_DIR/la33.log
# ./runlim -r $TO -s $MO  python3 -u main.py $HUEDATA_DIR/la34.txt 2>&1 | tee $HUERESULT_DIR/la34.log
# ./runlim -r $TO -s $MO  python3 -u main.py $HUEDATA_DIR/la35.txt 2>&1 | tee $HUERESULT_DIR/la35.log
# ./runlim -r $TO -s $MO  python3 -u main.py $HUEDATA_DIR/la36.txt 2>&1 | tee $HUERESULT_DIR/la36.log
# ./runlim -r $TO -s $MO  python3 -u main.py $HUEDATA_DIR/la37.txt 2>&1 | tee $HUERESULT_DIR/la37.log
# ./runlim -r $TO -s $MO  python3 -u main.py $HUEDATA_DIR/la38.txt 2>&1 | tee $HUERESULT_DIR/la38.log
# ./runlim -r $TO -s $MO  python3 -u main.py $HUEDATA_DIR/la39.txt 2>&1 | tee $HUERESULT_DIR/la39.log
# ./runlim -r $TO -s $MO  python3 -u main.py $HUEDATA_DIR/la40.txt 2>&1 | tee $HUERESULT_DIR/la40.log
# ./runlim -r $TO -s $MO  python3 -u main.py $HUEDATA_DIR/mt06.txt 2>&1 | tee $HUERESULT_DIR/mt06.log
# ./runlim -r $TO -s $MO  python3 -u main.py $HUEDATA_DIR/mt10.txt 2>&1 | tee $HUERESULT_DIR/mt10.log
# ./runlim -r $TO -s $MO  python3 -u main.py $HUEDATA_DIR/mt20.txt 2>&1 | tee $HUERESULT_DIR/mt20.log
# ./runlim -r $TO -s $MO  python3 -u main.py $HUEDATA_DIR/orb1.txt 2>&1 | tee $HUERESULT_DIR/orb1.log
# ./runlim -r $TO -s $MO  python3 -u main.py $HUEDATA_DIR/orb2.txt 2>&1 | tee $HUERESULT_DIR/orb2.log
# ./runlim -r $TO -s $MO  python3 -u main.py $HUEDATA_DIR/orb3.txt 2>&1 | tee $HUERESULT_DIR/orb3.log
# ./runlim -r $TO -s $MO  python3 -u main.py $HUEDATA_DIR/orb4.txt 2>&1 | tee $HUERESULT_DIR/orb4.log
# ./runlim -r $TO -s $MO  python3 -u main.py $HUEDATA_DIR/orb5.txt 2>&1 | tee $HUERESULT_DIR/orb5.log
# ./runlim -r $TO -s $MO  python3 -u main.py $HUEDATA_DIR/orb6.txt 2>&1 | tee $HUERESULT_DIR/orb6.log
# ./runlim -r $TO -s $MO  python3 -u main.py $HUEDATA_DIR/orb7.txt 2>&1 | tee $HUERESULT_DIR/orb7.log
# ./runlim -r $TO -s $MO  python3 -u main.py $HUEDATA_DIR/orb8.txt 2>&1 | tee $HUERESULT_DIR/orb8.log
# ./runlim -r $TO -s $MO  python3 -u main.py $HUEDATA_DIR/orb9.txt 2>&1 | tee $HUERESULT_DIR/orb9.log
# ./runlim -r $TO -s $MO  python3 -u main.py $HUEDATA_DIR/orb10.txt 2>&1 | tee $HUERESULT_DIR/orb10.log


# ./runlim -r $TO -s $MO  python3 -u main.py $HURDATA_DIR/abz5.txt 2>&1 | tee $HURRESULT_DIR/abz5.log
# ./runlim -r $TO -s $MO  python3 -u main.py $HURDATA_DIR/abz6.txt 2>&1 | tee $HURRESULT_DIR/abz6.log
# ./runlim -r $TO -s $MO  python3 -u main.py $HURDATA_DIR/abz7.txt 2>&1 | tee $HURRESULT_DIR/abz7.log
# ./runlim -r $TO -s $MO  python3 -u main.py $HURDATA_DIR/abz8.txt 2>&1 | tee $HURRESULT_DIR/abz8.log
# ./runlim -r $TO -s $MO  python3 -u main.py $HURDATA_DIR/abz9.txt 2>&1 | tee $HURRESULT_DIR/abz9.log
# ./runlim -r $TO -s $MO  python3 -u main.py $HURDATA_DIR/car1.txt 2>&1 | tee $HURRESULT_DIR/car1.log
# ./runlim -r $TO -s $MO  python3 -u main.py $HURDATA_DIR/car2.txt 2>&1 | tee $HURRESULT_DIR/car2.log
# ./runlim -r $TO -s $MO  python3 -u main.py $HURDATA_DIR/car3.txt 2>&1 | tee $HURRESULT_DIR/car3.log
# ./runlim -r $TO -s $MO  python3 -u main.py $HURDATA_DIR/car4.txt 2>&1 | tee $HURRESULT_DIR/car4.log
# ./runlim -r $TO -s $MO  python3 -u main.py $HURDATA_DIR/car5.txt 2>&1 | tee $HURRESULT_DIR/car5.log
# ./runlim -r $TO -s $MO  python3 -u main.py $HURDATA_DIR/car6.txt 2>&1 | tee $HURRESULT_DIR/car6.log
# ./runlim -r $TO -s $MO  python3 -u main.py $HURDATA_DIR/car7.txt 2>&1 | tee $HURRESULT_DIR/car7.log
# ./runlim -r $TO -s $MO  python3 -u main.py $HURDATA_DIR/car8.txt 2>&1 | tee $HURRESULT_DIR/car8.log
# ./runlim -r $TO -s $MO  python3 -u main.py $HURDATA_DIR/la01.txt 2>&1 | tee $HURRESULT_DIR/la01.log
# ./runlim -r $TO -s $MO  python3 -u main.py $HURDATA_DIR/la02.txt 2>&1 | tee $HURRESULT_DIR/la02.log
# ./runlim -r $TO -s $MO  python3 -u main.py $HURDATA_DIR/la03.txt 2>&1 | tee $HURRESULT_DIR/la03.log
# ./runlim -r $TO -s $MO  python3 -u main.py $HURDATA_DIR/la04.txt 2>&1 | tee $HURRESULT_DIR/la04.log
# ./runlim -r $TO -s $MO  python3 -u main.py $HURDATA_DIR/la05.txt 2>&1 | tee $HURRESULT_DIR/la05.log
# ./runlim -r $TO -s $MO  python3 -u main.py $HURDATA_DIR/la06.txt 2>&1 | tee $HURRESULT_DIR/la06.log
# ./runlim -r $TO -s $MO  python3 -u main.py $HURDATA_DIR/la07.txt 2>&1 | tee $HURRESULT_DIR/la07.log
# ./runlim -r $TO -s $MO  python3 -u main.py $HURDATA_DIR/la08.txt 2>&1 | tee $HURRESULT_DIR/la08.log
# ./runlim -r $TO -s $MO  python3 -u main.py $HURDATA_DIR/la09.txt 2>&1 | tee $HURRESULT_DIR/la09.log
# ./runlim -r $TO -s $MO  python3 -u main.py $HURDATA_DIR/la10.txt 2>&1 | tee $HURRESULT_DIR/la10.log
# ./runlim -r $TO -s $MO  python3 -u main.py $HURDATA_DIR/la11.txt 2>&1 | tee $HURRESULT_DIR/la11.log
# ./runlim -r $TO -s $MO  python3 -u main.py $HURDATA_DIR/la12.txt 2>&1 | tee $HURRESULT_DIR/la12.log
# ./runlim -r $TO -s $MO  python3 -u main.py $HURDATA_DIR/la13.txt 2>&1 | tee $HURRESULT_DIR/la13.log
# ./runlim -r $TO -s $MO  python3 -u main.py $HURDATA_DIR/la14.txt 2>&1 | tee $HURRESULT_DIR/la14.log
# ./runlim -r $TO -s $MO  python3 -u main.py $HURDATA_DIR/la15.txt 2>&1 | tee $HURRESULT_DIR/la15.log
# ./runlim -r $TO -s $MO  python3 -u main.py $HURDATA_DIR/la16.txt 2>&1 | tee $HURRESULT_DIR/la16.log
# ./runlim -r $TO -s $MO  python3 -u main.py $HURDATA_DIR/la17.txt 2>&1 | tee $HURRESULT_DIR/la17.log
# ./runlim -r $TO -s $MO  python3 -u main.py $HURDATA_DIR/la18.txt 2>&1 | tee $HURRESULT_DIR/la18.log
# ./runlim -r $TO -s $MO  python3 -u main.py $HURDATA_DIR/la19.txt 2>&1 | tee $HURRESULT_DIR/la19.log
# ./runlim -r $TO -s $MO  python3 -u main.py $HURDATA_DIR/la20.txt 2>&1 | tee $HURRESULT_DIR/la20.log   
# ./runlim -r $TO -s $MO  python3 -u main.py $HURDATA_DIR/la21.txt 2>&1 | tee $HURRESULT_DIR/la21.log
# ./runlim -r $TO -s $MO  python3 -u main.py $HURDATA_DIR/la22.txt 2>&1 | tee $HURRESULT_DIR/la22.log
# ./runlim -r $TO -s $MO  python3 -u main.py $HURDATA_DIR/la23.txt 2>&1 | tee $HURRESULT_DIR/la23.log
# ./runlim -r $TO -s $MO  python3 -u main.py $HURDATA_DIR/la24.txt 2>&1 | tee $HURRESULT_DIR/la24.log
# ./runlim -r $TO -s $MO  python3 -u main.py $HURDATA_DIR/la25.txt 2>&1 | tee $HURRESULT_DIR/la25.log
# ./runlim -r $TO -s $MO  python3 -u main.py $HURDATA_DIR/la26.txt 2>&1 | tee $HURRESULT_DIR/la26.log
# ./runlim -r $TO -s $MO  python3 -u main.py $HURDATA_DIR/la27.txt 2>&1 | tee $HURRESULT_DIR/la27.log
# ./runlim -r $TO -s $MO  python3 -u main.py $HURDATA_DIR/la28.txt 2>&1 | tee $HURRESULT_DIR/la28.log   
# ./runlim -r $TO -s $MO  python3 -u main.py $HURDATA_DIR/la29.txt 2>&1 | tee $HURRESULT_DIR/la29.log
# ./runlim -r $TO -s $MO  python3 -u main.py $HURDATA_DIR/la30.txt 2>&1 | tee $HURRESULT_DIR/la30.log
# ./runlim -r $TO -s $MO  python3 -u main.py $HURDATA_DIR/la31.txt 2>&1 | tee $HURRESULT_DIR/la31.log
# ./runlim -r $TO -s $MO  python3 -u main.py $HURDATA_DIR/la32.txt 2>&1 | tee $HURRESULT_DIR/la32.log
# ./runlim -r $TO -s $MO  python3 -u main.py $HURDATA_DIR/la33.txt 2>&1 | tee $HURRESULT_DIR/la33.log
# ./runlim -r $TO -s $MO  python3 -u main.py $HURDATA_DIR/la34.txt 2>&1 | tee $HURRESULT_DIR/la34.log
# ./runlim -r $TO -s $MO  python3 -u main.py $HURDATA_DIR/la35.txt 2>&1 | tee $HURRESULT_DIR/la35.log
# ./runlim -r $TO -s $MO  python3 -u main.py $HURDATA_DIR/la36.txt 2>&1 | tee $HURRESULT_DIR/la36.log
# ./runlim -r $TO -s $MO  python3 -u main.py $HURDATA_DIR/la37.txt 2>&1 | tee $HURRESULT_DIR/la37.log
# ./runlim -r $TO -s $MO  python3 -u main.py $HURDATA_DIR/la38.txt 2>&1 | tee $HURRESULT_DIR/la38.log
# ./runlim -r $TO -s $MO  python3 -u main.py $HURDATA_DIR/la39.txt 2>&1 | tee $HURRESULT_DIR/la39.log
# ./runlim -r $TO -s $MO  python3 -u main.py $HURDATA_DIR/la40.txt 2>&1 | tee $HURRESULT_DIR/la40.log
# ./runlim -r $TO -s $MO  python3 -u main.py $HURDATA_DIR/mt06.txt 2>&1 | tee $HURRESULT_DIR/mt06.log
# ./runlim -r $TO -s $MO  python3 -u main.py $HURDATA_DIR/mt10.txt 2>&1 | tee $HURRESULT_DIR/mt10.log
# ./runlim -r $TO -s $MO  python3 -u main.py $HURDATA_DIR/mt20.txt 2>&1 | tee $HURRESULT_DIR/mt20.log
# ./runlim -r $TO -s $MO  python3 -u main.py $HURDATA_DIR/orb1.txt 2>&1 | tee $HURRESULT_DIR/orb1.log
# ./runlim -r $TO -s $MO  python3 -u main.py $HURDATA_DIR/orb2.txt 2>&1 | tee $HURRESULT_DIR/orb2.log
# ./runlim -r $TO -s $MO  python3 -u main.py $HURDATA_DIR/orb3.txt 2>&1 | tee $HURRESULT_DIR/orb3.log
# ./runlim -r $TO -s $MO  python3 -u main.py $HURDATA_DIR/orb4.txt 2>&1 | tee $HURRESULT_DIR/orb4.log
# ./runlim -r $TO -s $MO  python3 -u main.py $HURDATA_DIR/orb5.txt 2>&1 | tee $HURRESULT_DIR/orb5.log
# ./runlim -r $TO -s $MO  python3 -u main.py $HURDATA_DIR/orb6.txt 2>&1 | tee $HURRESULT_DIR/orb6.log
# ./runlim -r $TO -s $MO  python3 -u main.py $HURDATA_DIR/orb7.txt 2>&1 | tee $HURRESULT_DIR/orb7.log
# ./runlim -r $TO -s $MO  python3 -u main.py $HURDATA_DIR/orb8.txt 2>&1 | tee $HURRESULT_DIR/orb8.log
# ./runlim -r $TO -s $MO  python3 -u main.py $HURDATA_DIR/orb9.txt 2>&1 | tee $HURRESULT_DIR/orb9.log
# ./runlim -r $TO -s $MO  python3 -u main.py $HURDATA_DIR/orb10.txt 2>&1 | tee $HURRESULT_DIR/orb10.log  


# ./runlim -r $TO -s $MO  python3 -u main.py $HUVDATA_DIR/abz5.txt 2>&1 | tee $HUVRESULT_DIR/abz5.log
# ./runlim -r $TO -s $MO  python3 -u main.py $HUVDATA_DIR/abz6.txt 2>&1 | tee $HUVRESULT_DIR/abz6.log
# ./runlim -r $TO -s $MO  python3 -u main.py $HUVDATA_DIR/abz7.txt 2>&1 | tee $HUVRESULT_DIR/abz7.log
# ./runlim -r $TO -s $MO  python3 -u main.py $HUVDATA_DIR/abz8.txt 2>&1 | tee $HUVRESULT_DIR/abz8.log
# ./runlim -r $TO -s $MO  python3 -u main.py $HUVDATA_DIR/abz9.txt 2>&1 | tee $HUVRESULT_DIR/abz9.log
# ./runlim -r $TO -s $MO  python3 -u main.py $HUVDATA_DIR/car1.txt 2>&1 | tee $HUVRESULT_DIR/car1.log
# ./runlim -r $TO -s $MO  python3 -u main.py $HUVDATA_DIR/car2.txt 2>&1 | tee $HUVRESULT_DIR/car2.log
# ./runlim -r $TO -s $MO  python3 -u main.py $HUVDATA_DIR/car3.txt 2>&1 | tee $HUVRESULT_DIR/car3.log
# ./runlim -r $TO -s $MO  python3 -u main.py $HUVDATA_DIR/car4.txt 2>&1 | tee $HUVRESULT_DIR/car4.log
# ./runlim -r $TO -s $MO  python3 -u main.py $HUVDATA_DIR/car5.txt 2>&1 | tee $HUVRESULT_DIR/car5.log
# ./runlim -r $TO -s $MO  python3 -u main.py $HUVDATA_DIR/car6.txt 2>&1 | tee $HUVRESULT_DIR/car6.log
# ./runlim -r $TO -s $MO  python3 -u main.py $HUVDATA_DIR/car7.txt 2>&1 | tee $HUVRESULT_DIR/car7.log
# ./runlim -r $TO -s $MO  python3 -u main.py $HUVDATA_DIR/car8.txt 2>&1 | tee $HUVRESULT_DIR/car8.log
# ./runlim -r $TO -s $MO  python3 -u main.py $HUVDATA_DIR/la01.txt 2>&1 | tee $HUVRESULT_DIR/la01.log
# ./runlim -r $TO -s $MO  python3 -u main.py $HUVDATA_DIR/la02.txt 2>&1 | tee $HUVRESULT_DIR/la02.log
# ./runlim -r $TO -s $MO  python3 -u main.py $HUVDATA_DIR/la03.txt 2>&1 | tee $HUVRESULT_DIR/la03.log
# ./runlim -r $TO -s $MO  python3 -u main.py $HUVDATA_DIR/la04.txt 2>&1 | tee $HUVRESULT_DIR/la04.log
# ./runlim -r $TO -s $MO  python3 -u main.py $HUVDATA_DIR/la05.txt 2>&1 | tee $HUVRESULT_DIR/la05.log
# ./runlim -r $TO -s $MO  python3 -u main.py $HUVDATA_DIR/la06.txt 2>&1 | tee $HUVRESULT_DIR/la06.log
# ./runlim -r $TO -s $MO  python3 -u main.py $HUVDATA_DIR/la07.txt 2>&1 | tee $HUVRESULT_DIR/la07.log
# ./runlim -r $TO -s $MO  python3 -u main.py $HUVDATA_DIR/la08.txt 2>&1 | tee $HUVRESULT_DIR/la08.log
# ./runlim -r $TO -s $MO  python3 -u main.py $HUVDATA_DIR/la09.txt 2>&1 | tee $HUVRESULT_DIR/la09.log
# ./runlim -r $TO -s $MO  python3 -u main.py $HUVDATA_DIR/la10.txt 2>&1 | tee $HUVRESULT_DIR/la10.log
# ./runlim -r $TO -s $MO  python3 -u main.py $HUVDATA_DIR/la11.txt 2>&1 | tee $HUVRESULT_DIR/la11.log
# ./runlim -r $TO -s $MO  python3 -u main.py $HUVDATA_DIR/la12.txt 2>&1 | tee $HUVRESULT_DIR/la12.log
# ./runlim -r $TO -s $MO  python3 -u main.py $HUVDATA_DIR/la13.txt 2>&1 | tee $HUVRESULT_DIR/la13.log
# ./runlim -r $TO -s $MO  python3 -u main.py $HUVDATA_DIR/la14.txt 2>&1 | tee $HUVRESULT_DIR/la14.log
# ./runlim -r $TO -s $MO  python3 -u main.py $HUVDATA_DIR/la15.txt 2>&1 | tee $HUVRESULT_DIR/la15.log
# ./runlim -r $TO -s $MO  python3 -u main.py $HUVDATA_DIR/la16.txt 2>&1 | tee $HUVRESULT_DIR/la16.log
# ./runlim -r $TO -s $MO  python3 -u main.py $HUVDATA_DIR/la17.txt 2>&1 | tee $HUVRESULT_DIR/la17.log
# ./runlim -r $TO -s $MO  python3 -u main.py $HUVDATA_DIR/la18.txt 2>&1 | tee $HUVRESULT_DIR/la18.log
# ./runlim -r $TO -s $MO  python3 -u main.py $HUVDATA_DIR/la19.txt 2>&1 | tee $HUVRESULT_DIR/la19.log
# ./runlim -r $TO -s $MO  python3 -u main.py $HUVDATA_DIR/la20.txt 2>&1 | tee $HUVRESULT_DIR/la20.log   
# ./runlim -r $TO -s $MO  python3 -u main.py $HUVDATA_DIR/la21.txt 2>&1 | tee $HUVRESULT_DIR/la21.log
# ./runlim -r $TO -s $MO  python3 -u main.py $HUVDATA_DIR/la22.txt 2>&1 | tee $HUVRESULT_DIR/la22.log
# ./runlim -r $TO -s $MO  python3 -u main.py $HUVDATA_DIR/la23.txt 2>&1 | tee $HUVRESULT_DIR/la23.log
# ./runlim -r $TO -s $MO  python3 -u main.py $HUVDATA_DIR/la24.txt 2>&1 | tee $HUVRESULT_DIR/la24.log
# ./runlim -r $TO -s $MO  python3 -u main.py $HUVDATA_DIR/la25.txt 2>&1 | tee $HUVRESULT_DIR/la25.log
# ./runlim -r $TO -s $MO  python3 -u main.py $HUVDATA_DIR/la26.txt 2>&1 | tee $HUVRESULT_DIR/la26.log
# ./runlim -r $TO -s $MO  python3 -u main.py $HUVDATA_DIR/la27.txt 2>&1 | tee $HUVRESULT_DIR/la27.log
# ./runlim -r $TO -s $MO  python3 -u main.py $HUVDATA_DIR/la28.txt 2>&1 | tee $HUVRESULT_DIR/la28.log   
# ./runlim -r $TO -s $MO  python3 -u main.py $HUVDATA_DIR/la29.txt 2>&1 | tee $HUVRESULT_DIR/la29.log
# ./runlim -r $TO -s $MO  python3 -u main.py $HUVDATA_DIR/la30.txt 2>&1 | tee $HUVRESULT_DIR/la30.log
# ./runlim -r $TO -s $MO  python3 -u main.py $HUVDATA_DIR/la31.txt 2>&1 | tee $HUVRESULT_DIR/la31.log
# ./runlim -r $TO -s $MO  python3 -u main.py $HUVDATA_DIR/la32.txt 2>&1 | tee $HUVRESULT_DIR/la32.log
# ./runlim -r $TO -s $MO  python3 -u main.py $HUVDATA_DIR/la33.txt 2>&1 | tee $HUVRESULT_DIR/la33.log
# ./runlim -r $TO -s $MO  python3 -u main.py $HUVDATA_DIR/la34.txt 2>&1 | tee $HUVRESULT_DIR/la34.log
# ./runlim -r $TO -s $MO  python3 -u main.py $HUVDATA_DIR/la35.txt 2>&1 | tee $HUVRESULT_DIR/la35.log
# ./runlim -r $TO -s $MO  python3 -u main.py $HUVDATA_DIR/la36.txt 2>&1 | tee $HUVRESULT_DIR/la36.log
# ./runlim -r $TO -s $MO  python3 -u main.py $HUVDATA_DIR/la37.txt 2>&1 | tee $HUVRESULT_DIR/la37.log
# ./runlim -r $TO -s $MO  python3 -u main.py $HUVDATA_DIR/la38.txt 2>&1 | tee $HUVRESULT_DIR/la38.log
# ./runlim -r $TO -s $MO  python3 -u main.py $HUVDATA_DIR/la39.txt 2>&1 | tee $HUVRESULT_DIR/la39.log
# ./runlim -r $TO -s $MO  python3 -u main.py $HUVDATA_DIR/la40.txt 2>&1 | tee $HUVRESULT_DIR/la40.log
# ./runlim -r $TO -s $MO  python3 -u main.py $HUVDATA_DIR/mt06.txt 2>&1 | tee $HUVRESULT_DIR/mt06.log
# ./runlim -r $TO -s $MO  python3 -u main.py $HUVDATA_DIR/mt10.txt 2>&1 | tee $HUVRESULT_DIR/mt10.log
# ./runlim -r $TO -s $MO  python3 -u main.py $HUVDATA_DIR/mt20.txt 2>&1 | tee $HUVRESULT_DIR/mt20.log
# ./runlim -r $TO -s $MO  python3 -u main.py $HUVDATA_DIR/orb1.txt 2>&1 | tee $HUVRESULT_DIR/orb1.log
# ./runlim -r $TO -s $MO  python3 -u main.py $HUVDATA_DIR/orb2.txt 2>&1 | tee $HUVRESULT_DIR/orb2.log
# ./runlim -r $TO -s $MO  python3 -u main.py $HUVDATA_DIR/orb3.txt 2>&1 | tee $HUVRESULT_DIR/orb3.log
# ./runlim -r $TO -s $MO  python3 -u main.py $HUVDATA_DIR/orb4.txt 2>&1 | tee $HUVRESULT_DIR/orb4.log
# ./runlim -r $TO -s $MO  python3 -u main.py $HUVDATA_DIR/orb5.txt 2>&1 | tee $HUVRESULT_DIR/orb5.log
# ./runlim -r $TO -s $MO  python3 -u main.py $HUVDATA_DIR/orb6.txt 2>&1 | tee $HUVRESULT_DIR/orb6.log
# ./runlim -r $TO -s $MO  python3 -u main.py $HUVDATA_DIR/orb7.txt 2>&1 | tee $HUVRESULT_DIR/orb7.log
# ./runlim -r $TO -s $MO  python3 -u main.py $HUVDATA_DIR/orb8.txt 2>&1 | tee $HUVRESULT_DIR/orb8.log
# ./runlim -r $TO -s $MO  python3 -u main.py $HUVDATA_DIR/orb9.txt 2>&1 | tee $HUVRESULT_DIR/orb9.log
# ./runlim -r $TO -s $MO  python3 -u main.py $HUVDATA_DIR/orb10.txt 2>&1 | tee $HUVRESULT_DIR/orb10.log  
