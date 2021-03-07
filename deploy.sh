address=$1
rsync -a /home/nate/automata-scope pi@$address:/home/pi
ssh pi@$address -t "python3 /home/pi/automata-scope/automata_scope"