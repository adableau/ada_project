# dynamic-nmf: Dynamic Topic Modeling

### Summary

* Required: [numpy >= 1.8.0](http://www.numpy.org/)
* Required: [scikit-learn >= 0.14](http://scikit-learn.org/stable/)
* Required for utility tools: [prettytable >= 0.7.2](https://code.google.com/p/prettytable/)
* Required for automatic model selection: [gensim >= 0.10.3](https://radimrehurek.com/gensim/)

### Basic Usage



##### Step 1: Pre-processing
Before applying dynamic topic modeling, the first step is to pre-process the documents from each time window
    -o data   output data address

    python prep-text.py /home/baiqingchun/00_data/20_output_data/test/alt.atheism -o data --tfidf --norm
python document-term-matrix.py /home/baiqingchun/00_data/data_done/news20test -o data --tfidf --norm
for the cvs data

    python prep--cvs-text.py -o data --tfidf --norm

The result of this process will be a collection of Joblib binary files (*.pkl and *.npy) written to the directory 'data'

##### Step 2: Topic Modeling

    python find-window-topics.py data/month1.pkl data/month2.pkl data/month3.pkl -k 5 -o out
 python find-window-topics.py data/news20test.pkl -k 128 -o out
When the process has completed, we can view the descriptiors (i.e. the top ranked terms) for the resulting window topics as follows:

	python display-topics.py out/month1_windowtopics_k05.pkl out/month2_windowtopics_k05.pkl out/month3_windowtopics_k05.pkl
	python display-topics.py out/.pkl_windowtopics_k15.pkl out/pkl_windowtopics_k05.pkl out/month3_windowtopics_k05.pkl

The top terms and document IDs can be exported from a NMF results file to two individual comma-separated files using 'export-csv.py'. For instance, to export the top 50 terms and document IDs for a single results file:

	python export-csv.py out/month1_windowtopics_k05.pkl -t 50

##### Step 3: Evaluate the topic Model



Standard topic modeling approaches assume the order of documents does not matter, making them unsuitable for time-stamped corpora. In contrast, *dynamic topic modeling* approaches track how language changes and topics evolve over time. We have developed a two-level approach for dynamic topic modeling via Non-negative Matrix Factorization (NMF), which links together topics identified in snapshots of text sources appearing over time.

Details of this approach are described in the following paper ([Link](http://arxiv.org/abs/1607.03055)):

	Exploring the Political Agenda of the European Parliament Using a Dynamic Topic Modeling Approach
	Derek Greene, James P. Cross. Political Analysis, 2016.
	
This repository contains a Python reference implementation of the above approach.

### Dependencies
Tested with Python 2.7 and Python 3.5, and requiring the following packages, which are available via PIP:


### Basic Usage

To perform dynamic topic modeling, the input corpus of documents should consist of plain text files (one document per file), organised into two or more sub-directories. Each of these sub-directories should correspond to a unique *time window*, representing a different time interval. The names of these sub-directories is arbitrary, once their alphabetic ordering corresponds to their order in time (e.g 2000, 2001, 2002; month1, month2, month3; 2010-q1, 2010-q2, 2010-q3). 

The dynamic topic modeling process consists of three steps, discussed below. The archive 'data/sample.zip' contains a sample corpus of 1,324 news articles divided into three time windows (month1, month2, month3), which is used to illustrate these steps.

##### Step 1: Pre-processing
Before applying dynamic topic modeling, the first step is to pre-process the documents from each time window (i.e. sub-directory), to produce a *document-term matrix* for those windows. This involves tokenizing the documents, removing common stop-words, and building a document-term matrix for the time window. In the example below, we parse all .txt files in the sub-directories of 'data/sample'. The output files will be stored in the directory 'data'. Note that the final options below indicate that we want to apply TF-IDF term weighting and document length normalization to the documents before writing each matrix.

	python prep-text.py /home/baiqingchun/00_data/20_output_data/test/alt.atheism/ -o data --tfidf --norm
python prep-text.py data/sample/month1 data/sample/month2 data/sample/month3 -o data --tfidf --norm
The result of this process will be a collection of Joblib binary files (*.pkl and *.npy) written to the directory 'data', where the prefix of each corresponds to the name of each time window (e.g. month1, month2 etc).

##### Step 2: Window Topic Modeling 
Once the data has been pre-processed, the next step is to generate the *window topics*, where a topic model is created by applying NMF to each the pre-process data for each time window. For the example data, we apply it to the three months. If we want to use the same number of topics for each window (e.g. 5 topics), we can run the following, where results are written to the directory 'out':
	
	python find-window-topics.py data/month1.pkl data/month2.pkl data/month3.pkl -k 5 -o out
	python find-window-topics.py data/.pkl -k 15 -o out

python find-window-topics.py data/atheism.pkl  -k 15 -o out
When the process has completed, we can view the descriptiors (i.e. the top ranked terms) for the resulting window topics as follows:

	python display-topics.py out/month1_windowtopics_k05.pkl out/month2_windowtopics_k05.pkl out/month3_windowtopics_k05.pkl
	python display-topics.py out/.pkl_windowtopics_k15.pkl out/pkl_windowtopics_k05.pkl out/month3_windowtopics_k05.pkl

The top terms and document IDs can be exported from a NMF results file to two individual comma-separated files using 'export-csv.py'. For instance, to export the top 50 terms and document IDs for a single results file:

	python export-csv.py out/month1_windowtopics_k05.pkl -t 50
python export-csv.py out/atheism_windowtopics_k15.pkl -t 50
python find-dynamic-topics.py out/atheism_windowtopics_k15.pkl -k 5 -o out

##### Step 3: Dynamic Topic Modeling 
Once the window topics have been created, we combine the results for the time windows to generate *dynamic topics* that span across multiple time windows. If we want to specify a fixed number of dynamic topics (e.g. *k=5*), we can run the following, where results are written to the directory 'out':

	python find-dynamic-topics.py out/month1_windowtopics_k05.pkl out/month2_windowtopics_k05.pkl out/month3_windowtopics_k05.pkl -k 5 -o out
	
In this case the results will be written to 'out/dynamictopics_k05.pkl'. When the process has completed, we can view the dynamic topic descriptiors using 'display-topics.py':

	python display-topics.py out/dynamictopics_k05.pkl

For the sample corpus, the output for the top 10 terms for 5 dynamic topics should look like:

	+------+------------+-----------+------------+--------+----------+
	| Rank | D01        | D02       | D03        | D04    | D05      |
	+------+------------+-----------+------------+--------+----------+
	|    1 | blair      | chelsea   | people     | best   | growth   |
	|    2 | labour     | game      | mobile     | band   | economy  |
	|    3 | election   | club      | users      | music  | oil      |
	|    4 | government | united    | software   | film   | sales    |
	|    5 | minister   | arsenal   | microsoft  | album  | prices   |
	|    6 | brown      | league    | technology | awards | market   |
	|    7 | party      | players   | net        | show   | bank     |
	|    8 | prime      | cup       | phone      | number | economic |
	|    9 | howard     | liverpool | computer   | award  | profits  |
	|   10 | told       | football  | security   | top    | company  |
	+------+------------+-----------+------------+--------+----------+

### Advanced Usage

The examples above involve using a manually-specified number of topics, for both window topics and dynamic topics. In cases where this number is not known in advance, a variety of strategies exist for automatically or semi-automatically choosing a number of topics. This package contains an implementation of the TC-W2V *topic coherence* measure, which can be used to compare different topic models and subsequently choose a model with a suitable number of topics. More details on the TC-W2V are included in the paper:
	
	An Analysis of the Coherence of Descriptors in Topic Modeling
	D. O'Callaghan, D. Greene, J. Carthy, P. Cunningham. 
	Expert Systems with Applications (ESWA), 2015.

The approach involves a number of steps, listed below. Again these steps are illustrated using the sample corpus.

##### Step 1: Build Word2Vec Model

As well as preparing the input text corpus, we also need to build a Word2Vec model from all of the documents in our corpus. The script 'prep-word2vec.py' uses [Gensim](https://radimrehurek.com/gensim/) to build the model. All of the text files in the specified sub-directories are used to build the model, which is written to the file 'out/w2v-model.bin'.  

	python prep-word2vec.py data/sample/month1 data/sample/month2 data/sample/month3 -o out

##### Step 2: Window Topic Modeling 

Next, we use topic coherence based on the pre-built Word2Vec model to evaluate a range of different values for the number of topics *k* for each time window. We use the same 'find-window-topics.py' script, but specify a comma-separated range of values to try *(kmin,kmax)* (e.g. 4,10 will test all numbers of topics from *k=4* to *k=10*), and also specify the path to Word2Vec model file:

	python find-window-topics.py data/month1.pkl data/month2.pkl data/month3.pkl -k 4,10 -o out -m out/w2v-model.bin 

The script will apply NMF to each time window for each value of *k*, writing a result file each time to the directory 'out'. The output of the above for the sample data will also include the following recommendations for the number of topics for each of the three time windows:

	Top recommendations for number of topics for 'month1': 6,5,9
	...
	Top recommendations for number of topics for 'month2': 5,6,7
	...
	Top recommendations for number of topics for 'month3': 6,7,4

##### Step 3: Dynamic Topic Modeling 

We can also run automatic selection for the number of dynamic topics, by running the script 'find-dynamic-topics.py' and specifying a comma-separated range *kmin,kmax* and the path to the Word2Vec model built on the entire corpus:

	python find-dynamic-topics.py out/month1_windowtopics_k05.pkl out/month2_windowtopics_k05.pkl out/month3_windowtopics_k05.pkl -k 4,10 -o out -m out/w2v-model.bin 

Applying this to the sample corpus for the range [4,10] results in the recommendation of 6 topics:

	Top recommendations for number of dynamic topics: 6,8,7

The corresponding results will be written to 'out/dynamictopics_k06.pkl'. When the process has completed, we can view the dynamic topic descriptiors using:

	python display-topics.py out/dynamictopics_k06.pkl

For the sample corpus, the output for the top 10 terms for 6 dynamic topics should look similar to:

	+------+------------+-----------+------------+--------+----------+----------+
	| Rank | D01        | D02       | D03        | D04    | D05      | D06      |
	+------+------------+-----------+------------+--------+----------+----------+
	|    1 | blair      | chelsea   | people     | band   | growth   | film     |
	|    2 | labour     | game      | mobile     | music  | economy  | best     |
	|    3 | election   | club      | users      | album  | oil      | award    |
	|    4 | government | united    | software   | best   | sales    | awards   |
	|    5 | minister   | arsenal   | microsoft  | show   | prices   | actor    |
	|    6 | brown      | league    | technology | number | market   | director |
	|    7 | party      | players   | net        | chart  | bank     | oscar    |
	|    8 | prime      | cup       | phone      | awards | economic | films    |
	|    9 | howard     | liverpool | computer   | rock   | profits  | actress  |
	|   10 | told       | football  | security   | song   | company  | star     |
	+------+------------+-----------+------------+--------+----------+----------+

##### Reviewing Results

To track the individual topics from each window that contribute to the overall dynamic topics, run the script 'track-dynamic-topics.py', specifying the file path for the output of dynamic topic modeling, following by the paths for all of the individual window topic models (ordered by time window). Note that multiple topics in a single time window can be related to a single dynamic topic. Following on from the example the above, to see the tracking for all dynamic topics, run:

	python track-dynamic-topics.py out/dynamictopics_k06.pkl out/*windowtopics*.pkl

To view tracking for only a subset of dynamic topics, specify one or more topic numbers comma separated:

	python track-dynamic-topics.py out/dynamictopics_k06.pkl out/*windowtopics*.pkl -d 1,4

For the sample corpus, the output for tracking the dynamic topics D01 and D04 will contain the top-ranked terms for both the overall dynamic topics and the associated time window topics:

	- Dynamic Topic: D01
	+------+------------+-------------+------------+------------+
	| Rank | Overall    | Window 1    | Window 2   | Window 3   |
	+------+------------+-------------+------------+------------+
	|    1 | mobile     | microsoft   | people     | mobile     |
	|    2 | people     | mobile      | technology | phone      |
	|    3 | users      | users       | computer   | people     |
	|    4 | phone      | software    | phone      | phones     |
	|    5 | software   | people      | games      | broadband  |
	|    6 | technology | security    | users      | service    |
	|    7 | microsoft  | net         | software   | technology |
	|    8 | net        | information | sites      | tv         |
	|    9 | computer   | programs    | site       | digital    |
	|   10 | service    | computer    | online     | video      |
	+------+------------+-------------+------------+------------+
	- Dynamic Topic: D04
	+------+---------+----------+----------+
	| Rank | Overall | Window 2 | Window 3 |
	+------+---------+----------+----------+
	|    1 | band    | album    | music    |
	|    2 | music   | band     | band     |
	|    3 | album   | music    | best     |
	|    4 | best    | number   | show     |
	|    5 | show    | chart    | album    |
	|    6 | number  | best     | rock     |
	|    7 | chart   | awards   | singer   |
	|    8 | awards  | show     | number   |
	|    9 | rock    | song     | awards   |
	|   10 | song    | top      | song     |
	+------+---------+----------+----------+
	
