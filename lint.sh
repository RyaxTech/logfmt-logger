#!/usr/bin/env bash

set -e
# For debug
# set -x

while getopts "fd:" opt; do
  case "$opt" in
    f)
      DO_CHECK_ONLY="false"
      ;;
    d)
      CHECK_DIR="$OPTARG"
      ;;
    ?)
      echo "script usage: $(basename $0) [-f] [-d directory]" >&2
      exit 1
      ;;
  esac
done

TO_CHECK_DIR=${CHECK_DIR:-"."}
CHECK_ONLY=${DO_CHECK_ONLY:-"true"}

if [[ $CHECK_ONLY == "true" ]]
then
    BLACK_EXTRA_OPTS="--check --diff"
    ISORT_EXTRA_OPTS="--check-only --diff"
fi

# Black compatibility from:
# https://black.readthedocs.io/en/stable/the_black_code_style.html
cat > .isort.cfg <<EOF
[settings]
multi_line_output=3
include_trailing_comma=True
force_grid_wrap=0
use_parentheses=True
line_length=88
sections=FUTURE,STDLIB,THIRDPARTY,FIRSTPARTY,LOCALFOLDER
no_lines_before=LOCALFOLDER
EOF

cat > .flake8 <<EOF
[flake8]
max-line-length = 80
select = C,E,F,W,B,B950
ignore = E203, E501, W503
EOF

echo "-- Checking import sorting"
isort --filter-files $ISORT_EXTRA_OPTS $TO_CHECK_DIR

echo "-- Checking python formating"
black $TO_CHECK_DIR --exclude "docs|ci" $BLACK_EXTRA_OPTS

echo "-- Checking python static checking"
flake8 $TO_CHECK_DIR --exclude="docs/*,ci/*" --per-file-ignores='*/__init__.py:F401'
