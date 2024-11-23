import praw
import requests
import sys
import os

# --- CONFIGURATION ---
# Reddit API credentials
REDDIT_CLIENT_ID = 'sFjETMQ15Bzeg9E_x7LyVw'  # Replace with your Reddit Client ID
REDDIT_CLIENT_SECRET = '_tuXaCKHflxhkYdkiXelsv26vlZdKw'  # Replace with your Reddit Client Secret
REDDIT_USER_AGENT = 'linux-solution-bot'  # Custom user agent for your app

if not REDDIT_CLIENT_ID or not REDDIT_CLIENT_SECRET or not REDDIT_USER_AGENT:
    print("Missing Reddit API credentials. Please make sure all values are set.")
    sys.exit(1)
# Define the Subreddits and Stack Exchange API
REDDIT_SUBREDDITS = {
    'ubuntu': 'ubuntu',
    'debian': 'debian',
    'fedora': 'fedora',
    'arch linux': 'archlinux',  # Use 'arch linux' as key for "archlinux" subreddit
    'linuxmint': 'linuxmint',
    'manjaro': 'manjaro',
}

STACK_EXCHANGE_URL = "https://api.stackexchange.com/2.3/search"

# --- Initialize Reddit API (PRAW) ---
reddit = praw.Reddit(client_id=REDDIT_CLIENT_ID,
                     client_secret=REDDIT_CLIENT_SECRET,
                     user_agent=REDDIT_USER_AGENT)

# Function to automatically detect the Linux distribution
def detect_distro():
    try:
        with open("/etc/os-release") as f:
            lines = f.readlines()
            for line in lines:
                if line.startswith("NAME="):
                    distro_name = line.strip().split('=')[1].strip('"').lower()
                    print(f"Detected Distro: {distro_name}")  # Debugging line
                    return distro_name
    except FileNotFoundError:
        print("Error: /etc/os-release file not found. Unable to detect distribution.")
        return None

# ANSI escape codes for coloring
RESET = '\033[0m'  # Reset all colors
BOLD = '\033[1m'  # Bold text
CYAN = '\033[36m'  # Cyan text
GREEN = '\033[32m'  # Green text
YELLOW = '\033[33m'  # Yellow text
RED = '\033[31m'  # Red text
MAGENTA = '\033[35m'  # Magenta text

# ASCII Art
ASCII_ART = """
.____    .__       ________          __   
|    |   |__|_____ \\_____  \\________/  |_ 
|    |   |  \\____ \\ /   |   \\_  __ \\   __\\
|    |___|  |  |_> >    |    \\  | \\/|  |  
|_______ \\__|   __/\\_______  /__|   |__|  
        \\/  |__|           \\/              
"""

# Function to search Reddit for Linux-related solutions across all distros
def search_reddit(query, distro):
    print(f"{CYAN}\nSearching Reddit for Linux-related solutions...{RESET}")
    
    # Match the distro name to the correct subreddit
    subreddit = REDDIT_SUBREDDITS.get(distro, None)
    if not subreddit:
        return f"{RED}No relevant subreddit found for the detected distro: {distro}. Please check your distro or query again.{RESET}"

    solutions = []
    subreddit_obj = reddit.subreddit(subreddit)
    try:
        # Search for the query in the specified subreddit
        for submission in subreddit_obj.search(query, limit=3):
            if query.lower() in submission.title.lower() or query.lower() in submission.selftext.lower():
                solutions.append(f"{GREEN}Title: {submission.title}\n{YELLOW}URL: https://reddit.com{submission.permalink}\n{RESET}")
    except Exception as e:
        print(f"{RED}Error searching Reddit for {subreddit}: {e}{RESET}")
    
    if not solutions:
        return f"{RED}No relevant solutions found on Reddit for {distro} related to your query.{RESET}"
    return '\n'.join(solutions)

# Function to search Stack Exchange for Linux-related solutions
def search_stack_exchange(query):
    print(f"{CYAN}\nSearching Stack Exchange for Linux-related solutions...{RESET}")
    
    params = {
        'site': 'unix',
        'order': 'desc',
        'sort': 'relevance',
        'intitle': query,
        'filter': '!-*jbN2x',  # Filter out some unnecessary fields
    }

    try:
        response = requests.get(STACK_EXCHANGE_URL, params=params)
        response.raise_for_status()  # Raise an exception for HTTP errors
    except requests.exceptions.RequestException as e:
        return f"{RED}Error fetching data from Stack Exchange: {e}{RESET}"
    
    if response.status_code == 200:
        data = response.json()
        solutions = []
        for item in data.get('items', [])[:3]:  # Limit to top 3 results
            title = item.get('title', 'No title available')
            link = item.get('link', 'No link available')
            
            if query.lower() in title.lower():
                solutions.append(f"{GREEN}Title: {title}\n{YELLOW}Link: {link}\n{RESET}")
        
        if not solutions:
            return f"{RED}No relevant solutions found on Stack Exchange.{RESET}"
        return '\n'.join(solutions)
    else:
        return f"{RED}Error fetching data from Stack Exchange.{RESET}"

# Function to handle the user's query and provide solutions
def handle_query(query):
    distro = detect_distro()  # Automatically detect the Linux distro
    if not distro:
        return f"{RED}Unable to detect the Linux distribution. Please try again or provide more information.{RESET}"

    reddit_solution = search_reddit(query, distro)
    stack_exchange_solution = search_stack_exchange(query)

    return f"{CYAN}\n--- Reddit Solutions for {distro.capitalize()} ---{RESET}\n{reddit_solution}\n\n--- Stack Exchange Solutions ---\n{stack_exchange_solution}"

def main():
    print(f"{MAGENTA}{ASCII_ART}{RESET}")
    print(f"{MAGENTA}Welcome to Liport, your Linux solution bot.{RESET}")
    print(f"{YELLOW}Type 'exit' to quit the bot.{RESET}")
    
    while True:
        query = input(f"{CYAN}Liport> {RESET}").strip()  # Wait for user input and remove unnecessary spaces
        
        if query.lower() == 'exit':
            print(f"{RED}Exiting Liport. Goodbye!{RESET}")
            sys.exit(0)

        if not query:  # Ensure the user doesn't input an empty query
            print(f"{YELLOW}Please enter a query to search.{RESET}")
            continue

        # Handle the query and get the response
        response = handle_query(query)
        
        # Display the response
        print(response)

if __name__ == "__main__":
    main()
