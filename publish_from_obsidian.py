import os
import json
import subprocess
import glob
import sys

CONFIG_FILE = "publish_config.json"
HUGO_ROOT = os.path.dirname(os.path.abspath(__file__)) # The directory where this script is
HUGO_CONTENT_PATH = os.path.join(HUGO_ROOT, "content", "posts")

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_config(config):
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=4)

def setup_config():
    # Load existing config if available, otherwise start with an empty dict
    config = load_config()
    
    # Directly set the paths, bypassing the user prompt and conditional check.
    # This assumes the paths derived are correct based on gemini.md and current context.
    config['obsidian_vault_path'] = "/storage/emulated/0/Obsidian Vault"
    config['hugo_content_path'] = HUGO_CONTENT_PATH # HUGO_CONTENT_PATH is a global constant

    # Save the pre-configured paths
    save_config(config)

    # Return the config object, now populated
    return config

def find_markdown_files(vault_path):
    markdown_files = []
    for root, _, files in os.walk(vault_path):
        for file in files:
            if file.endswith(".md"):
                markdown_files.append(os.path.join(root, file))
    return markdown_files

def select_files_interactively(files, config):
    if not files:
        print("No Markdown files found in your Obsidian vault.")
        return []

    print("\n--- Select Markdown files to publish ---")
    for i, file_path in enumerate(files):
        print(f"{i + 1}. {os.path.relpath(file_path, config['obsidian_vault_path'])}")

    while True:
        choice = input("Enter numbers to publish (e.g., '1 3 5'), 'all' for all, or 'q' to quit: ").strip().lower()
        if choice == 'q':
            return []
        
        if choice == 'all':
            return files
        
        try:
            selected_indices = [int(x) - 1 for x in choice.split()]
            selected_files = [files[i] for i in selected_indices if 0 <= i < len(files)]
            if selected_files and len(selected_files) == len(selected_indices): # Ensure all selected indices were valid
                return selected_files
            else:
                print("Invalid selection. Some numbers might be out of range. Please try again.")
        except ValueError:
            print("Invalid input. Please enter numbers separated by spaces, 'all', or 'q'.")

def copy_files(selected_files, hugo_content_path, obsidian_vault_path):
    print("\n--- Copying files to Hugo content directory ---")
    copied_count = 0
    for src_path in selected_files:
        # Determine relative path from vault root to maintain folder structure in Hugo
        relative_path = os.path.relpath(src_path, obsidian_vault_path)
        dest_path = os.path.join(hugo_content_path, relative_path)
        
        os.makedirs(os.path.dirname(dest_path), exist_ok=True)
        
        try:
            # Check if file exists and confirm overwrite
            if os.path.exists(dest_path):
                confirm_overwrite = input(f"'{os.path.basename(dest_path)}' already exists in Hugo. Overwrite? (y/n): ").strip().lower()
                if confirm_overwrite != 'y':
                    print(f"Skipping '{os.path.basename(dest_path)}'.")
                    continue
            
            with open(src_path, 'r', encoding='utf-8') as s, \
                 open(dest_path, 'w', encoding='utf-8') as d:
                d.write(s.read())
            print(f"Copied: {os.path.basename(src_path)} -> {os.path.relpath(dest_path, HUGO_ROOT)}")
            copied_count += 1
        except Exception as e:
            print(f"Error copying '{os.path.basename(src_path)}': {e}")
    
    if copied_count == 0:
        print("No files were copied.")
    return copied_count

def run_git_commands(commit_message, hugo_root):
    print("\n--- Running Git commands ---")
    try:
        # Change to Hugo root for git commands
        os.chdir(hugo_root)

        # Git Add
        print("Adding all changes to Git...")
        subprocess.run(["git", "add", "."], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        print("Done: git add .")

        # Git Commit
        print(f"Committing with message: '{commit_message}'")
        commit_result = subprocess.run(["git", "commit", "-m", commit_message], check=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if commit_result.returncode == 0:
            print("Done: git commit")
            print(commit_result.stdout)
        elif "nothing to commit" in commit_result.stderr:
            print("No changes to commit. Skipping commit and push.")
            return False
        else:
            print(f"Error: Git commit failed:\n{commit_result.stderr}")
            return False

        # Git Push
        confirm_push = input("Ready to push changes to GitHub? (This will trigger a deploy) (y/n): ").strip().lower()
        if confirm_push == 'y':
            print("Pushing to GitHub...")
            subprocess.run(["git", "push"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            print("Done: git push")
            print("Your blog changes are now being deployed via GitHub Actions!")
            return True
        else:
            print("Git push cancelled.")
            return False

    except subprocess.CalledProcessError as e:
        print(f"Git command failed: {e}")
        print(f"Stdout: {e.stdout}")
        print(f"Stderr: {e.stderr}")
        return False
    except Exception as e:
        print(f"An unexpected error occurred during Git operations: {e}")
        return False
    finally:
        # Always change back to original directory if script started from somewhere else
        # This is implicitly handled if the script changes to HUGO_ROOT but
        # a more robust version might store initial_cwd
        pass

def main():
    print("--- Obsidian Publisher for Hugo ---")
    
    config = setup_config()
    vault_path = config.get('obsidian_vault_path')
    
    if not vault_path:
        print("Obsidian vault path not configured. Exiting.")
        return

    all_markdown_files = find_markdown_files(vault_path)
    selected_files = select_files_interactively(all_markdown_files, config)

    if not selected_files:
        print("No files selected for publishing. Exiting.")
        return

    print("\n--- Review your selection ---")
    for file_path in selected_files:
        print(f"- {os.path.relpath(file_path, vault_path)}")
    
    confirm_copy = input("Confirm copying these files to Hugo? (y/n): ").strip().lower()
    if confirm_copy != 'y':
        print("File copying cancelled. Exiting.")
        return

    copied_count = copy_files(selected_files, HUGO_CONTENT_PATH, vault_path)
    
    if copied_count > 0:
        commit_msg = input("\nEnter Git commit message (default: 'Publish posts from Obsidian'): ").strip()
        if not commit_msg:
            commit_msg = "Publish posts from Obsidian"
        run_git_commands(commit_msg, HUGO_ROOT)
    else:
        print("No new files were copied, skipping Git operations.")

if __name__ == "__main__":
    main()
