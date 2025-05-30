# A Practical Guide on How to Use Git


## How to Install Git

**Windows:**
- Download from [git-scm.com](https://git-scm.com/)
- Run the installer with default settings
- Open Git Bash or Command Prompt to verify: `git --version`

**macOS:**
- Install via Homebrew: `brew install git`
- Or download from [git-scm.com](https://git-scm.com/)
- Verify: `git --version`

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install git
```

**First-time setup:**
```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

---

## Create Your First Git Repository

Let's start by creating a new directory for our project:

```bash
mkdir my_first_repo
cd my_first_repo
```

Now we have an empty folder. This is just a regular folder - it's not a git repository yet.

---

## Git Init

To turn our regular folder into a git repository, we use:

```bash
git init
```

**What happened?**
- Git created a hidden `.git` folder in your directory
- This folder contains all the git metadata and history
- Your folder is now a git repository!

You can see the hidden folder with:
```bash
ls -la  # On Linux/macOS
dir /a  # On Windows
```

---

## Basic Concepts and Jargon in Git - What is a Commit?

**Key Terms:**

**Repository (repo):** A folder that git is tracking. Contains your project files plus the `.git` folder with all the history.

**Commit:** A snapshot of your project at a specific point in time. Think of it like taking a photo of all your files at once. Each commit has:
- A unique ID (hash)
- A timestamp
- Your name and email
- A message describing what changed

**Working Directory:** The actual files you see and edit in your folder.

**Staging Area:** A "holding area" where you prepare files before committing them.

---

## Let's Create a First File in the Repo

Create a simple text file:

```bash
echo "Hello, Git!" > readme.txt
```

Or create it with your favorite text editor. The file should contain:
```
Hello, Git!
```

Now we have a file in our repository, but git doesn't know about it yet.

---

## Git Status - What Does It Do?

```bash
git status
```

**Output will look like:**
```
On branch main

No commits yet

Untracked files:
  (use "git add <file>..." to include in what will be committed)
        readme.txt

nothing added to commit but untracked files present (use "git add" to track)
```

**What this tells us:**
- We're on branch "main" (the default branch)
- No commits exist yet
- `readme.txt` is "untracked" - git sees it but isn't monitoring it
- Git suggests using `git add` to start tracking the file

---

## The Concept of a Staging Area

Git has a three-stage workflow:

1. **Working Directory** ← You edit files here
2. **Staging Area** ← You prepare files here (with `git add`)
3. **Repository** ← You save snapshots here (with `git commit`)

```
Working Directory → [git add] → Staging Area → [git commit] → Repository
```

The staging area lets you choose exactly which changes to include in your next commit.

**Add our file to staging:**
```bash
git add readme.txt
```

**Check status again:**
```bash
git status
```

Now you'll see:
```
On branch main

No commits yet

Changes to be committed:
  (use "git rm --cached <file>..." to unstage)
        new file:   readme.txt
```

The file is now "staged" and ready to be committed.

---

## Let's Make a Commit

```bash
git commit -m "Add initial readme file"
```

**What happened?**
- Git created a snapshot of the staged files
- The snapshot got a unique ID (hash)
- The message "Add initial readme file" describes this commit
- The staging area is now empty

**Check status:**
```bash
git status
```

Output:
```
On branch main
nothing to commit, working tree clean
```

This means everything is saved and there are no changes to commit.

---

## Let's Look at the History of the Repo - Git Log with Decorators

```bash
git log --oneline --decorate --graph
```

**Output looks like:**
```
* a1b2c3d (HEAD -> main) Add initial readme file
```

**Breaking it down:**
- `a1b2c3d`: The commit hash (shortened)
- `(HEAD -> main)`: Decorators showing where we are
- `Add initial readme file`: The commit message

**For more detail:**
```bash
git log
```

Shows full information: hash, author, date, and message.

---

## What Does HEAD Mean?

**HEAD** is a pointer that shows you where you currently are in your git history.

- HEAD points to the latest commit on your current branch
- Think of it as "You Are Here" marker
- When you make a new commit, HEAD moves to point to it
- `HEAD -> main` means HEAD is pointing to the latest commit on the main branch

---

## Let's Change the File and Make Another Commit

Edit your readme.txt file:
```bash
echo "Hello, Git! This is my first repository." > readme.txt
```

**Check what changed:**
```bash
git status
```

Output:
```
On branch main
Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git checkout -- <file>..." to discard changes in working directory)
        modified:   readme.txt
```

**Stage and commit the changes:**
```bash
git add readme.txt
git commit -m "Update readme with more descriptive text"
```

---

## Now We Can Look at Log Again

```bash
git log --oneline --decorate --graph
```

**Output:**
```
* b2c3d4e (HEAD -> main) Update readme with more descriptive text
* a1b2c3d Add initial readme file
```

**Notice:**
- We now have 2 commits
- HEAD points to the most recent commit
- Each commit has a unique hash
- The commits are listed newest to oldest

---

## Git Diff to Look at Differences Between Files

**See what changed in the working directory:**
```bash
git diff
```
(This shows nothing if there are no changes)

**See what's staged:**
```bash
git diff --staged
```

**See differences between commits:**
```bash
git diff a1b2c3d b2c3d4e
```
(Use your actual commit hashes)

**Make a small change to test diff:**
```bash
echo "Hello, Git! This is my first repository. I'm learning version control." > readme.txt
```

**Now check the diff:**
```bash
git diff
```

Shows exactly what lines changed, with `+` for additions and `-` for deletions.

---

## Let's Make an Additional File and Make a Commit

Create a new file:
```bash
echo "# My Project\n\nThis is a sample project for learning Git." > project_info.md
```

**Check status:**
```bash
git status
```

**Stage both files (the modified readme.txt and new project_info.md):**
```bash
git add .
```

The `.` means "add all changes in the current directory"

**Commit:**
```bash
git commit -m "Add project info and update readme"
```

---

## Look at the Log Again

```bash
git log --oneline --decorate --graph
```

**Output:**
```
* c3d4e5f (HEAD -> main) Add project info and update readme
* b2c3d4e Update readme with more descriptive text
* a1b2c3d Add initial readme file
```

**Try the detailed log:**
```bash
git log --stat
```

This shows which files were changed in each commit.

---

## What if We Want to Go Back to a Previous State? Git Checkout

**See your current files:**
```bash
ls
```

You should see both `readme.txt` and `project_info.md`

**Go back to the first commit:**
```bash
git checkout a1b2c3d
```
(Use your actual first commit hash)

**Important warning will appear:**
```
You are in 'detached HEAD' state...
```

**Look at your files now:**
```bash
ls
cat readme.txt
```

**What happened?**
- Only `readme.txt` exists
- It contains the original text: "Hello, Git!"
- `project_info.md` is gone
- This is exactly how your folder looked after the first commit

---

## Git Actually Changes the State of the Current Folder

This is the key insight: **Git doesn't just track history - it can recreate any previous state of your project.**

**Your folder literally becomes what it was at that commit:**
- Files that didn't exist yet disappear
- Files that were deleted come back
- All content reverts to exactly what it was

**To go back to the latest state:**
```bash
git checkout main
```

**Check your files:**
```bash
ls
cat readme.txt
```

Everything is back to the latest version!

**Alternative: You can also use commit hashes to jump around:**
```bash
git checkout b2c3d4e  # Go to second commit
git checkout main     # Always returns to latest
```

---

## Summary of Key Commands

```bash
git init                    # Initialize repository
git status                  # Check current state
git add <file>             # Stage files
git add .                  # Stage all changes
git commit -m "message"    # Create commit
git log                    # View history
git log --oneline          # Compact history
git diff                   # See unstaged changes
git diff --staged          # See staged changes
git checkout <commit>      # Go to specific commit
git checkout <branch>      # Go to specific branch
```

---

## Key Concepts Recap

1. **Repository**: A folder tracked by git
2. **Commit**: A snapshot of your project
3. **Staging Area**: Where you prepare changes before committing
4. **HEAD**: Pointer to your current location in history
5. **Working Directory**: The actual files you see and edit
6. **Git changes your folder**: When you checkout commits, git physically changes your files to match that point in history

The power of git is that it lets you save multiple snapshots of your work and jump between them instantly, like having a time machine for your code!