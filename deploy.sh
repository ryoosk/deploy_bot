#!/bin/sh

pip install requests==2.9.1 --target ./
zip -r lambda_function.zip ./*
