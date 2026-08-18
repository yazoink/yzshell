#!/usr/bin/env bash

pid="$(pidof wf-recorder)"
kill -SIGINT $"{pid}"
eww update recorder_selected=1