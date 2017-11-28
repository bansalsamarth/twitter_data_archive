#!/bin/bash
#Test program — Fetch network of Narendra Modi

echo "Narendra Modi's network"
python twecoll init NarendraModi
python twecoll fetch NarendraModi
python twecoll edgelist luca -m
