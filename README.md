### Hanja Graph Project

**Author**: Pablo Estrada \< pablo (at) snu (dot) ac (dot) kr \>

This repo contains the code resulting from the Hanja Graph Project, developed
by Pablo Estrada, as a sideproject.

####Folders
* Crawlers - This is the folder containing the crawlers to download the data.
At the moment of this writting, there is just one crawler implemented.
* Formatters - This is the folder containing the small python scripts that take
the files created by the crawlers and output an acceptable graph-format file.
* Analysis - This folder contains the scripts that do analysis over the graph.
* Test_data - This folder contains some data provided for test if anyone would
just want to have the data after all the processing
    * ```graph.graphml``` - This contains the full graph, with links between hanja
    and korean words. No bipartite distinction.
    * ```hanja_list.json``` - This contains the list of hanjas as returned by the
    crawler.
    * ```words.nospace.json``` - This contains the list of korean words, as
    returned by the crawler.
    * ```korean_unip_projection.graphml``` - This file contains the projection of
    the korean words from the bipartite graph. In the current version, the edge
    weights are 1 or 2, depending on how many chinese characters are shared
    between two words.
* d3viz - This directory contains the code for the project of d3 visualization
of the data. To use this directory, it is good to keep the d3 distro up to date
by executing ```wget https://github.com/mbostock/d3/zipball/master``` in the
directory.
