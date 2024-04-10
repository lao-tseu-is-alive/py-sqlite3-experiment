# py-sqlite3-experiment
Using python3 to manipulate sqlite3 database

## How to run :

```bash
python create-db.py data/test.sqlite3 lausanne%gratta%3
```
will output :
<pre>## [SearchDb::__init__] 👍 the database &apos;data/test.sqlite3&apos; was found
# 🚀 Connected to database data/test.sqlite3  successfully
## [SearchDb::count] 📊 Total rows in search_item table: 160190
# 📊 Total rows in search_item table: 160190
## [SearchDb::search] 🔍 Found 1 rows in search_item table with keyword &apos;lausanne%gratta%3&apos;
# 📊 Found 1 rows in search_item table with keyword &apos;lausanne%gratta%3&apos;
# num_record: 2
#records:
[{&quot;info&quot;:&quot;Avenue de Gratta-Paille 13, 1018 Lausanne&quot;,&quot;x&quot;:2537082,&quot;y&quot;:1154187},{&quot;info&quot;:&quot;Avenue de Gratta-Paille 3, 1018 Lausanne&quot;,&quot;x&quot;:2536993,&quot;y&quot;:1154182}]

## [SearchDb::close] 🏁 closed Database &apos;data/test.sqlite3&apos; successfully
</pre>





```bash
python create-db.py data/test.sqlite3 lausanne%gratta%3 |grep -v '#'|jq
```
will filter only the json output :

```json
[
  {
    "info": "Avenue de Gratta-Paille 13, 1018 Lausanne",
    "x": 2537082,
    "y": 1154187
  },
  {
    "info": "Avenue de Gratta-Paille 3, 1018 Lausanne",
    "x": 2536993,
    "y": 1154182
  }
]

