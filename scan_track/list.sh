rm LIST.spt

touch LIST.spt


target="$(pwd)"
let count=0
for f in "$target"/*.ent
do
  echo "load FILES $(basename $f) " >> LIST.spt
  echo "background white  ;" >> LIST.spt
  echo "set window 700 700; " >> LIST.spt
  echo "select carbon;  " >> LIST.spt
  echo "spacefill 0.0; " >> LIST.spt
  echo "select oxygen;  " >> LIST.spt
  echo "spacefill 0.0; " >> LIST.spt
  echo "select sulfur; " >> LIST.spt
  echo "spacefill 0.0;  " >> LIST.spt
  echo "display within (30, PLANE, {1 0 0} {0 0 0} {0 1 0}); " >> LIST.spt
  echo "set scale3d 4.8; " >> LIST.spt
  echo "select nitrogen; " >> LIST.spt
  echo "spacefill 0.5; " >> LIST.spt
  echo "select sulfur; " >> LIST.spt
  echo "wireframe 0.25; " >> LIST.spt
  echo "select oxygen; " >> LIST.spt
  echo "wireframe 0.25; " >> LIST.spt

 # if [[ $count -eq 0 ]]
#then
#  echo "save ORIENTATION View1">> LIST.spt
#fi
  
 # echo "restore ORIENTATION View1">> LIST.spt
 # echo "boundbox">> LIST.spt 
 # echo "boundbox CORNERS {-5.0 -5.0 -5.0} {5.0 5.0 5.0}">> LIST.spt  
  echo `printf "%s%012d%s\n" "write JPG" $count ".jpg ;"` >> LIST.spt
  let count=count+1
done
echo "exitjmol">> LIST.spt

java -jar /usr/share/java/Jmol.jar -s LIST.spt
#### первая это гиф
#convert -delay 5 *.jpg myimage.gif
#### вторая это через утилиту ви 1 тут это время на кадр
### -b это установка битрейта, без повышения битрейта шарики смазывались из-за хаотичного движения, -у разрешает перезапись файла без подтверждения
ffmpeg -r 10 -i JPG%012d.jpg -b 300000k  -y test.avi

