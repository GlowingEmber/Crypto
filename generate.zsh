#!/bin/zsh

### PARAMETERS

GENERATE_RESETS_DATA=true # options: true, false
PLAINTEXT="R" # options: 0, 1, "R" (random)

###

mkdir -p "$DATA_DIRECTORY_PATH"

###

if $GENERATE_RESETS_DATA;
    then ./clear.zsh
fi

###

CIPHERS_COUNT=1
if (( $# > 0 ));
    then CIPHERS_COUNT="$1"
fi

for _ in {1..$CIPHERS_COUNT}; do

    if [[ $PLAINTEXT == "R" ]];
        then INPUT="$(shuf -i 0-1 -n 1)"
    fi

    ENUM=0
    FILENAME="cipher_$ENUM"
    while [ -e "$DATA_DIRECTORY_PATH/$FILENAME" ]; do
        ENUM=$(( ENUM + 1 ))
        FILENAME="cipher_$ENUM"
    done

    mkdir "$DATA_DIRECTORY_PATH/$FILENAME"
    echo "$INPUT" > "$DATA_DIRECTORY_PATH/$FILENAME/plain_$ENUM"
    python3 ./src/encrypt/encrypt.py -y "$INPUT" -c "$CIPHERS_COUNT" > "$DATA_DIRECTORY_PATH/$FILENAME/$FILENAME"
    
done