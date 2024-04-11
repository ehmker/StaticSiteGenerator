import unittest
from block_md import split_block_markdown


class TestBlockMarkdown(unittest.TestCase):
    def test_split_block_markdown(self):
        text = """# This is a heading

                This is a paragraph of text. It has some **bold** and *italic* words inside of it.

                * This is a list item
                * This is another list item
            """
        self.assertListEqual(
            split_block_markdown(text),
            [
                "# This is a heading",
                "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
                "* This is a list item\n* This is another list item",
            ],
        )

        def test_markdown_to_blocks(self):
            md = """
                This is **bolded** paragraph

                This is another paragraph with *italic* text and `code` here
                This is the same paragraph on a new line

                * This is a list
                * with items
                """

            blocks = split_block_markdown(md)
            self.assertEqual(
                blocks,
                [
                    "This is **bolded** paragraph",
                    "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
                    "* This is a list\n* with items",
                ],
            )

    def test_markdown_to_blocks_newlines(self):
        md = """
            This is **bolded** paragraph




            This is another paragraph with *italic* text and `code` here
            This is the same paragraph on a new line

            * This is a list
            * with items
            """
        blocks = split_block_markdown(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
                "* This is a list\n* with items",
            ],
        )
