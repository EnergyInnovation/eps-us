---
layout: page
title:  "Download and Installation Instructions"
---

The Energy Policy Simulator (EPS) is developed in [Vensim](http://vensim.com/), a program produced by Ventana Systems for the creation and simulation of system dynamics models.  While Vensim is sold commercially in several tiers, Ventana Systems makes available a free Vensim Model Reader that can read and simulate (but not edit) models.  These instructions will walk you through the process of installing Vensim Model Reader and the Energy Policy Simulator.

## Note for Mac Users

Vensim is available for Windows and Mac operating systems.  We have developed and tested the EPS exclusively on Windows computers, and all of the directions below assume you are using Windows.  If you try using the Mac version of Vensim and encounter bugs or problems, you may consider running a copy of Windows using [Parallels Desktop](http://www.parallels.com/products/desktop/), [VMWare Fusion](https://www.vmware.com/products/fusion), or [Boot Camp](https://www.apple.com/support/bootcamp/getstarted/).  This will enable you to use the Windows version of Vensim on your Mac.

## How to Obtain the Model

Before downloading the model, you should install a copy of Vensim Model Reader.  You may download this software on the [Vensim Free Downloads page](http://vensim.com/free-download/).  Check the "Anti-spam" box on that web page.  **Be sure to change the radio button in the "Product" section from "Vensim PLE" to "Model Reader."**  The EPS will not function under Vensim PLE (personal learning edition).  Select your operating system, enter your name and email address, and click the "Download software" button.  You will receive an email with a link to download Vensim Model Reader.  Download and run this installer, following all prompts.  After installing Vensim Model Reader, open the program to ensure it runs successfully.

**Note for people who already have a copy of Vensim:** The EPS requires Vensim version 7.1 (released in July 2017) or later in order to produce correct numerical results.  This is because the model relies on bug fixes that were implemented in Vensim v7.1.  Additionally, the model relies heavily on subscripts, which are not available in Vensim PLE or Vensim PLE Plus (the lower-tier versions of the editor).  Please be sure you have Vensim Pro, Vensim DSS, or Vensim Model Reader version 7.1 or later before attempting to run the model.  If you own Vensim Pro or DSS with a current maintenance subscription, you can download an updated version [here](https://www.vensim.com/php-bin/download.html).  Otherwise, you should download the free Model Reader.

Once Model Reader is installed, you should download the EPS by clicking the button below.

<p><a href="https://github.com/Energy-Innovation/eps-us/archive/3.0.0.zip" class="btn">Download the Energy Policy Simulator</a></p>

A compressed archive (.zip file) will be downloaded named "eps-" followed by the model's current version number.  It is necessary to extract the files from the archive before running the model.  On Windows, .zip archives look similar to folders, and you can double-click on them to open them and even open the files inside them.  **This does not mean you have extracted the files from the archive.**  (Vensim cannot write files into a .zip archive, so Vensim will not be able to run the model properly, as this process generates an output file containing the run results.)  To extract the files, right-click on the .zip archive and select "Extract All..." then click "Extract" in the dialogue box that appears.  This will generate an uncompressed folder containing the model files.  You should now delete the .zip archive, so that there is no possibility of accidentally running the copy of the model that is still located inside the .zip archive.

The model folder will contain the following files and folder:

* three scripts in the Python programming language (with .py extension), used to produce Vensim command scripts.  Vensim command scripts are files only usable by Vensim DSS that allow for batch runs and other automated behavior.
* EPS.vpm, the model in compiled form, suitable for use in Vensim Model Reader
* EPS.mdl, the model source code, suitable for use in Vensim Pro or Vensim DSS (and viewable in a text editor)
* GraphDefinitions.vgd, a text file defining properties of graphs that appear when the model is opened in Vensim
* License.txt, a copy of the GNU General Public License version 3 (GPLv3), under which the EPS is licensed.  See the [Software License page](software-license.html) for more details.
* OutputVarsToExport.lst, a text file listing the names of output variables, which is used by the Python scripts
* ReadMe.pdf, a file containing some introductory information and a link to the documentation on this website
* three policy packages or scenarios (with .cin extension), which can be loaded by Vensim.  These scenarios are also featured in the online web application that runs the model on this website.
* WebAppData.xlsx, a spreadsheet that contains information used by the online web application that runs the model on this website
* InputData, a folder that contains all of the data files (in .csv format) read by the model at runtime, as well as the Excel files used to generate those data files.  The Excel files contain bibliographic source information, so model users know the origin of every piece of data used in the model.  Data are sorted into folders by model section and then by acronyms for variable names, or occasionally acronyms that encompass several variables.  (Acronyms are used to reduce file path lengths, because Windows would give errors if full variable names were used here.)  A key to the meaning of all acronyms is provided in the InputData folder (the file "acronym-key.xlsx").

It is easiest to use the EPS if your operating system is not configured to hide file extensions, which is the default behavior.  If you do not see file extensions such as .vpm, .mdl, .py, .lst, .vgd, .csv, and .xlsx in the files in the model distribution, it is recommended that you change your OS settings to display file extensions.  On Windows 7 and Windows 10, this can be done by going to the Control Panel/Settings, type "file extensions" in the search field, and click "Show or hide file extensions."  In the "Folder Options" dialogue box that appears, the "View" tab should be active.  Clear the box for "Hide extensions for known file types" and click "OK".  The process is likely to be similar on other versions of Windows.

If you are using Vensim Model Reader, the only files you will need are the compiled version of the model (with .vpm extension) and the InputData folder.  The .mdl file and .vgd file are only useful if you have Vensim Pro or Vensim DSS.  (A copy of GraphDefinitions.vgd is bundled into the compiled .vpm file, so you do not need the graph definitions text file to view graphs when using the compiled version of the model.)  The .py files and the .lst file are only useful if you have Vensim DSS (because this is the only version of Vensim that supports command scripts).  To use these scripts, you will also need to have [Python 3](https://www.python.org/downloads/) installed.  For more information, see the [Automated Analysis with Python Scripts](automated-analysis.html) page.

Double-click the .vpm model file to open the model in Vensim Model Reader.  (If the .vpm file extension is not associated to Vensim, you may need to browse for Vensim Model Reader (venread.exe) and select it in order to associate .vpm to this program.)  You may now examine and run the model.  For guidance, please see the [How to Conduct Analysis in Vensim Model Reader](how-to-conduct-analysis.html) page (and its sub-pages on the [documentation index](index.html)) and/or refer to [Vensim's help documentation](http://www.vensim.com/documentation/index.html).