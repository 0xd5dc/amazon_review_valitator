from pyspark.ml.classification import LogisticRegression, NaiveBayes, DecisionTreeClassifier, GBTClassifier, \
    RandomForestClassifier
import pyspark as ps
from pyspark.sql.types import StructField, StructType, StringType, IntegerType

DATA_FILE = '../../amazon_reviews_us_Camera_v1_00.tsv.gz'
APP_NAME = 'EDA'
FEATURES = ['star_rating', 'review_body', 'helpful_votes', 'total_votes', 'verified_purchase', 'review_date']
SAMPLE_SIZE = 10000

review_schema = StructType(
    [StructField('marketplace', StringType(), True),
     StructField('customer_id', StringType(), True),
     StructField('review_id', StringType(), True),
     StructField('product_id', StringType(), True),
     StructField('product_parent', StringType(), True),
     StructField('product_title', StringType(), True),
     StructField('product_category', StringType(), True),
     StructField('star_rating', IntegerType(), True),
     StructField('helpful_votes', IntegerType(), True),
     StructField('total_votes', IntegerType(), True),
     StructField('vine', StringType(), True),
     StructField('verified_purchase', StringType(), True),
     StructField('review_headline', StringType(), True),
     StructField('review_body', StringType(), True),
     StructField('review_date', StringType(), True)])

spark = (ps.sql.SparkSession.builder
         .master("local[1]")
         .appName(APP_NAME)
         .getOrCreate()
         )
sc = spark.sparkContext

df = spark.read.format("csv") \
    .option("header", "true") \
    .option("mode", "FAILFAST") \
    .option("sep", "\t") \
    .schema(review_schema) \
    .load(DATA_FILE)
df.createOrReplaceTempView("eda_sql_view")

review_all = df.select(FEATURES)
review_sample = df.select(FEATURES).limit(SAMPLE_SIZE).cache()
