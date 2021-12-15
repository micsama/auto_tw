#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <unistd.h>
#define fun system("python 1.py")
#define funw system("python 1.py hi")
struct tm *p;
short flag = 1;
int i = 0, flag = 0;

void run(float c) {
  i++;
  printf("下次提交在%f小时后\n", c);
  if (flag) {
    printf("进行第一次刻板立刻提交");
	if(flag){
		funw;
	}else  fun;
    flag = 0;
  }
  //千万注意 c语言 windows里sleep单位是毫秒，linux 单位是秒
  sleep(c * 3600 + 2);
  printf("过去了%lf小时，现在进行第%d次提交", c, i);
	if(flag){
		funw;
	}else  fun;
}

int main(int argc, char *argv[]) {
	if(arg!=1){
		flag=1;
	}
    time_t timep;
    while (1) {
    time(&timep);
    p = gmtime(&timep);
    int c = (8 + p->tm_hour) % 24;
    printf("-------------现在是 %d 点。每日早上7点与中午13点自动填体温\n", c);
    (c >= 0 && c < 12) ? run(13 - c) : run(31 - c);
  }
  return 0;
}
