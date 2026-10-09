from langchain_core.tools import tool
from langchain_community.tools import DuckDuckGoSearchRun

import requests
import ipaddress
import socket

from urllib.parse import urlparse
from bs4 import BeautifulSoup

search = DuckDuckGoSearchRun()

@tool
def web_search(query : str) -> str:
    """
    Search the web for the current information
    Use this tool when the user asks about recent or up-to-date information
    """
    return search.invoke(query)

# @tool
def webpage_reader(url : str) -> str:
    """
    Read a publicly accessible webpage using its url
    Use this to extract detailed information from a webpage
    """
    try:
        parsed = urlparse(url)

        if parsed.scheme not in ('http', 'https') or not parsed.hostname:
            return "Invalid Url. Only HTTP and HTTPS URLs supported"

        addresses = socket.getaddrinfo(
            parsed.hostname,None, type = socket.SOCK_STREAM
        )

        for address in addresses:
            ip = ipaddress.ip_address(address[4][0])
            if not ip.is_global:
                return "Access to private or local address is blocked"

        response = requests.get(url, timeout=10, headers={"User-Agent" : "Morzilla/5.0"},
                                allow_redirects = False)

        if response.is_redirect:
            return f"Redirect Detected. Please use the destination URL directly"

        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        for tag in soup(["script", "style", "nav", "footer", "header"]):
            tag.decompose()
        text = soup.get_text(separator = " ", strip = True)
        return text[:8000] if text else "No readable content found"

    except Exception as e:
        return f"Falied to read the webpage : {e}"


@tool
def calculator(expression: str) -> str:
    """Calculate the mathematical expression."""

    try:
        return str(eval(expression))
    except Exception:
        return "Invalid mathematical expression"