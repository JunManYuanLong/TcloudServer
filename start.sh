list="auth autotest extention flow interface message public tcdevices project jobs"
for i in $list;
do
nohup python -m apps.$i.run >logs/$i.log 2>&1 &
done
