import os
import subprocess
import argparse

def main():
    parser = argparse.ArgumentParser(description='Process Witcher 3 save file.')
    parser.add_argument('save_file_path', type=str, help='Path to the original save file')
    args = parser.parse_args()

    save_file_path = args.save_file_path
    offzip_path = r".\offzip.exe"
    
    # Get the directory of the save file
    save_file_dir = os.path.dirname(save_file_path)
    output_file = os.path.join(save_file_dir, "0000000c.snf")
    
    # Step 1: Execute Offzip command
    offzip_command = f"{offzip_path} -a {save_file_path} {save_file_dir}\ 0"
    print(f"Running command: {offzip_command}")

    try:
        result = subprocess.run(offzip_command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        print("stdout:", result.stdout)
        print("stderr:", result.stderr)
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while running command: {e}")
        print("stdout:", e.stdout)
        print("stderr:", e.stderr)
        return

    # Step 2: Modify the hex file
    with open(output_file, 'r+b') as f:
        f.seek(0xC16)
        f.write(bytes([0x12]))

    # Step 3: Rename the modified file
    new_save_file_name = save_file_path.replace(".sav", ".sav.pc_save")
    os.rename(output_file, new_save_file_name)
    print("Save file conversion complete.")

if __name__ == "__main__":
    main()
