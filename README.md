# TeleKrawl

A powerful Python script and offline viewer to download and browse content from your Telegram channels. Save messages, photos, and videos locally and view them anytime in a rich, browser-based interface that mimics the Telegram UI.



---

## ✨ Features

-   **Comprehensive Scraping**: Downloads all messages, text, photos, and videos from any channel you're in.
-   **Offline Viewer**: A single `viewer.html` file provides a beautiful, searchable interface to browse downloaded content offline.
-   **Incremental Downloads**: Automatically fetches only new messages since the last run, saving time and resources.
-   **Rich Media Experience**: The viewer includes a collage layout for grouped media and a full-screen carousel for easy viewing.
-   **Secure & Private**: All your data and session files are stored locally on your machine.

---

## 🚀 Setup and Usage

Follow these steps to get started:

### Step 1: Prerequisites

-   Python 3.8 or newer.
-   A Telegram account.

### Step 2: Get API Credentials

1.  Go to [my.telegram.org](https://my.telegram.org) and log in with your Telegram account.
2.  Click on "**API development tools**" and fill out the form.
3.  You will get an **`api_id`** and **`api_hash`**. Save these—you'll need them in a moment.

### Step 3: Clone & Install

1.  Clone this repository to your local machine:
    ```bash
    git clone https://github.com/1FahadShah/telekrawl.git
    cd telekrawl
    ```
2.  Install the required Python libraries:
    ```bash
    pip install -r requirements.txt
    ```

### Step 4: Configure the Script

1.  Open the `krawler.py` file in a text editor.
2.  Replace the placeholder values for `api_id`, `api_hash`, and `phone` with your own credentials:
    ```python
    # ===== CONFIG =====
    api_id = 12345678          # Replace with your api_id
    api_hash = 'your_api_hash' # Replace with your api_hash
    phone = '+919876543210'     # Your phone number with country code
    ```

### Step 5: Run the Krawler

1.  Execute the script from your terminal:
    ```bash
    python krawler.py
    ```
2.  The first time you run it, Telegram will send you a login code. Enter it in the terminal when prompted.
3.  The script will list the channels you are in. Follow the on-screen prompts to select which ones to download.

### Step 6: View Your Content

To ensure the viewer can load all your messages and media correctly, you need to run it from a local web server due to browser security policies.

1.  In your terminal (while in the project folder), run this command:
    ```bash
    python -m http.server 8000
    ```
2.  Open your web browser and navigate to the following address:
    **[http://localhost:8000/viewer.html](http://localhost:8000/viewer.html)**
3.  You can now browse all your downloaded content! To stop the server, go back to your terminal and press `Ctrl+C`.

---

## ⚠️ Important Notes

-   **NEVER** share your `api_id`, `api_hash`, or the `.session` file that is generated. The `.gitignore` file is configured to prevent this file from being uploaded to GitHub by accident.
-   Use this tool responsibly and be mindful of Telegram's Terms of Service.

