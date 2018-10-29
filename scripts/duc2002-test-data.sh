if [ "$#" -eq 2 ]; then
    TGT_DIR=`pwd`
elif [ "$#" -eq 3 ]; then
    TGT_DIR=$3
else
    echo "usage: $0 DUC_UNAME DUC_PASS [OUTPUT_DIRECTORY]"
    exit
fi

[ -d $TGT_DIR ] || mkdir -p $TGT_DIR

UNAME=$1
PASS=$2
TGT_PATH="${TGT_DIR}/DUC2002_test_data.tar.gz"
echo "Writing data to directory ${TGT_PATH}"

wget -r -q --no-parent https://${UNAME}:${PASS}@www-nlpir.nist.gov/projects/duc/past_duc/duc2002/data/test/ 
mv www-nlpir.nist.gov/projects/duc/past_duc/duc2002/data/test DUC2002_test_data
tar zcvf DUC2002_test_data.tar.gz DUC2002_test_data/
rm -rf DUC2002_test_data www-nlpir.nist.gov
mv DUC2002_test_data.tar.gz $TGT_PATH
