[![wercker status](https://app.wercker.com/status/723dc9ae58f0940dcdab0d2379126fa9/m "wercker status")](https://app.wercker.com/project/bykey/723dc9ae58f0940dcdab0d2379126fa9)

# Parse-LSDALTON
To parse input and ouput LSDALTON files 


Main directory structure:
```
├── README.md
├── main.py
├── read_LSDALTON_output.py
├── test_read_LSDALTON_output.py
├── compare_LSDALTON_outputs.py
├── test_compare_LSDALTON_outputs.py
├── plots/
│   ├── plotly01.py
│   └── plotly_HistidineFerrocene.py
└── files/
    └── lsdalton_files/
        ├── lsdalton20140924_b3lyp_gradient...
        └── lsdalton20140924_geomOpt-b3lyp_...
```

The code is testing continuously (after every `git push`) using [Wercker](http://wercker.com/) and explains why we need the following files:
```
├── wercker.yml
└── requirements.txt
```

You can just run the tests like so:
```
$ cd my_project
$ python -m unittest test_read_LSDALTON_output
```
or all of them at once with:
```
$ python -m unittest discover -v
```
(see https://docs.python.org/2/library/unittest.html for more information about unit testing)