
output: main.o
	g++ -Wall -g -pthread main.o -lgtest_main  -lgtest -lpthread -o output

main.o: main.cc
	g++ -Wall -g -pthread -c main.cc -lgtest_main  -lgtest -lpthread

clean:
	rm *.o output
