#!/bin/bash
#lets check the argument
    #if true then print Hello, World
    #else
        #print whoops
if [ -z $1]; then
    exit 1
fi
if [ $1 == "hello" ]; then
    echo "Hello, World!"
else
    echo "Whoops"
fi