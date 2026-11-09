# Evidence claims (project-local)

One JSON object per line (`.jsonl`). Each claim must reference a verified source
in the project registry and include a locator and checked date.

Example:

```json
{"id":"C001","statement":"...","value":1.0,"unit":"V","conditions":"1 kHz, 10 kOhm load","source":"S001","locator":"datasheet p. 5, table 2","confidence":"high","checked":"YYYY-MM-DD"}
```
