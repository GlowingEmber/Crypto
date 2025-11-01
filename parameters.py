import math

###
### Encryption
###

# N < M
N = 100 # 4 # NUMBER OF VARIABLES
M = 426 # 7 # NUMBER OF CLAUSES
K = 3  # NUMBER OF VARIABLES PER CLAUSE

# 2 <= BETA << (much less than) ALPHA
ALPHA = 3  # ~4 or 5 are the upper bounds for reasonable solve time right now
BETA = 10

# (a)
# To counter attacks discussed in Section 3.1.2, it is prefer-
# able if the clauses within one tuple share variables. This
# is particularly important if one of the clauses does not
# contain negations, i.e. s(i, 1) = . . . = s(i, k) = 0.
CONDITION_A = False

# (b)
# We have to ensure that each tuple shares at least one
# clause with another tuple to counter the attack dis-
# cussed in Section 3.2.
CONDITION_B = False

# (c)
# Each clause of pub is to appear in some tuple as dis
# cussed in Section 3.3.
CONDITION_C = False


CIPHER_SORTING_ORDER = [
        len, # shortness of monomial
        # lambda term: list(term) # literals of monomial, ascending
]
REVERSE_CIPHER_SORTING = False

###
### Codebreaking
###

TERM_LENGTH_CUTOFF = math.floor(1.9 * ALPHA)