# CSE533 - Social Network Analysis

## SciCon - Scientific Connections

### Project Structure

```
SNA_PROJECT
├────────── src
|           ├── graph.py
|           └── scicon.py
└────────── vendor
            └───── Gephi-0.10.1 (WINDOWS)
```

### Project Installation

1. Clone the repo, from the code tab above, to the desired location.
2. Installing vendor\Gephi
    1. If you already have `gephi` installed, you can either skip step 2 or move gephi under the `vendor` folder. If `gephi` isn't installed please follow step 2.
    2. Navigate to `vendor` and and install [gephi](https://gephi.org/users/download/) for your device under a folder named `Gephi` in vendor.

### Project Execution

1. Open command prompt and navigate under the `src` folder.

```
usage: scicon iterate [-v] [--gephi-path PATH_TO_GEPHI]
                      [head]
                      [connections]

positional arguments:
  head                  starting link to the person's profile
  connections           how many child connections to iterate

options:
  -v, --verbose         for detailed output
  --gephi-path          to use an installation of gephi other the one provided in vendor
```