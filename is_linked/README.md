# is_linked

Python script to detect if a pptx or xlsx is a linked file. Detection method is not perfect but works for my intended use.

Typical usage:

```bash
find . \( -name '*.pptx' -o -name '*.xlsx' \) -exec is_linked.py {} \;
```
Or even better:
```
find .  \( -name '*.pptx' -o -name '*.xlsx' \) | parallel -j 15 "is_linked.py -v {}" | tee -a out.txt
```

