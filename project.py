import copy
import os
from itertools import product
class STATE:    

    def __init__(self,name) :
        self.name = name

    def Name(self):
        print(self.name)


class NFA:
    def __init__(self,*args) :

        #############################
        self.states = set()         #
        self.alphabets = set()      #
        self.F = set()              #
        self.S = set()              #
        self.TF = dict()            #
        #############################

        if(len(args)==1):
            self.cons1(args)
        elif(len(args)==2):
            self.cons2(args)
        elif(len(args)==3):
            self.cons3(args)



    # constructor to be used when the NFA is made using only string
    def cons1 (self,args):
        self.states = set(range(len(args[0])+1))
        self.alphabets = set()
        self.TF = dict()
        for i in range(len(args[0])):
            self.alphabets.add(args[0][i])
            self.TF[(i,args[0][i])] = {i+1}
        self.S = {0}
        self.F = {len(args[0])}

    def cons3 (self,args):
        if(args[2] == "+"):
            self.S = {0}
            self.alphabets = args[0].alphabets | args[1].alphabets
            self.states = set(range(len(args[0].states)+len(args[1].states)+1))
            for (q,a) , sts in args[0].TF.items():
                self.TF[(q+1,a)] = set([s+1 for s in sts])
            l = len(args[0].states)
            for (q,a) , sts in args[1].TF.items():
                self.TF[(q+1+l,a)] = set([s+l+1 for s in sts])

            self.TF[(0,"ε")] = set([s+1 for s in args[0].S]) | set([s+l+1 for s in args[1].S])
            self.F = set([s+1 for s in args[0].F]) | set([s+l+1 for s in args[1].F])
        
        elif(args[2] == "."):
            self.S = copy.deepcopy(args[0].S)
            self.alphabets = args[0].alphabets | args[1].alphabets
            self.states = set(range(len(args[0].states)+len(args[1].states)))
            
            for (q,a),sts in args[0].TF.items():
                self.TF[(q,a)] = set([s for s in sts])

            l = len(args[0].states)
            for (q,a),sts in args[1].TF.items():
                self.TF[(q+l,a)] = set([s+l for s in sts])
            
            # print(self.TF)
            for f in args[0].F:
                if (f,"ε") in self.TF.keys():
                    self.TF[(f,"ε")] |= set([s+l for s in args[1].S])
                else:
                    self.TF[(f,"ε")] = set([s+l for s in args[1].S])
            # print(self.TF)
            self.F = set([s+l for s in args[1].F])
        else:
            print("Invalid NFA contruction")

    def cons2(self,args):
        if (args[1]=="*"):
            self.S = {0}
            self.alphabets = args[0].alphabets 
            self.states = set(range(len(args[0].states)+1))
            for (q,a) , sts in args[0].TF.items():
                self.TF[(q+1,a)] = set([s+1 for s in sts])

            self.TF[(0,"ε")] = set([s+1 for s in args[0].S]) 
            self.F = set([s+1 for s in args[0].F]) | {0}
            for f in self.F:
                if (f,"ε") in self.TF.keys():
                    self.TF[(f,"ε")] |= set([s+1 for s in args[0].S])
                else:
                    self.TF[(f,"ε")] = set([s+1 for s in args[0].S])

        else:
            print("Invalid NFA construction")



    def __str__(self):
        return f"states = {self.states}\n alphabets = {self.alphabets}\n TF = {self.TF}\n S = {self.S}\n F = {self.F}"
    
    def DELTA(self,stateAndAlpha):
        (s,i) = stateAndAlpha
        
        # if(s,"ε") in self.TF.keys():
        #     etrans = self.TF[(s,"ε")]    
        if stateAndAlpha in self.TF.keys():
            if (i=="ε"):
                return self.TF[stateAndAlpha] | {s}
            return self.TF[stateAndAlpha] 
        else:
            return set() 
    
    def addEpslnTrans(self,S):
        states = copy.deepcopy(S)
        flag = 1
        # adding ε transitions
        while (flag==1):
            flag=0
            for s in states:
                if((s,"ε") in self.TF.keys()):
                    epsilonSet = self.DELTA((s,"ε"))
                    if(epsilonSet & states != epsilonSet):
                        flag=1
                        states = copy.deepcopy(states | epsilonSet)
        return states
        

    def check(self,string):
        states = copy.deepcopy(self.S)
        nextStates = set()
        
        for i in string:
            states = self.addEpslnTrans(states)
            for s in list(states):
                nextStates  = copy.deepcopy(nextStates | self.DELTA((s,i)))
            
            states = copy.deepcopy(nextStates)
            nextStates = set()
            
        states = self.addEpslnTrans(states)
        if states.intersection(self.F)==set():
            return False
        else:
            return True

def splitAtComm(str):                             # This function is used to extract the two regular expression in concat(), union() etc
    count = 0
    ifFind = 0
    l = len(str)
    for i in range(l):
        if(count < 0):
            print("Invalid Expression")
            return "",""
        if(str[i]=="("):
            count+=1
        elif(str[i]==")"):
            count-=1
        elif(str[i]=="," and count == 0):
            ifFind = 1
            break
    if(ifFind == 0):
        print("Invalid Expression")
        return "",""
    return str[:i] , str[i+1:]

# converts a regular expression to a NFA
def regToNFA (regExp):
    l = len(regExp)
    regExp = regExp.replace(" ","")
    bPos = regExp.find("(")                     # bPos contains the location of first "(" bracket
    if(bPos == -1 or regExp[-1]!= ")"):         # if there is no "(" or no ")" at the end print invalid expression 
        print("Invalid Expression")
        return 
    else:
        if(regExp[:bPos]=="symbol"):
            # return regExp[bPos+1:-1]
            return NFA(regExp[bPos+1:-1])
        elif (regExp[:bPos]=="star"):
            # return "("+regToNFA(regExp[bPos+1:-1])+"*"+")"
            return NFA(regToNFA(regExp[bPos+1:-1]),"*")
        elif (regExp[:bPos]=="concat"):
            s1,s2 = splitAtComm(regExp[bPos+1:-1])
            # return "("+regToNFA(s1)+"."+regToNFA(s2)+")"
            return NFA(regToNFA(s1),regToNFA(s2),".")
        elif (regExp[:bPos]=="union"):
            s1,s2 = splitAtComm(regExp[bPos+1:-1])
            # return "("+regToNFA(s1)+"+"+regToNFA(s2)+")"
            return NFA(regToNFA(s1),regToNFA(s2),"+")

class DFA:
    def __init__(self,*args):
        
        self.states = set()
        self.alphabets =set()
        self.TF = dict()
        self.S = set()
        self.F = set()

        if(len(args)==5):
            self.cons1(args)
        elif(len(args)==2):
            if(args[1]=="c"):
                self.cons2(args)
        elif(len(args)==3):
            if(args[2]=="i"):
                self.cons3(args)

    def __str__(self):
        return f" states = {self.states}\n alphabets = {self.alphabets}\n TF = {self.TF}\n S = {self.S}\n F = {self.F}"

    def cons1(self,args):
        self.states = args[0]
        self.alphabets = args[1]
        self.TF = args[2]
        self.S = args[3]
        self.F = args[4]

    def cons2(self,args):
        self.states = args[0].states
        self.alphabets = args[0].alphabets
        self.TF = args[0].TF
        self.S = args[0].S
        self.F = args[0].states - args[0].F

    def makeStatesToInt (self):
        statToInt = dict()
        nState = len(self.states)
        i=0

        newStates = set()
        newF = set()
        newTF = dict()

        for s in self.states:
            newStates |= {i}
            statToInt[s] = i
            i+=1
        
        newS = statToInt[self.S]
        for f in self.F:
            newF |= {statToInt[f]}

        for (key,a),val in self.TF.items():
            newTF[(statToInt[key],a)] = statToInt[val]

        self.states = newStates
        self.S = newS
        self.TF = newTF
        self.F = newF

    def cons3(self,args):
        dfa1 = args[0]
        dfa2 = args[1]
        self.states = set(product(dfa1.states,dfa2.states))
        self.alphabets = dfa1.alphabets & dfa2.alphabets
        self.S = (dfa1.S,dfa2.S)
        self.F = set(product(dfa1.F,dfa2.F))

        for (i,j) in self.states:
            for a in self.alphabets:
                self.TF[((i,j),a)] = (dfa1.TF[(i,a)],dfa2.TF[(j,a)])

        self.makeStatesToInt()

    

    def delta (self,stateAndAlpha):
        (s,i) = stateAndAlpha
          
        if (i=="ε"):
            return s

        if stateAndAlpha in self.TF.keys():
            
            return self.TF[stateAndAlpha] 
        else:
            return -1

    def complement(self,dfa):
        self.states = dfa.states
        self.alphabets = dfa.alpabets
        self.delta = dfa.alphabets
        self.S = dfa.S
        self.F = dfa.states - dfa.F

    def check(self,string):
        state = self.S
        for a in string:
            state = self.delta((state,a))

        if(state in self.F):
            return True
        else:
            return False


def NFAtoDFA(nfa):
    
    #############################
    states = set()
    TF = dict()
    alphabets = nfa.alphabets
    S = 0
    F = set()
    #############################

    states |= {S}

    Sno = 1
    StoSetMap = dict()
    StoSetMap[0] = nfa.addEpslnTrans(nfa.S)

    while (1):
        flag = 0
        newStates = set()
        for sno in states:
            state = StoSetMap[sno]
            for a in nfa.alphabets:
                if((sno,a) not in TF.keys()):
                    # print(state,",",a)          #############
                    flag = 1
                    nextState = set()
                    
                    for s in state:
                        nextState |= nfa.DELTA((s,a))
                    nextState = nfa.addEpslnTrans(nextState)
                    # print(nextState,"\n")      #############

                    if(nextState not in StoSetMap.values()):
                        TF[(sno,a)] = Sno   
                        newStates |= {Sno}
                        StoSetMap[Sno] = nextState
                        Sno+=1
                    else:
                        key = [i for i in StoSetMap.keys() if StoSetMap[i]==nextState]
                        TF[(sno,a)] = key[0]
        states |= newStates
        if(flag==0):
            break

    for key,values in StoSetMap.items():
        if (values & nfa.F != set()):
            F |= {key}
    return DFA(states,alphabets,TF,S,F)

def MinimizeDFA(dfa):
    
    #############################
    states  = set()
    TF = dict()
    alphabets = dfa.alphabets
    S = set()
    F = set()
    #############################
    l = len(dfa.states)
    mark = [ [0]*(i+1) for i in range(l-1)]
    for i in range(l-1):
        for j in range(i+1):
            if (j in dfa.F) and (i+1 not in dfa.F):
                # print(".",i,j+1)
                mark[i][j] = 1 
            elif (j not in dfa.F) and (i+1 in dfa.F):
                # print(",",i,j+1)
                mark[i][j] = 1
            else:
                # print(i,j+1)
                mark[i][j] = 0


    while(1):
        flag = 0
        for i in range(l-1):
            for j in range(i+1):
                if(mark[i][j]==0):
                    for a in dfa.alphabets:                 #optimization can be done for the number of loops
                        n1 = dfa.TF[(j,a)]
                        n2 = dfa.TF[(i+1,a)]
                        if(n1>n2):
                            if(mark[n1-1][n2]==1):
                                flag = 1
                                mark[i][j] = 1
                        elif(n2>n1):
                            if(mark[n2-1][n1]==1):
                                flag = 1
                                mark[i][j] = 1
        if(flag==0):
            break
        
    # print(0)                            #############
    # for i in range(l-1):
    #     print(mark[i],i+1)

    newstateList = list()
    statemergedStat = [0 for i in range(l)]
    for i in range(l-1):
        for j in range(i+1):
            if(mark[i][j]==0):
                if(statemergedStat[i+1]==0 and statemergedStat[j]==0):
                    statemergedStat[i+1] = 1
                    statemergedStat[j] = 1
                    newstateList += [{j,i+1}]
                
                if(statemergedStat[i+1]==1 and statemergedStat[j]==0):
                    statemergedStat[j] = 1
                    group = set()
                    for ns in newstateList:
                        if ns & {i+1} != set():
                            group = ns
                    if(group != set()):
                        newstateList.remove(group)
                    else:
                        print("group is null set")
                    newstateList += [group | {j}]

                if(statemergedStat[i+1]==0 and statemergedStat[j]==1):
                    statemergedStat[i+1] = 1
                    group = set()
                    for ns in newstateList:
                        if ns & {j} != set():
                            group = ns
                    if(group != set()):
                        newstateList.remove(group)
                    else:
                        print("group is null set")
                    newstateList += [group | {i+1}]
    
                if(statemergedStat[i+1]==1 and statemergedStat[j]==1):
                    statemergedStat[j] = 1
                    group = set()
                    group2 = set()
                    for ns in newstateList:
                        if ns & {i+1} != set():
                            group = ns
                        elif ns & {j} != set():
                            group2 = ns

                    if(group != set()):
                        newstateList.remove(group)
                    if(group2 != set()):
                        newstateList.remove(group2)

                    newstateList += [group | group2]
    for i in range(l):
        if(statemergedStat[i]==0):
            newstateList += [{i}]
    
    newstateList.reverse()
    newStateNames = dict()

    for i in range(len(newstateList)):
        for j in newstateList[i]:
            newStateNames[j] = i

    for key,val in dfa.TF.items():
        TF[(newStateNames[key[0]],key[1])] = newStateNames[val]
    
    #finding the F,S,alphbates,TF,states

    for f in dfa.F:
        F |= {newStateNames[f]}
    S = newStateNames[dfa.S]
    states = set(range(len(newstateList)))

    #Removing non reachable states

    flag1 = 1
    while(flag1==1):
        flag1==1
        stateToRemove = (states - set(TF.values())) - {S}
        
        if(stateToRemove == set()):
            flag1 = 0
        
        if(flag1==1):
            for sToRem in stateToRemove:
                for a in alphabets:
                    del TF[(sToRem,a)]
        
        F -= stateToRemove
        states -= stateToRemove

    return DFA(states,alphabets,TF,S,F)


# # print("1")
# n1 = regToNFA("star(symbol(a))")
# # print(n1.check("aaaa"))

# # print()
# # print("2")
# n2 = regToNFA("concat(star(symbol(b)),symbol(a))")
# # print(n2.check("a"))

# # print()
# # print("3")
# n3 = regToNFA("concat(star(symbol(a)),union(symbol(b),symbol(c)))")
# # print(n3.check("aaaac"))

# # print()
# # print("4")
# n4 = regToNFA("concat(star(union(symbol(a),union(symbol(b),symbol(c)))),symbol(d))")
# # print(n4.check("abccbabad"))

# # print()
# # print("5")
# n5 = regToNFA("concat(concat(symbol(0),symbol(1)),star(union(symbol(0),symbol(1))))")
# # print(n5.check("01011"))
# # # print("ε")

# n6 = NFA("aabcbabd")
# d = NFAtoDFA(n2)
# d1 = NFAtoDFA(n5)
# # print(d1)
# # print(d3)
# choice = 'y'
# # while (choice != 'n' or choice != 'N'):
# #     print(d3.check(input("string: ")),"\n")
# #     # choice = input("choice: ")

# # mindfa = MinimizeDFA(d)
# # print(mindfa)
# # while (choice != 'n' or choice != 'N'):
# #     print(mindfa.check(input("string: ")),"\n")



# # dcomp = MinimizeDFA(DFA(d,d1,"i"))
# # # dcomp = DFA(d,d1,"i")
# # print(dcomp)
# # while (choice != 'n' or choice != 'N'):
# #     print(dcomp.check(input("string: ")),"\n")

# # testlocation = "tests/"
# # testcase = os.listdir(testlocation)
# # print("number of test files:",len(testcase))
# # total = 0
# # for tc in testcase:
# #     file = open(testlocation+tc,"r")
# #     file1 = open("testout/"+tc,"w")
# #     l = int(input())
# #     total+=l
# #     for i in range(l):
# #         regExp = file.readline()
# #         string = file.readline()
# #         # print(string)
# #         nfa = regToNFA(regExp=regExp[:-1])
# #         dfa = NFAtoDFA(nfa)
# #         mindfa = MinimizeDFA(dfa)
# #         t = mindfa.check(string[:-1])
# #         if(t):
# #             file1.write("Yes\n")
# #         else:
# #             file1.write("No\n")


# #     file.close()
# #     file1.close()

# # print("total number of testcases:",total)

def setAlphabets(str):

    setAlphas = set()
    for s in str:
        setAlphas |= {s}

    return setAlphas


if __name__ ==  "__main__":
    l = int(input())
    for i in range(l):
        nope = False

        regExp = input()
        string = input()
        # print(string)
        nfaRegExp = regToNFA(regExp=regExp)
        dfaReg = NFAtoDFA(nfaRegExp)
        cDfa = DFA(dfaReg,"c")
        minDfaReg = MinimizeDFA(cDfa)

        nfaString = NFA(string)
        dfaStr = NFAtoDFA(nfaString)
        mindfaStr = MinimizeDFA(dfaStr)

        # We have to make sure the input string does not contain any string not in the 
        # alphabet set of regular expression, If input string does contain some string 
        # Not in the regular expression, then number of final state of the inersection 
        # need not be null set {set()}.
        alphabetsInString = setAlphabets(string)
        if((alphabetsInString - dfaReg.alphabets) != set()):
            nope = True

        IntersecionDfa = MinimizeDFA(DFA(minDfaReg,mindfaStr,"i"))

        
        if(IntersecionDfa.F == set() and nope == False):
            print("Yes")
        else:
            print("No")