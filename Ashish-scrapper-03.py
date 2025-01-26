import requests

import re

class SocialMediaScraper:
    def __init__(self, api_keys):
        """
        Initialize scraper with necessary API keys.
        :param api_keys: Dictionary with API keys for YouTube, Instagram, TikTok, Facebook.
        """
        self.api_keys = api_keys

    def detect_platform(self, url):
        """
        Detect the platform from the given URL.
        """
        platforms = {
            "youtube.com": "YouTube",
            "youtu.be": "YouTube",
            "instagram.com": "Instagram",
            "tiktok.com": "TikTok",
            "facebook.com": "Facebook",
        }
        for domain, platform in platforms.items():
            if domain in url:
                return platform
        return None

    def scrape_data(self, url, data_type):
        """
        Main function to scrape data based on URL and data type.
        :param url: Profile or post URL.
        :param data_type: Type of data to scrape (e.g., 'followers', 'comments', 'likes').
        """
        platform = self.detect_platform(url)
        if not platform:
            return {"error": "Unsupported platform"}

        scrape_methods = {
            "YouTube": self.scrape_youtube,
            "Instagram": self.scrape_instagram,
            "TikTok": self.scrape_tiktok,
            "Facebook": self.scrape_facebook,
        }

        if platform in scrape_methods:
            return scrape_methods[platform](url, data_type)
        return {"error": f"Scraping not implemented for {platform}"}

    def scrape_youtube(self, url, data_type):
        """
        Scrape data from YouTube using YouTube Data API.
        """
        api_key = self.api_keys.get("YouTube")
        if not api_key:
            return {"error": "YouTube API key missing"}

        video_id = self.extract_youtube_video_id(url)
        if not video_id:
            return {"error": "Invalid YouTube video URL"}

        try:
            if data_type == "comments":
                endpoint = "https://www.googleapis.com/youtube/v3/commentThreads"
                params = {"part": "snippet", "videoId": video_id, "key": api_key}
                response = requests.get(endpoint, params=params)
                response.raise_for_status()
                return response.json()
            # Add more data types (e.g., likes, subscribers) as needed.
            return {"error": f"Data type '{data_type}' not supported for YouTube"}
        except requests.RequestException as e:
            return {"error": f"YouTube API request failed: {e}"}

    def scrape_instagram(self, url, data_type):
        """
        Scrape data from Instagram using Instagram Graph API.
        """
        access_token = self.api_keys.get("Instagram")
        if not access_token:
            return {"error": "Instagram API token missing"}

        post_id = self.extract_instagram_post_id(url)
        if not post_id:
            return {"error": "Invalid Instagram post URL"}

        try:
            if data_type == "comments":
                endpoint = f"https://graph.facebook.com/v16.0/{post_id}/comments"
                params = {"access_token": access_token}
                response = requests.get(endpoint, params=params)
                response.raise_for_status()
                return response.json()
            # Add more data types (e.g., followers, likes).
            return {"error": f"Data type '{data_type}' not supported for Instagram"}
        except requests.RequestException as e:
            return {"error": f"Instagram API request failed: {e}"}

    def scrape_tiktok(self, url, data_type):
        """
        Placeholder: Scrape data from TikTok using TikTok API for Business.
        """
        return {"message": "TikTok API integration pending"}

    def scrape_facebook(self, url, data_type):
        """
        Scrape data from Facebook using Facebook Graph API.
        """
        access_token = self.api_keys.get("Facebook")
        if not access_token:
            return {"error": "Facebook API token missing"}

        post_id = self.extract_facebook_post_id(url)
        if not post_id:
            return {"error": "Invalid Facebook post URL"}

        try:
            if data_type == "comments":
                endpoint = f"https://graph.facebook.com/v16.0/{post_id}/comments"
                params = {"access_token": access_token}
                response = requests.get(endpoint, params=params)
                response.raise_for_status()
                return response.json()
            # Add more data types (e.g., followers, likes).
            return {"error": f"Data type '{data_type}' not supported for Facebook"}
        except requests.RequestException as e:
            return {"error": f"Facebook API request failed: {e}"}

    @staticmethod
    def extract_youtube_video_id(url):
        """
        Extract the video ID from a YouTube URL.
        """
        match = re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11})", url)
        return match.group(1) if match else None

    @staticmethod
    def extract_instagram_post_id(url):
        """
        Extract the post ID from an Instagram URL.
        """
        match = re.search(r"/p/([^/?#&]+)", url)
        return match.group(1) if match else None

    @staticmethod
    def extract_facebook_post_id(url):
        """
        Extract the post ID from a Facebook URL.
        """
        match = re.search(r"/posts/([^/?#&]+)", url)
        return match.group(1) if match else None

# Example usage:
if __name__ == "__main__":
    api_keys = {
        "YouTube": "YOUTUBE_API_KEY",
        "Instagram": "INSTAGRAM_API_TOKEN",
        "Facebook": "FACEBOOK_API_TOKEN",
    }
    scraper = SocialMediaScraper(api_keys)
    result = scraper.scrape_data("https://www.youtube.com/watch?v=xyz123", "comments")
    print(result)
