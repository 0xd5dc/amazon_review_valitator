from pyspark.ml.classification import LogisticRegression, NaiveBayes, DecisionTreeClassifier, GBTClassifier, \
    RandomForestClassifier
from pyspark.ml.feature import VectorAssembler
from pyspark.mllib.evaluation import BinaryClassificationMetrics
from pyspark.sql.functions import current_date, expr, datediff, to_date
from pyspark.sql.functions import length, regexp_replace

from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize

import re


def get_kv_pairs(row, exclusions=[]):
    # get the text from the row entry
    text = str(row.review_body).lower()
    # create blacklist of words
    blacklist = set(stopwords.words('english'))
    # add explicit words
    [blacklist.add(i) for i in exclusions]
    # extract all words
    words = re.findall(r'([^\w+])', text)
    # for each word, send back a count of 1
    # send a list of lists
    return [[w, 1] for w in words if w not in blacklist]


def get_word_counts(texts, exclusions=[]):
    mapped_rdd = texts.rdd.flatMap(lambda row: get_kv_pairs(row, exclusions))
    counts_rdd = mapped_rdd.reduceByKey(lambda a, b: a + b).sortBy(lambda a: a[1])
    return counts_rdd.collect()


def convert_str_to_int(df, col='verified_purchase', type_='int'):
    return df.select((df[col] == 'Y').cast(type_))


def get_review_age(df):
    return df.select(datediff(current_date(), to_date(df['review_date'])))


def prepare_features(df):
    df = df.withColumn('exclam', length('review_body') - length(regexp_replace('review_body', '\!', '')))
    df = df.withColumn('age', datediff(current_date(), to_date(df['review_date'])))
    df = df.withColumn('review_length', length(df['review_body']))
    df = df.withColumn('helfulness', df['helpful_votes'] / df['total_votes'])
    df = df.withColumn('label', expr("CAST(verified_purchase='Y' As INT)"))
    select_cols = df.select(['star_rating', 'helfulness', 'age', 'review_length', 'label']).na.fill(0)
    return select_cols


def split_data(df, rate=.9):
    training = df.sampleBy("label", fractions={0: rate, 1: rate}, seed=12)
    return training, df.subtract(training)


def get_auc_roc(classifier, training, test):
    model = classifier.fit(training)
    out = model.transform(test) \
        .select("prediction", "label") \
        .rdd.map(lambda x: (float(x[0]), float(x[1])))
    metrics = BinaryClassificationMetrics(out)
    print("Model: {1}. Area under ROC: {0:2f}".format(metrics.areaUnderROC, clf.__class__))
    return model, out, metrics


def get_vectorized_features(df, cols=['star_rating']):
    va = VectorAssembler().setInputCols(cols).setOutputCol(
        'features')
    return va.transform(df)