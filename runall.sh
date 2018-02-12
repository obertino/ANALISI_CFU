ExamSet=(AGR0048    AGR0004    AGR0007    AGR0047    SAF0050    AGR0051    AGR0008    AGR0059    AGR0020   AGR0048    AGR0004    AGR0007    AGR0047    SAF0050    AGR0051    AGR0008    AGR0055    AGR0025   AGR0395    AGR0027    AGR0025    AGR0011    SAF0050    AGR0017    AGR0016    AGR0012    AGR0045    AGR0295   AGR0395    AGR0027    AGR0025    AGR0138    AGR0011    SAF0050    AGR0017    AGR0016    AGR0012    AGR0331    AGR0295) 

data=(dati2014 dati2015 dati2016)
Years=(2015 2016 2017)
k=-1
for j in ${data[@]};
do
k=$(expr $k + 1)
echo $k
for i in ${ExamSet[@]}; 
do 
echo $j, $k, $i, ${Years[k]}
python exal.py $j ${Years[k]} $i > $i-${Years[k]}
done
done
