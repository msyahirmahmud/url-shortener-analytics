import unittest
import time
from app import URLShortenerService

class TestURLShortener(unittest.TestCase):
    def test_shorten_valid_url(self):
        service = URLShortenerService()
        res = service.shorten_url("https://github.com/msyahirmahmud")
        self.assertIsNotNone(res["code"])
        self.assertEqual(len(res["code"]), 6)
        self.assertEqual(res["original_url"], "https://github.com/msyahirmahmud")

    def test_custom_alias_shorten(self):
        service = URLShortenerService()
        res = service.shorten_url("https://github.com/msyahirmahmud", custom_alias="my-github")
        self.assertEqual(res["code"], "my-github")
        self.assertEqual(res["short_url"], "http://short.ly/my-github")

    def test_duplicate_custom_alias_raises_error(self):
        service = URLShortenerService()
        service.shorten_url("https://github.com", custom_alias="my-github")
        with self.assertRaises(ValueError):
            service.shorten_url("https://python.org", custom_alias="my-github")

    def test_link_expiration_ttl(self):
        service = URLShortenerService()
        res = service.shorten_url("https://expiring-link.com", ttl_seconds=1)
        code = res["code"]
        self.assertEqual(service.redirect_code(code), "https://expiring-link.com")
        time.sleep(1.1)
        self.assertTrue(service.is_expired(code))
        self.assertIsNone(service.redirect_code(code))

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
