#!/usr/bin/env bash

## Prerequisites:
#sudo apt install pandoc
#sudo apt install texlive 

script_path=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )

cd $script_path
cd ..
mkdir -p pdf

find . -name "*.md" | xargs -I{} -t sh -c 'pandoc "{}" -V geometry:margin=1in -V colorlinks=true -V linkcolor=blue -V urlcolor=blue -V toccolor=gray -f markdown+rebase_relative_paths -f markdown+lists_without_preceding_blankline --standalone --output ./pdf/$(echo {} | sed -E "s#.*/([^/]+)/README\.md#\1#; t; s#.*/README\.md#readme#").pdf'