<p align="center">
  <h1 align="center">MeetingStats</h1>
</p>

## Overview

MeetingStats is a small Python utility to parse an iCalendar (ics) file to compute the time spent in meetings.

![Meeting Stats](docs/doc.png?raw=true "Meeting Stats")

## Getting Started

### Installing Anaconda Python (Recommended)

All perquisites are installed as a part of [Anaconda Python](https://www.anaconda.com/distribution/#download-section).

Supported Configurations:

| OS      | Python version |
| ------- | -------------- |
| MacOS   | 3.9  |
| Ubuntu  | 3.9  |
| Windows | 3.9  |


### (Optional) Create a virtual environment

I strongly recommend using a virtual environment to ensure dependencies are  installed safely. This is an optional setup, but if you have trouble running the scripts, try this first.

The instructions below assume you are using Conda, though Virtualenv is essentially interchangeable. To create a new Python 3.7 environment, run:

```bash
conda create --name meetingstats python=3.9
conda activate meetingstats
```

The shell should now look like `(meetingstats) $`. To deactivate the environment, run:

```bash
(meetingstats)$ conda deactivate
```

The prompt will return back to `$ ` or `(base)$`.

Note: Older versions of conda may use `source activate meetingstats` and `source
deactivate` (`activate meetingstats` and `deactivate` on Windows).

### Installing dependencies

All of the required packages should have been installed via Anaconda. If you are using another distribution of Python, then you might need to run
```bash
(meetingstats)$ pip install -r requirements.txt
```
To install the required packages.

### Cloning the repo

To checkout the repo:

```bash
git clone git@github.com:jiuguangw/MeetingStats.git
```

### Running the script
Place an ICS file (for example, exported from Google Calendar) in the same directory.

```bash
(meetingstats)$ python MeetingStats.py jw.ics
```
MeetingStats.pdf is generated with the plots.

## Contact

- Jiuguang Wang
- [jw@robo.guru](mailto:jw@robo.guru?subject=MeetingStats)
- [www.robo.guru](https://www.robo.guru)

Please drop me a line!
