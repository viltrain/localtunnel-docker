#!/bin/bash

sleep 1
echo "reloading"
kill -2 $(pidof python)
