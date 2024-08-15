#!/bin/sh

echo "[Debug] script - NEW_VERSION=${NEW_VERSION}";

sed -E "s/version: (.+)/version: ${NEW_VERSION}/g" -i galaxy.yml;
