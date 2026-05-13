# LaTeX Tools

Common commands for compiling, checking, and managing LaTeX files.

## Compilation

```bash
# Compile .tex to PDF
pdflatex -interaction=nonstopmode <file>.tex

# Smart compile (handles references, TOC automatically)
latexmk -pdf <file>.tex

# Clean intermediate files (.aux, .log, .toc, etc.)
latexmk -c <file>.tex
```

## Syntax Check

```bash
# Check for common LaTeX errors and style issues
chktex <file>.tex
```

## Notes

- Always use `pdflatex -interaction=nonstopmode` to avoid interactive prompts on errors.
- Run `pdflatex` twice if the document has cross-references (`\ref`, `\label`).
- Use `latexmk -pdf` to handle this automatically.
- After compilation, clean up with `latexmk -c` to remove intermediate files.
