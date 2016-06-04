# PyRegions
PyRegions is a simple Sublime Text plugin to add custom toggable regions in Python files. 
Other plugins (such as [SyntaxFold](https://github.com/jamalsenouci/sublimetext-syntaxfold)) do a great, if not better, job at this. However, I've always wanted to create a Sublime Text plugin, so here it is. :)

## Features
* Toggle regions independent of indentation.
* Shows the name of the region your cursor is currently in in the status bar

## Usage
Just add the following two lines around the block you want to create a region of:

    #region:<name>
    #endregion:<name>

## Development ideas
* Ability to use different comment syntax
* Perhaps be less strict on adding the name to the end of the region
