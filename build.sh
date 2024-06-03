#!/usr/bin/fish

gcc (pkg-config --cflags gtk4) src/main.c -o test (pkg-config --libs gtk4)