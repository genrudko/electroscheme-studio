# Patch 039 repair1 — fix VSDX page relations and resume

Patch 039 generated symbols but reported:

```text
VSDX_PAGE_BACKED_SYMBOL_COUNT=0
```

Cause: `pages.xml` stores relation ids inside child nodes:

```xml
<Page ...>
  <Rel r:id="rId1"/>
</Page>
```

Repair1 maps:

```text
Page -> Rel r:id -> pageN.xml -> Shape Master -> VSDX library category
```

It also adds the missing Ribbon model tab:

```text
Соединения
```
