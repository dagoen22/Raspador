# 🤖✨ **Website Scraper with Craw4ai** ✨🤖
> "Because copying and pasting is so last decade... and web scraping has never been easier! 🚀"

This is a powerful and flexible Python script to scrape website content and save the results in Markdown files. It uses `crawl4ai` to handle the heavy lifting and offers various options for customizing how the data is saved.

Easily create context for your LLM with just one command!
---
## 📦 **Prerequisites**
Before you begin, make sure you have the following installed:
1. **Python 3.8+**: Because Python is life! 🐍
2. **Git**: To clone the repository. (`sudo apt install git`)
3. **uv**: The fastest Python package manager in the world! ⚡ ([Install here](https://github.com/astral-sh/uv))
---
## 🚀 **Quick Installation**
### 1. Clone the repository
```bash
git clone https://github.com/dagoen22/Raspador.git
cd Raspador
```

## 🎮 **How to Use**
### 1. Run the script without parameters to see the help message
```bash
uv run python main.py
```
Output:
```
usage: main.py [-h] [--site SITE] [--split [SPLIT]]
Scrape a website and save the results as Markdown files.
options:
  -h, --help       show this help message and exit
  --site SITE      The base URL of the website to scrape (e.g., https://example.com)
  --split [SPLIT]  Split the output into multiple files. Provide a number to specify how many files to split into. If no number is provided, each URL will be saved in a separate file.
```
### 2. Scrape an entire site and save everything in a combined file 📝
```bash
uv run python main.py --site https://example.com
```
Result:
```
/documents
    example_com_combined.md
```
### 3. Split the content into separate files by URL 📂
```bash
uv run python main.py --site https://example.com --split
```
Result:
```
/documents
    example_com_1.md
    example_com_2.md
    example_com_3.md
    ...
```
### 4. Split the content into a specific number of files 🔢
```bash
uv run python main.py --site https://example.com --split 3
```
Result:
```
/documents
    example_com_1.md
    example_com_2.md
    example_com_3.md
```
---
## 🎨 **Customization Options**
| Option         | Description                                                                 | Example                              |
|---------------|---------------------------------------------------------------------------|--------------------------------------|
| `--site`      | The website you want to scrape. 🌐                                         | `--site https://example.com`        |
| `--split`     | Splits the content into separate files. Can be used with or without a number. | `--split`, `--split 3`              |
---
## 🛠️ **Tips and Tricks**
1. **Use `uv` to quickly install dependencies** ⚡
   ```bash
   uv pip install -r requirements.txt
   ```
2. **Check the `documents` directory after each run** 📁
   All Markdown files will be saved there!
3. **Scrape large sites carefully** 🚧
   Some websites may block your IP if you make too many requests quickly. Use proxies or intervals between requests if necessary.
4. **Keep it simple**
   Set an alias and call it via the command line. Example:
   ```bash
   echo "alias scraper=\"uv run {PWD}/main.py\"" >> .bashrc"
   ```
   When you want to use it, just call `scraper` via the command line, e.g.: `scraper --site example.com`
---
## 🤔 **Why Use This Script?**
- **Easy to use**: Just run the command and you're done! 🎉
- **Flexible**: Combine or split content however you like. 🧩
- **Fast**: With `uv`, your dependencies are installed in seconds! ⚡
- **Fun**: Who said programming can't be fun? 😄
## 🙏 **Contributions**
If you find bugs or want to add new features, feel free to open an issue or send a pull request! 🚀
---
## 📜 **License**
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.
---
🎉 **Happy scraping with style!** 🎉  
_"Because copying and pasting is so last decade."_ 🤖✨
