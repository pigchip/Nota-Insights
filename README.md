# Nota Insights 🚀

This application is a Natural Language Processing (NLP) tool focused on analyzing and manipulating textual information. It integrates various functionalities such as search engines, content recommendation, plagiarism analysis, identification of trends in social media, and automatic summary generation. To achieve this, it uses a news corpus stored in CSV format and BERT-based models to obtain semantic representations of texts.

## Key Features ✨

1. **Search Engine 🔍:**  
   Given a user prompt or query, the most relevant documents from the corpus are retrieved and ranked according to their similarity to the query.

2. **Content Recommendation 💡:**  
   Based on a series of keywords, the application suggests the most relevant articles or news.

3. **Plagiarism Analysis 📝:**  
   Detects duplication or textual similarity. It provides a plagiarism percentage after comparing the input text with documents from the corpus.

4. **Document Trends 📊:**  
   Identifies and summarizes the most relevant trends. Displays graphs and summaries of emerging topics based on available information.

5. **Automatic Summarization ✂️:**  
   Generates document summaries. It leverages BERT models to understand the semantic context of each text.

## Requirements and Dependencies 🛠️

- **Python 3.8+**  
- **Python Libraries:**  
  - `customtkinter` 🖥️  
  - `CTkTable` 📋  
  - `PIL` (Pillow) 🖼️
  - `PyInstaller` 🛠️

To install the dependencies, use `pip`:

```bash
pip install customtkinter CTkTable Pillow pyinstaller
```

## Corpus Preparation 📂

1. The corpus must be stored in CSV format.
2. Ensure that fields are structured appropriately to facilitate processing.

## Application Execution ▶️

1. Clone the repository or download the source code.
2. Install the dependencies (see the previous section).
3. Run the main script (e.g., `app.py` or `main.py`, depending on its actual name):

```bash
python src/main.py
```

4. The graphical interface will open. Use the sidebar to navigate through the different sections (Search, Recommendation, Plagiarism, Trends, Summary).

## Creating the Executable 🖱️

Use the following command in Git Bash or any terminal:

```bash
pyinstaller --onefile --noconsole --icon=assets/images/logo.ico \
--add-data "assets/images/logo.ico;assets/images" \
--add-data "assets/images/article.png;assets/images" \
--add-data "assets/images/bars.png;assets/images" \
--add-data "assets/images/bug.png;assets/images" \
--add-data "assets/images/like.png;assets/images" \
--add-data "assets/images/logo.png;assets/images" \
--add-data "assets/images/search.png;assets/images" \
--add-data "assets/images/chart.png;assets/images" \
--name "Nota Insights" \
src/main.py
```

### Command Details 🔧:

- **`--onefile`**: Generates a single executable file.
- **`--noconsole`**: Prevents a terminal window from appearing when running the application.
- **`--icon=logo.ico`**: Sets a custom icon for the executable.
- **`--add-data`**: Includes additional resources (images, icons, etc.) required for the application. Each item must specify its original path and destination path separated by `;`.

Once completed, the executable will be located in the `dist/` folder generated by PyInstaller. 📁

