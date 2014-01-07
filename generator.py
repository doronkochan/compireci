import sys
import AST
from AST import addToClass, Node
from semantic_rules import parameter_image
import svgwrite


@addToClass(AST.InstructionsNode)
def generate(self):
    spacing = 50
    left = 20
    
    Node.pos_x = Node.pos_x + left
    
    group = Node.dwg.g()
    for child in self.children:
        group.add(child.generate())
        Node.pos_y = Node.pos_y + Node.outer_h + spacing
    return group

@addToClass(AST.InstructionNode)
def generate(self):
    par_x = Node.pos_x
    par_y = Node.pos_y
    group = Node.dwg.g()
    
    # create instruction body
    instr_body_node = self.children[1].generate()
    group.add(instr_body_node)
    instr_body_size = (Node.outer_w, Node.outer_h)
    
    # create methode field
    Node.pos_x = Node.pos_x + instr_body_size[0]
    action_node = self.children[2].generate()
    group.add(action_node)
    action_size = (Node.outer_w, Node.outer_h)
    
    # create returning field
    Node.pos_x = Node.pos_x + action_size[0]
    ret_node = self.children[0].generate()
    ret_size = (Node.outer_w, Node.outer_h)
    group.add(ret_node)
    
    height_max = max(instr_body_size[1], action_size[1], ret_size[1])
    
    instr_body_node.translate(tx=0, ty=(height_max - instr_body_size[1])/2 )
    action_node.translate(tx=0, ty=(height_max - action_size[1])/2 )
    ret_node.translate(tx=0, ty=(height_max - ret_size[1])/2 )
    
    Node.outer_h = height_max
    Node.pos_x = par_x
    Node.pos_y = par_y
    
    return group

@addToClass(AST.InstructionBodyNode)
def generate(self):
    par_y = Node.pos_y
    group = Node.dwg.g()

    widths = []
    incredients = []
    for child in self.children:
        incredients.append(child.generate())
        Node.pos_y = Node.pos_y + Node.outer_h
        widths.append(Node.outer_w)

    Node.outer_h = Node.pos_y - par_y
    Node.outer_w = max(widths)
    
    rect_node = Node.dwg.rect(
        insert=(Node.pos_x, par_y),
        size = ("%spx"%(Node.outer_w), "%spx"%(Node.outer_h)))
    
    group.add(rect_node)
    
    for incredient in incredients:
        group.add(incredient)
    
    
    Node.pos_y = par_y
    return group

@addToClass(AST.IngredientNode)
def generate(self):
    top_bottom = 5
    left_right = 10
    font_height = 20
    
    txt = self.children[0].children[0].tok + " " + self.children[1].tok
    
    (txt_node, txt_size) = create_text_node(
        txt,
        font_height,
        Node.pos_x + left_right,
        Node.pos_y + top_bottom
    )
    
    
    
    # the ingredient is  a leaf node --> set outerHeight and outerWidth
    Node.outer_w = txt_size[0] + 2 * left_right
    Node.outer_h = txt_size[1] + 2 * top_bottom
    
    return txt_node

@addToClass(AST.MethodNode)
def generate(self):
    par_x = Node.pos_x
    par_y = Node.pos_y
    
    top_bottom = 0
    left_right = 20
    font_height = 20
    
    group = Node.dwg.g()
    
    Node.pos_y = Node.pos_y + top_bottom
    Node.pos_x = Node.pos_x + left_right
    
    txt = self.children[0].tok
    (txt_node, txt_size) = create_text_node(
        txt,
        font_height,
        Node.pos_x,
        Node.pos_y
    )   
        
    Node.pos_y = Node.pos_y + txt_size[1]
        
    param_node = self.children[1].generate(txt)
    param_size = (Node.outer_w, Node.outer_h)
    
    size = (
        max(param_size[0], txt_size[0]),
        max(param_size[1], txt_size[1])
    )
    
    txt_node.translate(tx=(size[0] - txt_size[0])/2, ty=0)
    param_node.translate(tx=(size[0] - param_size[0])/2, ty=0)

    rect_node = Node.dwg.rect(
        insert=(Node.pos_x, Node.pos_y-txt_size[1]),
        size = ("%spx"%(size[0]), "%spx"%(size[1]+txt_size[1])))

    Node.outer_w = size[0] + 2 * left_right
    Node.outer_h = size[1] + 2 * top_bottom
    
    group.add(rect_node)
    group.add(txt_node)
    group.add(param_node)
    
    Node.pos_x = par_x
    Node.pos_y = par_y
    
    return group

@addToClass(AST.MethodParametersNode)
def generate(self, method):
    par_y = Node.pos_y
    
    group = Node.dwg.g()
    
    widths = []
    for child in self.children:
        group.add(child.generate(method))
        Node.pos_y = Node.pos_y + Node.outer_h
        widths.append(Node.outer_w)
    
    Node.outer_h = Node.pos_y - par_y
    Node.outer_w = max(widths)
    
    Node.pos_y = par_y
    return group

@addToClass(AST.MethodArgumentNode)
def generate(self, method):
    group = Node.dwg.g()
    font_height = 15
    
    par = self.children[0].tok
    val = self.children[1].tok
    par_img = parameter_image(method, par, val)
    
    if par_img is not None:
        (img_node, img_size) = create_img_node(
            par_img[0],
            Node.pos_x,
            Node.pos_y)
        group.add(img_node)
        (Node.outer_w, Node.outer_h) = img_size
        
        if not par_img[1]:
            pos_x = Node.pos_x + img_size[0]
            (txt_node, txt_size) = create_text_node(
                val,
                font_height,
                pos_x,
                Node.pos_y)
            group.add(txt_node)
            
            txt_node.translate(tx=0, ty=(Node.outer_h - txt_size[1])/2 )
            img_node.translate(tx=0, ty=(Node.outer_h - img_size[1])/2 )
            
            Node.outer_w = txt_size[0] + img_size[0]
            Node.outer_h = max(txt_size[1], img_size[1])
    else:
        txt = "%s %s" % (par, val)
        (txt_node, txt_size) = create_text_node(
            txt,
            font_height,
            Node.pos_x,
            Node.pos_y)
        group.add(txt_node)
        (Node.outer_w, Node.outer_h) = txt_size
    
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
    top_bottom = 5
    left_right = 10
    font_height = 20
    
    txt = self.tok
    (txt_node, txt_size) = create_text_node(
        txt,
        font_height,
        Node.pos_x + left_right,
        Node.pos_y + top_bottom
    )
    
    Node.outer_w = txt_size[0] + 2 * left_right
    Node.outer_h = txt_size[1] + 2 * top_bottom
    
    return txt_node
    
def text_size(text, font_size):
    from PIL import ImageFont
    font = ImageFont.truetype("MANDINGO.TTF", font_size)
    size = font.getsize(text)
    return size

def image_size(img_path):
    from PIL import Image
    img = Image.open(img_path)
    return img.size

if __name__ == "__main__":
    from parser import parse
    prog = open(sys.argv[1]).read()
    ast = parse(prog)
    
    AST.Node.dwg = svgwrite.Drawing('test.svg', profile='tiny')
    AST.Node.pos_x = 20
    AST.Node.pos_y = 20
    AST.Node.outer_h = 0
    AST.Node.outer_w = 0
    AST.Node.dwg.add_stylesheet("style.css", "compireci stylesheet")
    
    AST.Node.dwg.add(ast.generate())
    AST.Node.dwg.save()

