#!/bin/bash
for f in *.info
do

temp_file="$f""_temp"
sed 's/#/|/g' "$f" |sed 's/ Portfolio //g'|cut -f 1,2,4,5 -d'|' |sed 's/| /|/g' > $temp_file

/usr/bin/mysql  -uroot -proot@1234 -e "use mutual_funds" -e "
      LOAD DATA LOCAL INFILE '$temp_file'
      INTO TABLE funds_name_info 
      FIELDS TERMINATED BY '|' 
      OPTIONALLY ENCLOSED BY '\"' 
      LINES TERMINATED BY '\n' 
      (mfFundName,mfFundHouse, mfCode,fundType);"

done


for f in *.txt
do
temp_file="$f""_temp";

cut -f 2,3,4,5,6,7,8 -d'#' "$f" |sed 's/,//g' > $temp_file

/usr/bin/mysql  -uroot -proot@1234 -e "use mutual_funds" -e "
      LOAD DATA LOCAL INFILE '$temp_file'
      INTO TABLE  funds_portfolio_holdings
      FIELDS TERMINATED BY '#' 
      OPTIONALLY ENCLOSED BY '\"' 
      LINES TERMINATED BY '\n' 
      (mfCode,fundType,companyName,sector, quantity, value,percentage);"

done

