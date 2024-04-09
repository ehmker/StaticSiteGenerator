import unittest

from htmlnode import HTMLNode, ParentNode, LeafNode


class TestTextNode(unittest.TestCase):
    def test_repr(self):
        node = HTMLNode("this is a tag", 'this is value', 'this is children', {"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(
            'HTMLNode(tag=this is a tag, value=this is value, children=this is children, props= href="https://www.google.com" target="_blank")', repr(node)
        )
        
    def test_props_to_html(self):
        node = HTMLNode('div', 
                        'test value', 
                        None, 
                        {"class": "greeting", "href": "https://google.com"})
        
        self.assertEqual(node.props_to_html(),
                         ' class="greeting" href="https://google.com"')
        
 ### LeafNode Tests ###
    def test_to_html(self):
        node = LeafNode("p", "This is a paragraph of text.")
        self.assertEqual(node.to_html(), '<p>This is a paragraph of text.</p>')
        
    def test_to_html_props(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')
               
### ParentNode Tests ###
    def test_to_html(self):
        node = ParentNode(
    "p",
    [
        LeafNode("b", "Bold text"),
        LeafNode(None, "Normal text"),
        LeafNode("i", "italic text"),
        LeafNode(None, "Normal text"),
    ],
)
        self.assertEqual(node.to_html(),'<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>')

    def test_to_html_parent(self):
        node = ParentNode(
        "p",
        [
        LeafNode("b", "Bold text"),
        ParentNode(
                "p",
                [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
                ],
            ),
        LeafNode("i", "italic text"),
        LeafNode(None, "Normal text")
            ],
        )
        self.assertEqual(node.to_html(),'<p><b>Bold text</b><p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p><i>italic text</i>Normal text</p>')
        
if __name__ == "__main__":
    unittest.main()
