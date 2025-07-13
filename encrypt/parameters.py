N = 100  # NUMBER OF VARIABLES
M = 426  # NUMBER OF CLAUSES
K = 3  # NUMBER OF VARIABLES PER CLAUSE

# 2 <= BETA << (much less than) ALPHA
ALPHA = 15
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


GENERATED_CIPHER_SORTING = [
        len, # shortness of monomial
        lambda term: [int(literal[1:]) for literal in term] # literals of monomial, ascending
]
REVERSE_CIPHER_SORTING = False