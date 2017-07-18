#!/usr/bin/env bash

declare -A array
array[2001]="http://movie.douban.com/doulist/243020/"
array[2009]="http://movie.douban.com/doulist/226734/"
array[2010]="http://www.douban.com/doulist/226207/"
array[2011]="http://movie.douban.com/doulist/665041/"
array[2012]="http://movie.douban.com/doulist/943009/"
array[2013]="http://movie.douban.com/doulist/1765813/"
array[2014]="http://movie.douban.com/doulist/3401345/"
array[2015]="http://www.douban.com/doulist/37815319/"
array[2017]="https://www.douban.com/doulist/45837913/"
array[1000]="https://www.douban.com/doulist/37621911/?start=0&sort=seq&sub_type="


for i in "${!array[@]}"
do
  scrapy crawl douban_movie_100 -a start_url=${array[$i]} -o downloads/douban_movie_$i.csv
done


