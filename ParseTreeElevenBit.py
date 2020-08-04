from Node import Node
import random
import queue

nodes = ['a0', 'a1', 'a2', 'd0', 'd1', 'd2', 'd3', 'd4', 'd5', 'd6', 'd7', 'and', 'or', 'if', 'not']

class ParseTree:

  def __init__(self, kind, Dmax):
    self.fit = 0
    if kind == 'full':
      self.full(Dmax)  # full tree gen
    else:
      self.grow(Dmax)  # grow tree gen
    self.fit = self.fitness()

  # Initializes tree with 'grow' method
  def grow(self, Dmax):
    q1 = queue.Queue(-1)
    q2 = queue.Queue(-1)
    tempIndex = random.randint(0, 14)
    temp = None
    if tempIndex < 11:
      temp = Node('t', nodes[tempIndex])
    else:
      temp = Node('f', nodes[tempIndex])
    self.head = temp
    curr = self.head
    if curr.kind == 'f':
      q1.put(curr)
    depth = 2
    while ((not q1.empty()) or (not q2.empty())) and depth <= Dmax:
      if depth < Dmax:  # Generate function or terminal for each
        if q1.empty():
          while not q2.empty():
            curr = q2.get()
            for i in range(len(curr.children)):  # Generate appropriate number of child function nodes
              tempIndex = random.randint(0, 14)
              if tempIndex < 11:
                temp = Node('t', nodes[tempIndex])
              else:
                temp = Node('f', nodes[tempIndex])
                q1.put(temp)
              curr.children[i] = temp
        else:
          while not q1.empty():
            curr = q1.get()
            for i in range(len(curr.children)):  # Generate appropriate number of child function nodes
              tempIndex = random.randint(0, 14)
              if tempIndex < 11:
                temp = Node('t', nodes[tempIndex])
              else:
                temp = Node('f', nodes[tempIndex])
                q2.put(temp)
              curr.children[i] = temp
      else:  # Generate terminals for each
        if q1.empty():
          while not q2.empty():
            curr = q2.get()
            for i in range(len(curr.children)):  # Generate appropriate number of child terminal nodes
              tempIndex = random.randint(0, 10)
              temp = Node('t', nodes[tempIndex])
              curr.children[i] = temp
        else:
          while not q1.empty():
            curr = q1.get()
            for i in range(len(curr.children)):  # Generate appropriate number of child terminal nodes
              tempIndex = random.randint(0, 10)
              temp = Node('t', nodes[tempIndex])
              curr.children[i] = temp
      depth += 1

  # Initializes tree with 'full' method
  def full(self, Dmax):
      q1 = queue.Queue(-1)
      q2 = queue.Queue(-1)
      if Dmax == 1:
        tempIndex = random.randint(0, 10)
      else:
        tempIndex = random.randint(11, 14)
      temp = None
      if tempIndex < 11:
        temp = Node('t', nodes[tempIndex])
      else:
        temp = Node('f', nodes[tempIndex])
      self.head = temp
      curr = self.head
      q1.put(curr)
      depth = 2
      while ((not q1.empty()) or (not q2.empty())) and depth <= Dmax:
        if depth < Dmax:  # Generate functions for each
          if q1.empty():
            while not q2.empty():
              curr = q2.get()
              for i in range(len(curr.children)):  # Generate appropriate number of child function nodes
                tempIndex = random.randint(11, 14)
                temp = Node('f', nodes[tempIndex])
                curr.children[i] = temp
                q1.put(temp)
          else:
            while not q1.empty():
              curr = q1.get()
              for i in range(len(curr.children)):  # Generate appropriate number of child function nodes
                tempIndex = random.randint(11, 14)
                temp = Node('f', nodes[tempIndex])
                curr.children[i] = temp
                q2.put(temp)
        else:  # Generate terminals for each
          if q1.empty():
            while not q2.empty():
              curr = q2.get()
              for i in range(len(curr.children)):  # Generate appropriate number of child terminal nodes
                tempIndex = random.randint(0, 10)
                temp = Node('t', nodes[tempIndex])
                curr.children[i] = temp
          else:
            while not q1.empty():
              curr = q1.get()
              for i in range(len(curr.children)):  # Generate appropriate number of child terminal nodes
                tempIndex = random.randint(0, 10)
                temp = Node('t', nodes[tempIndex])
                curr.children[i] = temp
        depth += 1

  # Recombination with another tree
  def recombine(self, other, p):
    curr = self.head  # Choose a head for subtree to switch
    ind1 = 9
    while curr.kind != 't':
      ind1 = random.choice([i for i in range(len(curr.children))])
      tempChild = curr.children[ind1]
      if random.random() < p:  # Lock subtree to switch (tempChild)
        break
      else:
        if curr.children[ind1].kind == 't':  # Lock terminal node to switch if that is the next one, and none is chosen yet
          break
        curr = curr.children[ind1]  # Move down tree

    curr2 = other.head  # Same as above for other tree
    ind2 = 9
    while curr2.kind != 't':
      ind2 = random.choice([i for i in range(len(curr2.children))])
      tempChild2 = curr2.children[ind2]
      if random.random() < p:  # Lock subtree to switch (tempChild2)
        break
      else:
        if curr2.children[
          ind2].kind == 't':  # Lock terminal node to switch if that is the next one, and none is chosen yet
          break
        curr2 = curr2.children[ind2]  # Move down tree

    # Switch subtrees
    if ind1 != 9 and ind2 != 9:  # normal case - both trees have depth > 1
      curr.children[ind1] = tempChild2
      curr2.children[ind2] = tempChild
    elif ind1 == 9 and ind2 != 9:  # if only calling tree has depth = 1
      self.head = tempChild2
      curr2.children[ind2] = curr
    elif ind2 == 9 and ind1 != 9:  # if only other tree has depth = 1
      other.head = tempChild
      curr.children[ind1] = curr2
    else:  # if both trees have depth = 1
      self.head = curr2
      other.head = curr

  # p is the chance that a given node will be the point of mutation
  def mutate(self, p):
    curr = self.head
    if random.random() < 0.5:
      tempTree = ParseTree('grow', 3)
    else:
      tempTree = ParseTree('full', 3)
    while curr.kind != 't':
      if random.random() < p:
        curr.children[random.choice([i for i in range(len(curr.children))])] = tempTree.head
        return
      else:
        tempIndex = random.choice([i for i in range(len(curr.children))])
        if curr.children[tempIndex].kind == 't':  # Replace with mutation anyways if terminal is reached and nothing replace yet
          curr.children[tempIndex] = tempTree.head
          return
        curr = curr.children[tempIndex]  # Move down tree

  # Returns string rep of tree
  def __str__(self):
    q1 = queue.Queue(-1)
    q2 = queue.Queue(-1)
    curr = self.head
    q1.put(curr)
    string = ""
    while (not q1.empty()) or (not q2.empty()):
      if q1.empty(): # print nodes from q2
        while not q2.empty():
          temp = q2.get()
          # then put all of temp's children into q1
          if temp.children is not None:
            for i in range(len(temp.children)):
              q1.put(temp.children[i])
          string += " " + temp.val
      else:
        while not q1.empty():
          temp = q1.get()
          # then put all of temp's children into q2
          if temp.children is not None:
            for i in range(len(temp.children)):
              q2.put(temp.children[i])
          string += " " + temp.val
      string += "\n"
    return string

  # Return fitness of tree (number of test cases passed, where max is undefined - but over 100 passed in GOOD)
  def fitness(self):
    sum = 0
    for a0 in range(2):
      for a1 in range(2):
        for a2 in range(2):
          for d0 in range(2):
            for d1 in range(2):
              for d2 in range(2):
                for d3 in range(2):
                  for d4 in range(2):
                    for d5 in range(2):
                      for d6 in range(2):
                        for d7 in range(2):
                          if random.random() < 0.05:  # Use only 5% of cases (otherwise too expensive)
                            if self.evalTree(self.head, a0, a1, a2, d0, d1, d2, d3, d4, d5, d6, d7) == self.dVal(a0, a1, a2, d0, d1, d2, d3, d4, d5, d6, d7):
                              sum += 1
    return sum

  # Return corresponding d bit value given terminal values
  def dVal(self, a0, a1, a2, d0, d1, d2, d3, d4, d5, d6, d7):
    if (not a0) and (not a1) and (not a2):
      return d0
    elif (not a0) and (not a1) and a2:
      return d1
    elif (not a0) and a1 and (not a2):
      return d2
    elif (not a0) and a1 and a2:
      return d3:
    elif a0 and (not a1) and (not a2):
      return d4
    elif a0 and (not a1) and a2:
      return d5
    elif a0 and a1 and (not a2):
      return d6
    else:
      return d7

  # Evaluate the tree given terminal values
  def evalTree(self, curr, a0, a1, a2, d0, d1, d2, d3, d4, d5, d6, d7):
    if curr.kind == 'f':
      if curr.val == 'and':
        return self.evalTree(curr.children[0], a0, a1, d0, d1, d2, d3, d4, d5, d6, d7) and self.evalTree(curr.children[1], a0, a1, d0, d1, d2, d3, d4, d5, d6, d7)
      elif curr.val == 'or':
        return self.evalTree(curr.children[0], a0, a1, d0, d1, d2, d3, d4, d5, d6, d7) or self.evalTree(curr.children[1], a0, a1, d0, d1, d2, d3, d4, d5, d6, d7)
      elif curr.val == 'if':
        if self.evalTree(curr.children[0], a0, a1, d0, d1, d2, d3, d4, d5, d6, d7):
          return self.evalTree(curr.children[1], a0, a1, d0, d1, d2, d3, d4, d5, d6, d7)
        else:
          return self.evalTree(curr.children[2], a0, a1, d0, d1, d2, d3, d4, d5, d6, d7)
      else: # not
        return not self.evalTree(curr.children[0], a0, a1, d0, d1, d2, d3, d4, d5, d6, d7)
    else:
      if curr.val == 'a0':
        return a0
      elif curr.val == 'a1':
        return a1
      elif curr.val == 'a2':
        return a2
      elif curr.val == 'd0':
        return d0
      elif curr.val == 'd1':
        return d1
      elif curr.val == 'd2':
        return d2
      elif curr.val == 'd3':
        return d3
      elif curr.val == 'd4':
        return d4
      elif curr.val == 'd5':
        return d5
      elif curr.val == 'd6':
        return d6
      else:
        return d7
      
  # Returns FULL fitness - number of correct test cases out of entire set of 2048
  def fullFitness(self):
    sum = 0
    for a0 in range(2):
      for a1 in range(2):
        for a2 in range(2):
          for d0 in range(2):
            for d1 in range(2):
              for d2 in range(2):
                for d3 in range(2):
                  for d4 in range(2):
                    for d5 in range(2):
                      for d6 in range(2):
                        for d7 in range(2):
                          if self.evalTree(self.head, a0, a1, a2, d0, d1, d2, d3, d4, d5, d6, d7) == self.dVal(a0, a1, a2, d0, d1, d2, d3, d4, d5, d6, d7):
                            sum += 1
    return sum
