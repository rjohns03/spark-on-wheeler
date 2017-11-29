# Introduction

The Apache Spark big data processing system is now available for use on the
CARC Wheeler system through the normal queueing mechanism without requiring a
full hadoop cluster running on decated hardware.  Users who wish to use
Spark will submit their job to the queue with `qsub` and when the job starts up
on the compute node(s) a Spark cluster is spawned in their allocation on
Wheeler, and this cluster is then used for a batch Spark program with or
without interaction. 

This repo contains a complete example for running a Spark map-reduce wordcount
job on the CARC HPC machine Wheeler without the need to have a full Hadoop
cluster running on dedicated hardware. These scripts can be used without too
much trouble to run any Spark job on the cluster, and not just the Python-based
map-reduce this demo uses. 

Spark-on-Wheeler is driven by the "pbs-spark-submit" script attached below.
This script is run within a PBS allocation, either batch scheduled (using qsub
and a PBS script file) or interactive (using qsub -I). It starts the Spark
cluster on the allocation provided by PBS, and then either runs a user-provided
Spark program, or allows the user to connect to the running Spark cluster (e.g.
using pyspark or spark-shell). Note that data to be processed by spark should
be housed in Wheeler's high performance scratch file systems
(/wheeler/scratch/$USER/...), as data-intensive Spark programs can place
significant load on the file system...


# Getting Started

## Cloning/downloading this repo to wheeler

You will first want to clone this repo to your account on the wheeler machine.
Once you have logged into wheeler, cd to the directory where you want
to save this repo, your home directory, for instance, and clone the repo from
github (the current link is inside the green "Clone or Download" button in the
upper right of this page github). 
Here is such a session: 

``` 
bash$ cd ~
bash$ git clone https://github.com/rjohns03/spark-on-wheeler.git 
bash$ cd spark-on-wheeler 
bash$ ls 
README.md        conf 		  small.txt		submit_spark.pbs 	
big.txt          pbs-spark-submit wordcount.log.reference	 wordcount.py 
```


One of the benifits of cloning a repository is the ease with which you can reset everything inside the repo to how it was when you first cloned it very easily. Let say you have made some changes, and there are some new .o and .e files, but you now want to reset it to its original state. You could delete it and clone it again, or far better, just reset it. 




# Running Batch Spark Jobs in the Cluster via PBS


submit_spark.pbs is a PBS batch script for submitting a Spark jobs. 

Currently, it set to  allocate a 1 hour, 2 node portion of wheeler to run a
spark job.  But this can be changed by editing the lines starting with "#PBS"
Note: Do not change the value of ppn=8, this is set by the machine hardware.

If you want to change the file that the word count is performed on, you must
edit this file and change the name of the DOCUMENT variable to the corrent name
of the file. It is easiest to put that file in this same directory as all the
other scripts.

To avoid I/O problems, work is done in the user's scratch directory on
wheeler-scratch, which is first created, then the required files are copied
from this directory there, then the Spark job is run, and finally, the output
is copied back here, and the scratch directory is removed. 

To submit this job, after the submit_spark.pbs file has been edited appropriately, 
run the following command:
```
qsub submit_spark.pbs
```

You can follow the status of the job with the `qstat -a` command and if you
need to delete a job that can be done by taking the Job Number from `qstat -a`
and running `qdel JobNum`. See `man qsub` for more details.



# Using the Spark Shell Interactively 

Here's an example of using Spark interactively on Wheeler:

```
user@wheeler-sn[519]> ls big.txt  conf/	pbs-spark-submit*  small.txt
user@wheeler-sn[520]> cd user@wheeler-sn[521]> qsub -I -l nodes=4:ppn=8
-l walltime=01:00:00 qsub: waiting for job 14319.wheeler-sn.alliance.unm.edu to
start qsub: job 14319.wheeler-sn.alliance.unm.edu ready

Wheeler Portable Batch System Prologue Job Id:
14319.wheeler-sn.alliance.unm.edu Username: user Job
14319.wheeler-sn.alliance.unm.edu running on nodes:
wheeler234 wheeler233

prologue running on host: wheeler240 user@wheeler240[500]> cd
/wheeler/scratch/user/spark user@wheeler240[501]> module load
spark-2.1.0-gcc-4.8.5-lifnga6 Autoloading hadoop-2.8.2-gcc-4.8.5-kmaqzrc
Autoloading jdk-8u141-b15-gcc-4.8.5-y6l4xae Autoloading
jdk-8u141-b15-gcc-4.8.5-y6l4xae user@wheeler240[502]> export
SPARK_HOME=$SPARK_DIR user@wheeler240[503]> ./pbs-spark-submit
SPARK_MASTER_HOST=wheeler240 SPARK_MASTER_PORT=7077 starting
org.apache.spark.deploy.master.Master, logging to
/wheeler/scratch/user/spark/spark-user-org.apache.spark.deploy.master.Master-1-wheeler240.out
17/11/21 21:46:16 WARN NativeCodeLoader: Unable to load native-hadoop library
kor your platform... using builtin-java classes where applicable 17/11/21
21:46:16 WARN NativeCodeLoader: Unable to load native-hadoop library for your
platform... using builtin-java classes where applicable 17/11/21 21:46:16 WARN
NativeCodeLoader: Unable to load native-hadoop library for your platform...
using builtin-java classes where applicable 17/11/21 21:46:16 WARN
NativeCodeLoader: Unable to load native-hadoop library for your platform...
using builtin-java classes where applicable 17/11/21 21:46:17 WARN Utils:
Service 'WorkerUI' could not bind on port 8081. Attempting port 8082.
user@wheeler240[504]> pyspark --master spark://wheeler240:7077 Python 2.7.5
(default, Aug  4 2017, 00:39:18) [GCC 4.8.5 20150623 (Red Hat 4.8.5-16)] on
linux2 Type "help", "copyright", "credits" or "license" for more information.
Setting default log level to "WARN".  To adjust logging level use
sc.setLogLevel(newLevel). For SparkR, use setLogLevel(newLevel).  17/11/21
21:46:58 WARN util.NativeCodeLoader: Unable to load native-hadoop library for
your platform... using builtin-java classes where applicable Welcome to ____ __
/ __/__  ___ _____/ /__ _\ \/ _ \/ _ `/ __/  '_/ /__ / .__/\_,_/_/ /_/\_\
version 2.1.0 /_/

Using Python version 2.7.5 (default, Aug  4 2017 00:39:18) SparkSession
available as 'spark'.
>>> rddread = sc.textFile("small.txt") rddread.takeSample(False, 10, 2)
[u'a savage place as holy and enchanted ', u'huge fragments vaulted like
rebounding hail ', u'   floated midway on the waves ', u'and all should cry
beware beware ', u'and from this chasm with ceaseless turmoil seething ',
u'enfolding sunny spots of greenery ', u'as if this earth in fast thick pants
were breathing ', u'and drunk the milk of paradise', u'five miles meandering
with a mazy motion ', u'where blossomed many an incensebearing tree ']
>>> exit()
user@wheeler240[505]> exit qsub: job 14319.wheeler-sn.alliance.unm.edu
completed user@wheeler-sn[522]>
```
