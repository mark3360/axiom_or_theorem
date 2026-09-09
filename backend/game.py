from check_lean_proof import check_lean_proof 
import re

def check_valid_axiom(axiom):
    if "#" in axiom:
        return False
    
    lean_file = f"""
        set_option warningAsError true
        set_option linter.all false

        variable {{D : Type}}

        def h : Prop := 
           ({axiom})

        #print h
    """
    return check_lean_proof(lean_file)

def check_valid_challenge(proof, axioms):
    if "#" in proof:
        return False

    if 'sorry' in proof:
        return False
    
    if 'admit' in proof:
        return False

    axioms = map(lambda x : x['message'], axioms)
    print(axioms)

    print("Proof", proof)

    lean_file = f"""
set_option warningAsError true
set_option linter.all false
variable {{D : Type}}

{"\n".join(axioms)}

{proof}

#check challenge
    """

    return check_lean_proof(lean_file)

def is_challenge(s: str, n: int) -> bool:
    s = re.sub(r"\s+", "", s)
    print("Challenge String")
    print(s)
    print("End Challenge String")
    prefix = 'challenge{D:Type}:'

    if not s.startswith(prefix):
        print("1")
        return False

    s = s[len(prefix):]

    # Split the two sides of the ∨
    parts = s.split("∨")
    if len(parts) != 2:
        print("2")
        return False

    left, right = parts

    if not (left.startswith("(") and left.endswith(")")):
        print("3")
        return False
    if not (right.startswith("(") and right.endswith(")")):
        print("4")
        return False

    left = left[1:-1]
    right = right[1:-1]

    # The final hypothesis must be h_k / ¬h_k
    if "→" not in left or "→" not in right:
        return False

    left_parts = left.split("→")
    right_parts = right.split("→")

    if len(left_parts) != n or len(right_parts) != n:
        print("5")
        return False

    # They must have the same prefix
    if left_parts[:-1] != right_parts[:-1]:
        print("6")
        return False

    final = left_parts[-1]
    neg_final = right_parts[-1]

    if not final.startswith("h"):
        print("7")
        return False

    if neg_final != "¬" + final:
        print("8")
        return False

    # Extract k
    try:
        k = int(final[1:])
    except ValueError:
        print("9")
        return False

    if not (1 <= k <= n):
        print("10")
        return False

    # Check that h1,...,hn except hk occur in ascending order
    expected_prefix = [
        f"h{i}" for i in range(1, n + 1)
        if i != k
    ]

    if left_parts[:-1] != expected_prefix:
        print("11")
        return False

    return True