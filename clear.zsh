#!/bin/zsh

if [ ! -z "$( ls -A './data' )" ]; then
    rm -rf ./data/*
fi