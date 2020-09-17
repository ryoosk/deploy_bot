#!/bin/sh

npm install
zip -r lambda_functions.zip index.js node_modules
