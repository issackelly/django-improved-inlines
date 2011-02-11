from django.conf import settings
from django.test import TestCase

from improved_inlines import parser

from improved_inlines.tests.models import Image, Video


class SimpleTest(TestCase):

    def setUp(self):
        for i in range(3):
            img = Image()
            img.title = "Image-%i" % (i+1)
            img.save()
            vid = Video()
            vid.title = "Video-%i" % (i+1)
            vid.save()

    def test_rendering_tags(self):
        fp_type_id     = """<div data-inline-type="tests.image" data-inline-id="2">Content</div>"""
        fp_type_ids    = """<p data-inline-type="tests.video" data-inline-ids="1,2,3">Content</p>"""
        fp_type_filter = """<div data-inline-type="tests.image" data-inline-filter="title__contains='Image'">Content</div>"""
        # These three should be simply ignored since they don't have all the right attributes
        fp_type        = """<div data-inline-type="tests.video">Content</div>"""
        fp_id          = """<li data-inline-id="2">Content</li>"""
        fp_ignore      = """<span class="test">Content</span>"""

        fp_list = [fp_type_ids, fp_type_id, fp_type_filter, fp_type, fp_id, ]
        rendered_list = []

        for fp in fp_list:
            rendered_list.append(parser.inlines(fp))

        expected_result_list = [
            """<video src="/tests/media/" alt="Video-1">Test</video><video src="/tests/media/" alt="Video-2">Test</video><video src="/tests/media/" alt="Video-3">Test</video>\n""",
            """<img src="/tests/media/" alt="Image-2" />\n""",
            """<img src="/tests/media/" alt="Image-1" /><img src="/tests/media/" alt="Image-2" /><img src="/tests/media/" alt="Image-3" />\n""",
            # These three remain the same as the originals
            """<div data-inline-type="tests.video">Content</div>""",
            """<li data-inline-id="2">Content</li>""",
            """<span class="test">Content</span>""",
        ]

        for expected, result in zip(expected_result_list, rendered_list):
            self.assertEqual(expected, result)
