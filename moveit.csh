set yr = 1990
while ( $yr < 2016 )
 set mo = 1
 while ( $mo <= 12 )
  if ( $mo < 10 ) set mo = 0$mo

  echo "$yr$mo??_* ../../Us/$yr/$yr:q_$mo/"
  mv -n $yr$mo??_* ../../Us/$yr/$yr:q_$mo/
  @ mo = $mo + 1

 end
 @ yr = $yr + 1
end
