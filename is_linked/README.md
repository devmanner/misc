# is_linked

Python script to detect if a pptx or xlsx is a linked file. Detection method is not perfect but works for my intended use.

Typica usage:

```bash
find . \( -name '*.pptx' -o -name '*.xlsx' \) -exec is_linked.py {} \;
```

