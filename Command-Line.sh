#!/bin/bash

pip install csvkit
wget https://adm2022.s3.amazonaws.com/instagram_profiles.zip
unzip instagram_profiles.zip
wget https://adm2022.s3.amazonaws.com/instagram_posts.zip
unzip instagram_posts.zip


cut -f 3,4,8 instagram_posts.csv > posts.csv
cut -f 2,3 instagram_profiles.csv  > profiles.csv

csvgrep -c 3 -r".{100,}" --t posts.csv | head -11 > SageMaker/top_desc.csv
csvjoin -c 2,1 SageMaker/top_desc.csv profiles.csv --left | sed  -e 's/,$/,User was not found!/' | csvcut -c 1,2,4


