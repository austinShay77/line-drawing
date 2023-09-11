default:
	cp CG_hw1.py CG_hw1
	chmod +x CG_hw1

all:
	python3 CG_hw1.py -f hw1.ps -a 0 -b 0 -c 499 -d 499 -s 1.0 -m 0 -n 0 -r 0 > out.ps
	python3 CG_hw1.py -f hw1.ps -a 0 -b 0 -c 499 -d 499 -s 0.8 -m 85 -n 25 -r 10 > hw1_out.ps
	python3 CG_hw1.py -f hw1.ps -s 0.5 > scale.ps
	python3 CG_hw1.py -f hw1.ps -r -30 > nrotate.ps
	python3 CG_hw1.py -f hw1.ps -m 100 -n 100 > translate.ps
	python3 CG_hw1.py -f hw1.ps -a -25 -b -50 -c 399 -d 399 > worldwindow.ps
	python3 CG_hw1.py -f hw1.ps -a 25 -b 50 -c 399 -d 399 -r 30 -m 100 -n 100 -s 0.5 > all.ps
	python3 CG_hw1.py -f hw1_line.ps -r -17 -m -10 -n 400 > line1.ps
