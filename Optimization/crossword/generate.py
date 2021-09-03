import sys

from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        w, h = draw.textsize(letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        for var, var_domain in self.domains.items():
            for d in list(var_domain):
                if len(d) != var.length:
                    self.domains[var].remove(d)

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        revised = False

        overlap = self.crossword.overlaps[x, y]

        if overlap is None:
            return revised

        for dx in list(self.domains[x]):
            check = 0
            for dy in self.domains[y]:
                if dy[overlap[1]] == dx[overlap[0]]:
                    check += 1
            if check == 0:
                self.domains[x].remove(dx)
                revised = True
        
        return revised
    
    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        queue = list()

        if arcs is None:
            for overlap in self.crossword.overlaps:
                if self.crossword.overlaps[overlap] is not None:
                    queue.append(overlap)
        else:
            queue = arcs

        # #Removing overlap arcs
        # for q1 in list(queue):
        #     for q2 in list(queue):
        #         if q1[0] == q2[1] and q1[1] == q2[0]:
        #             queue.remove(q1)

        while queue:
            arc = queue.pop()
            if self.revise(arc[0], arc[1]):
                if len(self.domains[arc[0]]) == 0:
                    return False
                #For each z in x neighbors except y
                for z in self.crossword.neighbors(arc[0]):
                    if z != arc[1]:
                        queue.append((z, arc[0]))

        return True

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        if len(assignment) == len(self.crossword.variables):
            return True
        
        return False

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        constraints = list()

        for overlap in self.crossword.overlaps:
            if self.crossword.overlaps[overlap] is not None:
                constraints.append(overlap)

        for (x, y) in constraints:
            # Only consider arcs where both are assigned
            if x not in assignment or y not in assignment:
                continue

            if len(assignment[x]) != x.length or len(assignment[y]) != y.length:
                return False

            overlap = self.crossword.overlaps[x, y]
            if assignment[x][overlap[0]] != assignment[y][overlap[1]]:
                return False

        #Check if there are duplicate words in the assignment values
        assign_var = list(assignment.values())
        if len(assign_var) != len(set(assign_var)):
            return False

        # If nothing inconsistent, then assignment is consistent
        return True



    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        sorted_var_domain = list()

        var_domain = list(self.domains[var])

        var_neighbors = self.crossword.neighbors(var)

        temp = dict()
        for value in var_domain:
            count = 0
            for neighbor in var_neighbors:
                overlap = self.crossword.overlaps[var, neighbor]
                for neighbor_value in self.domains[neighbor]:
                    if value[overlap[0]] != neighbor_value[overlap[1]]:
                        count += 1
                    if value == neighbor_value:
                        count += 1
            temp[value] = count

        sorted_var_domain = list(dict(sorted(temp.items(), key=lambda x: x[1], reverse=False)).keys())

        return sorted_var_domain

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        var_min = None

        min_domain = 1000000
        for var in self.crossword.variables:
            if var not in assignment:
                if len(self.domains[var]) < min_domain:
                    var_min = var
                    min_domain = len(self.domains[var])
        
        return var_min

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        # Check if assignment is complete
        if len(assignment) == len(self.crossword.variables):
            return assignment
        
        # Try a new variable
        var = self.select_unassigned_variable(assignment)
        for value in self.order_domain_values(var, assignment):
            new_assignment = assignment.copy()
            new_assignment[var] = value
            if self.consistent(new_assignment):
                result = self.backtrack(new_assignment)
                if result is not None:
                    return result
        
        return None


def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
