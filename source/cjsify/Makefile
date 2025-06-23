CC = cl

CFLAGS = /nologo /O2 /LD /MD /I"C:\ProgramData\miniconda3\Include"
LDFLAGS = /link /LIBPATH:"C:\ProgramData\miniconda3\libs"

TARGET = jsify.pyd
SOURCES = Undefined.c Object.c Tuple.c List.c Dict.c Iterator.c jsify.c

all: $(TARGET) copy

$(TARGET): $(SOURCES)
	$(CC) $(CFLAGS) $(SOURCES) /link /OUT:$(TARGET) $(LDFLAGS)

copy:
	copy $(TARGET) ..\jsify\

clean:
	del /Q $(TARGET) *.obj
