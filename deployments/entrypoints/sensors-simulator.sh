#!/bin/bash
set -e

sleep 2

if [ $ENABLE_TRACE = "true" ]
then
   echo "Running with OpenTelemetry"
  opentelemetry-instrument python sensors_simulator $@
else
  echo "OpenTelemetry isn't enable"
  python sensors_simulator $@
fi
