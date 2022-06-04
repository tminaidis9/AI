class Stack:

    def __init__(self, name):
        self.StackList = [] #h list sthn opoia tha kratame ta stoixeia ths stack
        self.Stackname = name
        print('New Stack %s created'%(name))

    def empty(self):
        for i in range(1,len(self.StackList)): #gia kathe stoixeio ths stack
            print(f"{self.StackList[-1]} popped out") 
            self.pop() #kanw pop     
        print('Now Stack is empty')

    def push(self, NewElement):
        self.StackList.append(NewElement) #prosthesi antikeimenoy sthn lista
        print(NewElement,'inserted into Stack')

    def pop(self):
        print(self.StackList[-1],'popped out')
        self.StackList.remove(self.StackList[-1]) #afairesh antikeimenou apo thn lista
        
#main
MyStack =Stack('MyStack')
MyString = input()
for i in MyString:
    MyStack.push(i)
MyStack.empty()

#strings for trial:
# ({[]})
# {[()]}
# (){}
