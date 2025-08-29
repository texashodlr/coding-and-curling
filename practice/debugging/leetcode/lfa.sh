#!/bin/bash

grep '^ERROR:' log_file.log | awk '{print $2}' | sort -u