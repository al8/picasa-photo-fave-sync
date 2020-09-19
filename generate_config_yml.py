
#!/usr/bin/env python3

import yaml

def main(filename):
    data = [
        {r"D:\!Memories\staging area\Eye-Fi": [
                {"regex": {"dir": r"\d{4}[-]\d\d[-]\d\d[-].+",
                          "file": r"(((DSC|IMG_|[A-Z]+)\d+)|(\d+-\d+-\d+ \d+.\d+.\d+))[.]jpg"}},
            ]},
        {r"D:\!Memories\Photos\2011": [
            {"regex": {"dir": r"\d{8} .+",
                      "file": r"\d{8}_\d{4}.+[.]jpg", },
                      },
            "picasa",
        ]},
        r"D:\!Memories\Photos\2011",
        r"D:\!Memories\Photos\2012",
        r"D:\!Memories\Photos\2013",
        r"D:\!Memories\Photos\2014",
        r"D:\!Memories\Photos\2015",
        r"D:\!Memories\Photos\2016",
        r"D:\!Memories\Photos\2017",
        r"D:\!Memories\Photos\2018",
        r"D:\!Memories\Photos\2019",
        r"D:\!Memories\Photos\2020",
    ]

    with open("out.%s" % filename, 'w') as f:
        yaml.dump(data, f)

if __name__ == "__main__":
    main("sample-config-gen.yml")