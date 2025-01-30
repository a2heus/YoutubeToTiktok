# YoutubeToTiktok

A **Python** script that takes a long YouTube video, splits it into multiple 75-second TikTok-friendly segments (vertical format), and overlays a "satisfying" video at the bottom to capture attention. This longer-than-one-minute approach can help with monetization by maintaining viewer interest.


## Requirements

- **Python 3.7+**  
- **pip** (to install dependencies)  
- **ffmpeg** (MoviePy depends on it for video processing)

### Python Dependencies

- `pytube` (YouTube video downloading)  
- `moviepy` (video editing)  
- `colorama` (colored console output)  
- `requests` (HTTP requests for uploading and Discord webhook)

Install them via:
```bash
pip install -r requirements.txt
```

*(Or manually: `pip install pytube moviepy colorama requests`)*

---

## Installation

1. **Clone or Download** the repository:
   ```bash
   git clone https://github.com/<your-username>/YoutubeToTiktok.git
   cd YoutubeToTiktok
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
   Make sure `ffmpeg` is installed on your system (e.g., `sudo apt-get install ffmpeg`, `brew install ffmpeg`, etc.).

3. **Place the Satisfying Video** (Optional):
   - If you have a special "satisfying" clip, name it `sat.mp4` and put it inside the `misc/` folder.
   - The script will overlay it at the bottom of each TikTok segment.

---

## Configuration

- **Discord Webhook**:  
  - By default, the script can read an environment variable `DISCORD_WEBHOOK_URL` for the webhook.  
  - Alternatively, you can hardcode the webhook URL in the script.  
  - Example (Linux/macOS):
    ```bash
    export DISCORD_WEBHOOK_URL="https://discord.com/api/webhooks/..."
    ```
  - Windows (Command Prompt):
    ```cmd
    set DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/...
    ```

- **Segment Length**:  
  - The default segment length is 75 seconds.  
  - Adjust `part_duration = 75` in the script if you need a different duration.

---

## Usage

1. **Run the script**:
   ```bash
   python youtube_to_tiktok.py
   ```
2. **Input the YouTube URL** when prompted.  
3. The script will:
   - Download the video,
   - Split it into 75-second segments,
   - Convert each segment to a 1080×1920 vertical format,
   - Overlay `sat.mp4` at the bottom if provided,
   - Render each segment to a local `.mp4`,
   - Upload each `.mp4` to `tmpfiles.org`,
   - Post the resulting file link to the configured Discord webhook (if set),
   - Finally, display the link in the console.

4. **Check your Discord channel** to see the incoming links or watch the console output for direct URLs.

---

## How It Works

1. **Download**  
   - [pytube](https://github.com/pytube/pytube) fetches the YouTube video and saves it locally (`video.mp4`).
2. **Split & Convert**  
   - [MoviePy](https://github.com/Zulko/moviepy) cuts the video into multiple 75s clips.  
   - A background of 1080×1920 is generated, placing the original clip at the top and `sat.mp4` at the bottom.
3. **Rendering**  
   - Outputs each part as `partie_1.mp4`, `partie_2.mp4`, etc.
4. **Uploading**  
   - The script uploads each segment to [tmpfiles.org](https://tmpfiles.org/).  
   - If you prefer another service, modify `upload_url` in the script.
5. **Discord Webhook**  
   - The generated URL is posted to the Discord webhook so you can quickly retrieve or share them.

---

## Tips & Customization

- **Longer Durations**: If you want segments longer than 1 minute for monetization or other reasons, simply increase `part_duration`.
- **Watermark/Satisfying Clip**: Replace `sat.mp4` with any loop or short clip. Perfect for capturing attention or brand watermark.
- **Video Layout**: Customize the positioning in the script’s `CompositeVideoClip` logic.

---

## Contributing

Feel free to open Pull Requests or Issues on GitHub if you have improvements or find bugs.

## Dont forget to star this repo if you like it <3
