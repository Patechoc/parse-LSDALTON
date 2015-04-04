# Parse-LSDALTON
To parse input and ouput [LSDALTON](http://daltonprogram.org/) files, and build visualizations of benchmarked methods.

## Local installation using [setuptools](https://pythonhosted.org/setuptools/setuptools.html) in a virtual environment
```
git clone https://github.com/Patechoc/parse-LSDALTON.git
cd parseLSDALTON
sudo easy_install pip
virtualenv myPackage
source myPackage/bin/activate
sudo ./myPackage/bin/pip install -r requirements.txt
...
cd test
python -m unittest discover -v
deactivate
```

## Code structure

Main directory structure:
```
├── README.md
├── main.py
├── src
│   ├── read_LSDALTON_output.py
│   ├── compare_LSDALTON_outputs.py
│   └── plots/
│       ├── plotly01.py
│       └── plotly_HistidineFerrocene.py
├── files/
│    └── lsdalton_files/
│       ├── lsdalton20140924_b3lyp_gradient...
│       └── lsdalton20140924_geomOpt-b3lyp_...
├── ...
└── test/
    ├── test_read_LSDALTON_output.py
    ├── ...
    └── test_compare_LSDALTON_outputs.py
```

## Dependencies
This code is using other module/libraries.
- RMS Deviation between 2 geometries: https://github.com/charnley/rmsd
- Conversion from cartesian to various formats (.pdb, .gzmat, .mol2): [Openbabel ](http://openbabel.org/)


## Testing the code
### using the standard Python unit testing framework ([PyUnit](https://docs.python.org/2/library/unittest.html))
You can just run the tests like so:
```
$ cd test
$ python -m unittest test_read_LSDALTON_output
```
or all of them at once with:
```
$ python -m unittest discover -v
```
(see https://docs.python.org/2/library/unittest.html for more information about unit testing)

### using [PyTest](http://pytest.org/)
```
$ cd test
$ py.test -q test_read_LSDALTON_output
```
or simply
```
$ cd test
$ py.test
```

## Continuous delivery
The code is testing continuously (after every `git push`) using [Wercker](http://wercker.com/) and explains why we need the following files:
```
├── wercker.yml
└── requirements.txt
```
wercker.yml will specify the flow of packages to install, variables to setup and commands to perform, while requirements.txt includes the list of packages to install and eventually which version you required.

[![wercker status](https://app.wercker.com/status/723dc9ae58f0940dcdab0d2379126fa9/m "wercker status")](https://app.wercker.com/project/bykey/723dc9ae58f0940dcdab0d2379126fa9)

