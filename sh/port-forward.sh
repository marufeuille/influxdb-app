#!/bin/bash

gcloud compute ssh --zone asia-northeast1-b "influxdb-instance" -- -N -f -L 8086:localhost:8086
