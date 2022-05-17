#!/bin/bash
set -e

sleep 2

if [ $ENABLE_TRACE = "true" ]
then
   echo "Running with OpenTelemetry"
  opentelemetry-instrument uvicorn sensors_api.api:app --host=0.0.0.0 $(test ${ENV} = "development" && echo "--reload")
else
  echo "OpenTelemetry isn't enable"
uvicorn sensors_api.api:app --host=0.0.0.0 $(test ${ENV} = "development" && echo "--reload")
fi
