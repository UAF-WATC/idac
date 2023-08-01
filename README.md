# Infrasound Data Augmentation and Classification (IDAC)

IDAC is a suite of functions to 
1.  Generate a synthetic dataset by propagating a variety of source time functions through realistic atmospheres
1.  Classify infrasound signals by training machine learning (ML) models 
1.  Predict real (or synthetic) data in near real time

The motivation of the repository was to identify large nuclear blast waves from single sensor infrasound microphones but other applications including volcano monitoring are feasable. 

## Installation Instructions and Dependencies
IDAC depends on a number of softwares and codes.  Testing is currently focusing on linux and mac os systems.  


### AVOG2S 

The software [AVOG2S](https://github.com/usgs/volcano-avog2s) generates atmospheres using climatological and reanalysis models.  AVOG2S can be installed easily on Linux and Mac Os via git and homebrew.

1.  First install git (only needed once, if not already installed):

`sudo apt-get install git`

2.  install homebrew by typing (only needed once, if not already installed): 

`/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"`

2b. add brew to your PATH:

`echo 'eval "$(/home/linuxbrew/.linuxbrew/bin/brew shellenv)"' >> ~/.bash_profile
eval "$(/home/linuxbrew/.linuxbrew/bin/brew shellenv)"`

3.  tap the [Alaskan Volcano Observatories's (AVO) repository](https://github.com/ibrewster/homebrew-avo) (only needed once)

`brew tap ibrewster/avo`

4.  install the AVOG2S formula using homebrew 

`brew install avog2s`

### NCPAProp
NCPAProp is used to propagate source time functions (e.g. blast waves) through the modeled atmospheres. 

NCPAProp relies on several libraries, which must be downloaded and compiled by source.  

First download the [FFTW library](http://www.fftw.org/download.html) and extract the tar.gz file to a temporary directory (e.g. Desktop).  Then open a terminal and `cd` to the extracted files and run:
`./configure`
`make`
`make install`
Note you may need sudo privalges to install.

Second we need download the latest version of [GSL](ftp://ftp.gnu.org/gnu/gsl/).  After download, extract the files to a temporary directory (e.g. Desktop).  








To install NCPAProp:

1.  Download the NCPAProp software from its github repo: [NCPAprop](https://github.com/chetzer-ncpa/ncpaprop)

2.  Open a terminal and `cd` into the directory where the code was downloaded and run `./configure` with appropriate parameters. We recommend the following parameters, which install required PETSc and SLEPc libraries locally within the ncpaprop installation:

`./configure --with-localpetsc --enable-autodependencies`

For more information on how to use `./configure` see the [NCPAprop manual](https://github.com/chetzer-ncpa/ncpaprop/blob/master/docs/ncpaprop-manual.pdf) and search for */configure* or *installation overview*.  As a side note, the NCPAprop manual is a wonderful reference to better understand how waveforms are propagated.  

3.  Run `make`

### Downloading IDAC
Idac is a python module, meaning it can (and should) be imported directly to a python environment (e.g. `import idac as ida`).  

First navigate to the [IDAC repository](https://github.com/UAF-WATC/idac) and download the source code.  There are numerous ways to do this, the easiest being to click on the green "code" button > 'Download Zip'.  Then, unzip the module in an appropriate directory.  For example, "python_modules" or "github_packages" are good directory names if you have other python/github projects.  We do not recommend unpacking to your "Desktop" or other similar temporary locations. 

Before installing IDAC, we must ensure the environment is set up correctly.  

### Python Dependencies and Conda Environment
IDAC requires several python modules, which are listed below.  The easiest way to install these dependencies is to build the environment from either the idac_linux_environment.yml or idac_mac_environment file in the root directory of the idac repository.  

To build the environment from a .yml file, make sure you have [conda installed](https://docs.conda.io/projects/conda/en/latest/user-guide/install/), then from the idac_linux_environment.yml file:

1.  Open a terminal and `cd` into the directory where the idac repo is downloaded.  
2.  build the environment with: 
`conda env create -f idac_linux_environment.yml`
3.  After building the environment, be sure to activate it with: 
`conda activate idac`

#### Building environment manually 
If you are running a different operating system, or you prefer to build the environment manually: 

1.  Create an environment with the 'correct' version of python
`conda create --name idac python=3.5 `
2.  Install obspy with:
`conda install obspy`
3.  Install pandas with: 
`conda install pandas`
4.  Install scikitlearn with 
`conda install scikit-learn`
5.  

### Installing IDAC

Once the environment has been set-up, we can install IDAC using pip.  First activate the idac environment: 

`conda activate idac`

Then install the module with pip: 

`pip install /path/to/idac/directory`

# Using IDAC

The following tutorial walks you through a simple case 'start to finish' workflow, which highlights the functionality of IDAC.  WARNING, IDAC functions typically write files to your local disk.  If care isn't taken, IDAC can write many GBs of data and fill up your disk space. 

## Infrasound Data Augmentation

### Generating Source Time Functions 


### Generating Atmospheres 


### Propagating Source Time Functions 

#### Building dispersion curves 

#### Propagating waveforms 

### Adding noise to waveform 

## Infrasound Classification

### Generating features 

### Training Machine Learning Model

### Classifying Data




