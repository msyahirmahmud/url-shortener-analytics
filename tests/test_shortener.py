import unittest
from app import URLShortenerService

class TestURLShortener(unittest.TestCase):
    def test_shorten_valid_url(self):
        service = URLShortenerService()
        res = service.shorten_url("https://github.com/msyahirmahmud")
        self.assertIsNotNone(res["code"])
        self.assertEqual(len(res["code"]), 6)
        self.assertEqual(res["original_url"], "https://github.com/msyahirmahmud")

    def test_redirect_increments_click_counter(self):
        service = URLShortenerService()
        res = service.shorten_url("https://python.org")
        code = res["code"]
        
        redirect_target = service.redirect_code(code)
        self.assertEqual(redirect_target, "https://python.org")
        
        stats = service.get_analytics(code)
        self.assertEqual(stats["clicks"], 1)

    def test_invalid_url_raises_error(self):
        service = URLShortenerService()
        with self.assertRaises(ValueError):
            service.shorten_url("invalid-url-string")

if __name__ == '__main__':
    unittest.main()
