import os
import requests
import pytube
import moviepy.editor as mp
from colorama import Fore, Style

DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL", "")  

def send_discord_webhook(url):

    if not DISCORD_WEBHOOK_URL:
        print(f"{Fore.YELLOW}[!] Aucune URL de webhook Discord n'est configurée.{Style.RESET_ALL}")
        return
    
    data = {'content': url}
    response = requests.post(DISCORD_WEBHOOK_URL, json=data)
    if response.status_code == 204:
        print(f"{Fore.GREEN}[+]{Style.RESET_ALL} URL envoyée avec succès au webhook Discord.")
    else:
        print(f"{Fore.RED}[-]{Style.RESET_ALL} Échec de l'envoi de l'URL au webhook Discord. Code d'état : {response.status_code}")

def main():

    while True:
        try:
            video_url = input(f'{Fore.GREEN}[+]{Style.RESET_ALL} URL de la vidéo YouTube (ou "q" pour quitter) : ')
            if video_url.lower() == 'q':
                print("Fermeture du script.")
                break

            print(f"{Fore.CYAN}[i]{Style.RESET_ALL} Téléchargement de la vidéo...")
            video_instance = pytube.YouTube(video_url)
            stream = video_instance.streams.get_highest_resolution()

            if not stream:
                print(f"{Fore.RED}[-]{Style.RESET_ALL} Aucun flux haute résolution disponible.")
                continue

            video_filename = "video.mp4"
            if os.path.exists(video_filename):
                os.remove(video_filename) 

            stream.download(filename=video_filename)
            print(f"{Fore.GREEN}[+]{Style.RESET_ALL} Vidéo téléchargée : '{video_instance.title}'")

            video_clip = mp.VideoFileClip(video_filename)

            # Définir la durée d'une partie (en secondes)
            part_duration = 75  

            num_parts = int(video_clip.duration // part_duration)

            for part_num in range(num_parts):
                start_time = part_num * part_duration
                end_time = (part_num + 1) * part_duration

                part_clip = video_clip.subclip(start_time, end_time)

                target_resolution = (1080, 1920)

                blank_clip = mp.ColorClip(target_resolution, color=(0, 0, 0), duration=part_clip.duration)

                sat_filepath = os.path.join("misc", "sat.mp4")
                if os.path.exists(sat_filepath):
                    sat_clip = mp.VideoFileClip(sat_filepath)
                    sat_clip = sat_clip.subclip(0, min(sat_clip.duration, part_clip.duration))
                    sat_clip = sat_clip.resize(height=1200)  # par exemple
                else:
                    sat_clip = None

                final_clips = [blank_clip, part_clip.set_position(("center", "top"))]

                if sat_clip:
                    final_clips.append(sat_clip.set_position(("center", "bottom")))

                final_clip = mp.CompositeVideoClip(final_clips)

                final_filename = f"partie_{part_num + 1}.mp4"

                final_clip.write_videofile(final_filename, codec='libx264', threads=4)
                print(f"{Fore.GREEN}[+]{Style.RESET_ALL} Partie {part_num + 1} générée ({target_resolution[0]}x{target_resolution[1]})")

                upload_url = "https://tmpfiles.org/api/v1/upload"
                with open(final_filename, "rb") as f:
                    files = {"file": f}
                    response = requests.post(upload_url, files=files)

                if response.status_code == 200:
                    file_url = response.json()["data"]["url"]
                    print(f"{Fore.GREEN}[+]{Style.RESET_ALL} Partie {part_num + 1} uploadée : {file_url}")
                    send_discord_webhook(file_url)
                else:
                    print(f"{Fore.RED}[-]{Style.RESET_ALL} Échec de l'upload : code {response.status_code}")

            if os.path.exists(video_filename):
                os.remove(video_filename)

        except Exception as e:
            print(f"{Fore.RED}[-]{Style.RESET_ALL} Une erreur s'est produite : {e}")

if __name__ == "__main__":
    main()
