# Misc utility functions/classes

# String truncation
def trunc(strn, ln):
    return (strn[:ln+3] + '...') if len(strn) > ln else strn
