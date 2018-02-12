#data=(dati2014 dati2015 dati2016)
data=(dati2016)
Years=(2017)
k=-1
for j in ${data[@]};
do
k=$(expr $k + 1)
echo $k
echo $j, $k, ${Years[k]}
python exal_all_root.py $j ${Years[k]} > All_Res.dat
done
