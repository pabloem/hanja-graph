## Obtaining the synonyms training set
To generate the synonyms training set we need to follow these steps:

1. Use the graph dataset to obtain the features of each node pair
```
    $> nohup ./generate_csv_p.py hanja_unip.graphml res.csv 4
```
2. Obtain the 'zeros' in the training set
```
    $> shuf -n 1000 res.csv > training_zeros
    $> ./remove_first_three.py training_zeros ../synonyms/training_non_related.csv
``` 
3. Obtain the 'synonyms' in the training set
    * Obtain a random set of hanjas from the `res.csv` file
``` 
    $> shuf -n 1000 res.csv | awk -F "," '{print $3}' > tmp
    $> cat tmp | sort | uniq > random_hanjas.txt
``` 
    * Obtain synonyms and antonyms for these hanjas
``` 
    $> ../crawlers/anto-syno/sample_getter.py random_hanjas.txt synonyms_hanja.txt antonyms_hanja.txt
``` 
    * Get the features from these pairs of synonyms or antonyms
``` 
    $> ./generate_training_csv.py synonyms_hanja.txt res.csv ../synonyms/synonyms.csv
``` 
4. Use the result to run a classification scheme ; )


## Runing the classification script
