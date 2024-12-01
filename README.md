# htuning

## Prerequires
<pre>
<code>
pip install pandas
pip install openpyxl
pip install tqdm
</code>
</pre>

## Generate hipblaslt.log
Before running your APP:
<pre>
<code>
export HIPBLASLT_LOG_MASK=32
export HIPBLASLT_LOG_FILE=./hipblaslt.log
</code>
</pre>

## Download htuning
After running your APP, a hipblaslt.log file will be generated in the execution directory. Then, copy the hipblaslt.log file to the htuning directory.
<pre>
<code>
git clone https://github.com/ClementLinCF/htuning.git
cd htuning
cp &lt;your hipblaslt.log&gt; .
</code>
</pre>


## Auto tuning
<pre>
<code>
"Usage: bash alltuning.sh &lt;rocm_bin_path&gt; &lt;training GPU devices&gt; &lt;assign the verified GPU device&gt;"
</code>
</pre>


For example, the following command will execute on GPU device 8 to 31 in parallel and verify the final performance result on GPU device 31
<pre>
<code>
bash alltuning.sh /opt/rocm-6.3.0.1/bin "8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31" 31
</code>
</pre>

The **ftuning.txt** and **comparison.xlsx** files will eventually be generated. The **ftuning.txt** is the file which records the final tuning config with best solution id. The **comparison.xlsx** records the performance before and after tuning, as well as the percentage improvement in performance. 

## Apply tuning config

<pre>
<code>
export HIPBLASLT_TUNING_OVERRIDE_FILE=ftuning.txt
</code>
</pre>
And run your app
