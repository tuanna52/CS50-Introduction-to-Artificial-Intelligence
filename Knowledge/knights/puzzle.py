from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."
Asays = And(AKnight, AKnave)
knowledge0 = And(
    Or(AKnight, AKnave),
    Biconditional(AKnight, Not(AKnave)),
    Biconditional(AKnight, Asays)
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
Asays = And(AKnave, BKnave)

knowledge1 = And(
    Or(AKnight, AKnave),
    Or(BKnight, BKnave),
    Biconditional(AKnight, Not(AKnave)),
    Biconditional(BKnight, Not(BKnave)),
    Biconditional(AKnight, Asays)
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
Asays = Or(And(AKnight, BKnight), And(AKnave, BKnave))
Bsays = Or(And(AKnight, BKnave), And(AKnave, BKnight))
knowledge2 = And(
    Or(AKnight, AKnave),
    Or(BKnight, BKnave),
    Biconditional(AKnight, Not(AKnave)),
    Biconditional(BKnight, Not(BKnave)),
    Biconditional(AKnight, Asays),
    Biconditional(BKnight, Bsays)
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
Asays = Or(AKnight, AKnave)
Bsays = And(CKnave, And(Asays, AKnave))
Csays = AKnight
knowledge3 = And(
    Or(AKnight, AKnave),
    Or(BKnight, BKnave),
    Or(CKnight, CKnave),
    Biconditional(AKnight, Not(AKnave)),
    Biconditional(BKnight, Not(BKnave)),
    Biconditional(CKnight, Not(CKnave)),
    Biconditional(AKnight, Asays),
    Biconditional(BKnight, Bsays),
    Biconditional(CKnight, Csays)
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
