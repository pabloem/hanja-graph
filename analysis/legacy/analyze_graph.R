library(igraph)
library(psych)

setwd("/home/pablo/codes/hanja/")
#g <- read.graph("bipartite_graph.gexf",format="lgl")
g<-read.graph("graph_files/output_numeic_ids.graphml",format="graphml")
str(g)
summary(g)

sum(V(g)$type)

biproj = bipartite.projection(g)
summary(biproj$proj1)

write.graph(biproj$proj2,"korean_unip_projection.graphml",format="graphml")
write.graph(biproj$proj1,"projection1.graphml",format="graphml")

word_graph <- biproj$proj2

#Start observing the resulting graph of sino-korean words

#1. Plot degree distribution
hist(degree(word_graph),breaks=30)
barplot(degree.distribution(word_graph))
str(degree(word_graph))
describe(degree(word_graph))
summary(degree(word_graph))

table(E(word_graph)$weight)

