#!/bin/zsh

if [ ! -z "$( ls -A $DATA_DIRECTORY )" ]; then
    rm -rf $DATA_DIRECTORY/*
fi