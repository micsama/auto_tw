
cmd="./autotw";
screen_name="autotw"
start:
	git pull
	gcc ./do.c -o autotw
	./autotw
