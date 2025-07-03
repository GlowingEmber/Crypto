#!/bin/zsh

if [ ! -z "$( ls -A $DATA_DIRECTORY_PATH )" ]; then
    rm -rf $DATA_DIRECTORY_PATH/*
fi