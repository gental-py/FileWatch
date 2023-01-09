# File Watch.

*Logs all changes in files structure.*

<mark>Only for windows.</mark>

---

# Description.

Every time any file get created/deleted/moved, information with *time, date and source path* is saved into logs file according to disk. All disks have their own file. You can specify **special** paths where changes are saved into `specials.log` file instead of disk's one.

---

# Todo.

- [ ]  Automatically add to auto start.

- [ ]  Create stats viewer

- [ ]  (maybe) Create a shell?

- [ ]  Create dev_docs.md

---

# Installation.

Use .exe file:

`Download filewatch.rar and run filewatch.exe`


Compile python code by Yourself:

```c
1. Downlaod/clone repository
2. Install packages: pip install -r requirements.txt
3. Run filewatch.py
```

---

# Paths.

All files are saved in user's `appdata` directory: 
Main directory: `C:\Users\your_username\AppData\Local\FILE STRUCT LOGS\`
Here you can find those files:

| File           | Description              |
|:-------------- | ------------------------ |
| `config.json`  | User configuration.      |
| `specials.log` | Logs from special paths. |
| `<disk>.log`   | All disk's logs.         |

---

# Configuration.

In configuration file, you can change: which logs are saved, specify special paths, change logs file size required to alert you.

###### Remember, that entire file should follow JSON format. Config file will not load if JSON could not parse it's config and You will se error message.

| Name                 | Type      | Description                                                                                                                                                                                     | Default |
| -------------------- | --------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------- |
| `skip_temp`          | bool      | Do not save events for files with `temp` phrases in it's paths.                                                                                                                                 | `true`  |
| `skip_log`           | bool      | Do not save events for files with `log` phrases in it's paths.                                                                                                                                  | `true`  |
| `skip_custom`        | list      | List of custom phrases. If any of those phrase would be found in file's source path, the action will not be logged.                                                                             | `[]`    |
| `specials`           | list      | List of special paths. All events that would happen in those places will be saved in `specials.log` and `<disk>.log` files.                                                                     | `[]`    |
| `logs_size_alert_gb` | int/float | Amount of Gigabytes required to send alert (as messagebox) with information that **log file has achieved that amount of GB**.                                                                   | `2`     |
| `only_specials`      | bool      | Decides if FileWatch should watch all disks or only those specified in `specials` setting.                                                                                                      | `false` |
| `log_edits`          | bool      | Decides if FileWatch will log file's content modification events. **Remember, that most of programs edits it's files while running and log files will fill up very fast with `Modified` logs!** | `true`  |

###### <mark>Notice</mark>, that You don't have to include all available settings in `config.json`. **All missing settings from file will be filled with default settings**

---

# Logs.

Possible files events: `Created`, `Moved`, `Deleted`, `Modified`

Log's syntax: `dd/mm/YYYY hh/mm/ss | type | source path`

#### Example log:

```c
# Files tree before:
C:\[showcase]
|-[an_directory]
|-an_file.txt

# Files tree after:
C:\[showcase]
|-[an_directory]
|-an_file.txt
|-new_file.txt (+ created)


# Log message:
09/01/2023 23:13:44 | Created   | C:\showcase\new_file.txt
```

###### <mark>Notice:</mark> Manually moved files are treated as two separated events: `Deleted`, `Created`

```c
# Files tree before:
C:\[showcase]
|-[abc]
|-file.txt

# Files tree after:
C:\[showcase]
|-[abc]\
| |-file.txt 


# Log messages:
09/01/2023 23:05:19 | Deleted   | C:\showcase\file.txt 
09/01/2023 23:05:19 | Created   | C:\showcase\abc\file.txt 
```

---

# Entire developer documentation can be found in `dev_docs.md`!


