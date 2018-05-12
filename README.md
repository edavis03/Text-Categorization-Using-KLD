# Text-Categorization-Using-KLD
Text Categorizer using Kullback-Leibler Distance </br>
Emily Davis

kld.py is a program to run text categorization using the
Kullback-Leibler distance measure.  It is run by the
following command:

        python kld.py [trainingfile] [testingfile] [true/false]

where
        
1. trainingfile is the name of the dataset to train our
machine on.  Where documents are represented as
a single line of text followed by a tab followed by
a classification (either 0 or 1) followed immediately
by a new line </br>
examples:
</br> </br>
I love kittens. 1 
</br>
Thought the muppets were creepy!        0
</br> </br>
        
2. testingfile is the name of the dataset that we would
like to classify.  Documents are represented in the
same way as in the training file
        
3. true/false indicates whether or not misclassified
training examples should be printed to stdout.

Several datasets (including imdb_labelled.txt,
yelp_labelled.txt, amazon_cells_labelled.txt,
yelpfirst.txt, yelpsecond.txt)
are included in the directory for testing purposes.
The files yelpfirst.txt and yelpsecond.txt are just the
yelp datafile split into the first 500 lines and the 
second 500 lines.
