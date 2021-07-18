#include<cstdio>
#include<iostream>
#include<fstream>
#include<ctime>
using namespace std;
void info(char *info){
	printf("[+]%s\n",info);
}
void error(char *err){
	printf("[-]%s\n",err);
}
int main(int argc,char *argv[]){
	unsigned char uch;
    ifstream infile(argv[2],ios::in|ios::binary);
	ofstream outfile(argv[3],ios::out|ios::binary);
	if(!infile) {
        error("ERROR:Infile does not exist");
        return 0;
    }
    if(!outfile){
    	error("ERROR:Unable to open file for write");
	}
	time_t curtime;
	time(&curtime);
	info(ctime(&curtime));
	info("Start");
	while(!infile.eof()){
		infile.read((char*)&uch,sizeof(uch));
		uch^=*argv[1];
		outfile.write((const char*)&uch,sizeof(uch));
	}
	info("Completed");
}