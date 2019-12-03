set yr = 1990
while ( $yr < 2005 )
 set mo = 1
 while ( $mo <= 12 )
  if ( $mo < 10 ) set mo = 0$mo

  set folder = $yr:q_$mo
  echo "Going to " $folder

  if ( -d $folder ) then
   echo "Yep"
   cd $folder

   set date = "$yr":"$mo":01
   set fdate = "$date 01:01:01"
   exiftool.pl -alldates=$fdate:q .
   echo "$yr":"$mo":01 01:01:01 .

   pwd
   cd ..

  endif

  @ mo = $mo + 1

 end
 @ yr = $yr + 1
end
