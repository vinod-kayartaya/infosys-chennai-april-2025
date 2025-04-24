# Vim Editor Tutorial

## Table of Contents

1. [Introduction to Vim](#introduction-to-vim)
2. [Installation](#installation)
3. [Basic Concepts](#basic-concepts)
4. [Modes in Vim](#modes-in-vim)
5. [Basic Commands](#basic-commands)
6. [Advanced Features](#advanced-features)
7. [Tips and Tricks](#tips-and-tricks)
8. [Practice Exercises](#practice-exercises)

## Introduction to Vim

Vim (Vi IMproved) is a highly configurable text editor built to enable efficient text editing. It is an improved version of the vi editor distributed with most UNIX systems. Vim is often called a "programmer's editor" and is so useful for programming that many consider it an entire IDE.

### Why Learn Vim?

- Available on almost every Unix-like system
- Works in terminal environments
- Highly efficient for text editing
- Powerful features for programming
- Lightweight and fast
- Extensive customization options

## Installation

### Installing Vim on Ubuntu

```bash
# Update package list
sudo apt update

# Install Vim
sudo apt install vim

# Verify installation
vim --version
```

### Installing Additional Vim Features

```bash
# Install Vim with additional features
sudo apt install vim-gtk3  # For GUI support
sudo apt install vim-doc   # For documentation
```

## Basic Concepts

### Vim's Philosophy

Vim follows a modal editing approach, where different modes are used for different tasks:

- Normal mode: For navigation and commands
- Insert mode: For typing text
- Visual mode: For selecting text
- Command mode: For executing commands

### The Vim Interface

When you start Vim, you'll see:

- Status line at the bottom
- Line numbers (if enabled)
- Current mode indicator
- File information

## Modes in Vim

### 1. Normal Mode

- Default mode when Vim starts
- Used for navigation and commands
- Press `Esc` to return to Normal mode
- Commands are case-sensitive

### 2. Insert Mode

- Used for typing text
- Enter with `i`, `a`, `o`, `O`
- Exit with `Esc`
- Different ways to enter Insert mode:
  - `i`: Insert before cursor
  - `a`: Append after cursor
  - `o`: New line below
  - `O`: New line above

### 3. Visual Mode

- Used for selecting text
- Enter with `v`, `V`, `Ctrl+v`
- Exit with `Esc`
- Different visual modes:
  - `v`: Character-wise selection
  - `V`: Line-wise selection
  - `Ctrl+v`: Block-wise selection

### 4. Command Mode

- Used for executing commands
- Enter with `:`
- Exit with `Enter` or `Esc`
- Examples:
  - `:w` - Save file
  - `:q` - Quit
  - `:wq` - Save and quit

## Basic Commands

### Navigation

```vim
h - Move left
j - Move down
k - Move up
l - Move right

w - Move to next word
b - Move to previous word
e - Move to end of word

0 - Move to start of line
$ - Move to end of line

gg - Move to start of file
G - Move to end of file

Ctrl+f - Page down
Ctrl+b - Page up
```

### Editing

```vim
i - Insert before cursor
a - Append after cursor
o - New line below
O - New line above

x - Delete character under cursor
dd - Delete line
yy - Copy line
p - Paste after cursor
P - Paste before cursor

u - Undo
Ctrl+r - Redo
```

### Search and Replace

```vim
/pattern - Search forward
?pattern - Search backward
n - Next match
N - Previous match

:%s/old/new/g - Replace all occurrences
:%s/old/new/gc - Replace with confirmation
```

### File Operations

```vim
:w - Save file
:q - Quit
:wq - Save and quit
:q! - Quit without saving
:w filename - Save as new file
```

## Advanced Features

### 1. Registers

- Vim has multiple registers for storing text
- Use `"` followed by register name
- Examples:
  ```vim
  "ayy - Copy line to register a
  "ap - Paste from register a
  ```

### 2. Macros

- Record and replay sequences of commands
- Start recording: `q` followed by register name
- Stop recording: `q`
- Play macro: `@` followed by register name

### 3. Marks

- Set marks to jump to specific locations
- Set mark: `m` followed by letter
- Jump to mark: `'` followed by letter
- Examples:
  ```vim
  ma - Set mark a
  'a - Jump to mark a
  ```

### 4. Folding

- Collapse sections of text
- Commands:
  ```vim
  zf - Create fold
  zo - Open fold
  zc - Close fold
  zR - Open all folds
  zM - Close all folds
  ```

## Tips and Tricks

### 1. Configuration

Create or edit `~/.vimrc`:

```vim
" Basic settings
set number          " Show line numbers
set relativenumber  " Show relative line numbers
set autoindent      " Auto-indent new lines
set smartindent     " Smart auto-indenting
set tabstop=4       " Number of spaces per tab
set shiftwidth=4    " Number of spaces for auto-indent
set expandtab       " Convert tabs to spaces
set showmatch       " Show matching brackets
set incsearch       " Incremental search
set hlsearch        " Highlight search results
```

### 2. Useful Plugins

- Vim-Plug (Plugin manager)
- NERDTree (File explorer)
- YouCompleteMe (Code completion)
- vim-airline (Status bar)
- vim-gitgutter (Git integration)

### 3. Keyboard Shortcuts

```vim
Ctrl+w s - Split window horizontally
Ctrl+w v - Split window vertically
Ctrl+w h/j/k/l - Navigate between windows
Ctrl+w +/- - Increase/decrease window height
Ctrl+w </> - Increase/decrease window width
```

## Practice Exercises

### Exercise 1: Basic Navigation

1. Open a new file: `vim practice.txt`
2. Enter some text
3. Practice moving around using h, j, k, l
4. Try word navigation with w, b, e
5. Save and quit

### Exercise 2: Editing

1. Create a new file
2. Practice inserting text
3. Try deleting and copying lines
4. Practice undoing and redoing changes
5. Save your work

### Exercise 3: Search and Replace

1. Create a file with repeated words
2. Practice searching for words
3. Try replacing words
4. Use different search patterns
5. Save and quit

### Exercise 4: Advanced Features

1. Try using registers
2. Record and play a macro
3. Set and use marks
4. Practice folding
5. Save and quit

## Additional Resources

- [Vim Documentation](https://vimhelp.org/)
- [Vim Interactive Tutorial](https://www.openvim.com/)
- [Vim Cheat Sheet](https://vim.rtorr.com/)
- [Vim Adventures](https://vim-adventures.com/)
- [Vim Stack Exchange](https://vi.stackexchange.com/)
