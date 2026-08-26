#!/usr/bin/env python3
"""Regression tests for scripts/wiki/render.py (added 2026-08-26, review batch 8).

Covers the corrected defects: continuation lines must stay inside their list item,
nested lists must nest inside their parent <li>, and emphasis markers (including
multiple strong spans, and bold spanning wrapped lines) must render as balanced
<strong> markup with no raw Markdown markers left in the HTML.
"""
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from render import render_md  # noqa: E402


def body(md):
    return render_md(md)[0]


class TestContinuationLines(unittest.TestCase):
    def test_wrapped_item_is_one_li(self):
        html = body("- first line of an item\n  that wraps onto a second line\n- next item")
        self.assertIn("<li>first line of an item that wraps onto a second line</li>", html)
        self.assertEqual(html.count("<ul>"), 1)

    def test_blank_separated_items_form_one_list(self):
        html = body("- a\n\n- b\n\n- c")
        self.assertEqual(html.count("<ul>"), 1)
        self.assertEqual(html.count("</ul>"), 1)
        self.assertEqual(html.count("<li>"), 3)

    def test_numbered_list_with_blank_lines_is_single_ol(self):
        html = body("1. one\n\n2. two\n\n3. three")
        self.assertEqual(html.count("<ol>"), 1)
        self.assertEqual(html.count("<li>"), 3)

    def test_nested_list_stays_inside_parent_li(self):
        html = body("- parent\n\n  - child one\n  - child two\n- sibling")
        # child <ul> must appear inside the parent's <li> ... </li>
        self.assertIn("<li>parent<ul><li>child one</li><li>child two</li></ul></li>", html)
        self.assertIn("<li>sibling</li>", html)
        # no <ul> directly inside another <ul> without an <li> wrapper
        self.assertNotIn("<ul><ul>", html)
        # tags balance (no swallowed or unclosed list levels)
        self.assertEqual(html.count("<ul>"), html.count("</ul>"))

    def test_deep_nesting_then_dedent(self):
        html = body("- a\n\n  - b\n\n- c")
        self.assertIn("<li>a<ul><li>b</li></ul></li><li>c</li>", html)


class TestStrongSpans(unittest.TestCase):
    def test_bold_spanning_wrapped_lines(self):
        html = body("- **U6 (P1): work-order template files with the standing\n"
                    "  directive's evaluation block built in** (answers the mandate).")
        self.assertIn("<strong>U6 (P1): work-order template files with the standing "
                      "directive's evaluation block built in</strong>", html)
        self.assertNotIn("**", html)

    def test_multiple_strong_spans_one_item(self):
        html = body("- **first** and **second** and **third** here")
        self.assertEqual(html.count("<strong>"), 3)
        self.assertEqual(html.count("</strong>"), 3)
        self.assertNotIn("**", html)

    def test_no_raw_markers_in_o7_style_detail(self):
        html = body("5. **Dependencies/permissions/security:** hooks execute shell on hxs-5 at every\n"
                    "   matching tool call — the script must be repo-reviewed like code, carry no\n"
                    "   secrets, and stay under a 5–10 s timeout. **The hook system is fail-open** by design.")
        self.assertIn("<strong>Dependencies/permissions/security:</strong>", html)
        self.assertIn("<strong>The hook system is fail-open</strong>", html)
        self.assertNotIn("**", html)


class TestUnchangedSurfaces(unittest.TestCase):
    def test_heading_anchor(self):
        self.assertIn('<h2 id="hello-world">Hello World</h2>', body("## Hello World"))

    def test_table(self):
        html = body("| A | B |\n| --- | --- |\n| 1 | **2** |")
        self.assertIn("<table><thead><tr><th>A</th><th>B</th></tr></thead><tbody><tr><td>1</td><td><strong>2</strong></td></tr></tbody></table>", html)

    def test_code_fence_untouched(self):
        html = body("```bash\necho **not bold**\n```")
        self.assertIn("**not bold**", html)  # code keeps literal markers, escaped only
        self.assertNotIn("<strong>", html)

    def test_mermaid_block(self):
        out, has = render_md("```mermaid\nflowchart LR\n```")
        self.assertTrue(has)
        self.assertIn('<pre class="mermaid">', out)


if __name__ == "__main__":
    unittest.main()
