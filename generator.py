import sys
import AST
from AST import addToClass, Node
import svgwrite


@addToClass(AST.InstructionsNode)
def generate(self):
    spacing = 50
    leftMargin = 20
    
    Node.xPos = Node.xPos + leftMargin
    
    group = Node.dwg.g()
    for child in self.children:
        group.add(child.generate())
        Node.yPos = Node.yPos + Node.outerHeight + spacing
    return group

@addToClass(AST.InstructionNode)
def generate(self):
    parentX = Node.xPos
    parentY = Node.yPos
    group = Node.dwg.g()
    
    # create instruction body
    instructionBodyNode = self.children[1].generate()
    group.add(instructionBodyNode)
    instructionBodyHeight = Node.outerHeight
    instructionBodyWitdth = Node.outerWidth
    
    # create methode field
    Node.xPos = Node.xPos + instructionBodyWitdth
    methodNode = self.children[2].generate()
    group.add(methodNode)
    methodHeight = Node.outerHeight
    methodWitdth = Node.outerWidth
    
    # create returning field
    Node.xPos = Node.xPos + methodWitdth
    returingNode = self.children[0].generate()
    returningHeight = Node.outerHeight
    group.add(returingNode)
    
    maxHeight = max(instructionBodyHeight, methodHeight, returningHeight)
    
    instructionBodyNode.translate(tx=0, ty=(maxHeight - instructionBodyHeight)/2 )
    methodNode.translate(tx=0, ty=(maxHeight - methodHeight)/2 )
    returingNode.translate(tx=0, ty=(maxHeight - returningHeight)/2 )
    
    Node.outerHeight = maxHeight
    Node.xPos = parentX
    Node.yPos = parentY
    
    return group

@addToClass(AST.InstructionBodyNode)
def generate(self):
    parentY = Node.yPos
    group = Node.dwg.g()

    outerWidths = []
    incredients = []
    for child in self.children:
        incredients.append(child.generate())
        Node.yPos = Node.yPos + Node.outerHeight
        outerWidths.append(Node.outerWidth)

    Node.outerHeight = Node.yPos - parentY
    Node.outerWidth = max(outerWidths)
    
    rectNode = Node.dwg.rect(
        insert=(Node.xPos, parentY),
        size = ("%spx"%(Node.outerWidth), "%spx"%(Node.outerHeight)))
    
    group.add(rectNode)
    for incredient in incredients:
        group.add(incredient)
    
    
    Node.yPos = parentY
    return group

@addToClass(AST.MethodArgumentNode)
def generate(self):
    print("MethodArgumentNode:")
    pass

@addToClass(AST.QuantityNode)
def generate(self):
    print("QuantityNode:")
    pass

@addToClass(AST.IngredientNode)
def generate(self):
    topBottomMargin = 5
    leftRightMargin = 10
    fontHeight = 20
    
    text = self.children[0].children[0].tok + " " + self.children[1].tok;
    textSize = text_size(text, fontHeight);
    
    textNode = Node.dwg.text(
        text,
        insert=(Node.xPos + leftRightMargin, Node.yPos + topBottomMargin + fontHeight ),
        font_size='%spx' % fontHeight)
    
    
    # the ingredient is  a leaf node --> set outerHeight and outerWidth
    Node.outerWidth = textSize[0] + 2 * leftRightMargin;
    Node.outerHeight = textSize[1] + 2 * topBottomMargin;
    
    return textNode

@addToClass(AST.MethodNode)
def generate(self):
    topBottomMargin = 5
    leftRightMargin = 10
    fontHeight = 20
    
    group = Node.dwg.g()
    
    text = self.children[0].tok
    textSize = text_size(text, fontHeight);
    
    rectNode = Node.dwg.rect(
        insert=(Node.xPos + leftRightMargin, Node.yPos + topBottomMargin ),
        size = ("%spx"%(textSize[0]), "%spx"%(textSize[1])))
    
    textNode = Node.dwg.text(
        text,
        insert=(Node.xPos + leftRightMargin, Node.yPos + topBottomMargin + fontHeight),
        font_size='%spx' % fontHeight)

    Node.outerWidth = textSize[0] + 2 * leftRightMargin;
    Node.outerHeight = textSize[1] + 2 * topBottomMargin;
    
    group.add(rectNode)
    group.add(textNode)

    return group

@addToClass(AST.MethodParametersNode)
def generate(self):
    print("MethodParametersNode:")
    pass

@addToClass(AST.TokenNode)
def generate(self):
    topBottomMargin = 5
    leftRightMargin = 10
    fontHeight = 20
    
    text = self.tok
    textSize = text_size(text, fontHeight);
    
    textNode = Node.dwg.text(
        text,
        insert=(Node.xPos + leftRightMargin, Node.yPos + topBottomMargin + fontHeight),
        font_size='%spx' % fontHeight)
    
    Node.outerWidth = textSize[0] + 2 * leftRightMargin;
    Node.outerHeight = textSize[1] + 2 * topBottomMargin;
    
    return textNode
    
def text_size(text, font_size):
    from PIL import ImageFont
    font = ImageFont.truetype("MANDINGO.TTF", font_size)
    size = font.getsize(text)
    return size

if __name__ == "__main__":
        from parser import parse
        import sys
        prog = open(sys.argv[1]).read()
        ast = parse(prog)
        
        AST.Node.dwg = svgwrite.Drawing('test.svg', profile='tiny')
        AST.Node.xPos = 20
        AST.Node.yPos = 20
        AST.Node.outerHeight = 0;
        AST.Node.outerWidth = 0;
        AST.Node.dwg.add_stylesheet("style.css", "compireci stylesheet");
        
        AST.Node.dwg.add(ast.generate())
        AST.Node.dwg.save()

