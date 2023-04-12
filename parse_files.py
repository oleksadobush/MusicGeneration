import requests
import json
import os


if __name__ == "__main__":
    main_url = "https://www.vgmusic.com/"
    root_dir = "./data"

    with open("midi_files.json", "r") as infile:
        data = json.load(infile)
        for url in data.keys():
            for section_name in data[url].keys():
                os.makedirs(root_dir + url[6:] + section_name, mode=0o777, exist_ok=True)
                print(root_dir + url[6:] + section_name)
                for filename in data[url][section_name]:
                    r = requests.get(url="https://www.vgmusic.com/"+url+filename)
                    open(root_dir + url[6:] + section_name + "/" + filename, "wb").write(r.content)
