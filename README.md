# Introduction

This repo contains a complete example for running a Spark map-reduce wordcount job on the CARC HPC machine Wheeler without the need to have a full Hadoop cluster running on dedicated hardware. These scripts can be used without too much trouble to run any Spark job on the cluster, and not just the Python-based map-reduce this demo uses. 

# Installation

You will first want to clone this repo to your account on the wheeler machine. Once you have logged into wheeler, you can cd to the directory where you want to place this repo, for example your home directory, then clone the repo from github (the current link is inside the green "Clone or fownload" button in the upper right of this page on github). Here is such a session:
'''
bash$ cd ~
bash$ git clone https://github.com/rjohns03/spark-on-wheeler.git
bash$ cd spark-on-wheeler
bash$ ls
README.md               conf                    small.txt               wordcount.pbs
big.txt                 pbs-spark-submit        wordcount.log.reference wordcount.py
'''



The Apache Spark big data processing system is now available for use on the CARC Wheeler system
through normal queueing mechanisms without requiring there to be a full hadoop cluster running on decated hardware.  Users who wish to use Spark will submit their job to the queue with `qsub` and when the job starts up on the compute node(s) a Spark cluster is spawned in their allocation on Wheeler, and this cluster is then used for a batch Spark program with or without interaction. 

Spark-on-Wheeler is driven by the "pbs-spark-submit" script attached below. This script is run
within a PBS allocation, either batch scheduled (using qsub and a PBS script file)
or interactive (using qsub -I). It starts the Spark cluster on the allocation provided
by PBS, and then either runs a user-provided Spark program, or allows the user to connect
to the running Spark cluster (e.g. using pyspark). Note that data to be processed by spark 
should be housed in Wheeler's high performance scratch file systems (/wheeler/scratch/$USER/...),
as data-intensive Spark programs can place significant load on the file system..




Running Batch Spark Jobs in the Cluster via PBS
###############################################


****
Here is a PBS batch script submitting a Spark jobs:
# wordcount.pbs - This PBS script allocate a 2 minute 4 node 32 processor
# portion of wheeler to run a spark job. 
#PBS -l nodes=4:ppn=8
#PBS -l walltime=00:05:00
#PBS -N wordcount

# Work is done in the user's scratch # directory, and assumes that 
# /wheeler/scratch/$USER/spark exists.
SCRATCHDIR=/wheeler/scratch/$USER/spark

# Load the Spark package, and set SPARK_HOME to the appropriate directory
module load spark-2.1.0-gcc-4.8.5-lifnga6
export SPARK_HOME=$SPARK_DIR

# Copy the script we want to run, the data to process, and the config
# files, and the drive script  for spark to scratch directory 
cd $PBS_O_WORKDIR
cp wordcount.py $SCRATCHDIR
cp big.txt $SCRATCHDIR
cp -r conf $SCRATCHDIR
cp pbs-spark-submit $SCRATCHDIR

# Start the spark cluster running the wordcount python spark script
cd $SCRATCHDIR
$PBS_O_WORKDIR/pbs-spark-submit wordcount.py $SCRATCHDIR/big.txt > wordcount.log

# Copy the output of the spark job back to the directory the job was submitted from
cp wordcount.log $PBS_O_WORKDIR



Using the Spark Shell Interactively
###################################

Here's an example of using Spark interactively on Wheeler:
bridges@wheeler-sn[519]> ls
big.txt  conf/	pbs-spark-submit*  small.txt
bridges@wheeler-sn[520]> cd
bridges@wheeler-sn[521]> qsub -I -l nodes=4:ppn=8 -l walltime=01:00:00
qsub: waiting for job 14319.wheeler-sn.alliance.unm.edu to start
qsub: job 14319.wheeler-sn.alliance.unm.edu ready

Wheeler Portable Batch System Prologue
Job Id: 14319.wheeler-sn.alliance.unm.edu
Username: bridges
Job 14319.wheeler-sn.alliance.unm.edu running on nodes:
wheeler240 wheeler235 wheeler234 wheeler233

prologue running on host: wheeler240
bridges@wheeler240[500]> cd /wheeler/scratch/bridges/spark
bridges@wheeler240[501]> module load spark-2.1.0-gcc-4.8.5-lifnga6
Autoloading hadoop-2.8.2-gcc-4.8.5-kmaqzrc
Autoloading jdk-8u141-b15-gcc-4.8.5-y6l4xae
Autoloading jdk-8u141-b15-gcc-4.8.5-y6l4xae
bridges@wheeler240[502]> export SPARK_HOME=$SPARK_DIR
bridges@wheeler240[503]> ./pbs-spark-submit
SPARK_MASTER_HOST=wheeler240
SPARK_MASTER_PORT=7077
starting org.apache.spark.deploy.master.Master, logging to /wheeler/scratch/bridges/spark/spark-bridges-org.apache.spark.deploy.master.Master-1-wheeler240.out
17/11/21 21:46:16 WARN NativeCodeLoader: Unable to load native-hadoop library for your platform... using builtin-java classes where applicable
17/11/21 21:46:16 WARN NativeCodeLoader: Unable to load native-hadoop library for your platform... using builtin-java classes where applicable
17/11/21 21:46:16 WARN NativeCodeLoader: Unable to load native-hadoop library for your platform... using builtin-java classes where applicable
17/11/21 21:46:16 WARN NativeCodeLoader: Unable to load native-hadoop library for your platform... using builtin-java classes where applicable
17/11/21 21:46:17 WARN Utils: Service 'WorkerUI' could not bind on port 8081. Attempting port 8082.
bridges@wheeler240[504]> pyspark --master spark://wheeler240:7077
Python 2.7.5 (default, Aug  4 2017, 00:39:18)
[GCC 4.8.5 20150623 (Red Hat 4.8.5-16)] on linux2
Type "help", "copyright", "credits" or "license" for more information.
Setting default log level to "WARN".
To adjust logging level use sc.setLogLevel(newLevel). For SparkR, use setLogLevel(newLevel).
17/11/21 21:46:58 WARN util.NativeCodeLoader: Unable to load native-hadoop library for your platform... using builtin-java classes where applicable
Welcome to
      ____              __
     / __/__  ___ _____/ /__
    _\ \/ _ \/ _ `/ __/  '_/
   /__ / .__/\_,_/_/ /_/\_\   version 2.1.0
      /_/

Using Python version 2.7.5 (default, Aug  4 2017 00:39:18)
SparkSession available as 'spark'.
>>> rddread = sc.textFile("small.txt")
>>> rddread.takeSample(False, 10, 2)
[u'a savage place as holy and enchanted ', u'huge fragments vaulted like rebounding hail ', u'   floated midway on the waves ', u'and all should cry beware beware ', u'and from this chasm with ceaseless turmoil seething ', u'enfolding sunny spots of greenery ', u'as if this earth in fast thick pants were breathing ', u'and drunk the milk of paradise', u'five miles meandering with a mazy motion ', u'where blossomed many an incensebearing tree ']
>>> exit()
bridges@wheeler240[505]> exit
qsub: job 14319.wheeler-sn.alliance.unm.edu completed
bridges@wheeler-sn[522]>
