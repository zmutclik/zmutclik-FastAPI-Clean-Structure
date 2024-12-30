import os
import json

snippet_body = []
snippet_body.append("import os")


def scan_folder(source_folder):
    if not os.path.exists(source_folder):
        raise FileNotFoundError(f"Folder sumber '{source_folder}' tidak ditemukan.")

    for root, dirs, files in os.walk(source_folder):
        # Hitung path relatif dari folder sumber
        relative_path = os.path.relpath(root, source_folder)
        # Gabungkan path relatif dengan folder target
        # target_path = os.path.join(target_folder, relative_path)

        # Buat folder di target
        # os.makedirs(relative_path, exist_ok=True)
        # print(relative_path)

        snippet_body.append(f'os.makedirs("{relative_path}", exist_ok=True)')

        for file in files:
            source_file_path = os.path.join(root, file)
            target_file_path = os.path.join(relative_path, file)
            print("source_file_path : ",source_file_path)
            # if not os.path.exists(target_file_path):
            #     open(target_file_path, 'w').close()
            with open(source_file_path, "r") as f:
                file_contents = f.readlines()

            snippet_body.append(f'if not os.path.exists("{target_file_path}"):')
            snippet_body.append(f"  file = open(\"{target_file_path}\", 'a')")
            for line in file_contents:
                # snippet_body.append(line.rstrip())
                linestr = line.rstrip()
                linestr = linestr.replace("\"", "\\\"")
                snippet_body.append(f'  file.write("' + linestr + ' \\n")')
                
            snippet_body.append(f'  file.close()')


def generate_snippet_from_file(file_path, snippet_name, prefix, description):
    # if not os.path.exists(file_path):
    #     raise FileNotFoundError(f"File '{file_path}' not found.")

    # # Read the contents of the file
    # with open(file_path, "r") as f:
    #     file_contents = f.readlines()

    # # Prepare the snippet body
    # for line in file_contents:
    #     snippet_body.append(line.rstrip())

    # Generate snippet
    snippet = {
        snippet_name: {
            "prefix": prefix,
            "body": snippet_body,
            "description": description,
        }
    }
    return snippet


def save_snippet(snippet, output_folder, output_file):
    output_file = os.path.join(output_folder, output_file)
    with open(output_file, "w") as f:
        json.dump(snippet, f, indent=4)
    print(f"Snippet saved to '{output_file}'")


if __name__ == "__main__":

    base_folder = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.join(base_folder, "genappmodule")
    print(base_folder)

    # Snippet details
    # snippet_name = input("Enter folder to copy: ")
    snippet_name = "genappmodule"
    description = "Generate a Python module with a full folder structure and files"
    output_file = "genappmodule.code-snippets"

    if not os.path.exists(snippet_name):
        raise FileNotFoundError(f"Folder sumber '{snippet_name}' tidak ditemukan.")

    scan_folder(file_path)

    try:
        snippet = generate_snippet_from_file(
            file_path,
            snippet_name,
            snippet_name,
            description,
        )
        save_snippet(snippet, base_folder, output_file)
    except Exception as e:
        print(f"Error: {e}")
