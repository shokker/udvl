import tableau

class TableauBuilder(object):
    def build(self, signedFormulas):
        """ Vytvori a vrati uzavrete alebo uplne tablo pre zoznam oznacenych formul. """
        alphas = list()
        betas = list()
        branch = dict()
        # vyplnime prve vrcholy podla zoznamu vstupnych formul
        self.tabl = tableau.Tableau()
        lastNode = None
        closed = False
        
        for sign, formula in signedFormulas:
            newNode = tableau.Node(sign, formula)
            if self.append(lastNode, newNode, alphas, betas, branch):
                closed = True
            lastNode = newNode

        if not closed:
            self.expand(lastNode, alphas, betas, branch)
        
        

        return self.tabl
    
    def expand(self, node, alphas, betas, branch):
        lastNode = node
        for n in alphas:
            for sign, formula in n.formula.signedSubf(n.sign):
                newNode = tableau.Node(sign, formula, n)
                if self.append(lastNode, newNode, alphas, betas, branch):
                    return
                lastNode = newNode
        # minuli sa alfy, treba betu
        if betas:
            beta = betas.pop()
            for sign, formula in beta.formula.signedSubf(beta.sign):
                newNode = tableau.Node(sign, formula, beta)
                newAlphas = list()
                betasCopy = betas[:]
                branchCopy = dict((k,l[:]) for (k,l) in branch.items())
                self.append(lastNode, newNode, newAlphas, betasCopy, branchCopy)
                self.expand(newNode, newAlphas, betasCopy, branchCopy)

        
    def append(self, parent, node, alphas, betas, branch):
        self.tabl.append(parent, node)
        if node.formula.getType(node.sign) == tableau.ALPHA:
            alphas.append(node)
        elif node.formula.getType(node.sign) == tableau.BETA:
            betas.append(node)
        strFormula = node.formula.toString()
        if not strFormula in branch:
            branch[strFormula] = list()
        branch[strFormula].append(node) 


        for n in branch[strFormula]:
            if n.sign == (not node.sign):
                node.close(n)
                return True
        return False


    
# vim: set sw=4 ts=8 sts=4 et :
