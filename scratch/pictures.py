import os


def get_folder_imgs(folder_path):
    return sorted(
        [
            os.path.join(folder_path, f)
            for f in os.listdir(folder_path)
            if os.path.isfile(os.path.join(folder_path, f))
        ]
    )


def get_python_pictures():
    pictures = {}
    pictures["greeting"] = get_folder_imgs(
        "/Users/vadim/Documents/algoritmika/my_cards/"
    )
    pictures["cards"] = get_folder_imgs(
        "/Users/vadim/Documents/algoritmika/scratch_img"
    )
    pictures["invitation"] = "/Users/vadim/Documents/algoritmika/scratch_invitation.jpeg"
    return pictures
