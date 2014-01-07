import sys
import AST
from AST import addToClass, Node
from semantic_rules import parameter_image
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
    parentX = Node.xPos
    parentY = Node.yPos
    
    topBottomMargin = 0
    leftRightMargin = 20
    fontHeight = 20
    
    group = Node.dwg.g()
    
    txt = self.children[0].tok
    txt_size = text_size(txt, fontHeight);
    
    Node.yPos = Node.yPos + topBottomMargin
    Node.xPos = Node.xPos + leftRightMargin
    
    txt_node = Node.dwg.text(
        txt,
        insert=(Node.xPos, Node.yPos + fontHeight),
        font_size='%spx' % fontHeight)
        
        
    Node.yPos = Node.yPos + fontHeight
        
    param_node = self.children[1].generate(txt)
    param_size = (Node.outerWidth, Node.outerHeight)
    
    size = (
        max(param_size[0], txt_size[0]),
        max(param_size[1], txt_size[1])
    )
    
    txt_node.translate(tx=(size[0] - txt_size[0])/2, ty=0)
    param_node.translate(tx=(size[0] - param_size[0])/2, ty=0)

    rect_node = Node.dwg.rect(
        insert=(Node.xPos, Node.yPos-txt_size[1]),
        size = ("%spx"%(size[0]), "%spx"%(size[1]+txt_size[1])))

    Node.outerWidth = size[0] + 2 * leftRightMargin;
    Node.outerHeight = size[1] + 2 * topBottomMargin;
    
    group.add(rect_node)
    group.add(txt_node)
    group.add(param_node)
    
    Node.xPos = parentX
    Node.yPos = parentY
    
    return group

@addToClass(AST.MethodParametersNode)
def generate(self, method):
    parentY = Node.yPos
    
    group = Node.dwg.g()
    
    widths = []
    for child in self.children:
        group.add(child.generate(method))
        Node.yPos = Node.yPos + Node.outerHeight
        widths.append(Node.outerWidth)
    
    Node.outerHeight = Node.yPos - parentY
    Node.outerWidth = max(widths);
    
    Node.yPos = parentY
    return group

@addToClass(AST.MethodArgumentNode)
def generate(self, method):
    group = Node.dwg.g()
    font_height = 15
    
    par = self.children[0].tok
    val = self.children[1].tok
    par_img = parameter_image(method, par, val)
    
    if par_img is not None:
        (img_node, img_size) = create_img_node(par_img[0], Node.xPos, Node.yPos)
        group.add(img_node)
        (Node.outerWidth, Node.outerHeight) = img_size
        
        if not par_img[1]:
            pos_x = Node.xPos + img_size[0]
            (txt_node, txt_size) = create_text_node(val, font_height, pos_x, Node.yPos)
            group.add(txt_node)
            
            txt_node.translate(tx=0, ty=(Node.outerHeight - txt_size[1])/2 )
            img_node.translate(tx=0, ty=(Node.outerHeight - img_size[1])/2 )
            
            Node.outerWidth = txt_size[0] + img_size[0]
            Node.outerHeight = max(txt_size[1], img_size[1])
    else:
        txt = "%s %s"%(par, val)
        (txt_node, txt_size) = create_text_node(txt, font_height, Node.xPos, Node.yPos)
        group.add(txt_node)
        (Node.outerWidth, Node.outerHeight) = txt_size
    
    return group

def create_text_node(txt, font_height, pos_x, pos_y):
    size = text_size(txt, font_height)
    node = Node.dwg.text(
        txt,
        insert=(pos_x, pos_y+font_height),
        font_size='%spx' % font_height
    )
    return (node, size)

def create_img_node(img, pos_x, pos_y):
    size = image_size(img)
    node = Node.dwg.image(
        img,
        insert=(pos_x, pos_y),
        size=size
    )
    return (node, size)

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

def image_size(img_path):
    from PIL import Image
    im=Image.open(img_path)
    return im.size

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

