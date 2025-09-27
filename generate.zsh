#!/bin/zsh

### PARAMETERS

GENERATE_RESETS_DATA=true # OPTIONS: true, false
PLAINTEXT=0 # OPTIONS: 0, 1, "random"

### OPTIONAL CIPHER DIRECTORY FILES

# cipher_x_display__txt=true
comments_x__txt=true
# map_x__txt=true
plain_x__txt=true

###

mkdir -p "$DATA_DIRECTORY"

if $GENERATE_RESETS_DATA;
    then ./clear.zsh
fi

cipher_count=1
if (( $# > 0 ));
    then cipher_count="$1"
fi

###

for _ in {1..$cipher_count}; do

    if [[ $PLAINTEXT == "random" ]];
        then plaintext_n="$(shuf -i 0-1 -n 1)"
    else
        plaintext_n=$PLAINTEXT
    fi


    ### Finding smallest n so that data/cipher_n is NOT used
    n=0
    file="cipher_$n"
    cipher_n_directory="$DATA_DIRECTORY/${file}_dir"

    while [ -e "$cipher_n_directory" ]; do
        n=$(( n + 1 ))
        file="cipher_$n"
        cipher_n_directory="$DATA_DIRECTORY/${file}_dir"
    done
    mkdir $cipher_n_directory

    ### Running scripts

    if [[ $plain_x__txt ]];
        then echo "$plaintext_n" > "$cipher_n_directory/plain_$n.txt"
    fi
    
    if [[ $comments_x__txt ]]; then
        comments_x__txt_path="$cipher_n_directory/comments_$n.txt"
    else
        comments_x__txt_path="/dev/null"
    fi

    creation_time=("$( { time python3 ./src/encrypt/encrypt.py -y "$plaintext_n" -c "$n" >$comments_x__txt_path ; } 2>&1 )")
    echo "cipher $n created in $creation_time"


    ### Keeping track of run time
    ns_used+=($n)
    (( total_creation_time += $((${creation_time%?})) ))
done


### Printing run time
if [[ $cipher_count > 1 ]]; then
    FORMATTED_TIME=$(printf "%.2f" "$total_creation_time")
    echo "$cipher_count ciphers (${(j:, :)ns_used}) created in ${FORMATTED_TIME}s"
fi