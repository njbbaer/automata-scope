address=$1
rsync -a /home/nate/autoscope pi@$address:/home/pi
ssh pi@$address -t "python3 /home/pi/autoscope/autoscope"