#!/bin/zsh

### PARAMETERS

# DEFAULT_PLAINTEXT="1"
RANDOMIZE_INPUT=true
GENERATE_RESETS_DATA=true
DATA_DIRECTORY_PATH="./data"

###

if $GENERATE_RESETS_DATA;
    then ./clear.zsh
fi

INPUT="$DEFAULT_PLAINTEXT"

if $RANDOMIZE_INPUT;
    then INPUT="$(shuf -i 0-1 -n 1)"
fi

if (( $# > 0 ));
    then INPUT="$1"
fi

ENUM=0
FILENAME="cipher_$ENUM"

while [ -e "$DATA_DIRECTORY_PATH/$FILENAME" ]; do
    ENUM=$(( ENUM + 1 ))
    FILENAME="cipher_$ENUM"
done


###

mkdir -p "$DATA_DIRECTORY_PATH"
mkdir "$DATA_DIRECTORY_PATH/$FILENAME"
echo "$INPUT" > "$DATA_DIRECTORY_PATH/$FILENAME/plain_$ENUM"
python3 ./encrypt/encryption.py -y "$INPUT" > "$DATA_DIRECTORY_PATH/$FILENAME/$FILENAME"