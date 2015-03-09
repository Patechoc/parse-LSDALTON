# Parse-LSDALTON
To parse input and ouput [LSDALTON](http://daltonprogram.org/) files, and build visualizations of benchmarked methods.

## Code structure

Main directory structure:
```
├── README.md
├── main.py
├── read_LSDALTON_output.py
├── compare_LSDALTON_outputs.py
├── ...
├── plots/
│   ├── plotly01.py
│   └── plotly_HistidineFerrocene.py
├── test/
│   ├── test_read_LSDALTON_output.py
│   ├── ...
│   └── test_compare_LSDALTON_outputs.py
└── files/
    └── lsdalton_files/
        ├── lsdalton20140924_b3lyp_gradient...
        └── lsdalton20140924_geomOpt-b3lyp_...
```
## Testing the code
### using the standard Python unit testing framework ([PyUnit](https://docs.python.org/2/library/unittest.html))
You can just run the tests like so:
```
$ cd parse-lsdalton
$ python -m unittest test_read_LSDALTON_output
```
or all of them at once with:
```
$ python -m unittest discover -v
```
(see https://docs.python.org/2/library/unittest.html for more information about unit testing)

### using [PyTest](http://pytest.org/)



## Continuous delivery
The code is testing continuously (after every `git push`) using [Wercker](http://wercker.com/) and explains why we need the following files:
```
├── wercker.yml
└── requirements.txt
```
wercker.yml will specify the flow of packages to install, variables to setup and commands to perform, while requirements.txt includes the list of packages to install and eventually which version you required.
[![wercker status](https://app.wercker.com/status/723dc9ae58f0940dcdab0d2379126fa9/m "wercker status")](https://app.wercker.com/project/bykey/723dc9ae58f0940dcdab0d2379126fa9)

