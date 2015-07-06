library(rjson)
library(plyr)
library(reshape2)

setwd("/home/pablo/codes/hanja/")
hanjas = fromJSON(paste(readLines("hanja_new1.json"),collapse=""))

# First we need to get the list data into a dataframe
h_meaning <-vapply(hanjas,function(x) x$meaning,hanjas[[1]][[1]])
h_radicals <-vapply(hanjas,function(x) if(!is.null(x$radicals)){x$radicals} else " ",hanjas[[1]][[1]])
h_chinese <- vapply(hanjas,function(x) x$chinese,hanjas[[1]][[1]])

hanja.df <- data.frame(chinese,radicals,meaning)

#words <- fromJSON(paste(readLines("words_order.json"),collapse=""))
words <- fromJSON(paste(readLines("words.nospace.json"),collapse=""))
chinese <- vapply(words,function(x) x$chinese, words[[1]][[1]])
korean <- vapply(words,function(x) x$korean,words[[1]][[1]])
english <- vapply(words,function(x) x$english, words[[1]][[1]])

words.df <- data.frame(chinese,korean,english)

bipartite_matrix <- matrix(nrow = length(chinese), ncol = length(h_chinese))