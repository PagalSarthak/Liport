<div align="center">
<img src="https://github.com/user-attachments/assets/c61fa08c-3ed2-4ea2-ad0c-9aa62262877a" width="200" />
</div>

# Liport: Linux Solution Bot
+ Liport is a command-line bot that helps users find solutions to their Linux-related queries by searching Reddit and Stack Exchange. It automatically detects your Linux distribution and queries the relevant subreddits and Stack Exchange for answers.

# Features
+ **Automatic Distro Detection**:  Detects your Linux distribution by reading ``/etc/os-release.``

+ **Reddit Integration**: Searches relevant subreddits based on your Linux distro.

+ **Stack Exchange Integration**: Fetches Linux-related solutions from Stack Exchange.

+ **Interactive Command Line** Interface: Chat with the bot and get solutions for your Linux problems.

# Requirements
+ Python 3.x
+ Praw (Python Reddit API Wrapper): Install using pip install praw.
+ Requests: Install using pip install requests.

# Setup
**Install Dependencies:**

+ Make sure you have Python 3 installed, then install the required libraries:

bash
Copy code

```
pip install praw requests
```

**Reddit API Credentials:**

You need to create a Reddit application to get the API credentials.

+ Go to [Reddit's app preferences.](https://www.reddit.com/prefs/apps)
+ Create a new "script" application and obtain the ``client_id``, ``client_secret``, and ``user_agent``.
  
    Add your credentials in the script:
```  
REDDIT_CLIENT_ID = 'YOUR_CLIENT_ID'
REDDIT_CLIENT_SECRET = 'YOUR_CLIENT_SECRET'
REDDIT_USER_AGENT = 'YOUR_USER_AGENT'
```
> [!NOTE]
> If you can't able to install praw or request in your distro use virtual environment.

```
python3 -m venv venv
venv/bin/pip install praw requests
sudo venv/bin/python3 Liport.py
```

# Usage

+ Start the Bot: Simply run the bot with the following command:

```
python3 liport.py
```
+ Type your query: Once the bot starts, it will prompt you with Liport>. Type in your query (Linux-related issue or problem).

+ View Results: The bot will search for solutions and display results from:
Relevant subreddits (e.g., ubuntu, debian, archlinux, etc.).
Stack Exchange Unix & Linux section.

+ Exit the Bot: Type exit to quit the bot

# Example Interaction:

```
Welcome to Liport, your Linux solution bot.
Type 'exit' to quit the bot.

Liport> How to fix "sudo: unable to resolve host" error?

--- Reddit Solutions for Ubuntu ---
Title: Fixing sudo: unable to resolve host issue
URL: https://reddit.com/r/ubuntu/comments/abcd123

--- Stack Exchange Solutions ---
Title: How to fix sudo: unable to resolve host
Link: https://unix.stackexchange.com/questions/123456

```

# License

This project is licensed under the MIT License - see the LICENSE file for details.


