rsync -a /home/nate/autoscope pi@192.168.1.96:/home/pi
ssh pi@192.168.1.96 -t "python3 /home/pi/autoscope/autoscope"