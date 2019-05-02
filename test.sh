#/bin/bash
for i in $(git status | grep modified | grep .py | awk '{print $2}'); do echo -n "$i: "; python $i&> /dev/null; echo $?; done
