from app import URLShortenerService

service = URLShortenerService()

if __name__ == "__main__":
    print("URL Shortener Engine Initialized.")
    url = service.shorten_url("https://github.com/msyahirmahmud")
    print("Generated Short URL:", url)
