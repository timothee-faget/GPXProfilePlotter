# GPXProfilePlotter

Tool for plotting a GPX elevation profile

Import plot_gpx_profile function to use:
``from gpxprofpy import plot_gpx_profile``

Parameters
----------

**filename** : str
    GPX file name.

**plot_slope**: bool, optional
    Plot slope segments (default: False). If activated, plot segments that are longer than
    variable SEUIL defined in .params. Segments colors are chosen accordingly to their
    mean slope, and colors are also defined in .params.

**plot_points**: bool, optional
    Plot remarquables points (default: False). If activated, module tries to open a CSV file
    with the same name as the main GPX file. Remarquable points are red as
    (distance, label, has_water). Points are then added on the profile, with different
    styling for start and finish points. Colors are also defined in .params.

**save_fig**: bool, optional
    Save plot as png file (default: False). If activated, plot is saved to a png
    file with the same name as the main GPX file.

Examples
--------

``plot_gpx_profile("data/MyGPXFile.gpx")``
Plots elevation profile only

``plot_gpx_profile("data/MyGPXFile.gpx", True, True, True)``
Plots elevation profile, slope segments, remarquables points and saves a png file

``plot_gpx_profile("data/MyGPXFile.gpx", save_fig=True)``
Plots elevation profile and saves a png file

# Changelog

## v0.1.0

Major refactoring of the code

Add:

- Tests for basic functions. More to come
- Merging segments tools

Fix:

- Slope segment detection now detect all segments
- Micro segments are detected and merged

## v0.0.5

Add:

- README information

## v0.0.4

Fix:

- Versioning issues

## v0.0.3

Fix:

- Projects URL in toml configuration file

## v0.0.2

Initial version

# Features to come (in random order)

- Colors choice
- Miles / km option
- Change files names

# Known bugs

- When plotting without remarquable points, y limit is badly configured
