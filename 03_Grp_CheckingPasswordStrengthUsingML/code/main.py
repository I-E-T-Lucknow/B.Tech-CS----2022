from flask import Flask, render_template, flash, request
from sklearn.externals import joblib

app = Flask(__name__)

@app.route('/')
def homepage():
    return render_template('index.html')


@app.route('/main/', methods=['GET', 'POST'])
def mainpage():
    if request.method == "POST":
        enteredPassword = request.form['password']
    else:
        return render_template('index.html')

    # Load the algorithm models
    DecisionTree_Model = joblib.load('DecisionTree_Model.joblib')
    
    Password = [enteredPassword]

    # Predict the strength
    DecisionTree_Test = DecisionTree_Model.predict(Password)
    
    return render_template("main.html", DecisionTree=DecisionTree_Test)

if __name__ == "__main__":
    app.run(debug=True)

class TrieNode:
    
    # Trie node class
    def __init__(self):
        self.children = [None]*26

       
        self.isEndOfWord = False

class Trie:
    
    
    def __init__(self):
        self.root = self.getNode()

    def getNode(self):
    
        
        return TrieNode()

    def _charToIndex(self,ch):
        
        return ord(ch)-ord('a')


    def insert(self,key):
        
    
        pCrawl = self.root
        length = len(key)
        for level in range(length):
            index = self._charToIndex(key[level])

            if not pCrawl.children[index]:
                pCrawl.children[index] = self.getNode()
            pCrawl = pCrawl.children[index]

        # mark last node as leaf
        pCrawl.isEndOfWord = True

    def search(self, key):
        
        pCrawl = self.root
        length = len(key)
        for level in range(length):
            index = self._charToIndex(key[level])
            if not pCrawl.children[index]:
                return False
            pCrawl = pCrawl.children[index]

        return pCrawl.isEndOfWord

def main():

    keys = []
    output = []

    t = Trie()

    for key in keys:
        t.insert(key)



class PasswordFeature:
    def PasswordFeature(self, root: 'TreeNode', p: 'TreeNode', q: 'TreeNode') -> 'TreeNode':
        stack = [root]
        parent = {root: None}
        while stack:
            node = stack.pop()
            if node.left:
                parent[node.left] = node
                stack.append(node.left)
            if node.right:
                parent[node.right] = node
                stack.append(node.right)
        ancestors = set()
        while p:
            ancestors.add(p)
            p = parent[p]
        while q not in ancestors:
            q = parent[q]
        return q



class PasswordFeature:
    def PasswordFeature(self, root: 'TreeNode', p: 'TreeNode', q: 'TreeNode') -> 'TreeNode':

        if  root == None or root == p or root == q :
            return root
        
        left = self.PasswordFeature(root.left, p, q)
        right = self.PasswordFeature(root.right, p, q)
        
        if left and right:
            return root
        print(root.val,left, right)
        return left if left  else right


def getsum(BITTree,i):
    s = 0

    i = i+1

    while i > 0:

        s += BITTree[i]

        i -= i & (-i)
    return s

def updatebit(BITTree , n , i ,v):

    i += 1

    while i <= n:

        BITTree[i] += v
        i += i & (-i)


def construct(arr, n):

    BITTree = [0]*(n+1)

    for i in range(n):
        updatebit(BITTree, n, i, arr[i])
    return BITTree
