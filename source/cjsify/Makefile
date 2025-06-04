CC = gcc
#CC = i686-w64-mingw32-gcc
CFLAGS = -Wall -Wextra -O2 -fPIC $(shell python3-config --includes)
LDFLAGS = $(shell python3-config --ldflags)

TARGET = jsify.so
SOURCES = Undefined.c Object.c Tuple.c List.c Dict.c Iterator.c jsify.c

all: $(TARGET) copy

$(TARGET): $(SOURCES)
	$(CC) $(CFLAGS) -shared -o $(TARGET) $(SOURCES) $(LDFLAGS)

copy:
	cp $(TARGET) ../jsify/

clean:
	rm -f $(TARGET) *.o