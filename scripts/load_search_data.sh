#!/bin/bash
source ./venv/bin/activate
echo "## $0 received NUM ARGS : " $#
ERROR_MSG="## 💥💥 expecting first argument to be a tab delimited data file to import into the sqlite3 database"
DB_FILENAME='data/search.sqlite3'
if [ $# -eq 1 ]; then
  TSV_FILENAME=${1}
elif [ $# -eq 2 ]; then
  TSV_FILENAME=${1}
  DB_FILENAME=${2}
else
  echo "$ERROR_MSG"
  echo "## the sqlite3 database is an optional second argument (default to {$DB_FILENAME} file"
  exit 1
fi
echo "## 📂 DB_FILENAME : $DB_FILENAME"
if [ -r "$TSV_FILENAME" ]; then
  python3 create-db.py "$DB_FILENAME"
  sqlite3 "$DB_FILENAME" ".mode tabs" ".import ${TSV_FILENAME} search_item" ".quit"
  python3 create-db.py "$DB_FILENAME"
else
  echo "$ERROR_MSG"
  exit 1
fi
