# JSONBinIO

This is a light python wrapper for the [JSONBinIO](https://jsonbin.io/) api, provides free JSON storage.

## Installation

Download repo, cd into directory, then:

```
pip install . --upgrade
```

## Usage

**Open a session**

```
session = JSONBinIO("secret key")
```

**Create a bin**

```
mydata = {'data': 5}
collection_id = "adg984hg0" # optional
mybin = session.create_bin(mydata, collection_id=collection_id)
```

**Open existing bin**

```
bin_id = "ajfse98234hgo8say9t8yhw"
mybin = session.bin(bin_id)
```

**Read bin**

```
mybin.read()
```

**Update bin**

```
mybin.update({"data": 6})
```

**Merge bin**

```
mybin.merge({"newdata": "this is added to existing data")
```

**Delete bin**

```
mybin.delete()
```